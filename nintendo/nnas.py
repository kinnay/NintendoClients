
from nintendo.miis import MiiData

from bs4 import BeautifulSoup
import pkg_resources
import collections
import requests
import hashlib
import base64
import struct
import time

import logging
logger = logging.getLogger(__name__)


CERT = pkg_resources.resource_filename("nintendo", "files/cert/wiiu_common.crt")
KEY = pkg_resources.resource_filename("nintendo", "files/cert/wiiu_common.key")


def calc_password_hash(pid, password):
	data = struct.pack("<I", pid) + b"\x02\x65\x43\x46" + password.encode("ascii")
	return hashlib.sha256(data).hexdigest()


class NexToken(collections.namedtuple("NexToken", "host port username password token")):
	@classmethod
	def parse(cls, obj):
		return cls(
			obj.host.text,
			int(obj.port.text),
			obj.pid.text,
			obj.nex_password.text,
			obj.token.text
		)
		
class Email(collections.namedtuple("Email", "address id parent primary reachable type validated validation_date")):
	@classmethod
	def parse(cls, obj):
		return cls(
			obj.address.text,
			int(obj.id.text),
			obj.parent.text == "Y",
			obj.primary.text == "Y",
			obj.reachable.text == "Y",
			obj.type.text,
			obj.validated.text == "Y",
			obj.validated_date.text
		)

class Mii(collections.namedtuple("Mii", "data id images name pid primary nnid")):
	@classmethod
	def parse(cls, obj):
		return cls(
			MiiData.parse(base64.decodebytes(obj.data.text.encode("ascii"))),
			int(obj.id.text),
			{image.type.text: image.url.text for image in obj.images},
			obj.find("name").text,
			int(obj.pid.text),
			obj.primary.text == "Y",
			obj.user_id.text
		)
		
		
class ProfileMii(collections.namedtuple("Mii", "data id hash images name primary")):
	@classmethod
	def parse(cls, obj):
		return cls(
			MiiData.parse(base64.decodebytes(obj.data.text.encode("ascii"))),
			int(obj.id.text),
			obj.mii_hash.text,
			{image.type.text: image.url.text for image in obj.mii_images},
			obj.find("name").text,
			obj.primary.text == "Y"
		)
		
		
class Account(collections.namedtuple("Account", "attributes domain type username")):
	@classmethod
	def parse(cls, obj):
		return cls(
			obj.attributes.text,
			obj.domain.text,
			obj.type.text,
			obj.username.text
		)
		
class Profile(collections.namedtuple(
		"Profile",
		"accounts active birthday country creation_date device_attributes gender language "
		"updated marketing off_device pid email mii region timezone nnid utc_offset"
	)):
	@classmethod
	def parse(cls, obj):
		return cls(
			[Account.parse(account) for account in obj.accounts],
			obj.active_flag.text == "Y",
			obj.birth_date.text,
			obj.country.text,
			obj.create_date.text,
			{attrib.find("name").text: attrib.value.text for attrib in obj.device_attributes},
			obj.gender.text,
			obj.language.text,
			obj.updated.text,
			obj.marketing_flag.text == "Y",
			obj.off_device_flag.text == "Y",
			int(obj.pid.text),
			Email.parse(obj.email),
			ProfileMii.parse(obj.mii),
			int(obj.region.text),
			obj.tz_name.text,
			obj.user_id.text,
			int(obj.utc_offset.text)
		)
		
class TimeZone(collections.namedtuple("TimeZone", "area language name utc_offset order")):
	@classmethod
	def parse(cls, obj):	
		return cls(
			str(obj.contents[1]),
			obj.language.text,
			obj.find("name").text,
			int(obj.utc_offset.text),
			int(obj.order.text)
		)
		

class NNASError(Exception): pass


class Request:
	def __init__(self, api):
		self.api = api
		self.headers = api.headers.copy()
		
	def auth(self, token):
		self.headers["X-Nintendo-Client-ID"] = ""
		self.headers["X-Nintendo-Client-Secret"] = ""
		self.headers["Authorization"] = "Bearer %s" %token
		
	def format(self, url):
		return "https://account.nintendo.net/v1/api/%s" %url
		
	def get(self, url, params=None):
		req = requests.Request("GET", self.format(url), self.headers, params=params)
		return self.request(req)
		
	def post(self, url, data=None):
		req = requests.Request("POST", self.format(url), self.headers, data=data)
		return self.request(req)
		
	def request(self, req):
		prepped = req.prepare()
		response = self.api.session.send(prepped, verify=False, cert=(CERT, KEY))
		content = BeautifulSoup(response.text, "lxml")
		
		if response.status_code != 200:
			logger.error("HTTP request returned status code %i\n%s", response.status_code, response.text)
			raise NNASError("Account request failed: %s" %content.error.message.text)
		
		return content
		
		
