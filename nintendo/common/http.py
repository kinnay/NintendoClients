
from . import socket, ssl, util, scheduler, types
import datetime
import time
import json

import logging
logger = logging.getLogger(__name__)


RESULT_DONE = 0
RESULT_INCOMPLETE = 1
RESULT_ERROR = 2


STATUS_NAMES = {
	100: "Continue",
	200: "OK",
	400: "Bad Request",
	401: "Unauthorized",
	403: "Forbidden",
	404: "Not Found",
	405: "Method Not Allowed",
	406: "Not Acceptable",
	409: "Conflict",
	412: "Precondition Failed",
	422: "Unprocessable Entity",
	500: "Internal Server Error",
	502: "Bad Gateway",
	503: "Service Unavailable"
}


JSON_TYPES = [
	"application/json",
	"application/problem+json"
]

TEXT_TYPES = [
	"application/x-www-form-urlencoded",
	"text/plain",
	*JSON_TYPES
]


def format_date():
	now = datetime.datetime.now(datetime.timezone.utc)
	return now.strftime("%a, %d %b %Y %H:%M:%S GMT")


class HTTPHeaders(types.CaseInsensitiveDict):
	pass


class HTTPFormData(types.OrderedDict):
	def parse(self, data):
		fields = data.split("&")
		for field in fields:
			if not "=" in field:
				logger.error("Malformed form parameter")
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
		self.version = "HTTP/1.1"
	
		self.headers = HTTPHeaders()
		self.body = b""
		
		self.text = None
		
		self.files = types.OrderedDict()
		self.form = HTTPFormData()
		self.json = None
		
		self.boundary = "--------BOUNDARY--------"
		
	def prepare(self, *, headers=None, body=None, form=None, json=None, files=None):
		if headers: self.headers = headers
		if body: self.body = body
		if form: self.form = form
		if json: self.json = json
		if files: self.files = files
		
	def check_version(self):
		if not self.version.startswith("HTTP/"):
			logger.error("HTTP version must start with HTTP/")
			return False
			
		if self.version != "HTTP/1.1":
			logger.error("HTTP version not supported")
			return False
			
		return True
		
	def transfer_encodings(self):
		encoding = self.headers.get("Transfer-Encoding", "identity")
		return [enc.strip() for enc in encoding.split(",")]
		
	def is_chunked(self):
		return "chunked" in self.transfer_encodings()
		
	def finish(self):
		content_type = self.headers.get("Content-Type", "")
		fields = content_type.split("; ")
		type = fields[0]
		
		param = {}
		for field in fields[1:]:
			if not "=" in field:
				logger.error("Malformed directive Content-Type header")
				return False
			
			key, value = field.split("=", 1)
			param[key] = value
		
		if type in TEXT_TYPES:
			try:
				self.text = self.body.decode(param.get("charset", "UTF-8"))
			except UnicodeDecodeError:
				logger.error("Failed to decode HTTP body")
				return False
		
		if type == "application/x-www-form-urlencoded":
			if not self.form.parse(self.text):
				return False
		
		if type in JSON_TYPES:
			try:
				self.json = json.loads(self.text)
			except json.JSONDecodeError:
				logger.error("Failed to decode JSON body")
				return False
		
		return True
		
	def check_conflicts(self):
		params = [self.form, self.json, self.files, self.text, self.body]
		if len([x for x in params if x]) > 1:
			raise ValueError("Parameters are incompatible")
		
	def prepare_body(self):
		self.check_conflicts()
		
		if self.form:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "application/x-www-form-urlencoded"
			self.text = self.form.encode()
		
		elif self.json is not None:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "application/json"
			self.text = json.dumps(self.json)
			
		elif self.files is not None:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "multipart/form-data"
			self.headers["Content-Type"] += "; boundary=%s" %self.boundary
				
			self.body = b""
			for name, data in self.files.items():
				self.body += b"--%s\r\n" %self.boundary.encode()
				self.body += b"Content-Disposition: form-data; name=\"%s\"\r\n\r\n" %name.encode()
				self.body += data + b"\r\n"
			self.body += b"--%s--\r\n" %self.boundary.encode()
			
		if self.text is not None:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "text/plain"
			self.body = self.text.encode()
			
		if self.is_chunked():
			self.body = b"%x\r\n" %len(self.body) + self.body + b"\r\n0\r\n\r\n"
		else:
			self.headers["Content-Length"] = len(self.body)
			if len(self.body) > 1024:
				self.headers["Expect"] = "100-continue"
			
	def encode_start_line(self): return ""
	
	def encode(self):
		return self.encode_headers() + self.encode_body()
	
	def encode_headers(self):
		lines = [self.encode_start_line()]
		for key, value in self.headers.items():
			lines.append("%s: %s" %(key, value))
		
		text = "\r\n".join(lines) + "\r\n\r\n"
		return text.encode()
		
	def encode_body(self):
		return self.body


