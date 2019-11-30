
from . import socket, ssl, signal, util, scheduler, types
import json

import logging
logger = logging.getLogger(__name__)


RESULT_DONE = 0
RESULT_INCOMPLETE = 1
RESULT_ERROR = 2


STATUS_NAMES = {
	200: "OK",
	400: "Bad Request",
	401: "Unauthorized",
	403: "Forbidden",
	404: "Not Found",
	405: "Method Not Allowed",
	500: "Internal Server Error"
}


TEXT_TYPES = [
	"application/x-www-form-urlencoded",
	"application/json"
]


class HTTPHeaders(types.CaseInsensitiveDict):
	pass


class HTTPFormData(types.OrderedDict):
	def parse(self, data):
		fields = data.split("&")
		for field in fields:
			if not "=" in field:
				logger.warning("Malformed form parameter")
				return False
			key, value = field.split("=", 1)
			self[key] = value
		return True
		
	def encode(self):
		fields = []
		for key, value in self.items():
			fields.append("%s=%s" %(key, value))
		return "&".join(fields)


class HTTPMessage:
	def __init__(self):
		self.headers = HTTPHeaders()
		self.body = b""
		
		self.text = None
		
		self.form = HTTPFormData()
		self.json = None
		
	def prepare(self, *, headers=None, body=None, form=None, json=None):
		if headers: self.headers = headers
		if body: self.body = body
		if form: self.form = form
		
	def finish(self):
		content_type = self.headers.get("Content-Type", "")
		fields = content_type.split("; ")
		type = fields[0]
		
		param = {}
		for field in fields[1:]:
			if not "=" in field:
				logger.warning("Malformed directive Content-Type header")
				return False
			
			key, value = field.split("=", 1)
			param[key] = value
		
		if type in TEXT_TYPES:
			try:
				self.text = self.body.decode(param.get("charset", "UTF-8"))
			except UnicodeDecodeError:
				logger.warning("Failed to decode HTTP body")
				return False
		
		if type == "application/x-www-form-urlencoded":
			if not self.form.parse(self.text):
				return False
		
		if type == "application/json":
			try:
				self.json = json.loads(self.text)
			except json.JSONDecodeError:
				logger.warning("Failed to decode JSON body")
				return False
		
		return True
		
	def encode(self):
		self.encode_body()
		
		self.headers["Content-Length"] = len(self.body)
		
		lines = [self.encode_header()]
		for key, value in self.headers.items():
			lines.append("%s: %s" %(key, value))
		
		text = "\r\n".join(lines) + "\r\n\r\n"
		return text.encode() + self.body
		
	def encode_body(self):
		if self.text is not None:
			self.body = self.text.encode()
	
		if self.form:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "application/x-www-form-urlencoded"
			self.body = self.form.encode()
		elif self.json is not None:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "application/json"
			self.body = json.dumps(self.json)
			
		self.body = self.body.encode()
		
	def encode_header(self): return ""


class HTTPRequest(HTTPMessage):
	def __init__(self):
		super().__init__()
		self.method = "GET"
		self.path = "/"
		self.version = "HTTP/1.1"
		
		self.params = HTTPFormData()
		self.form = HTTPFormData()
		
	def finish(self):
		if not super().finish():
			return False
			
		if "?" in self.path:
			self.path, params = self.path.split("?", 1)
			if not self.params.parse(params):
				return False
		return True
		
	def encode_header(self):
		path = self.path
		if self.params:
			path += "?" + self.params.encode()
		return "%s %s %s" %(self.method, path, self.version)
	
	@staticmethod
	def build(method, path, *, params=None, **kwargs):
		request = HTTPRequest()
		request.method = method
		request.path = path
		if params:
			request.params = params
		request.prepare(**kwargs)
		return request
		
	@staticmethod
	def get(*args, **kwargs):
		return HTTPRequest.build("GET", *args, **kwargs)
		
	@staticmethod
	def post(*args, **kwargs):
		return HTTPRequest.build("POST", *args, **kwargs)
		

class HTTPResponse(HTTPMessage):
	def __init__(self):
		super().__init__()
		self.version = "HTTP/1.1"
		self.status = 400
		self.status_name = "Bad Request"
		
	def encode_header(self):
		return "%s %i %s" %(self.version, self.status, self.status_name)
		
	@staticmethod
	def build(status, **kwargs):
		response = HTTPResponse()
		response.status = status
		response.status_name = STATUS_NAMES[status]
		response.prepare(**kwargs)
		return response


