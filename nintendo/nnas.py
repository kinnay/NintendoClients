
from nintendo.common import http, tls
import pkg_resources
import hashlib
import struct
import base64

import logging
logger = logging.getLogger(__name__)


CA = pkg_resources.resource_filename("nintendo", "files/cert/CACERT_NINTENDO_CA_G3.der")
CERT = pkg_resources.resource_filename("nintendo", "files/cert/WIIU_COMMON_1_CERT.der")
KEY = pkg_resources.resource_filename("nintendo", "files/cert/WIIU_COMMON_1_RSA_KEY.der")


def calc_password_hash(pid, password):
	data = struct.pack("<I", pid) + b"\x02\x65\x43\x46" + password.encode("ascii")
	return hashlib.sha256(data).hexdigest()


class NNASError(Exception):
	def __init__(self, status_code, errors):
		self.status_code = status_code
		self.errors = errors
	
	def __str__(self):
		if self.errors:
			return "Account request failed: %s" %self.errors
		else:
			return "Account request failed with status %i" %self.status_code


class OAuth20:
	def __init__(self):
		self.token = None
		self.refresh_token = None
		self.expires_in = None
	
	@classmethod
	def parse(cls, tree):
		access_token = tree["access_token"]
		
		inst = cls()
		inst.token = access_token["token"].text
		inst.refresh_token = access_token["refresh_token"].text
		inst.expires_in = int(access_token["expires_in"].text)
		return inst


class NexToken:
	def __init__(self):
		self.host = None
		self.port = None
		self.pid = None
		self.password = None
		self.token = None
	
	@classmethod
	def parse(cls, tree):
		inst = cls()
		inst.host = tree["host"].text
		inst.port = int(tree["port"].text)
		inst.pid = int(tree["pid"].text)
		inst.password = tree["nex_password"].text
		inst.token = tree["token"].text
		return inst
		

class Mii:
	def __init__(self):
		self.data = None
		self.id = None
		self.name = None
		self.images = None
		self.primary = None
		self.pid = None
		self.nnid = None
	
	@classmethod
	def parse(cls, mii):
		inst = cls()
		inst.data = base64.b64decode(mii["data"].text)
		inst.id = int(mii["id"].text)
		inst.name = mii["name"].text
		inst.images = {image["type"].text: image["url"].text for image in mii["images"]}
		inst.primary = mii["primary"].text == "Y"
		inst.pid = int(mii["pid"].text)
		inst.nnid = mii["user_id"].text
		return inst