class HTTPRequest(HTTPMessage):
	def __init__(self):
		super().__init__()
		self.method = "GET"
		self.path = "/"
		
		self.params = HTTPFormData()
		
		self.certificate = None
		
	def finish(self):
		if not super().finish():
			return False
			
		if "?" in self.path:
			self.path, params = self.path.split("?", 1)
			if not self.params.parse(params):
				return False
		return True
		
	def encode_start_line(self):
		path = self.path
		if self.params:
			path += "?" + self.params.encode()
		return "%s %s %s" %(self.method, path, self.version)
		
	def parse_start_line(self, line):
		fields = line.split(maxsplit=2)
		if len(fields) != 3:
			logger.error("Failed to parse HTTP request start line")
			return False
		
		self.method = fields[0]
		self.path = fields[1]
		self.version = fields[2]
		return self.check_version()
	
	@staticmethod
	def build(method, path, *, params=None, certificate=None, **kwargs):
		request = HTTPRequest()
		request.method = method
		request.path = path
		if params:
			request.params = params
		request.certificate = certificate
		request.prepare(**kwargs)
		return request
		
	@staticmethod
	def get(*args, **kwargs):
		return HTTPRequest.build("GET", *args, **kwargs)
		
	@staticmethod
	def post(*args, **kwargs):
		return HTTPRequest.build("POST", *args, **kwargs)
		

class HTTPResponse(HTTPMessage):
	def __init__(self, status=500):
		super().__init__()
		self.status = status
		self.status_name = STATUS_NAMES[status]
		
	def encode_start_line(self):
		return "%s %i %s" %(self.version, self.status, self.status_name)
		
	def parse_start_line(self, line):
		fields = line.split(maxsplit=2)
		if len(fields) != 3:
			logger.error("Failed to parse HTTP response start line")
			return False
		
		self.version = fields[0]
		if not self.check_version():
			return False
			
		if not util.is_numeric(fields[1]):
			logger.error("Received invalid status code in HTTP response")
			return False
			
		self.status = int(fields[1])
		self.status_name = fields[2]
		return True
		
	@staticmethod
	def build(status, **kwargs):
		response = HTTPResponse(status)
		response.prepare(**kwargs)
		return response
		
		
