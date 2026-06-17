
from anynet import tls, util
from nintendo.nex import prudp, common, kerberos, settings, streams
from typing import AsyncIterator, Self

import anyio
import anyio.abc
import contextlib
import struct
import typing

import logging
logger = logging.getLogger(__name__)


Settings = settings.Settings


class RMCResponse:
	pass


class RMCMessage:
	REQUEST = 0
	RESPONSE = 1

	settings: Settings

	mode: int
	protocol: int
	method: int
	call_id: int
	result: int
	body: bytes
	
	def __init__(self, settings: Settings):
		self.settings = settings
		
		self.mode = RMCMessage.REQUEST
		self.protocol = 0
		self.method = 0
		self.call_id = 0
		self.result = -1
		self.body = b""
		
	@classmethod
	def prepare(
		cls, settings: Settings, mode: int, protocol: int, method: int,
		call_id: int, body: bytes
	) -> Self:
		inst = cls(settings)
		inst.mode = mode
		inst.protocol = protocol
		inst.method = method
		inst.call_id = call_id
		inst.body = body
		return inst
		
	@classmethod
	def request(
		cls, settings: Settings, protocol: int, method: int,
		call_id: int, body: bytes
	) -> Self:
		return cls.prepare(
			settings, RMCMessage.REQUEST, protocol, method, call_id, body
		)
		
	@classmethod
	def response(
		cls, settings: Settings, protocol: int, method: int,
		call_id: int, body: bytes
	) -> Self:
		return cls.prepare(
			settings, RMCMessage.RESPONSE, protocol, method, call_id, body
		)
		
	@classmethod
	def error(
		cls, settings: Settings, protocol: int, method: int,
		call_id: int, error: int
	) -> Self:
		inst = cls(settings)
		inst.mode = RMCMessage.RESPONSE
		inst.protocol = protocol
		inst.method = method
		inst.call_id = call_id
		inst.result = error
		return inst
	
	@classmethod
	def parse(cls, settings: Settings, data: bytes) -> Self:
		inst = cls(settings)
		inst.decode(data)
		return inst
		
	def encode(self) -> bytes:
		stream = streams.StreamOut(self.settings)
		
		flag = 0x80 if self.mode == self.REQUEST else 0
		if self.protocol < 0x80:
			stream.u8(self.protocol | flag)
		else:
			stream.u8(0x7F | flag)
			stream.u16(self.protocol)
		
		if self.mode == self.REQUEST:
			stream.u32(self.call_id)
			stream.u32(self.method)
			stream.write(self.body)
		else:
			if self.result != -1 and self.result & 0x80000000:
				stream.bool(False)
				stream.u32(self.result)
				stream.u32(self.call_id)
			else:
				stream.bool(True)
				stream.u32(self.call_id)
				stream.u32(self.method | 0x8000)
				stream.write(self.body)
		return struct.pack("I", stream.size()) + stream.get()
	
	def decode(self, data: bytes) -> None:
		stream = streams.StreamIn(data, self.settings)
		
		length = stream.u32()
		if length != stream.size() - 4:
			raise ValueError("RMC message has unexpected size")
		
		protocol = stream.u8()
		self.protocol = protocol & ~0x80
		if self.protocol == 0x7F:
			self.protocol = stream.u16()
		
		if protocol & 0x80:
			self.mode = self.REQUEST
			self.call_id = stream.u32()
			self.method = stream.u32()
			self.body = stream.readall()
		else:
			self.mode = self.RESPONSE
			if stream.bool():
				self.call_id = stream.u32()
				self.method = stream.u32() & ~0x8000
				self.body = stream.readall()
			else:
				self.result = stream.u32()
				self.call_id = stream.u32()
				if not stream.eof():
					raise ValueError("RMC error message is bigger than expected")


class RMCHandler(typing.Protocol):
	async def logout(self, client: RMCClient) -> None:
		...
	
	async def handle(
		self, client: RMCClient, method: int,
		input: streams.StreamIn, output: streams.StreamOut
	) -> None:
		...


