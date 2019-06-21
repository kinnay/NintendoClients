
from . import socket, signal, util, scheduler

import logging
logger = logging.getLogger(__name__)


class HTTPFormData:
	def __init__(self):
		self.fields = {}
		
	def parse(self, data):
		fields = data.split("&")
		for field in fields:
			if not "=" in field:
				logger.warning("Malformed form parameter")
				return False
			key, value = field.split("=", 1)
			self.fields[key] = value
		return True
		
	def __contains__(self, item):
		return item in self.fields
		
	def __getitem__(self, item):
		return self.fields[item]


class HTTPRequest:
	def __init__(self, client):
		self.client = client
		
		self.method = None
		self.path = None
		self.version = None
		self.headers = util.CaseInsensitiveDict()
		self.body = ""
		
		self.params = HTTPFormData()
		self.form = HTTPFormData()
		
	def process(self):
		if "?" in self.path:
			self.path, params = self.path.split("?", 1)
			if not self.params.parse(params):
				return False
				
		if self.headers.get("Content-Type") == "application/x-www-form-urlencoded":
			if not self.form.parse(self.body):
				return False
		return True
		
		
RESPONSE_TEMPLATE = "%s %i %s\r\n%s\r\n"

class HTTPResponse:
	status_names = {
		200: "OK",
		400: "Bad Request",
		401: "Unauthorized",
		403: "Forbidden",
		404: "Not Found",
		405: "Method Not Allowed"
	}
	
	def __init__(self, status):
		self.version = "HTTP/1.1"
		self.status = status
		self.headers = util.CaseInsensitiveDict()
		self.body = ""
		
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
		return (header + self.body).encode("ascii")

	
class HTTPState:
	
	RESULT_OK = 0
	RESULT_INCOMPLETE = 1
	RESULT_ERROR = 2
	
	def __init__(self, socket):
		self.socket = socket
		
		self.buffer = b""
		self.state = self.state_header
		self.event = scheduler.add_socket(self.handle_recv, socket)
		self.request = HTTPRequest(socket)
		
		self.message_event = signal.Signal()
		
	def handle_recv(self, data):
		if not data:
			scheduler.remove(self.event)
			return
		
		self.buffer += data
		result = self.state()
		while self.buffer and result == self.RESULT_OK:
			result = self.state()
			
		if result == self.RESULT_ERROR:
			logger.warning("Failed to parse HTTP request")
			response = HTTPResponse(400)
			self.socket.send(response.encode())
			
			scheduler.remove(self.event)
			self.socket.close()
			
	def finish(self):
		if not self.request.process():
			return self.RESULT_ERROR
		self.message_event(self.request)
		self.request = HTTPRequest(self.socket)
		self.state = self.state_header
		return self.RESULT_OK
			
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
		
		if "Content-Length" in self.request.headers:
			if not util.is_numeric(self.request.headers["Content-Length"]):
				logger.warning("Invalid Content-Length header")
				return self.RESULT_ERROR
			
			self.state = self.state_body
		
		else:
			return self.finish()
		return self.RESULT_OK
	
	def state_header(self):
		if b"\r\n\r\n" in self.buffer:
			header, self.buffer = self.buffer.split(b"\r\n\r\n", 1)
			return self.handle_header(header)
		return self.RESULT_INCOMPLETE
		
	def state_body(self):
		length = int(self.request.headers["Content-Length"])
		if len(self.buffer) < length:
			return self.RESULT_INCOMPLETE
		
		try:
			self.request.body = self.buffer[:length].decode("ascii")
		except UnicodeDecodeError:
			logger.warning("Failed to decode HTTP request body")
			return self.RESULT_ERROR
		self.buffer = self.buffer[length:]
		
		return self.finish()

	
class HTTPServer:
	def __init__(self, ssl, server=None):
		self.ssl = ssl
		self.server = server
		
		if not self.server:
			if ssl:
				self.server = socket.SocketServer(socket.TYPE_SSL)
			else:
				self.server = socket.SocketServer(socket.TYPE_TCP)
				
	def set_certificate(self, cert, key):
		self.server.set_certificate(cert, key)
				
	def start(self, host, port):
		logger.info("Starting HTTP server at %s:%i", host, port)
		self.server.start(host, port)
		scheduler.add_server(self.handle_conn, self.server)
		
	def handle_conn(self, socket):
		address = socket.remote_address()
		logger.debug("New HTTP connection: %s:%i", address[0], address[1])
		
		state = HTTPState(socket)
		state.message_event.add(self.handle_req)
		
	def handle_req(self, request):
		logger.debug("Received HTTP request: %s %s", request.method, request.path)
		response = self.handle(request)
		logger.debug("Sending HTTP response (%i)", response.status)
		request.client.send(response.encode())
		
	def handle(self, request):
		pass