class HTTPParser:
	def __init__(self):
		self.buffer = b""
		self.state = self.state_header
		self.message = None
		
		self.message_event = signal.Signal()
		
	def update(self, data):
		self.buffer += data
		
		result = self.state()
		while self.buffer and result == RESULT_DONE:
			result = self.state()
		
		return result
		
	def finish(self):
		if not self.message.finish():
			return RESULT_ERROR
		
		self.message_event(self.message)
		
		self.state = self.state_header
		self.message = None
		return RESULT_DONE
	
	def state_header(self):
		if not b"\r\n\r\n" in self.buffer:
			return RESULT_INCOMPLETE
		
		header, self.buffer = self.buffer.split(b"\r\n\r\n", 1)
		
		try:
			lines = header.decode().splitlines()
		except UnicodeDecodeError:
			logger.warning("Failed to decode HTTP message")
			return RESULT_ERROR
			
		if len(lines) == 0:
			logger.warning("HTTP message must start with header line")
			return RESULT_ERROR
		
		fields = lines[0].split(maxsplit=2)
		if len(fields) != 3:
			logger.warning("Invalid HTTP start line")
			return RESULT_ERROR
		
		if fields[0].startswith("HTTP/"):
			if not util.is_numeric(fields[1]):
				logger.warning("Invalid HTTP status code")
				return RESULT_ERROR
			self.message = HTTPResponse()
			self.message.version = fields[0]
			self.message.status = int(fields[1])
			self.message.status_name = fields[2]
		
		elif fields[2].startswith("HTTP/"):
			self.message = HTTPRequest()
			self.message.method = fields[0]
			self.message.path = fields[1]
			self.message.version = fields[2]
			
		else:
			logger.warning("Invalid HTTP start line")
			return RESULT_ERROR
		
		for header in lines[1:]:
			if not ": " in header:
				logger.warning("Invalid line in HTTP headers")
				return RESULT_ERROR
			key, value = header.split(": ", 1)
			self.message.headers[key] = value
		
		encoding = self.message.headers.get("Transfer-Encoding", "identity")
		encodings = [enc.strip() for enc in encoding.split(",")]
		
		if "chunked" in encodings:
			self.state = self.state_chunk_header
			return self.state()
		
		elif "Content-Length" in self.message.headers:
			if not util.is_numeric(self.message.headers["Content-Length"]):
				logger.warning("Invalid Content-Length header")
				return RESULT_ERROR
			
			self.state = self.state_body
			return self.state()
		
		return self.finish()
		
	def state_chunk_header(self):
		if not b"\r\n" in self.buffer:
			return RESULT_INCOMPLETE
		
		line, self.buffer = self.buffer.split(b"\r\n", 1)
		try:
			line = line.decode()
		except UnicodeDecodeError:
			logger.warning("Failed to decode chunk length")
			return RESULT_ERROR
			
		if not util.is_hexadecimal(line):
			logger.warning("Invalid HTTP chunk length")
			return RESULT_ERROR
		
		self.chunk_length = int(line, 16)
			
		self.state = self.state_chunk_body
		return self.state()
		
	def state_chunk_body(self):
		if len(self.buffer) < self.chunk_length + 2:
			return RESULT_INCOMPLETE
			
		if self.buffer[self.chunk_length : self.chunk_length + 2] != b"\r\n":
			logger.warning("HTTP chunk should be terminated with \\r\\n")
			return RESULT_ERROR
		
		self.message.body += self.buffer[:self.chunk_length]
		
		self.buffer = self.buffer[self.chunk_length + 2:]
		
		if self.chunk_length == 0:
			return self.finish()
		
		self.state = self.state_chunk_header
		return self.state()
		
	def state_body(self):
		length = int(self.message.headers["Content-Length"])
		if len(self.buffer) < length:
			return RESULT_INCOMPLETE
			
		self.message.body = self.buffer[:length]
		
		self.buffer = self.buffer[length:]
		
		return self.finish()
		
		
class HTTPSocket:
	def __init__(self, sock, server):
		self.sock = sock
		self.server = server
		
		self.parser = HTTPParser()
		self.parser.message_event.add(self.process_message)
		
		self.event = scheduler.add_socket(self.process_data, sock)
		
		self.active = True
		self.closed = signal.Signal()
		
		self.messages = []
	
	def set_certificate(self, cert, key):
		self.sock.set_certificate(cert, key)
		
	def close(self):
		if self.active:
			self.active = False
			scheduler.remove(self.event)
			self.sock.close()
			self.closed()
		
	def process_data(self, data):
		if not data:
			logger.debug("HTTP socket was closed")
			scheduler.remove(self.event)
			self.closed()
			self.active = False
		else:
			self.parser.update(data)
		
	def process_message(self, message):
		if isinstance(message, HTTPRequest):
			if self.server:
				self.messages.append(message)
			else:
				logger.warning("Received unexpected HTTP request")
		else:
			if not self.server:
				self.messages.append(message)
			else:
				logger.warning("Received unexpected HTTP response")
	
	def send(self, message):
		self.sock.send(message.encode())
	
	def recv(self):
		if self.messages:
			return self.messages.pop(0)
			
			
