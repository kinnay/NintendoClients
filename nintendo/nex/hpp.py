
from nintendo.common.http import HTTPClient, HTTPRequest
from nintendo.nex import service, kerberos, streams, common
from nintendo.settings import Settings
import requests
import secrets
import hashlib
import hmac


class HppClient(service.RMCClientBase):
	def __init__(self, settings):
		super().__init__(settings)
		self.game_server_id = None
		self.access_key = None
		self.nex_version = None
		
		self.pid = None
		self.password = None
		
		self.environment = "L1"
		
		self.key_derivation = kerberos.KeyDerivationOld(65000, 1024)
		
		self.client = HTTPClient()
		self.call_id = 0
		
	def set_environment(self, env): self.environment = env
		
	def configure(self, game_server_id, access_key, nex_version):
		self.game_server_id = game_server_id
		self.access_key = access_key
		self.nex_version = nex_version
		
		self.settings.set("nex.version", 20000)
		
	def login(self, pid, password):
		self.pid = pid
		self.password = password
		
	def host(self):
		return "hpp-%08x-%s.n.app.nintendo.net" %(self.game_server_id, self.environment.lower())
		
	def send_request(self, protocol, method, body):
		call_id = self.call_id
		self.call_id += 1
		
		message = service.RMCMessage.request(self.settings, protocol, method, call_id, body)
		
		data = message.encode()
		
		key1 = bytes.fromhex(self.access_key).ljust(8, b"\0")
		key2 = self.key_derivation.derive_key(self.password.encode(), self.pid)
		
		signature1 = hmac.new(key1, data, hashlib.md5).hexdigest()
		signature2 = hmac.new(key2, data, hashlib.md5).hexdigest()
		
		random = secrets.token_hex(8).upper()
		
		req = HTTPRequest.post("https://%s/hpp/" %self.host())
		req.headers["Host"] = self.host()
		req.headers["pid"] = str(self.pid)
		req.headers["version"] = self.nex_version
		req.headers["token"] = "normaltoken"
		req.headers["signature1"] = signature1.upper()
		req.headers["signature2"] = signature2.upper()
		req.headers["Content-Type"] = "multipart/form-data"
		req.headers["Content-Length"] = 0
		req.boundary = "--------BOUNDARY--------" + random
		req.files["file"] = data
		
		response = self.client.request(req, True)
		if response.status != 200:
			raise ValueError("Hpp request failed with status %i" %response.status)
		
		stream = streams.StreamIn(response.body, self.settings)
		if stream.u32() != stream.available():
			raise ValueError("Hpp response has unexpected size")
		
		success = stream.bool()
		if not success:
			error = stream.u32()
			if call_id != stream.u32():
				raise ValueError("Hpp error response has unexpected call id")
			if not stream.eof():
				raise ValueError("Hpp error response is bigger than expected")
			raise common.RMCError(error)
		
		if call_id != stream.u32():
			raise ValueError("Hpp response has unexpected call id")
		method_id = stream.u32()
		if method_id != method | 0x8000:
			raise ValueError("Hpp response has unexpected method id")
		return stream.readall()
