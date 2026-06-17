
from anynet import http, tls
from nintendo import resources
from nintendo.nex import common, kerberos, rmc, settings, streams
import hashlib
import hmac
import secrets


class HppClient:
	def __init__(
		self, settings: settings.Settings, game_server_id: int,
		nex_version: int, pid: int, password: str
	):
		self._settings = settings
		self._game_server_id = game_server_id
		self._nex_version = nex_version
		self._pid = pid
		self._password = password
		
		self._environment = "L1"
		
		self._key_derivation = kerberos.KeyDerivationOld(65000, 1024)
		
		self._call_id = 1
		
		ca = resources.certificate("Nintendo_Class_2_CA_G3.der")
		self._context = tls.TLSContext()
		self._context.set_authority(ca)

	def set_environment(self, env: str):
		self._environment = env
	
	def host(self) -> str:
		return "hpp-%08x-%s.n.app.nintendo.net" %(
			self._game_server_id, self._environment.lower()
		)

	async def request(self, protocol: int, method: int, body: bytes) -> bytes:
		call_id = self._call_id
		self._call_id = (call_id + 1) & 0xFFFFFFFF
		
		message = rmc.RMCMessage.request(
			self._settings, protocol, method, call_id, body
		)
		
		data = message.encode()
		
		key1 = bytes.fromhex(self._settings["prudp.access_key"]).ljust(8, b"\0")
		key2 = self._key_derivation.derive_key(
			self._password.encode(), self._pid
		)
		
		signature1 = hmac.new(key1, data, hashlib.md5).hexdigest()
		signature2 = hmac.new(key2, data, hashlib.md5).hexdigest()
		
		random = secrets.token_hex(8).upper()
		
		req = http.HTTPRequest.post(f"https://{self.host()}/hpp/")
		req.headers["Host"] = self.host()
		req.headers["pid"] = str(self._pid)
		req.headers["version"] = self._nex_version
		req.headers["token"] = "normaltoken"
		req.headers["signature1"] = signature1.upper()
		req.headers["signature2"] = signature2.upper()
		req.headers["Content-Type"] = "multipart/form-data"
		req.headers["Content-Length"] = 0
		req.boundary = "--------BOUNDARY--------" + random
		req.files = {"file": data}
		
		response = await http.request(self.host(), req, self._context)
		if response.error():
			raise ValueError(
				"Hpp request failed with status {response.status_code}"
			)
		
		stream = streams.StreamIn(response.body, self._settings)
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