class HTTPReqMgr:
	def __init__(self, sock):
		self.sock = sock
		self.event = scheduler.add_socket(self.handle, sock)
		
		self.closed = signal.Signal()
		self.sock.closed.add(self.handle_closed)
		
		self.request_id = 0
		self.response_id = 0
		self.responses = {}
		
	def handle_closed(self):
		for i in range(self.response_id, self.request_id):
			self.responses[i] = -1
		self.closed()
		
	def close(self):
		scheduler.remove(self.event)
		self.sock.close()

	def handle(self, message):
		self.responses[self.response_id] = message
		self.response_id += 1
		
	def cancel(self, id):
		self.responses[id] = -2
		
	def request(self, req, timeout=5):
		id = self.request_id
		self.request_id += 1
		
		self.sock.send(req)
		
		event = scheduler.add_timeout(self.cancel, timeout, param=id)
		while id not in self.responses:
			scheduler.update()
		scheduler.remove(event)
		
		response = self.responses.pop(id)
		if response == -1:
			raise ConnectionError("HTTP connection was closed unexpectedly")
		elif response == -2:
			self.close()
			raise ConnectionError("HTTP request timed out")
			
		if response.headers.get("Connection") == "close":
			logger.debug("Server requested connection close")
			self.close()
		
		return response
		
		
class HTTPPool:
	def __init__(self):
		self.clients = {}
		self.timeouts = {}
		
	def get(self, req, ssl, cert=None):
		if "Host" not in req.headers:
			raise ValueError("HTTP request requires Host header")
			
		host = req.headers["Host"]
		key = (host, ssl, cert if ssl else None)
		
		if key not in self.clients:
			sock = self.connect(req, ssl, cert)
			if not sock:
				return None
			self.clients[key] = sock
			self.timeouts[key] = scheduler.add_timeout(self.timeout, 15, param=key)
			sock.closed.add(lambda: self.kill(key))
		else:
			logger.debug("Reusing HTTP connection for %s", host)
			self.timeouts[key].reset()
		return self.clients[key]
		
	def connect(self, req, tls, cert):
		host = req.headers["Host"]
		
		logger.debug("Establishing HTTP connection for %s", host)
		
		if tls:
			sock = ssl.SSLClient()
			if cert:
				sock.set_certificate(cert[0], cert[1])
		else:
			sock = socket.TCPSocket()
		
		port = 443 if ssl else 80
		if not sock.connect(host, port):
			logger.error("Failed to establish HTTP connection")
			return None
		
		httpsock = HTTPSocket(sock, False)
		return HTTPReqMgr(httpsock)
		
	def timeout(self, key):
		logger.debug("Closing HTTP connection due to inactivity")
		self.clients[key].close()
		
	def kill(self, key):
		scheduler.remove(self.timeouts.pop(key))
		self.clients.pop(key)
		
		
class HTTPClient:
	def __init__(self):
		self.pool = HTTPPool()
	
	def request(self, req, ssl, cert=None, timeout=5):
		client = self.pool.get(req, ssl, cert)
		return client.request(req, timeout)


class HTTPServer:
	def __init__(self, use_ssl, server=None):
		self.ssl = use_ssl
		self.server = server
		
		if not self.server:
			if use_ssl:
				self.server = ssl.SSLServer()
			else:
				self.server = socket.TCPServer()
				
	def set_certificate(self, cert, key):
		self.server.set_certificate(cert, key)
				
	def start(self, host, port):
		logger.info("Starting HTTP server at %s:%i", host, port)
		self.server.start(host, port)
		scheduler.add_server(self.handle_conn, self.server)
		
	def handle_conn(self, socket):
		address = socket.remote_address()
		logger.debug("New HTTP connection: %s:%i", address[0], address[1])
		
		httpsock = HTTPSocket(socket, True)
		event = scheduler.add_socket(self.handle_req, httpsock, httpsock)
		httpsock.closed.add(lambda: scheduler.remove(event))
		
	def handle_req(self, request, sock):
		logger.debug("Received HTTP request: %s %s", request.method, request.path)
		
		response = self.handle(request)
		if not isinstance(response, HTTPResponse):
			logger.error("HTTP handler must return HTTPResponse")
			response = HTTPResponse.build(500)
		
		logger.debug("Sending HTTP response (%i)", response.status)
		sock.send(response)
		
		if request.headers.get("Connection") == "close":
			logger.debug("Client requested connection close")
			sock.close()
