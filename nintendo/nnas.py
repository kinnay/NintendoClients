
from anynet import http, tls, xml
from nintendo import resources
import datetime
import hashlib
import struct
import base64

import logging
logger = logging.getLogger(__name__)


def calc_password_hash(pid: int, password: str) -> str:
	data = struct.pack("<I", pid)
	data += b"\x02\x65\x43\x46"
	data += password.encode("ascii")
	return hashlib.sha256(data).hexdigest()


class NNASError(Exception):
	def __init__(self, status_code, errors):
		self.status_code = status_code
		self.errors = errors
	
	def __str__(self) -> str:
		if self.errors:
			return f"Account request failed: {self.errors}"
		else:
			return f"Account request failed with status {self.status_code}"


class OAuth20:
	token: str
	refresh_token: str
	expires_in: int

	def __init__(self, tree: xml.XMLTree):
		access_token = tree["access_token"]
		
		self.token = access_token["token"].text
		self.refresh_token = access_token["refresh_token"].text
		self.expires_in = int(access_token["expires_in"].text)


class NexToken:
	host: str
	port: int
	pid: int
	password: str
	token: str

	def __init__(self, tree: xml.XMLTree):
		self.host = tree["host"].text
		self.port = int(tree["port"].text)
		self.pid = int(tree["pid"].text)
		self.password = tree["nex_password"].text
		self.token = tree["token"].text
		
		
class MiiImage:
	id: int
	type: str
	url: str
	cached_url: str

	def __init__(self, image: xml.XMLTree):
		self.id = int(image["id"].text)
		self.type = image["type"].text
		self.url = image["url"].text
		self.cached_url = image["cached_url"].text
		

class Mii:
	data: bytes
	id: int
	name: str
	images: list[MiiImage]
	primary: bool
	pid: int
	nnid: str
	
	def __init__(self, mii: xml.XMLTree):
		self.data = base64.b64decode(mii["data"].text)
		self.id = int(mii["id"].text)
		self.name = mii["name"].text
		self.images = [MiiImage(image) for image in mii["images"]]
		self.primary = mii["primary"].text == "Y"
		self.pid = int(mii["pid"].text)
		self.nnid = mii["user_id"].text


class Account:
	domain: str
	type: str
	username: str
	
	def __init__(self, account: xml.XMLTree):
		self.domain = account["domain"].text
		self.type = account["type"].text
		self.username = account["username"].text
		
		
class DeviceAttribute:
	created_date: datetime.datetime
	name: str
	value: str
	
	def __init__(self, attribute: xml.XMLTree):
		self.created_date = datetime.datetime.fromisoformat(
			attribute["created_date"].text
		)
		self.name = attribute["name"].text
		self.value = attribute["value"].text
		
		
class Email:
	id: int
	address: str
	primary: bool
	parent: bool
	reachable: bool
	type: str
	validated: bool
	vlaidated_date: datetime.datetime

	def __init__(self, email: xml.XMLTree):
		self.id = int(email["id"].text)
		self.address = email["address"].text
		self.parent = email["parent"].text == "Y"
		self.primary = email["primary"].text == "Y"
		self.reachable = email["reachable"].text == "Y"
		self.type = email["type"].text
		self.validated = email["validated"].text == "Y"
		self.validated_date = datetime.datetime.fromisoformat(
			email["validated_date"].text
		)


class ProfileMii:
	id: int
	name: str
	data: bytes
	primary: bool
	status: str
	hash: str
	images: list[MiiImage]
	
	def __init__(self, mii: xml.XMLTree):
		self.status = mii["status"].text
		self.data = base64.b64decode(mii["data"].text)
		self.id = int(mii["id"].text)
		self.hash = mii["mii_hash"].text
		self.images = [MiiImage(image) for image in mii["mii_images"]]
		self.name = mii["name"].text
		self.primary = mii["primary"].text == "Y"


