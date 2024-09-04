
from anynet import http, tls
from nintendo import resources
import datetime
import hashlib
import struct
import base64

import logging
logger = logging.getLogger(__name__)


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
		
		
class MiiImage:
	def __init__(self):
		self.id = None
		self.type = None
		self.url = None
		self.cached_url = None
	
	@classmethod
	def parse(cls, image):
		inst = cls()
		inst.cached_url = image["cached_url"].text
		inst.id = int(image["id"].text)
		inst.url = image["url"].text
		inst.type = image["type"].text
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
		inst.images = [MiiImage.parse(image) for image in mii["images"]]
		inst.primary = mii["primary"].text == "Y"
		inst.pid = int(mii["pid"].text)
		inst.nnid = mii["user_id"].text
		return inst


class Account:
	def __init__(self):
		self.domain = None
		self.type = None
		self.username = None
	
	@classmethod
	def parse(cls, account):
		inst = cls()
		inst.domain = account["domain"].text
		inst.type = account["type"].text
		inst.username = account["username"].text
		return inst
		
		
class DeviceAttribute:
	def __init__(self):
		self.created_date = None
		self.name = None
		self.value = None
	
	@classmethod
	def parse(cls, attribute):
		inst = cls()
		inst.created_date = datetime.datetime.fromisoformat(attribute["created_date"].text)
		inst.name = attribute["name"].text
		inst.value = attribute["value"].text
		return inst
		
		
class Email:
	def __init__(self):
		self.address = None
		self.id = None
		self.parent = None
		self.primary = None
		self.reachable = None
		self.type = None
		self.validated = None
		self.validated_date = None
	
	@classmethod
	def parse(cls, email):
		inst = cls()
		inst.address = email["address"].text
		inst.id = int(email["id"].text)
		inst.parent = email["parent"].text == "Y"
		inst.primary = email["primary"].text == "Y"
		inst.reachable = email["reachable"].text == "Y"
		inst.type = email["type"].text
		inst.validated = email["validated"].text == "Y"
		inst.validated_date = datetime.datetime.fromisoformat(email["validated_date"].text)
		return inst


class ProfileMii:
	def __init__(self):
		self.id = None
		self.data = None
		self.status = None
		self.hash = None
		self.images = None
		self.name = None
		self.primary = None
	
	@classmethod
	def parse(cls, mii):
		inst = cls()
		inst.status = mii["status"].text
		inst.data = base64.b64decode(mii["data"].text)
		inst.id = int(mii["id"].text)
		inst.hash = mii["mii_hash"].text
		inst.images = [MiiImage.parse(image) for image in mii["mii_images"]]
		inst.name = mii["name"].text
		inst.primary = mii["primary"].text == "Y"
		return inst


class Profile:
	def __init__(self):
		self.accounts = None
		self.active_flag = None
		self.birth_date = None
		self.country = None
		self.create_date = None
		self.device_attributes = None
		self.forgot_pw_email_sent = None
		self.gender = None
		self.language = None
		self.updated = None
		self.marketing_flag = None
		self.off_device_flag = None
		self.pid = None
		self.email = None
		self.mii = None
		self.region = None
		self.temporary_password_expiration = None
		self.tz_name = None
		self.nnid = None
		self.utc_offset = None
	
	@classmethod
	def parse(cls, profile):
		inst = cls()
		inst.accounts = [Account.parse(account) for account in profile["accounts"]]
		inst.active_flag = profile["active_flag"] == "Y"
		inst.birth_date = datetime.date.fromisoformat(profile["birth_date"].text)
		inst.country = profile["country"].text
		inst.create_date = datetime.datetime.fromisoformat(profile["create_date"].text)
		inst.device_attributes = [DeviceAttribute.parse(attrib) for attrib in profile["device_attributes"]]
		if "forgot_pw_email_sent" in profile:
			inst.forgot_pw_email_sent = datetime.datetime.fromisoformat(profile["forgot_pw_email_sent"].text)
		inst.gender = profile["gender"].text
		inst.language = profile["language"].text
		inst.updated = datetime.datetime.fromisoformat(profile["updated"].text)
		inst.marketing_flag = profile["marketing_flag"].text == "Y"
		inst.off_device_flag = profile["off_device_flag"].text == "Y"
		inst.pid = int(profile["pid"].text)
		inst.email = Email.parse(profile["email"])
		inst.mii = ProfileMii.parse(profile["mii"])
		inst.region = int(profile["region"].text)
		if "temporary_password_expiration" in profile:
			inst.temporary_password_expiration = datetime.datetime.fromisoformat(profile["temporary_password_expiration"].text)
		inst.tz_name = profile["tz_name"].text
		inst.nnid = profile["user_id"].text
		inst.utc_offset = int(profile["utc_offset"].text)
		return inst


