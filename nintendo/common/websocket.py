
from . import socket, scheduler
import hashlib
import secrets
import struct
import base64

import logging
logger = logging.getLogger(__name__)


OPCODE_CONTINUE = 0
OPCODE_TEXT = 1
OPCODE_BINARY = 2
OPCODE_DISCONNECT = 8
OPCODE_PING = 9
OPCODE_PONG = 10

STATE_READY = 0
STATE_ACCEPTING = 1
STATE_CONNECTING = 2
STATE_CONNECTED = 3
STATE_DISCONNECTED = 4


class WebSocketClient:
	handshake_template = "GET %s HTTP/1.1\r\n" \
		"Host: %s\r\n" \
		"Upgrade: websocket\r\n" \
		"Connection: upgrade\r\n" \
		"Sec-WebSocket-Key: %s\r\n" \
		"Sec-WebSocket-Version: 13\r\n" \
		"Sec-WebSocket-Protocol: %s\r\n" \
		"\r\n"
		
	response_template = "HTTP/1.1 101 Switching Protocols\r\n" \
		"Connection: upgrade\r\n" \
		"Upgrade: WebSocket\r\n" \
		"Sec-WebSocket-Accept: %s\r\n" \
		"Sec-WebSocket-Protocol: %s\r\n" \
		"\r\n"
		
	def __init__(self, ssl, protocol="NEX", sock=None):
		self.protocol = protocol
		self.sock = sock
		
		if not self.sock:
			if ssl:
				self.sock = socket.Socket(socket.TYPE_SSL)
			else:
				self.sock = socket.Socket(socket.TYPE_TCP)
		
		self.state = STATE_READY
		
		self.buffer = b""
		self.fragments = None
		self.message_type = None
		self.packets = []

	def connect(self, host, port, timeout=None):
		if self.state != STATE_READY:
			raise RuntimeError("Socket may only be used once")
			
		self.state = STATE_CONNECTING
		
		path = "/"
		if "/" in host:
			path = host[host.index("/"):]
			host = host[:host.index("/")]
			
		logger.debug("Connecting websocket: (%s, %i)", host, port)
		
		if not self.sock.connect(host, port):
			logger.error("Socket connection failed")
			self.state = STATE_DISCONNECTED
			return False

		self.socket_event = scheduler.add_socket(self.handle_recv, self.sock)
		
		self.key = secrets.token_urlsafe()
		handshake = self.handshake_template %(path, host, self.key, self.protocol)
		self.sock.send(handshake.encode("ascii"))
		
		while self.state == STATE_CONNECTING:
			scheduler.update()
		if self.state != STATE_CONNECTED:
			logger.error("Websocket connection failed")
			return False
			
		logger.debug("Websocket connection OK")
		return True
		
	def accept(self):
		if self.state != self.STATE_READY:
			raise RuntimeError("Socket may only be used once")
			
		self.state = STATE_ACCEPTING
			
		self.socket_event = scheduler.add_socket(self.handle_recv, self.sock)
		
		while self.state == STATE_ACCEPTING:
			scheduler.update()
		return self.state == STATE_CONNECTED
		
	def cleanup(self):
		self.state = STATE_DISCONNECTED
		if self.socket_event:
			scheduler.remove(self.socket_event)
		
	def calculate_key_hash(self, key):
		string = key.encode("ascii") + b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
		hash = hashlib.sha1(string).digest()
		text = base64.encodebytes(hash).decode("ascii")
		return text.strip()
		
	def parse_headers(self, lines):
		headers = {}
		for line in lines:
			if ": " in line:
				key, value = line.split(": ", 1)
				headers[key] = value
		return headers
			
	def handle_recv(self, data):
		if not data:
			logger.debug("Server closed the connection")
			return self.cleanup()
	
		self.buffer += data
		while self.buffer:
			if self.state == STATE_CONNECTING:
				if b"\r\n\r\n" not in self.buffer:
					return

				response, self.buffer = self.buffer.split(b"\r\n\r\n", 1)
				lines = response.decode("ascii").splitlines()
				if not lines[0].startswith("HTTP/1.1"):
					logger.error("Invalid handshake response")
					return self.cleanup()
				
				code = int(lines[0][9:12])
				if code != 101:
					logger.error("Server replied with status code %i" %code)
					return self.cleanup()
					
				expected_header = "Sec-WebSocket-Accept: " + self.calculate_key_hash(self.key)
				if expected_header not in lines:
					logger.error("Sec-WebSocket-Accept check failed")
					return self.cleanup()
				
				self.state = STATE_CONNECTED
					
			elif self.state == STATE_ACCEPTING:
				if b"\r\n\r\n" not in self.buffer:
					return
				
				request, self.buffer = self.buffer.split(b"\r\n\r\n", 1)
				lines = request.decode("ascii").splitlines()
				
				if not lines[0].startswith("GET") or "HTTP/1.1" not in lines[0]:
					logger.error("Invalid handshake request")
					return self.cleanup()
				
				headers = self.parse_headers(lines[1:])
				
				if "Sec-WebSocket-Key" not in headers:
					logger.error("Sec-WebSocket-Key header missing")
					return self.cleanup()
					
				if "Sec-WebSocket-Protocol" not in headers:
					logger.error("Sec-WebSocket-Protocol header missing")
					return self.cleanup()
				
				self.protocol = headers["Sec-WebSocket-Protocol"]
				
				accept = self.calculate_key_hash(headers["Sec-WebSocket-Key"])
				response = self.response_template % (accept, self.protocol)
				
				self.state = STATE_CONNECTED
					
			elif self.state == STATE_CONNECTED:
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
				payload = self.apply_mask(self.buffer[offset : offset + size], mask_key)
				
				if opcode == OPCODE_CONTINUE:
					if self.message_type not in [OPCODE_TEXT, OPCODE_BINARY]:
						logger.error("Invalid continuation frame received")
						return self.cleanup()
					self.fragments += payload
				else:
					self.fragments = payload
					self.message_type = opcode
				
				if fin:
					self.process_packet(opcode, self.fragments)
					self.fragments = None
					self.message_type = None
				
				self.buffer = self.buffer[offset + size:]
				
	def process_packet(self, opcode, payload):
		if opcode == OPCODE_BINARY:
			self.packets.append(payload)
		else:
			logger.error("Unknown opcode received: %i" %opcode)
			self.cleanup()
		
	def apply_mask(self, data, key):
		return bytes([data[i] ^ key[i % 4] for i in range(len(data))])
		
	def send_packet(self, opcode, payload=b""):
		data = bytes([0x80 | opcode])
		
		length = len(payload)
		if length < 126:
			data += bytes([0x80 | length])
		elif length <= 0xFFFF:
			data += struct.pack(">BH", 0xFE, length)
		else:
			data += struct.pack(">BQ", 0xFF, length)
			
		mask = secrets.token_bytes(4)
		data += mask + self.apply_mask(payload, mask)
		self.sock.send(data)
		
	def close(self):
		if self.state == STATE_CONNECTED:
			self.send_packet(OPCODE_DISCONNECT)
		self.sock.close()
		self.cleanup()

	def send(self, data):
		if self.state != STATE_CONNECTED:
			raise RuntimeError("Can't send data on a disconnected websocket")
		self.send_packet(OPCODE_BINARY, data)

	def recv(self):
		if self.state != STATE_CONNECTED: return b""
		if self.packets:
			return self.packets.pop(0)
			
	def local_address(self): return self.sock.local_address()
	def remote_address(self): return self.sock.remote_address()

	
class WebSocketServer:
	def __init__(self, ssl, server=None):
		self.ssl = ssl
		self.server = server
		
		if not self.server:
			if ssl:
				self.server = socket.SocketServer(socket.TYPE_SSL)
			else:
				self.server = socket.SocketServer(socket.TYPE_TCP)
				
		self.sockets = []
		
	def start(self, host, port):
		self.server.start(host, port)
		scheduler.add_server(self.handle, self.server)
		
	def handle(self, socket):
		client = WebSocketClient(self.ssl, sock=socket)
		if client.accept():
			self.sockets.append(client)
		
	def accept(self, client):
		pass
	