class Profile:
	accounts: list[Account]
	active_flag: bool
	birth_date: datetime.datetime
	country: str
	create_date: datetime.datetime
	device_attributes: list[DeviceAttribute]
	forgot_pw_email_sent: datetime.datetime
	gender: str
	language: str
	updated: datetime.datetime
	marketing_flag: bool
	off_device_flag: bool
	pid: int
	email: Email
	mii: ProfileMii
	region: int
	temporary_password_expiration: datetime.datetime
	tz_name: str
	nnid: str
	utc_offset: int

	def __init__(self, profile: xml.XMLTree):
		self.accounts = [Account(account) for account in profile["accounts"]]
		self.active_flag = profile["active_flag"] == "Y"
		self.birth_date = \
			datetime.datetime.fromisoformat(profile["birth_date"].text)
		self.country = profile["country"].text
		self.create_date = \
			datetime.datetime.fromisoformat(profile["create_date"].text)
		self.device_attributes = [
			DeviceAttribute(attrib) for attrib in profile["device_attributes"]
		]
		if "forgot_pw_email_sent" in profile:
			self.forgot_pw_email_sent = datetime.datetime.fromisoformat(
				profile["forgot_pw_email_sent"].text
			)
		self.gender = profile["gender"].text
		self.language = profile["language"].text
		self.updated = datetime.datetime.fromisoformat(profile["updated"].text)
		self.marketing_flag = profile["marketing_flag"].text == "Y"
		self.off_device_flag = profile["off_device_flag"].text == "Y"
		self.pid = int(profile["pid"].text)
		self.email = Email(profile["email"])
		self.mii = ProfileMii(profile["mii"])
		self.region = int(profile["region"].text)
		if "temporary_password_expiration" in profile:
			self.temporary_password_expiration = \
				datetime.datetime.fromisoformat(
					profile["temporary_password_expiration"].text
				)
		self.tz_name = profile["tz_name"].text
		self.nnid = profile["user_id"].text
		self.utc_offset = int(profile["utc_offset"].text)