class RMCClient:
	settings: settings.Settings

	_client: prudp.PRUDPClient
	_call_id: int

	_servers: dict[int, RMCHandler]
	_requests: dict[int, anyio.abc.Event]
	_responses: dict[int, RMCMessage]

	_closed: bool

	def __init__(self, settings: Settings, client: prudp.PRUDPClient):
		self.settings = settings.copy()

		self._client = client
		self._call_id = 1
		
		if self._client.minor_version() >= 3:
			self.settings["nex.struct_header"] = True
		
		self._servers = {}
		self._requests = {}
		self._responses = {}
		
		self._closed = False

	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tb):
		await self._cleanup()
	
	def register_server(self, server) -> None:
		if server.PROTOCOL_ID in self._servers:
			raise ValueError("Server with protocol id %i already exists" %server.PROTOCOL_ID)
		self._servers[server.PROTOCOL_ID] = server
	
	async def _cleanup(self):
		if not self._closed:
			self._closed = True
			for event in self._requests.values():
				event.set()
			
			for server in self._servers.values():
				await server.logout(self)
	
	async def close(self):
		if not self._closed:
			await self._cleanup()
			await self._client.close()
	
	async def disconnect(self):
		if not self._closed:
			await self._cleanup()
			await self._client.disconnect()
	
	async def start(self, servers: list[RMCHandler]) -> None:
		for server in servers:
			self.register_server(server)
		
		while not self._closed:
			try:
				data = await self._client.recv()
			except anyio.EndOfStream:
				logger.info("Connection was closed")
				await self._cleanup()
				return
			
			message = RMCMessage.parse(self.settings, data)
			if message.mode == RMCMessage.REQUEST:
				logger.debug(
					"Received RMC request: protocol=%i method=%i call=%i",
					message.protocol, message.method, message.call_id
				)
				await self._handle_request(message)
			else:
				logger.debug(
					"Received RMC response: protocol=%i method=%s call=%i",
					message.protocol, message.method, message.call_id
				)
				if message.call_id in self._requests:
					self._responses[message.call_id] = message
					event = self._requests.pop(message.call_id)
					event.set()
				else:
					logger.warning("RMC response has invalid call id")
	
	async def _handle_request(self, request: RMCMessage) -> None:
		input = streams.StreamIn(request.body, self.settings)
		output = streams.StreamOut(self.settings)
		
		result = common.Result()
		if request.protocol in self._servers:
			try:
				server = self._servers[request.protocol]
				await server.handle(self, request.method, input, output)
			except common.RMCError as e:
				logger.warning("RMC failed: %s" %e)
				result = e.result()
			except Exception as e:
				logger.exception("Exception occurred while handling a method call")
				
				if isinstance(e, TypeError): result = common.Result.error("PythonCore::TypeError")
				elif isinstance(e, IndexError): result = common.Result.error("PythonCore::IndexError")
				elif isinstance(e, MemoryError): result = common.Result.error("PythonCore::MemoryError")
				elif isinstance(e, KeyError): result = common.Result.error("PythonCore::KeyError")
				else:
					result = common.Result.error("PythonCore::Exception")
			
			if getattr(self._servers[request.protocol], "NORESPONSE", False):
				return
		else:
			logger.warning("Received RMC request with unimplemented protocol id: %i", request.protocol)
			result = common.Result.error("Core::NotImplemented")
		
		if result.is_success():
			response = RMCMessage.response(
				self.settings, request.protocol, request.method,
				request.call_id, output.get()
			)
		else:
			response = RMCMessage.error(
				self.settings, request.protocol, request.method,
				request.call_id, result.code()
			)
		await self._client.send(response.encode())
	
	async def request(
		self, protocol: int, method: int, body: bytes,
		noresponse: bool = False
	) -> bytes:
		if self._closed:
			raise RuntimeError("RMC connection is closed")
		
		call_id = self._call_id
		self._call_id = (self._call_id + 1) & 0xFFFFFFFF
		
		if not noresponse:
			event = anyio.Event()
			self._requests[call_id] = event
		
		message = RMCMessage.request(self.settings, protocol, method, call_id, body)
		await self._client.send(message.encode())
		
		if not noresponse:
			await event.wait()
			
			if self._closed:
				raise RuntimeError("RMC connection is closed")
			
			message = self._responses.pop(call_id)
			if message.result != -1:
				raise common.RMCError(message.result)
			return message.body
		
		return b""
	
	def pid(self) -> int | None:
		return self._client.pid()
	
	def local_address(self) -> tuple[str, int]:
		return self._client.local_address()
	
	def remote_address(self) -> tuple[str, int]:
		return self._client.remote_address()
	
	def local_sid(self) -> int:
		return self._client.local_sid()
	
	def remote_sid(self) -> int:
		return self._client.remote_sid()


@contextlib.asynccontextmanager
async def connect(
	settings: Settings, host: str, port: int, vport: int = 1,
	context: tls.TLSContext | None = None,
	credentials: kerberos.Credentials | None = None,
	servers: list[RMCHandler] = []
) -> AsyncIterator[RMCClient]:
	logger.debug("Connecting RMC client to %s:%i:%i", host, port, vport)
	async with prudp.connect(settings, host, port, vport, 10, context, credentials) as client:
		rmc = RMCClient(settings, client)
		async with rmc:
			async with util.create_task_group() as group:
				group.start_soon(rmc.start, servers)
				yield rmc
	logger.debug("RMC client is closed")

@contextlib.asynccontextmanager
async def serve(
	settings: Settings, servers: list[RMCHandler], host: str = "",
	port: int = 0, vport: int = 1, context: tls.TLSContext | None = None,
	key: bytes | None = None
) -> AsyncIterator[None]:
	async def handle(client: prudp.PRUDPClient) -> None:
		host, port = client.remote_address()
		logger.debug("New RMC connection: %s:%i", host, port)
		
		rmc = RMCClient(settings, client)
		async with rmc:
			await rmc.start(servers)
	
	logger.info("Starting RMC server at %s:%i:%i", host, port, vport)
	async with prudp.serve(handle, settings, host, port, vport, 10, context, key):
		yield
	logger.info("RMC server is closed")

@contextlib.asynccontextmanager
async def serve_on_transport(
	settings: Settings, servers: list[RMCHandler],
	transport: prudp.PRUDPServerTransport, port: int, key: bytes | None = None
) -> AsyncIterator[None]:
	async def handle(client):
		host, port = client.remote_address()
		logger.debug("New RMC connection: %s:%i", host, port)
		
		client = RMCClient(settings, client)
		async with client:
			await client.start(servers)
	
	logger.info("Starting RMC server at PRUDP port %i", port)
	async with transport.serve(handle, port, 10, key):
		yield
	logger.info("RMC server is closed")

serve_prudp = serve_on_transport