class HTTPParser:
	def __init__(self, cls, sock):
		self.cls = cls
		self.sock = sock
		
		self.buffer = b""
		self.state = self.state_header
		self.result = RESULT_INCOMPLETE
		self.message = self.cls()
		self.messages = []
		self.callback = None
		
		self.event = scheduler.add_socket(self.process, self.sock)
		
	def cleanup(self):
		scheduler.remove(self.event)
		self.sock.close()
		
		self.sock = None
		
	def listen(self, callback):
		self.callback = callback
		
	def wait(self, timeout):
		start = time.monotonic()
		while self.sock and not self.messages:
			if time.monotonic() - start > timeout:
				self.cleanup()
				raise RuntimeError("HTTP request timed out")
			scheduler.update()
			
		if not self.messages:
			raise RuntimeError("HTTP request failed")
		
		return self.messages.pop(0)
		
	def process(self, data):
		if not data:
			self.cleanup()
			return
	
		self.buffer += data
		
		result = self.state()
		while self.buffer and result == RESULT_DONE:
			result = self.state()
		
		if result == RESULT_ERROR:
			self.cleanup()
		
	def finish(self):
		if not self.message.finish():
			return RESULT_ERROR
		
		if self.callback:
			self.callback(self.message)
		else:
			self.messages.append(self.message)
		self.message = self.cls()
		self.state = self.state_header
		return RESULT_DONE
		
	def state_header(self):
		if not b"\r\n\r\n" in self.buffer:
			return RESULT_INCOMPLETE
		
		header, self.buffer = self.buffer.split(b"\r\n\r\n", 1)
		
		try:
			lines = header.decode().splitlines()
		except UnicodeDecodeError:
			logger.error("Failed to decode HTTP message")
			return RESULT_ERROR
			
		if len(lines) == 0:
			logger.error("HTTP message must start with header line")
			return RESULT_ERROR
			
		if not self.message.parse_start_line(lines[0]):
			return RESULT_ERROR
			
		for header in lines[1:]:
			if not ": " in header:
				logger.error("Invalid line in HTTP headers")
				return RESULT_ERROR
			key, value = header.split(": ", 1)
			self.message.headers[key] = value
			
		if self.message.headers.get("Expect") == "100-continue":
			logger.debug("Sending 100-continue response")
			self.sock.send(HTTPResponse(100).encode())
			
		if self.message.is_chunked():
			self.state = self.state_chunk_header
			return self.state()
		elif "Content-Length" in self.message.headers:
			if not util.is_numeric(self.message.headers["Content-Length"]):
				logger.error("Invalid Content-Length header")
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
			logger.error("Failed to decode chunk length")
			return RESULT_ERROR
			
		if not util.is_hexadecimal(line):
			logger.error("Invalid HTTP chunk length")
			return RESULT_ERROR
		
		self.chunk_length = int(line, 16)
			
		self.state = self.state_chunk_body
		return self.state()
		
	def state_chunk_body(self):
		if len(self.buffer) < self.chunk_length + 2:
			return RESULT_INCOMPLETE
			
		if self.buffer[self.chunk_length : self.chunk_length + 2] != b"\r\n":
			logger.error("HTTP chunk should be terminated with \\r\\n")
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


class HTTPReqClient:
	def create_socket(self, req, tls):
		if tls:
			sock = ssl.SSLClient(ssl.VERSION_TLS12)
			
			cert = req.certificate
			if cert:
				sock.set_certificate(cert[0], cert[1])
		else:
			sock = socket.TCPClient()
		return sock
	
	def connect(self, req, tls, timeout):
		if "Host" not in req.headers:
			raise ValueError("HTTP request requires Host header")
	
		sock = self.create_socket(req, tls)
			
		host = req.headers["Host"]
		port = 443 if tls else 80
		
		logger.info("Establishing HTTP connection with %s:%i", host, port)
		if not sock.connect(host, port, timeout):
			raise RuntimeError("Failed to establish HTTP connection")
			
		return sock
		
	def process(self, req, tls, timeout):
		sock = self.connect(req, tls, timeout)
		parser = HTTPParser(HTTPResponse, sock)

		req.prepare_body()
		sock.send(req.encode_headers())
		
		if req.headers.get("Expect") == "100-continue":
			response = parser.wait(timeout)
			if response.status != 100:
				parser.cleanup()
				return response
			
		sock.send(req.encode_body())

		response = parser.wait(timeout)
		parser.cleanup()
		
		return response
				
				
class HTTPReqServer:
	def __init__(self, sock):
		self.sock = sock
		
	def accept(self, callback):
		self.callback = callback
		self.decoder = HTTPParser(HTTPRequest, self.sock)
		self.decoder.listen(self.process_request)
				
	def process_request(self, request):
		response = self.callback(request)
		response.prepare_body()
		self.sock.send(response.encode())
		
		if request.headers.get("Connection") == "close":
			logger.debug("Client requested connection close")
			self.cleanup()
			return


class HTTPClient:
	def request(self, req, tls, timeout=3):
		client = HTTPReqClient()
		logger.info("Performing HTTP request: %s %s", req.method, req.path)
		response = client.process(req, tls, timeout)
		logger.info("Received HTTP response: %i", response.status)
		return response


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
		logger.info("New HTTP connection: %s:%i", address[0], address[1])
		
		httpsock = HTTPReqServer(socket)
		httpsock.accept(self.handle_req)
		
	def handle_req(self, request):
		logger.info("Received HTTP request: %s %s", request.method, request.path)
		
		response = self.handle(request)
		if not isinstance(response, HTTPResponse):
			logger.error("HTTP handler must return HTTPResponse")
			response = HTTPResponse(500)
		
		logger.info("Sending HTTP response (%i)", response.status)
		return response
		
	def handle(self, request):
		logger.error("Server does not implement a HTTP request handler")
		return HTTPResponse(500)