class NNASClient:
	def __init__(self):
		self.url = "account.nintendo.net"

		ca = resources.certificate("CACERT_NINTENDO_CA_G3.der")
		cert = resources.certificate("WIIU_COMMON_1_CERT.der")
		key = resources.private_key("WIIU_COMMON_1_RSA_KEY.der")
		
		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		self.context.set_certificate(cert, key)
		
		self.client_id = "a2efa818a34fa16b8afbc8a74eba3eda"
		self.client_secret = "c91cdb5658bd4954ade78533a339cf9a"
		
		self.platform_id = 1
		self.device_type = 2
		
		self.device_id = None
		self.serial_number = None
		self.system_version = 0x260
		self.device_cert = None
		
		self.region = 4
		self.country = "NL"
		self.language = "en"
		
		self.fpd_version = 0
		self.environment = "L1"
		
		self.title_id = None
		self.title_version = None
		
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
		response = await http.request(self.url, req, self.context)
		if response.error():
			logger.error("Account request returned status code %i\n%s", response.status_code, response.text)
			raise NNASError(response.status_code, response.xml)
		return response.xml
		
	async def login(self, username, password, password_type=None):
		req = http.HTTPRequest.post("/v1/api/oauth20/access_token/generate")
		self.prepare(req, cert=self.device_cert)
		
		req.form = {
			"grant_type": "password",
			"user_id": username,
			"password": password,
		}
		
		if password_type is not None:
			req.form["password_type"] = password_type
		
		response = await self.request(req)
		return OAuth20.parse(response)
	
	async def get_nex_token(self, access_token, game_server_id):
		req = http.HTTPRequest.get("/v1/api/provider/nex_token/@me")
		req.params = {
			"game_server_id": "%08X" %game_server_id
		}
		
		self.prepare(req, access_token)
		
		response = await self.request(req)
		return NexToken.parse(response)
	
	async def get_service_token(self, access_token, client_id):
		req = http.HTTPRequest.get("/v1/api/provider/service_token/@me")
		req.params = {
			"client_id": client_id
		}
		
		self.prepare(req, access_token)
		
		response = await self.request(req)
		return response["token"].text
	
	async def get_profile(self, access_token):
		req = http.HTTPRequest.get("/v1/api/people/@me/profile")
		self.prepare(req, access_token)
		
		response = await self.request(req)
		return Profile.parse(response)
		
	#The following functions can be used without logging in
		
	async def get_miis(self, pids):
		req = http.HTTPRequest.get("/v1/api/miis")
		req.params = {
			"pids": ",".join([str(pid) for pid in pids])
		}
		
		self.prepare(req)
		
		response = await self.request(req)
		return [Mii.parse(mii) for mii in response]
	
	async def get_pids(self, nnids):
		req = http.HTTPRequest.get("/v1/api/admin/mapped_ids")
		req.params = {
			"input_type": "user_id",
			"output_type": "pid",
			"input": ",".join(nnids)
		}
		self.prepare(req)
		
		response = await self.request(req)
		return {id["in_id"].text: int(id["out_id"].text) for id in response if id["out_id"].text}
		
	async def get_nnids(self, pids):
		req = http.HTTPRequest.get("/v1/api/admin/mapped_ids")
		req.params = {
			"input_type": "pid",
			"output_type": "user_id",
			"input": ",".join([str(pid) for pid in pids])
		}
		self.prepare(req)
		
		response = await self.request(req)
		return {int(id["in_id"].text): id["out_id"].text for id in response if id["out_id"].text}
	
	async def get_mii(self, pid): return (await self.get_miis([pid]))[0]
	async def get_pid(self, nnid): return (await self.get_pids([nnid]))[nnid]
	async def get_nnid(self, pid): return (await self.get_nnids([pid]))[pid]
