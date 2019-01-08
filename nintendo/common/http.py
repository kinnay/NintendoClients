
from . import socket, signal, util, scheduler
from requests.structures import CaseInsensitiveDict

import logging
logger = logging.getLogger(__name__)


class HTTPRequest:
	def __init__(self):
		self.client = None
		self.method = None
		self.path = None
		self.version = None
		self.headers = CaseInsensitiveDict()
		self.body = b""
		
		
RESPONSE_TEMPLATE = "%s %i %s\r\n%s\r\n"

class HTTPResponse:
	status_names = {
		200: "OK",
		404: "Not Found"
	}
	
	def __init__(self, status):
		self.version = "HTTP/1.1"
		self.status = status
		self.headers = CaseInsensitiveDict()
		self.body = b""
		
	def encode(self):
		self.headers["Content-Length"] = len(self.body)
		
		headers = ""
		for key, value in self.headers.items():
			headers += "%s: %s\r\n" %(key, value)
		header = RESPONSE_TEMPLATE %(
			self.version, self.status,
			self.status_names[self.status],
			headers
		)
		return header.encode("ascii") + self.body

	
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
		self.request.client = socket
		
	def handle_recv(self, data):
		if not data:
			scheduler.remove(self.event)
			return
		
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
			logger.warning("Failed to decode HTTP request")
			return self.RESULT_ERROR
		
		fields = lines[0].split()
		if len(fields) != 3:
			logger.warning("Invalid HTTP request")
			return self.RESULT_ERROR
			
		self.request.method = fields[0]
		self.request.path = fields[1]
		self.request.version = fields[2]
		for header in lines[1:]:
			if not ": " in header:
				logger.warning("Invalid HTTP request header")
				return self.RESULT_ERROR
			key, value = header.split(": ", 1)
			self.request.headers[key.lower()] = value
			
		if "content-length" in self.request.headers:
			if not util.is_numeric(self.request.headers["content-length"]):
				logger.warning("Invalid Content-Length header")
				return self.RESULT_ERROR
			
			self.state = self.state_body
			
		else:
			self.message_event(self.request)
			self.request = HTTPRequest()
			self.request.client = self.socket
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
		self.request = HTTPRequest()
		self.request.client = self.socket
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
		logger.info("Starting HTTP server at %s:%i", host, port)
		self.server.start(host, port)
		scheduler.add_server(self.handle_conn, self.server)
		
	def handle_conn(self, socket):
		state = HTTPState(socket)
		state.message_event.add(self.handle_req)
		
	def handle_req(self, request):
		logger.debug("Received HTTP request: %s %s", request.method, request.path)
		response = self.handle(request)
		logger.debug("Sending HTTP response (%i)", response.status)
		request.client.send(response.encode())
		
	def handle(self, request):
		pass