class NNASClient:
	def __init__(self):
		self.headers = {
			"Accept-Language": "en",
			"X-Nintendo-Platform-ID": "1",
			"X-Nintendo-Device-Type": "2",
			"X-Nintendo-Client-ID": "a2efa818a34fa16b8afbc8a74eba3eda",
			"X-Nintendo-Client-Secret": "c91cdb5658bd4954ade78533a339cf9a",
			"X-Nintendo-FPD-Version": "0000",
			"X-Nintendo-Environment": "L1"
		}
		self.session = requests.Session()
		
		self.access_token = None
		self.refresh_token = None
		self.refresh_time = None
		self.device_cert = None
		
	def set_device(self, device_id, serial_number, system_version, region, country, device_cert=None):
		self.headers["X-Nintendo-Device-ID"] = str(device_id)
		self.headers["X-Nintendo-Serial-Number"] = serial_number
		self.headers["X-Nintendo-System-Version"] = "%04X" %system_version
		self.headers["X-Nintendo-Region"] = str(region)
		self.headers["X-Nintendo-Country"] = country
		self.device_cert = device_cert
		
	def set_title(self, title_id, application_version):
		self.headers["X-Nintendo-Title-ID"] = "%016X" %title_id
		self.headers["X-Nintendo-Unique-ID"] = "%05X" %((title_id & 0xFFFFF00) >> 8)
		self.headers["X-Nintendo-Application-Version"] = "%04X" %application_version

	def set_header(self, name, value):
		self.headers[name] = value
		
	def get_access_token(self):
		if time.time() >= self.refresh_time:
			self.refresh_login()
		return self.access_token

	def login(self, username, password, hash=False):
		data = {
			"grant_type": "password",
			"user_id": username,
			"password": password
		}
		if hash:
			data["password_type"] = "hash"

		request = Request(self)
		if self.device_cert:
			request.headers["X-Nintendo-Device-Cert"] = self.device_cert

		response = request.post(
			"oauth20/access_token/generate",
			data = data
		)
		
		self.access_token = response.oauth20.access_token.token.text
		self.refresh_token = response.oauth20.access_token.refresh_token.text
		self.refresh_time = time.time() + int(response.oauth20.access_token.expires_in.text)
		
	def refresh_login(self):
		request = Request(self)
		if self.device_cert:
			request.headers["X-Nintendo-Device-Cert"] = self.device_cert

		response = request.post(
			"oauth20/access_token/generate",
			data = {
				"grant_type": "refresh_token",
				"refresh_token": self.refresh_token
			}
		)
		
		self.access_token = response.oauth20.access_token.token.text
		self.refresh_token = response.oauth20.access_token.refresh_token.text
		self.refresh_time = time.time() + int(response.oauth20.access_token.expires_in.text)
		
	def get_emails(self):
		request = Request(self)
		request.auth(self.get_access_token())
		response = request.get(
			"people/@me/emails"
		)
		
		return [Email.parse(email) for email in response.emails]
		
	def get_profile(self):
		request = Request(self)
		request.auth(self.get_access_token())
		response = request.get(
			"people/@me/profile"
		)
		
		return Profile.parse(response.person)
		
	def get_nex_token(self, game_server_id):
		request = Request(self)
		request.auth(self.get_access_token())
		response = request.get(
			"provider/nex_token/@me",
			params = {
				"game_server_id": "%08X" %game_server_id
			}
		)
		
		return NexToken.parse(response.nex_token)
		
	#The following functions can be used without logging in first
	
	def validate_email(self, email):
		request = Request(self)
		request.post(
			"support/validate/email",
			data = {"email": email}
		)
		#An error is thrown if validation fails
		
	def get_miis(self, pids):
		request = Request(self)
		response = request.get(
			"miis",
			params = {
				"pids": ",".join([str(pid) for pid in pids])
			}
		)
		return [Mii.parse(mii) for mii in response.miis]
		
	def get_mii(self, pid):
		return self.get_miis([pid])[0]
		
	def get_pids(self, nnids):
		request = Request(self)
		response = request.get(
			"admin/mapped_ids",
			params = {
				"input_type": "user_id",
				"output_type": "pid",
				"input": ",".join(nnids)
			}
		)
		return {id.in_id.text: int(id.out_id.text) for id in response.mapped_ids}
		
	def get_nnids(self, pids):
		request = Request(self)
		response = request.get(
			"admin/mapped_ids",
			params = {
				"input_type": "pid",
				"output_type": "user_id",
				"input": ",".join([str(pid) for pid in pids])
			}
		)
		return {int(id.in_id.text): id.out_id.text for id in response.mapped_ids}
		
	def get_pid(self, nnid): return self.get_pids([nnid])[nnid]
	def get_nnid(self, pid): return self.get_nnids([pid])[pid]
		
	def get_time_zones(self, country, language):
		request = Request(self)
		response = request.get(
			"content/time_zones/%s/%s" %(country, language)
		)
		return [TimeZone.parse(tz) for tz in response.timezones]
