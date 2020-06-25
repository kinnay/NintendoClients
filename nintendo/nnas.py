
from nintendo.common.http import HTTPClient, HTTPRequest
from nintendo.common import xml, ssl, util

import pkg_resources
import collections
import hashlib
import struct
import base64
import urllib.parse

import logging
logger = logging.getLogger(__name__)


CERT = pkg_resources.resource_filename("nintendo", "files/cert/wiiu_common.crt")
KEY = pkg_resources.resource_filename("nintendo", "files/cert/wiiu_common.key")


def calc_password_hash(pid, password):
	data = struct.pack("<I", pid) + b"\x02\x65\x43\x46" + password.encode("ascii")
	return hashlib.sha256(data).hexdigest()
	

# Types
NexToken = collections.namedtuple("NexToken", "host port username password token")
Email = collections.namedtuple("Email", "address id parent primary reachable type validated validation_date")
Mii = collections.namedtuple("Mii", "data id images name pid primary nnid")
ProfileMii = collections.namedtuple("Mii", "data id hash images name primary")
Account = collections.namedtuple("Account", "attributes domain type username")
Profile = collections.namedtuple(
	"Profile",
	"accounts active birthday country creation_date device_attributes gender language "
	"updated marketing off_device pid email mii region timezone nnid utc_offset"
)

# Parsers
NexToken.parse = lambda obj: NexToken(
	obj["host"].value,
	int(obj["port"].value),
	obj["pid"].value,
	obj["nex_password"].value,
	obj["token"].value
)
Email.parse = lambda obj: Email(
	obj["address"].value,
	int(obj["id"].value),
	obj["parent"].value == "Y",
	obj["primary"].value == "Y",
	obj["reachable"].value == "Y",
	obj["type"].value,
	obj["validated"].value == "Y",
	obj["validated_date"].value
)
Mii.parse = lambda obj: Mii(
	base64.b64decode(obj["data"].value),
	int(obj["id"].value),
	{image["type"].value: image["url"].value for image in obj["images"]},
	obj["name"].value,
	int(obj["pid"].value),
	obj["primary"].value == "Y",
	obj["user_id"].value
)
ProfileMii.parse = lambda obj: ProfileMii(
	base64.b64decode(obj["data"].value),
	int(obj["id"].value),
	obj["mii_hash"].value,
	{image["type"].value: image["url"].value for image in obj["mii_images"]},
	obj["name"].value,
	obj["primary"].value == "Y",
)
Account.parse = lambda obj: Account(
	obj["attributes"].value,
	obj["domain"].value,
	obj["type"].value,
	obj["username"].value
)
Profile.parse = lambda obj: Profile(
	[Account.parse(account) for account in obj["accounts"]],
	obj["active_flag"].value == "Y",
	obj["birth_date"].value,
	obj["country"].value,
	obj["create_date"].value,
	{attrib["name"].value: attrib["value"].value for attrib in obj["device_attributes"]},
	obj["gender"].value,
	obj["language"].value,
	obj["updated"].value,
	obj["marketing_flag"].value == "Y",
	obj["off_device_flag"].value == "Y",
	int(obj["pid"].value),
	Email.parse(obj["email"]),
	ProfileMii.parse(obj["mii"]),
	int(obj["region"].value),
	obj["tz_name"].value,
	obj["user_id"].value,
	int(obj["utc_offset"].value)
)
		

class NNASError(Exception): pass


class NNASClient:
	def __init__(self):
		self.client = HTTPClient()
		
		cert = ssl.SSLCertificate.load(CERT, ssl.TYPE_PEM)
		key = ssl.SSLPrivateKey.load(KEY, ssl.TYPE_PEM)
		self.cert = cert, key
		
		self.url = "account.nintendo.net"
		
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
		
	def set_certificate(self, cert, key): self.cert = cert, key
	
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
		req.certificate = self.cert
		
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
			req.headers["Authorization"] = auth
			
	def request(self, req):
		response = self.client.request(req, True)
		if response.error():
			logger.error("Account request returned status code %i\n%s", response.status, response.text)
			raise NNASError("Account request failed with status %i" %response.status)
		return response.xml
		
	def login(self, username, password, password_type=None):
		req = HTTPRequest.post("/v1/api/oauth20/access_token/generate")
		self.prepare(req, cert=self.device_cert)
		
		req.form["grant_type"] = "password"
		req.form["user_id"] = urllib.parse.quote(username)
		req.form["password"] = urllib.parse.quote(password)
		if password_type is not None:
			req.form["password_type"] = password_type
		
		response = self.request(req)
		self.auth_token = "Bearer " + response["access_token"]["token"].value
		
	def get_emails(self):
		req = HTTPRequest.get("/v1/api/people/@me/emails")
		self.prepare(req, self.auth_token)
		return [Email.parse(email) for email in self.request(req)]
		
	def get_profile(self):
		req = HTTPRequest.get("/v1/api/people/@me/profile")
		self.prepare(req, self.auth_token)
		return Profile.parse(self.request(req))
		
	def get_nex_token(self, game_server_id):
		req = HTTPRequest.get("/v1/api/provider/nex_token/@me")
		req.params["game_server_id"] = "%08X" %game_server_id
		self.prepare(req, self.auth_token)
		return NexToken.parse(self.request(req))
		
	#The following functions can be used without logging in
		
	def get_miis(self, pids):
		req = HTTPRequest.get("/v1/api/miis")
		req.params["pids"] = urllib.parse.quote(",".join([str(pid) for pid in pids]))
		self.prepare(req)
		
		response = self.request(req)
		return [Mii.parse(mii) for mii in response]
		
	def get_pids(self, nnids):
		req = HTTPRequest.get("/v1/api/admin/mapped_ids")
		req.params["input_type"] = "user_id"
		req.params["output_type"] = "pid"
		req.params["input"] = urllib.parse.quote(",".join(nnids))
		self.prepare(req)
		
		response = self.request(req)
		return {id["in_id"].value: int(id["out_id"].value) for id in response}
		
	def get_nnids(self, pids):
		req = HTTPRequest.get("/v1/api/admin/mapped_ids")
		req.params["input_type"] = "pid"
		req.params["output_type"] = "user_id"
		req.params["input"] = urllib.parse.quote(",".join([str(pid) for pid in pids]))
		self.prepare(req)
		
		response = self.request(req)
		return {int(id["in_id"].value): id["out_id"].value for id in response}
	
	def get_mii(self, pid): return self.get_miis([pid])[0]
	def get_pid(self, nnid): return self.get_pids([nnid])[nnid]
	def get_nnid(self, pid): return self.get_nnids([pid])[pid]
