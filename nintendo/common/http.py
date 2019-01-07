
from . import socket, signal, util, scheduler

import logging
logger = logging.getLogger(__name__)


class HTTPRequest:
	def __init__(self):
		self.method = None
		self.path = None
		self.version = None
		self.headers = {}
		self.body = b""

	
class HTTPState:
	message_event = signal.Signal()
	
	RESULT_OK = 0
	RESULT_INCOMPLETE = 1
	RESULT_ERROR = 2
	
	def __init__(self, socket):
		self.socket = socket
		
		self.buffer = b""
		self.state = self.state_header
		self.event = scheduler.add_socket(self.handle_recv, socket)
		self.request = HTTPRequest()
		
	def handle_recv(self, data):
		if not data:
			scheduler.remove(self.event)
			self.close_event(self)
		
		self.buffer += data
		result = self.state()
		while self.buffer and result == self.RESULT_OK:
			result = self.state()
			
		if result == self.RESULT_ERROR:
			self.socket.close()
			scheduler.remove(self.event)
			
	def handle_header(self, data):
		try:
			lines = data.decode("ascii").splitlines()
		except UnicodeDecodeError:
			return self.RESULT_ERROR
		
		fields = lines[0].split()
		if len(fields) != 3:
			return self.RESULT_ERROR
			
		self.request.method = fields[0]
		self.request.path = fields[1]
		self.request.version = fields[2]
		for header in lines[1:]:
			if not ": " in header:
				return self.RESULT_ERROR
			key, value = header.split(": ", 1)
			self.request.headers[key.lower()] = value
			
		if not "content-length" in self.request.headers:
			return self.RESULT_ERROR
		if not util.is_numeric(self.request.headers["content-length"]):
			return self.RESULT_ERROR
			
		self.state = self.state_body
		return self.RESULT_OK
	
	def state_header(self):
		if b"\r\n\r\n" in self.buffer:
			header, self.buffer = self.buffer.split(b"\r\n\r\n", 1)
			return self.handle_header(header)
		return self.RESULT_INCOMPLETE
		
	def state_body(self):
		length = int(self.request.headers["content-length"])
		if len(self.buffer) < length:
			return self.RESULT_INCOMPLETE
		
		self.request.body = self.buffer[:length]
		self.buffer = self.buffer[length:]
		
		self.message_event(self.request)
		self.state = self.state_header
		return self.RESULT_OK

	
class HTTPServer:
	def __init__(self, ssl, server=None):
		self.ssl = ssl
		self.server = server
		
		if not self.server:
			if ssl:
				self.server = socket.SocketServer(socket.TYPE_SSL)
			else:
				self.server = socket.SocketServer(socket.TYPE_TCP)
				
	def start(self, host, port):
		self.server.start(host, port)
		scheduler.add_server(self.handle_conn, self.server)
		
	def handle_conn(self, socket):
		state = HTTPState(socket)
		state.message_event.add(self.handle)
		
	def handle(self, request):
		pass
