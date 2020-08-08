
from nintendo.common import tls, http, socketutils
import contextlib
import secrets
import hashlib
import base64
import struct
import anyio

import logging
logger = logging.getLogger(__name__)


OPCODE_CONTINUE = 0
OPCODE_TEXT = 1
OPCODE_BINARY = 2
OPCODE_DISCONNECT = 8
OPCODE_PING = 9
OPCODE_PONG = 10


def calculate_key_hash(key):
	string = key.encode("ascii") + b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
	hash = hashlib.sha1(string).digest()
	return base64.b64encode(hash).decode()
	
def apply_mask(data, key):
	return bytes([data[i] ^ key[i % 4] for i in range(len(data))])


class WSError(Exception): pass


class WSPacket:
	def __init__(self, opcode, payload=b""):
		self.opcode = opcode
		self.payload = payload


class WSPacketClient:
	def __init__(self, protocol, client, group):
		self.protocol = protocol
		self.client = client
		self.group = group
	
		self.packets = socketutils.PacketQueue()
		
		self.buffer = b""
		self.fragments = None
		self.message_type = None # For continuation frames
		
		self.server_mode = False
	
	async def start_handshake(self, host, path):
		logger.debug("Performing WS handshake")
		
		self.server_mode = False
		
		key = secrets.token_urlsafe()
		
		request = http.HTTPRequest.get(path)
		request.headers["Host"] = host
		request.headers["Upgrade"] = "websocket"
		request.headers["Connection"] = "upgrade"
		request.headers["Sec-WebSocket-Key"] = key
		request.headers["Sec-WebSocket-Version"] = 13
		request.headers["Sec-WebSocket-Protocol"] = self.protocol
		await self.client.send(request.encode())
		
		while b"\r\n\r\n" not in self.buffer:
			self.buffer += await self.client.recv()
		
		index = self.buffer.index(b"\r\n\r\n")
		header = self.buffer[:index + 4]
		self.buffer = self.buffer[index + 4:]
		
		response = http.HTTPResponse.parse(header)
		if response.status_code != 101:
			raise WSError("WS server replied with status code %i" %response.status)
		
		if "Sec-WebSocket-Accept" not in response.headers:
			raise WSError("Sec-WebSocket-Accept header is missing")
		if response.headers["Sec-WebSocket-Accept"] != calculate_key_hash(key):
			raise WSError("Sec-WebSocket-Accept check failed")
		
		logger.debug("WS handshake succeeded")
		
		await self.group.spawn(self.process)
		
	async def accept_handshake(self):
		logger.debug("Accepting WS handshake")
		
		self.server_mode = True
		
		while b"\r\n\r\n" not in self.buffer:
			self.buffer += await self.client.recv()
		
		index = self.buffer.index(b"\r\n\r\n")
		header = self.buffer[:index + 4]
		self.buffer = self.buffer[index + 4:]
		
		request = http.HTTPRequest.parse(header)
		if request.method != "GET":
			raise WSError("WS request has unexpected method: %s" %request.method)
		
		if "Sec-WebSocket-Key" not in request.headers:
			raise WSError("Sec-WebSocket-Key header is missing")
		if "Sec-WebSocket-Protocol" not in request.headers:
			raise WSError("Sec-WebSocket-Protocol header is missing")
			
		if request.headers["Sec-WebSocket-Protocol"] != self.protocol:
			raise WSError("Sec-WebSocket-Protocol header has unexpected value")
			
		accept = calculate_key_hash(request.headers["Sec-WebSocket-Key"])
		
		response = http.HTTPResponse(101)
		response.headers["Connection"] = "upgrade"
		response.headers["Upgrade"] = "WebSocket"
		response.headers["Sec-WebSocket-Accept"] = accept
		response.headers["Sec-WebSocket-Protocol"] = self.protocol
		await self.client.send(response.encode())
		
		logger.debug("WS handshake succeeded")
		
		await self.group.spawn(self.process)
		
	async def process(self):
		while True:
			await self.process_buffer()
			try:
				self.buffer += await self.client.recv()
			except anyio.exceptions.ClosedResourceError:
				await self.packets.close()
				return
			
	async def process_buffer(self):
		while self.buffer:
			if len(self.buffer) < 2: return
			
			fin = self.buffer[0] >> 7
			opcode = self.buffer[0] & 0xF
			mask = self.buffer[1] >> 7
			size = self.buffer[1] & 0x7F
			
			offset = 2
			if size == 126:
				if len(self.buffer) < offset + 2: return
				size = struct.unpack_from(">H", self.buffer, offset)[0]
				offset += 2
			elif size == 127:
				if len(self.buffer) < offset + 8: return
				size = struct.unpack_from(">Q", self.buffer, 2)[0]
				offset += 8

			mask_key = b"\0\0\0\0"
			if mask:
				if len(self.buffer) < offset + 4: return
				mask_key = self.buffer[offset : offset + 4]
				offset += 4
				
			if len(self.buffer) < offset + size: return
			payload = apply_mask(self.buffer[offset : offset + size], mask_key)
			
			self.buffer = self.buffer[offset + size:]
			
			await self.process_packet(opcode, payload, fin)
			
	async def process_packet(self, opcode, payload, fin):
		if opcode in [OPCODE_TEXT, OPCODE_BINARY, OPCODE_CONTINUE]:
			if opcode in [OPCODE_TEXT, OPCODE_BINARY]:
				if self.message_type is not None:
					raise WSError("Expected continuation frame")
				self.message_type = opcode
				self.fragments = payload
			else:
				if self.message_type is None:
					raise WSError("Received unexpected continuation frame")
				self.fragments += payload
			
			if fin:
				packet = WSPacket(self.message_type, self.fragments)
				self.message_type = None
				self.fragments = None
				await self.packets.put(packet)
		else:
			if not fin:
				raise WSError("Control frame must have FIN set")
			packet = WSPacket(opcode, payload)
			await self.packets.put(packet)
			
	async def send(self, opcode, payload=b""):
		data = bytes([0x80 | opcode])
		
		mask = 0x80 if not self.server_mode else 0
		
		length = len(payload)
		if length < 126:
			data += bytes([mask | length])
		elif length <= 0xFFFF:
			data += struct.pack(">BH", mask | 0x7E, length)
		else:
			data += struct.pack(">BQ", mask | 0x7F, length)
			
		if not self.server_mode:
			mask = secrets.token_bytes(4)
			payload = mask + apply_mask(payload, mask)
		data += payload

		await self.client.send(data)
		
	async def recv(self):
		return await self.packets.get()
		
	async def close(self):
		await self.packets.close()
		await self.client.close()
	
	def local_address(self): return self.client.local_address()
	def remote_address(self): return self.client.remote_address()


