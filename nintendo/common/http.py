
from nintendo.common import tls, util, types, xml
import urllib.parse
import contextlib
import datetime
import anyio
import json

import logging
logger = logging.getLogger(__name__)


STATUS_NAMES = {
	100: "Continue",
	200: "OK",
	201: "Created",
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

STATUS_SUCCESS = [200, 201]


JSON_TYPES = [
	"application/json",
	"application/problem+json"
]

XML_TYPES = [
	"application/xml",
	"text/xml"
]

TEXT_TYPES = [
	"application/x-www-form-urlencoded",
	"text/plain",
	*JSON_TYPES,
	*XML_TYPES
]


class HTTPError(Exception): pass


def format_date():
	now = datetime.datetime.now(datetime.timezone.utc)
	return now.strftime("%a, %d %b %Y %H:%M:%S GMT")
	
	
def urlencode(data):
	return urllib.parse.quote(data)
def urldecode(data):
	return urllib.parse.unquote(data)
	
def formencode(data, url=True):
	fields = []
	for key, value in data.items():
		if url:
			key = urlencode(str(key))
			value = urlencode(str(value))
		fields.append("%s=%s" %(key, value))
	return "&".join(fields)

def formdecode(data, url=True):
	if not data: return {}
		
	fields = {}
	for field in data.split("&"):
		if not "=" in field:
			raise HTTPError("Malformed form parameter")
		key, value = field.split("=", 1)
		if url:
			key = urldecode(key)
			value = urldecode(value)
		fields[key] = value
	return fields


class HTTPMessage:
	def __init__(self):
		self.version = "HTTP/1.1"
	
		self.headers = types.CaseInsensitiveDict()
		self.body = b""
		
		self.text = None
		
		self.files = {}
		self.form = {}
		self.plainform = {}
		self.json = {}
		self.xml = None
		
		self.boundary = "--------BOUNDARY--------"
		
	def check_version(self):
		if not self.version.startswith("HTTP/"):
			raise HTTPError("HTTP version must start with HTTP/")
		if self.version != "HTTP/1.1":
			raise HTTPError("HTTP version not supported")
		
	def transfer_encodings(self):
		encoding = self.headers.get("Transfer-Encoding", "identity")
		return [enc.strip() for enc in encoding.split(",")]
		
	def is_chunked(self):
		return "chunked" in self.transfer_encodings()
		
	def finish_parsing(self):
		content_type = self.headers.get("Content-Type", "")
		fields = content_type.split(";")
		type = fields[0].strip()
		
		param = {}
		for field in fields[1:]:
			field = field.strip()
			if not "=" in field:
				raise HTTPError("Malformed directive in Content-Type header")
			
			key, value = field.split("=", 1)
			param[key] = value
		
		if type in TEXT_TYPES:
			try:
				self.text = self.body.decode(param.get("charset", "UTF-8"))
			except UnicodeDecodeError:
				raise HTTPError("Failed to decode HTTP body")
		
		if type == "application/x-www-form-urlencoded":
			self.form = formdecode(self.text)
			self.plainform = formdecode(self.text, False)
		
		if type in JSON_TYPES:
			try:
				self.json = json.loads(self.text)
			except json.JSONDecodeError:
				raise HTTPError("Failed to decode JSON body")
				
		if type in XML_TYPES:
			try:
				self.xml = xml.parse(self.text)
			except ValueError as e:
				raise HTTPError("Failed to decode XML body: %s" %e)
		
	def encode_body(self):
		text = self.text
		body = self.body
		
		if self.plainform:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "application/x-www-form-urlencoded"
			text = formencode(self.plainform, False)
			
		elif self.form:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "application/x-www-form-urlencoded"
			text = formencode(self.form)
		
		elif self.json:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "application/json"
			text = json.dumps(self.json)
			
		elif self.xml is not None:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "application/xml"
			text = self.xml.encode()
			
		elif self.files:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "multipart/form-data"
			self.headers["Content-Type"] += "; boundary=%s" %self.boundary
			
			text = None
			body = b""
			for name, data in self.files.items():
				body += b"--%s\r\n" %self.boundary.encode()
				body += b"Content-Disposition: form-data; name=\"%s\"\r\n\r\n" %name.encode()
				body += data + b"\r\n"
			body += b"--%s--\r\n" %self.boundary.encode()
			
		if text is not None:
			if "Content-Type" not in self.headers:
				self.headers["Content-Type"] = "text/plain"
			body = text.encode()
		
		if body and "Content-Type" not in self.headers:
			self.headers["Content-Type"] = "application/octet-stream"
		
		if self.is_chunked():
			if not body:
				return b"0\r\n\r\n"
			return b"%x\r\n" %len(body) + body + b"\r\n0\r\n\r\n"
		else:
			if body:
				self.headers["Content-Length"] = len(body)
			return body
	
	def encode_start_line(self): return ""
	
	def encode_headers(self):
		self.encode_body()
		
		lines = [self.encode_start_line()]
		for key, value in self.headers.items():
			lines.append("%s: %s" %(key, value))
		
		text = "\r\n".join(lines) + "\r\n\r\n"
		return text.encode()
	
	def encode(self):
		return self.encode_headers() + self.encode_body()
		
	@classmethod
	def parse(cls, data):
		parser = HTTPParser(cls)
		parser.update(data)
		
		if not parser.complete():
			raise HTTPError("HTTP message is incomplete")
		
		return parser.message


class HTTPRequest(HTTPMessage):
	def __init__(self):
		super().__init__()
		self.method = "GET"
		self.path = "/"
		
		self.params = {}
		self.continue_threshold = 1024
		
		self.certificate = None
		
	def finish_parsing(self):
		super().finish_parsing()
		
		if "?" in self.path:
			self.path, params = self.path.split("?", 1)
			self.params = formdecode(params)
		
	def encode_start_line(self):
		path = self.path
		if self.params:
			path += "?" + formencode(self.params)
		return "%s %s %s" %(self.method, path, self.version)
		
	def parse_start_line(self, line):
		fields = line.split(maxsplit=2)
		if len(fields) != 3:
			raise HTTPError("Failed to parse HTTP request start line")
		
		self.method = fields[0]
		self.path = fields[1]
		self.version = fields[2]
		
		self.check_version()
		
	def encode_body(self):
		body = super().encode_body()
		if self.continue_threshold is not None:
			if len(body) > self.continue_threshold:
				self.headers["Expect"] = "100-continue"
		return body
	
	@staticmethod
	def build(method, path):
		request = HTTPRequest()
		request.method = method
		request.path = path
		return request
		
	@staticmethod
	def get(path):
		return HTTPRequest.build("GET", path)
		
	@staticmethod
	def post(path):
		return HTTPRequest.build("POST", path)
		

class HTTPResponse(HTTPMessage):
	def __init__(self, status_code=500):
		super().__init__()
		self.status_code = status_code
		self.status_name = STATUS_NAMES.get(status_code, "Unknown")
		
	def success(self):
		return self.status_code in STATUS_SUCCESS
		
	def error(self):
		return not self.success()
	
	def raise_if_error(self):
		if self.error():
			raise HTTPError("HTTP request failed with status %i" %self.status_code)
		
	def encode_start_line(self):
		return "%s %i %s" %(self.version, self.status_code, self.status_name)
		
	def parse_start_line(self, line):
		fields = line.split(maxsplit=2)
		if len(fields) != 3:
			raise HTTPError("Failed to parse HTTP response start line")
		
		self.version = fields[0]
		self.check_version()
		
		if not fields[1].isdecimal():
			raise HTTPError("HTTP response has invalid status code")
		
		self.status_code = int(fields[1])
		self.status_name = fields[2]
		

class HTTPParser:
	def __init__(self, cls):
		self.message = cls()
		
		self.buffer = b""
		self.state = self.state_header
		
	def complete(self): return self.state is None
	def header_complete(self): return self.state != self.state_header
	
	def update(self, data):
		self.buffer += data
		while not self.state():
			pass
			
	def finish(self):
		self.message.finish_parsing()
		if self.buffer:
			raise HTTPError("Got more data than expected")
		self.state = None
		return self.message
	
	def state_header(self):
		if not b"\r\n\r\n" in self.buffer:
			return True
		
		header, self.buffer = self.buffer.split(b"\r\n\r\n", 1)
		
		try:
			lines = header.decode().splitlines()
		except UnicodeDecodeError:
			raise HTTPError("Failed to decode HTTP header")
			
		if len(lines) == 0:
			raise HTTPError("HTTP message must start with header line")
		
		self.message.parse_start_line(lines[0])
		
		for header in lines[1:]:
			if not ": " in header:
				raise HTTPError("Invalid line in HTTP headers")
			key, value = header.split(": ", 1)
			self.message.headers[key] = value
		
		if self.message.is_chunked():
			self.state = self.state_chunk_header
			return False
		elif "Content-Length" in self.message.headers:
			if not self.message.headers["Content-Length"].isdecimal():
				raise HTTPError("Invalid Content-Length header")
			self.state = self.state_body
			return False
		
		self.finish()
		return True
		
	def state_chunk_header(self):
		if not b"\r\n" in self.buffer:
			return True
			
		line, self.buffer = self.buffer.split(b"\r\n", 1)
		try:
			line = line.decode()
		except UnicodeDecodeError:
			raise HTTPError("Failed to decode chunk length")

		if not util.is_hexadecimal(line):
			raise HTTPError("Invalid HTTP chunk length")
		
		self.chunk_length = int(line, 16)
		
		self.state = self.state_chunk_body
		return False
		
	def state_chunk_body(self):
		if len(self.buffer) < self.chunk_length + 2:
			return True
			
		if self.buffer[self.chunk_length : self.chunk_length + 2] != b"\r\n":
			raise HTTPError("HTTP chunk should be terminated with \\r\\n")
		
		self.message.body += self.buffer[:self.chunk_length]
		
		self.buffer = self.buffer[self.chunk_length + 2:]
		
		if self.chunk_length == 0:
			self.finish()
			return True
			
		self.state = self.state_chunk_header
		return False
		
	def state_body(self):
		length = int(self.message.headers["Content-Length"])
		if len(self.buffer) < length:
			return True
			
		self.message.body = self.buffer[:length]
		self.buffer = self.buffer[length:]
		self.finish()
		return True


class HTTPClient:
	def __init__(self, sock):
		self.sock = sock
	
	async def request(self, req):
		logger.debug("Sending HTTP request headers")
		await self.sock.send(req.encode_headers())
		
		if req.headers.get("Expect") == "100-continue":
			response = await self.receive_response()
			if response.status_code != 100:
				raise HTTPError("Expected 100-continue response")
		
		logger.debug("Sending HTTP request body")
		await self.sock.send(req.encode_body())
		response = await self.receive_response()
		
		return response
			
	async def receive_response(self):
		parser = HTTPParser(HTTPResponse)
		while not parser.complete():
			data = await self.sock.recv()
			parser.update(data)
		return parser.message
		
		
class HTTPServerClient:
	def __init__(self, handler, client):
		self.handler = handler
		self.client = client
	
	async def process(self):
		try:
			parser = HTTPParser(HTTPRequest)
			while not parser.header_complete():
				data = await self.client.recv()
				parser.update(data)
			
			if parser.message.headers.get("Expect") == "100-continue":
				await self.client.send(HTTPResponse(100).encode())
			
			while not parser.complete():
				data = await self.client.recv()
				parser.update(data)
			
			request = parser.message
			request.certificate = self.client.remote_certificate()
			
			response = await self.handle_request(request)
			await self.client.send(response.encode())
		except Exception:
			logger.exception("Failed to process HTTP request")
	
	async def handle_request(self, request):
		logger.info("Received HTTP request: %s %s", request.method, request.path)
		
		try:
			response = await self.handler(request)
			if not isinstance(response, HTTPResponse):
				logger.error("HTTP handler must return HTTPResponse")
				response = HTTPResponse(500)
		except Exception:
			logger.exception("HTTP handler raised an exception")
			response = HTTPResponse(500)
		
		logger.info("Sending HTTP response (%i)", response.status_code)
		return response


async def request(req, context = None):
	if "Host" not in req.headers:
		raise ValueError("HTTP request requires Host header")
	
	logger.info("Performing HTTP request: %s %s", req.method, req.path)
	
	host = req.headers["Host"]
	port = 443 if context else 80
	
	if ":" in host:
		host, port = host.split(":", 1)
		if not port.isdecimal():
			raise ValueError("HTTP request has invalid Host header")
		port = int(port)
		
	logger.info("Establishing HTTP connection with %s:%i", host, port)
	
	async with tls.connect(host, port, context) as client:
		response = await HTTPClient(client).request(req)
	
	logger.info("Received HTTP response: %i", response.status_code)
	return response

async def get(url, headers={}, context=None):
	if "://" in url:
		scheme, url = url.split("://", 1)
		if scheme == "http":
			context = None
		elif scheme == "https":
			if context is None:
				context = tls.TLSContext()
				context.load_default_authorities()
		else:
			raise ValueError("Invalid HTTP url scheme: %s" %scheme)
	
	if "/" in url:
		host, path = url.split("/", 1)
	else:
		host = url
		path = "/"
	
	req = HTTPRequest.get("/" + path)
	req.headers = types.CaseInsensitiveDict(headers)
	req.headers["Host"] = host
	return await request(req, context)

@contextlib.asynccontextmanager
async def serve(handler, host="", port=0, context=None):
	async def handle(client):
		host, port = client.remote_address()
		logger.debug("New HTTP connection: %s:%i", host, port)
		
		client = HTTPServerClient(handler, client)
		await client.process()
	
	logger.info("Starting HTTP server at %s:%i", host, port)
	async with tls.serve(handle, host, port, context):
		yield
	logger.info("HTTP server is closed")
