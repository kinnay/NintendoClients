
from . import socket, scheduler
import random
import struct
import time

import logging
logger = logging.getLogger(__name__)


OPCODE_CONTINUE = 0
OPCODE_TEXT = 1
OPCODE_BINARY = 2
OPCODE_DISCONNECT = 8
OPCODE_PING = 9
OPCODE_PONG = 10

STATE_DISCONNECTED = 0
STATE_CONNECTING = 1
STATE_CONNECTED = 2


class WebSocket:
	handshake_template = "GET %s HTTP/1.1\r\n" \
		"Host: %s\r\n" \
		"Upgrade: websocket\r\n" \
		"Connection: upgrade\r\n" \
		"Sec-WebSocket-Key: NEX\r\n" \
		"Sec-WebSocket-Version: 13\r\n" \
		"Sec-WebSocket-Protocol: NEX\r\n" \
		"\r\n"
		
	def __init__(self):
		self.state = STATE_DISCONNECTED

	def connect(self, host, port=None, timeout=None):
		if self.state != STATE_DISCONNECTED:
			raise RuntimeError("Socket was not disconnected")
		
		scheme = None
		if "://" in host:
			scheme, host = host.split("://", 1)
			
		self.state = STATE_CONNECTING
		
		path = "/"
		if "/" in host:
			path = host[host.index("/"):]
			host = host[:host.index("/")]
			
		if scheme is None:
			if port is None:
				raise ValueError("Neither scheme nor port specified")
			if port not in [80, 443]:
				raise ValueError("Couldn't derive scheme from port")
			scheme = "wss" if port == 443 else "ws"
			
		if scheme not in ["wss", "ws"]:
			raise ValueError("Invalid scheme")
			
		if port is None:
			port = 443 if scheme == "wss" else 80

		if scheme == "wss":
			self.s = socket.Socket(socket.TYPE_SSL)
		else:
			self.s = socket.Socket(socket.TYPE_TCP)
			
		logger.debug("Connecting websocket: (%s, %i)", host, port)
		
		self.buffer = b""
		self.fragments = b""
		self.packets = []
		if not self.s.connect(host, port):
			logger.error("Socket connection failed")
			self.state = STATE_DISCONNECTED

		self.socket_event = scheduler.add_socket(self.handle_recv, self.s)
		
		handshake = self.handshake_template %(path, host)
		self.s.send(handshake.encode("ascii"))
		
		while self.state == STATE_CONNECTING:
			scheduler.update()
			time.sleep(0.05)
		if self.state != STATE_CONNECTED:
			logger.error("Websocket connection failed")
			return False
			
		logger.debug("Websocket connection OK")
		return True
		
	def remove_events(self):
		scheduler.remove(self.socket_event)
			
	def handle_recv(self, data):
		if not data:
			logger.debug("Server closed the connection")
			self.state = STATE_DISCONNECTED
			self.remove_events()
	
		self.buffer += data
		if self.state == STATE_CONNECTING:
			if b"\r\n\r\n" in self.buffer:
				if not self.buffer.startswith(b"HTTP/1.1"):
					logger.error("Invalid handshake response")
					self.state = STATE_DISCONNECTED
					self.remove_events()
				
				code = int(data[9:12])
				if code != 101:
					logger.error("Server replied with status code %i" %code)
					self.state = STATE_DISCONNECTED
					self.remove_events()
					
				self.buffer = self.buffer.split(b"\r\n\r\n", 1)[1]
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
			
			self.fragments += payload
			if fin:
				self.packets.append(self.fragments)
				self.fragments = b""
			
			self.buffer = self.buffer[offset + size:]
		
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
			
		mask = struct.pack(">I", random.randint(0, 0xFFFFFFFF))
		data += mask + self.apply_mask(payload, mask)
		self.s.send(data)
		
	def close(self):
		if self.state != STATE_DISCONNECTED:
			self.send_packet(OPCODE_DISCONNECT)
			self.s.close()
			
			self.state = STATE_DISCONNECTED
			self.remove_events()

	def send(self, data):
		if self.state != STATE_CONNECTED:
			raise RuntimeError("Can't send data on a disconnected websocket")
		self.send_packet(OPCODE_BINARY, data)

	def recv(self):
		if self.state != STATE_CONNECTED: return b""
		if self.packets:
			return self.packets.pop(0)
			
	def get_address(self): return self.s.get_address()
	def get_port(self): return self.s.get_port()