class WebSocketClient:
	def __init__(self, protocol, client, group):
		self.client = WSPacketClient(protocol, client, group)
		self.group = group
		
		self.binary_packets = socketutils.PacketQueue()
		self.text_packets = socketutils.PacketQueue()
		
		self.closing = False
		self.closed = anyio.create_event()
		
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tb):
		if typ is None:
			try:
				await self.close()
			except:
				await self.abort()
				raise
		else:
			await self.abort()
		
	async def start_handshake(self, host, path):
		await self.client.start_handshake(host, path)
		await self.group.spawn(self.process)
		
	async def accept_handshake(self):
		await self.client.accept_handshake()
		await self.group.spawn(self.process)
		
	async def process(self):
		while True:
			try:
				packet = await self.client.recv()
			except anyio.exceptions.ClosedResourceError:
				async with anyio.open_cancel_scope(shield=True):
					await self.cleanup()
				return
			await self.process_packet(packet.opcode, packet.payload)
	
	async def process_packet(self, opcode, payload):
		if self.closing:
			if opcode == OPCODE_DISCONNECT:
				await self.abort()
		else:
			if opcode == OPCODE_BINARY:
				await self.binary_packets.put(payload)
			elif opcode == OPCODE_TEXT:
				await self.text_packets.put(payload.decode())
			elif opcode == OPCODE_PING:
				await self.client.send(OPCODE_PONG, payload)
			elif opcode == OPCODE_DISCONNECT:
				await self.client.send(OPCODE_DISCONNECT)
				await self.abort()
			else:
				raise ValueError("WS packet has unknown opcode: %i" %opcode)
	
	async def cleanup(self):
		await self.group.cancel_scope.cancel()
		await self.closed.set()
		await self.binary_packets.close()
		await self.text_packets.close()
	
	async def abort(self):
		async with anyio.open_cancel_scope(shield=True):
			await self.cleanup()
			await self.client.close()
		
	async def close(self):
		if not self.closed.is_set():
			logger.debug("Closing WS connection")
			self.closing = True
			await self.client.send(OPCODE_DISCONNECT)
			await self.closed.wait()
			logger.debug("WS connection is closed")
			
	async def send(self, data):
		await self.client.send(OPCODE_BINARY, data)
	async def send_text(self, text):
		await self.client.send(OPCODE_TEXT, text.encode())

	async def recv(self):
		return await self.binary_packets.get()
	async def recv_text(self):
		return await self.text_packets.get()
		
	def local_address(self): return self.client.local_address()
	def remote_address(self): return self.client.remote_address()
	

@contextlib.asynccontextmanager
async def connect(protocol, host, port, context=None):
	path = "/"
	if "/" in host:
		path = host[host.index("/"):]
		host = host[:host.index("/")]
	
	logger.debug("Connecting WS client to %s:%i", host, port)
	
	async with tls.connect(host, port, context) as client:
		async with anyio.create_task_group() as group:
			async with WebSocketClient(protocol, client, group) as client:
				await client.start_handshake(host, path)
				yield client
	
	logger.debug("WS client is closed")

@contextlib.asynccontextmanager
async def serve(handler, protocol, host="", port=0, context=None):
	async def handle(client):
		host, port = client.remote_address()
		logger.debug("New WS connection: %s:%i", host, port)
		
		async with anyio.create_task_group() as group:
			async with WebSocketClient(protocol, client, group) as client:
				await client.accept_handshake()
				await handler(client)
	
	logger.info("Starting WS server at %s:%i", host, port)
	async with tls.serve(handle, host, port, context):
		yield
	logger.info("WS server is closed")
