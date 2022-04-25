
from nintendo.nex import prudp, common, streams
from anynet import util
import contextlib
import struct
import anyio

import logging
logger = logging.getLogger(__name__)


class RMCResponse:
	pass


class RMCMessage:
	REQUEST = 0
	RESPONSE = 1
	
	def __init__(self, settings):
		self.settings = settings
		
		self.mode = RMCMessage.REQUEST
		self.protocol = None
		self.method = None
		self.call_id = 0
		self.error = -1
		self.body = b""
		
	@staticmethod
	def prepare(settings, mode, protocol, method, call_id, body):
		inst = RMCMessage(settings)
		inst.mode = mode
		inst.protocol = protocol
		inst.method = method
		inst.call_id = call_id
		inst.body = body
		return inst
		
	@staticmethod
	def request(settings, protocol, method, call_id, body):
		return RMCMessage.prepare(
			settings, RMCMessage.REQUEST, protocol, method, call_id, body
		)
		
	@staticmethod
	def response(settings, protocol, method, call_id, body):
		return RMCMessage.prepare(
			settings, RMCMessage.RESPONSE, protocol, method, call_id, body
		)
		
	@staticmethod
	def error(settings, protocol, method, call_id, error):
		inst = RMCMessage(settings)
		inst.mode = RMCMessage.RESPONSE
		inst.protocol = protocol
		inst.method = method
		inst.call_id = call_id
		inst.error = error
		return inst
	
	@staticmethod
	def parse(settings, data):
		inst = RMCMessage(settings)
		inst.decode(data)
		return inst
		
	def encode(self):
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
			if self.error != -1 and self.error & 0x80000000:
				stream.bool(False)
				stream.u32(self.error)
				stream.u32(self.call_id)
			else:
				stream.bool(True)
				stream.u32(self.call_id)
				stream.u32(self.method | 0x8000)
				stream.write(self.body)
		return struct.pack("I", stream.size()) + stream.get()
	
	def decode(self, data):
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
				self.error = stream.u32()
				self.call_id = stream.u32()
				if not stream.eof():
					raise ValueError("RMC error message is bigger than expected")


class RMCClient:
	def __init__(self, settings, client):
		self.settings = settings.copy()
		self.client = client
		self.call_id = 1
		
		if self.client.minor_version() >= 3:
			self.settings["nex.struct_header"] = True
		
		self.servers = {}
		self.requests = {}
		self.responses = {}
		
		self.closed = False

	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tb):
		await self.cleanup()
	
	def register_server(self, server):
		if server.PROTOCOL_ID in self.servers:
			raise ValueError("Server with protocol id %i already exists" %server.PROTOCOL_ID)
		self.servers[server.PROTOCOL_ID] = server
	
	async def cleanup(self):
		if not self.closed:
			self.closed = True
			for event in self.requests.values():
				event.set()
			
			for server in self.servers.values():
				await server.logout(self)
	
	async def close(self):
		if not self.closed:
			await self.cleanup()
			await self.client.close()
	
	async def disconnect(self):
		if not self.closed:
			await self.cleanup()
			await self.client.disconnect()
	
	async def start(self, servers):
		for server in servers:
			self.register_server(server)
		
		while not self.closed:
			try:
				data = await self.client.recv()
			except anyio.EndOfStream:
				logger.info("Connection was closed")
				await self.cleanup()
				return
			
			message = RMCMessage.parse(self.settings, data)
			if message.mode == RMCMessage.REQUEST:
				logger.debug(
					"Received RMC request: protocol=%i method=%i call=%i",
					message.protocol, message.method, message.call_id
				)
				await self.handle_request(message)
			else:
				logger.debug(
					"Received RMC response: protocol=%i method=%s call=%i",
					message.protocol, message.method, message.call_id
				)
				if message.call_id in self.requests:
					self.responses[message.call_id] = message
					event = self.requests.pop(message.call_id)
					event.set()
				else:
					logger.warning("RMC response has invalid call id")
	
	async def handle_request(self, request):
		input = streams.StreamIn(request.body, self.settings)
		output = streams.StreamOut(self.settings)
		
		result = common.Result()
		if request.protocol in self.servers:
			try:
				await self.servers[request.protocol].handle(self, request.method, input, output)
			except common.RMCError as e:
				logger.warning("RMC failed: %s" %e)
				result = e.result()
			except Exception as e:
				logger.exception("Exception occurred while handling a method call")
				
				if isinstance(e, TypeError): result = common.Result.error("PythonCore::TypeError")
				elif isinstance(e, IndexError): result = common.Result.error("PythonCore::IndexError")
				elif isinstance(e, MemoryError): result = common.Result.error("PythonCore::MemoryError")
				elif isinstance(e, KeyError): result = common.Result.error("PythonCore::KeyError")
				else: result = common.Result.error("PythonCore::Exception")
			except anyio.ExceptionGroup as e:
				logger.exception("Multiple exceptions occurred while handling a method call")
				
				filtered = []
				for exc in e.exceptions:
					if not isinstance(exc, Exception):
						raise
				
				result = common.Result.error("PythonCore::Exception")
			
			if getattr(self.servers[request.protocol], "NORESPONSE", False):
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
		await self.client.send(response.encode())
	
	async def request(self, protocol, method, body, noresponse=False):
		if self.closed:
			raise RuntimeError("RMC connection is closed")
		
		call_id = self.call_id
		self.call_id = (self.call_id + 1) & 0xFFFFFFFF
		
		if not noresponse:
			event = anyio.Event()
			self.requests[call_id] = event
		
		message = RMCMessage.request(self.settings, protocol, method, call_id, body)
		await self.client.send(message.encode())
		
		if not noresponse:
			await event.wait()
			
			if self.closed:
				raise RuntimeError("RMC connection is closed")
			
			message = self.responses.pop(call_id)
			if message.error != -1:
				raise common.RMCError(message.error)
			return message.body
	
	def pid(self): return self.client.pid()
	
	def local_address(self):
		return self.client.local_address()
	def remote_address(self):
		return self.client.remote_address()
	
	def local_sid(self):
		return self.client.local_sid()
	def remote_sid(self):
		return self.client.remote_sid()


@contextlib.asynccontextmanager
async def connect(settings, host, port, vport=1, context=None, credentials=None, servers=[]):
	logger.debug("Connecting RMC client to %s:%i:%i", host, port, vport)
	async with prudp.connect(settings, host, port, vport, 10, context, credentials) as client:
		client = RMCClient(settings, client)
		async with client:
			async with util.create_task_group() as group:
				group.start_soon(client.start, servers)
				yield client
	logger.debug("RMC client is closed")

@contextlib.asynccontextmanager
async def serve(settings, servers, host="", port=0, vport=1, context=None, key=None):
	async def handle(client):
		host, port = client.remote_address()
		logger.debug("New RMC connection: %s:%i", host, port)
		
		client = RMCClient(settings, client)
		async with client:
			await client.start(servers)
	
	logger.info("Starting RMC server at %s:%i:%i", host, port, vport)
	async with prudp.serve(handle, settings, host, port, vport, 10, context, key):
		yield
	logger.info("RMC server is closed")

@contextlib.asynccontextmanager
async def serve_on_transport(settings, servers, transport, port, key=None):
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