class NNASClient:
	_url: str
	_context: tls.TLSContext

	_client_id: str
	_client_secret: str

	_platform_id: int
	_device_type: int

	_device_id: int | None
	_serial_number: str | None
	_system_version: int
	_device_cert: str | None

	_region: int
	_country: str
	_language: str

	_fpd_version: int
	_environment: str

	_title_id: int | None
	_title_version: int | None

	def __init__(self):
		self._url = "account.nintendo.net"

		ca = resources.certificate("Nintendo_CA_G3.der")
		cert = resources.certificate("Wii_U_Common_Prod_1.der")
		key = resources.private_key("Wii_U_Common_Prod_1.key")
		
		self._context = tls.TLSContext()
		self._context.set_authority(ca)
		self._context.set_certificate(cert, key)
		
		self._client_id = "a2efa818a34fa16b8afbc8a74eba3eda"
		self._client_secret = "c91cdb5658bd4954ade78533a339cf9a"
		
		self._platform_id = 1
		self._device_type = 2
		
		self._device_id = None
		self._serial_number = None
		self._system_version = 0x260
		self._device_cert = None
		
		self._region = 4
		self._country = "NL"
		self._language = "en"
		
		self._fpd_version = 0
		self._environment = "L1"
		
		self._title_id = None
		self._title_version = None
		
	def set_context(self, context: tls.TLSContext) -> None:
		self._context = context
	
	def set_url(self, url: str) -> None:
		self._url = url
	
	def set_client_id(self, client_id: str) -> None:
		self._client_id = client_id
	
	def set_client_secret(self, client_secret: str) -> None:
		self._client_secret = client_secret
	
	def set_platform_id(self, platform_id: int) -> None:
		self._platform_id = platform_id
	
	def set_device_type(self, device_type: int) -> None:
		self._device_type = device_type
	
	def set_device(
		self, device_id: int, serial_number: str, system_version: int,
		cert: str | None = None
	) -> None:
		self._device_id = device_id
		self._serial_number = serial_number
		self._system_version = system_version
		self._device_cert = cert
		
	def set_locale(self, region: int, country: str, language: str) -> None:
		self._region = region
		self._country = country
		self._language = language
		
	def set_fpd_version(self, version: int) -> None:
		self._fpd_version = version
	
	def set_environment(self, environment: str) -> None:
		self._environment = environment
	
	def set_title(self, title_id: int, title_version: int) -> None:
		self._title_id = title_id
		self._title_version = title_version
	
	def prepare(
		self, req: http.HTTPRequest, auth: str | None = None,
		cert: str | None = None
	) -> None:
		req.headers["Host"] = self._url
		req.headers["X-Nintendo-Platform-ID"] = self._platform_id
		req.headers["X-Nintendo-Device-Type"] = self._device_type
		
		if self._device_id is not None:
			req.headers["X-Nintendo-Device-ID"] = self._device_id
		if self._serial_number is not None:
			req.headers["X-Nintendo-Serial-Number"] = self._serial_number
			
		req.headers["X-Nintendo-System-Version"] = f"{self._system_version:04X}"
		req.headers["X-Nintendo-Region"] = self._region
		req.headers["X-Nintendo-Country"] = self._country
		req.headers["Accept-Language"] = self._language
		
		req.headers["X-Nintendo-Client-ID"] = self._client_id
		req.headers["X-Nintendo-Client-Secret"] = self._client_secret
			
		req.headers["Accept"] = "*/*"
		req.headers["X-Nintendo-FPD-Version"] = f"{self._fpd_version:04X}"
		req.headers["X-Nintendo-Environment"] = self._environment
		
		if self._title_id is not None:
			unique_id = (self._title_id >> 8) & 0xFFFFF
			req.headers["X-Nintendo-Title-ID"] = f"{self._title_id:016X}"
			req.headers["X-Nintendo-Unique-ID"] = f"{unique_id:05X}"
		
		if self._title_version is not None:
			req.headers["X-Nintendo-Application-Version"] = \
				f"{self._title_version:04X}"
			
		if cert is not None:
			req.headers["X-Nintendo-Device-Cert"] = cert
			
		if auth is not None:
			req.headers["Authorization"] = "Bearer " + auth
			
	async def request(self, req: http.HTTPRequest) -> xml.XMLTree:
		response = await http.request(self._url, req, self._context)
		if response.error():
			status_code = response.status_code
			logger.error(
				f"Account request returned status code {status_code}\n" \
				f"{response.text}"
			)
			raise NNASError(status_code, response.xml)
		return response.xml
		
	async def login(
		self, username: str, password: str, password_type: str | None = None
	) -> OAuth20:
		req = http.HTTPRequest.post("/v1/api/oauth20/access_token/generate")
		self.prepare(req, cert=self._device_cert)
		
		req.form = {
			"grant_type": "password",
			"user_id": username,
			"password": password,
		}
		
		if password_type is not None:
			req.form["password_type"] = password_type
		
		response = await self.request(req)
		return OAuth20(response)
	
	async def get_nex_token(
		self, access_token: str, game_server_id: int
	) -> NexToken:
		req = http.HTTPRequest.get("/v1/api/provider/nex_token/@me")
		req.params = {
			"game_server_id": f"{game_server_id:08X}"
		}
		
		self.prepare(req, access_token)
		
		response = await self.request(req)
		return NexToken(response)
	
	async def get_service_token(self, access_token: str, client_id: str) -> str:
		req = http.HTTPRequest.get("/v1/api/provider/service_token/@me")
		req.params = {
			"client_id": client_id
		}
		
		self.prepare(req, access_token)
		
		response = await self.request(req)
		return response["token"].text
	
	async def get_profile(self, access_token: str) -> Profile:
		req = http.HTTPRequest.get("/v1/api/people/@me/profile")
		self.prepare(req, access_token)
		
		response = await self.request(req)
		return Profile(response)
		
	#The following functions can be used without logging in
		
	async def get_miis(self, pids: list[int]) -> list[Mii]:
		req = http.HTTPRequest.get("/v1/api/miis")
		req.params = {
			"pids": ",".join([str(pid) for pid in pids])
		}
		
		self.prepare(req)
		
		response = await self.request(req)
		return [Mii(mii) for mii in response]
	
	async def get_pids(self, nnids: list[str]) -> dict[str, int]:
		req = http.HTTPRequest.get("/v1/api/admin/mapped_ids")
		req.params = {
			"input_type": "user_id",
			"output_type": "pid",
			"input": ",".join(nnids)
		}
		self.prepare(req)
		
		response = await self.request(req)
		return {
			id["in_id"].text: int(id["out_id"].text) for id in response if \
				id["out_id"].text
		}
		
	async def get_nnids(self, pids: list[int]) -> dict[int, str]:
		req = http.HTTPRequest.get("/v1/api/admin/mapped_ids")
		req.params = {
			"input_type": "pid",
			"output_type": "user_id",
			"input": ",".join([str(pid) for pid in pids])
		}
		self.prepare(req)
		
		response = await self.request(req)
		return {
			int(id["in_id"].text): id["out_id"].text for id in response if \
				id["out_id"].text
		}
	
	async def get_mii(self, pid: int) -> Mii:
		return (await self.get_miis([pid]))[0]
	
	async def get_pid(self, nnid: str) -> int:
		return (await self.get_pids([nnid]))[nnid]
	
	async def get_nnid(self, pid: int) -> str:
		return (await self.get_nnids([pid]))[pid]