class NNASClient:
	def __init__(self):
		self.url = "account.nintendo.net"
		
		ca = tls.TLSCertificate.load(CA, tls.TYPE_DER)
		cert = tls.TLSCertificate.load(CERT, tls.TYPE_DER)
		key = tls.TLSPrivateKey.load(KEY, tls.TYPE_DER)
		
		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		self.context.set_certificate(cert, key)
		
		self.client_id = "a2efa818a34fa16b8afbc8a74eba3eda"
		self.client_secret = "c91cdb5658bd4954ade78533a339cf9a"
		
		self.platform_id = 1
		self.device_type = 2
		
		self.device_id = None
		self.serial_number = None
		self.system_version = 0x250
		self.device_cert = None
		
		self.region = 4
		self.country = "NL"
		self.language = "en"
		
		self.fpd_version = 0
		self.environment = "L1"
		
		self.title_id = None
		self.title_version = None
		
		self.auth_token = None
		
	def set_context(self, context):
		self.context = context
	
	def set_url(self, url): self.url = url
	
	def set_client_id(self, client_id): self.client_id = client_id
	def set_client_secret(self, client_secret): self.client_secret = client_secret
	
	def set_platform_id(self, platform_id): self.platform_id = platform_id
	def set_device_type(self, device_type): self.device_type = device_type
	
	def set_device(self, device_id, serial_number, system_version, cert=None):
		self.device_id = device_id
		self.serial_number = serial_number
		self.system_version = system_version
		self.device_cert = cert
		
	def set_locale(self, region, country, language):
		self.region = region
		self.country = country
		self.language = language
		
	def set_fpd_version(self, version): self.fpd_version = version
	def set_environment(self, environment): self.environment = environment
	
	def set_title(self, title_id, title_version):
		self.title_id = title_id
		self.title_version = title_version
	
	def prepare(self, req, auth=None, cert=None):
		req.headers["Host"] = self.url
		req.headers["X-Nintendo-Platform-ID"] = self.platform_id
		req.headers["X-Nintendo-Device-Type"] = self.device_type
		
		if self.device_id is not None:
			req.headers["X-Nintendo-Device-ID"] = self.device_id
		if self.serial_number is not None:
			req.headers["X-Nintendo-Serial-Number"] = self.serial_number
			
		req.headers["X-Nintendo-System-Version"] = "%04X" %self.system_version
		req.headers["X-Nintendo-Region"] = self.region
		req.headers["X-Nintendo-Country"] = self.country
		req.headers["Accept-Language"] = self.language
		
		if auth is None:
			req.headers["X-Nintendo-Client-ID"] = self.client_id
			req.headers["X-Nintendo-Client-Secret"] = self.client_secret
			
		req.headers["Accept"] = "*/*"
		req.headers["X-Nintendo-FPD-Version"] = "%04X" %self.fpd_version
		req.headers["X-Nintendo-Environment"] = self.environment
		
		if self.title_id is not None:
			req.headers["X-Nintendo-Title-ID"] = "%016X" %self.title_id
			req.headers["X-Nintendo-Unique-ID"] = "%05X" %((self.title_id >> 8) & 0xFFFFF)
		if self.title_version is not None:
			req.headers["X-Nintendo-Application-Version"] = "%04X" %self.title_version
			
		if cert is not None:
			req.headers["X-Nintendo-Device-Cert"] = cert
			
		if auth is not None:
			req.headers["Authorization"] = "Bearer " + auth
			
	async def request(self, req):
		response = await http.request(req, self.context)
		if response.error():
			logger.error("Account request returned status code %i\n%s", response.status_code, response.text)
			raise NNASError(response.status_code, response.xml)
		return response.xml
		
	async def login(self, username, password, password_type=None):
		req = http.HTTPRequest.post("/v1/api/oauth20/access_token/generate")
		self.prepare(req, cert=self.device_cert)
		
		req.form["grant_type"] = "password"
		req.form["user_id"] = username
		req.form["password"] = password
		if password_type is not None:
			req.form["password_type"] = password_type
		
		response = await self.request(req)
		return OAuth20.parse(response)
	
	async def get_nex_token(self, access_token, game_server_id):
		req = http.HTTPRequest.get("/v1/api/provider/nex_token/@me")
		req.params["game_server_id"] = "%08X" %game_server_id
		self.prepare(req, access_token)
		
		response = await self.request(req)
		return NexToken.parse(response)
		
	#The following functions can be used without logging in
		
	async def get_miis(self, pids):
		req = http.HTTPRequest.get("/v1/api/miis")
		req.params["pids"] = ",".join([str(pid) for pid in pids])
		self.prepare(req)
		
		response = await self.request(req)
		return [Mii.parse(mii) for mii in response]
	
	async def get_pids(self, nnids):
		req = http.HTTPRequest.get("/v1/api/admin/mapped_ids")
		req.params["input_type"] = "user_id"
		req.params["output_type"] = "pid"
		req.params["input"] = ",".join(nnids)
		self.prepare(req)
		
		response = await self.request(req)
		return {id["in_id"].text: int(id["out_id"].text) for id in response if id["out_id"].text}
		
	async def get_nnids(self, pids):
		req = http.HTTPRequest.get("/v1/api/admin/mapped_ids")
		req.params["input_type"] = "pid"
		req.params["output_type"] = "user_id"
		req.params["input"] = ",".join([str(pid) for pid in pids])
		self.prepare(req)
		
		response = await self.request(req)
		return {int(id["in_id"].text): id["out_id"].text for id in response if id["out_id"].text}
	
	async def get_mii(self, pid): return (await self.get_miis([pid]))[0]
	async def get_pid(self, nnid): return (await self.get_pids([nnid]))[nnid]
	async def get_nnid(self, pid): return (await self.get_nnids([pid]))[pid]
