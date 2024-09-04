
from anynet import http, tls
from nintendo import resources
from nintendo.nex import common, kerberos, rmc, streams
import hashlib
import hmac
import secrets


class HppClient:
	def __init__(self, settings, game_server_id, nex_version, pid, password):
		self.settings = settings
		self.game_server_id = game_server_id
		self.nex_version = nex_version
		self.pid = pid
		self.password = password
		
		self.environment = "L1"
		
		self.key_derivation = kerberos.KeyDerivationOld(65000, 1024)
		
		self.call_id = 1
		
		ca = resources.certificate("files/cert/CACERT_NINTENDO_CLASS2_CA_G3.der")
		self.context = tls.TLSContext()
		self.context.set_authority(ca)

	def set_environment(self, env): self.environment = env
	
	def host(self):
		return "hpp-%08x-%s.n.app.nintendo.net" %(self.game_server_id, self.environment.lower())

	async def request(self, protocol, method, body):
		call_id = self.call_id
		self.call_id = (call_id + 1) & 0xFFFFFFFF
		
		message = rmc.RMCMessage.request(self.settings, protocol, method, call_id, body)
		
		data = message.encode()
		
		key1 = bytes.fromhex(self.settings["prudp.access_key"]).ljust(8, b"\0")
		key2 = self.key_derivation.derive_key(self.password.encode(), self.pid)
		
		signature1 = hmac.new(key1, data, hashlib.md5).hexdigest()
		signature2 = hmac.new(key2, data, hashlib.md5).hexdigest()
		
		random = secrets.token_hex(8).upper()
		
		req = http.HTTPRequest.post("https://%s/hpp/" %self.host())
		req.headers["Host"] = self.host()
		req.headers["pid"] = str(self.pid)
		req.headers["version"] = self.nex_version
		req.headers["token"] = "normaltoken"
		req.headers["signature1"] = signature1.upper()
		req.headers["signature2"] = signature2.upper()
		req.headers["Content-Type"] = "multipart/form-data"
		req.headers["Content-Length"] = 0
		req.boundary = "--------BOUNDARY--------" + random
		req.files = {"file": data}
		
		response = await http.request(self.host(), req, self.context)
		if response.error():
			raise ValueError("Hpp request failed with status %i" %response.status_code)
		
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
