
from anynet import tls, http
from nintendo import resources
import base64

import logging
logger = logging.getLogger(__name__)


USER_AGENT = {
	 900: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 901: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 910: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 920: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	1000: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1001: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1002: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1003: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1004: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1010: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1011: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1020: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1100: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 11.4.0.0; Add-on 11.4.0.0)",
	1101: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 11.4.0.0; Add-on 11.4.0.0)",
	1200: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1201: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1202: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1203: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1210: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1300: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.3.0.0; Add-on 13.3.0.0)",
	1310: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1320: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1321: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1400: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1410: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1411: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1412: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1500: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)",
	1501: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)",
	1600: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1601: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1602: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1603: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1610: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1700: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 17.5.0.0; Add-on 17.5.0.0)",
	1701: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 17.5.0.0; Add-on 17.5.0.0)",
	1800: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 18.3.0.0; Add-on 18.3.0.0)",
	1801: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 18.3.0.0; Add-on 18.3.0.0)",
	1810: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 18.3.0.0; Add-on 18.3.0.0)",
	1900: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 19.3.0.0; Add-on 19.3.0.0)",
	1901: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 19.3.0.0; Add-on 19.3.0.0)",
}

LATEST_VERSION = 1901

LANGUAGES = [
	"en-US", "en-GB", "ja", "fr", "de", "es-419", "es", "it", "nl"
	"fr-CA", "pt", "ru", "zh-Hans", "zh-Hant", "ko", "pt-BR"
]


class FiveError(Exception):
	INVALID_PARAMETER = 2
	INVALID_REQUEST_URI = 3
	UNAUTHORIZED = 6
	RESOURCE_NOT_FOUND = 10
	APPLICATION_DATA_TOO_LARGE = 11
	
	def __init__(self, response):
		self.response = response
		
		self.code = int(response.json["error"]["code"])
		self.message = response.json["error"]["message"]
	
	def __str__(self):
		return self.message


class FiveClient:
	def __init__(self):
		self.request_callback = http.request
		
		ca = resources.certificate("CACERT_NINTENDO_CA_G3.der")
		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		
		self.host = "app.lp1.five.nintendo.net"
		
		self.system_version = LATEST_VERSION
		self.user_agent = USER_AGENT[LATEST_VERSION]
	
	def set_request_callback(self, callback): self.request_callback = callback
	def set_context(self, context): self.context = context
	def set_host(self, host): self.host = host
	
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		self.system_version = version
		self.user_agent = USER_AGENT[version]
	
	async def request(self, req, access_token):
		req.headers["Host"] = self.host
		req.headers["User-Agent"] = self.user_agent
		req.headers["Accept"] = "*/*"
		
		if req.method != "GET":
			if req.json is not None:
				req.headers["Content-Type"] = "application/json"
				req.headers["Authorization"] = "Bearer " + access_token
				req.headers["Content-Length"] = 0
			elif req.form is not None:
				req.headers["Content-Type"] = "application/x-www-form-urlencoded"
				req.headers["Authorization"] = "Bearer " + access_token
				req.headers["Content-Length"] = 0
			else:
				req.headers["Authorization"] = "Bearer " + access_token
				req.headers["Content-Length"] = 0
				req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		else:
			req.headers["Authorization"] = "Bearer " + access_token
		
		response = await self.request_callback(self.host, req, self.context)
		if response.json and "error" in response.json:
			logger.warning("Five server returned an error: %s" %response.json)
			raise FiveError(response)
		response.raise_if_error()
		return response
	
	async def get_unread_invitation_count(self, access_token, user_id):
		req = http.HTTPRequest.get("/v1/users/%016x/invitations/inbox" %user_id)
		req.params = {
			"fields": "count",
			"read": "false"
		}
		response = await self.request(req, access_token)
		return response.json["count"]
	
	async def get_inbox(self, access_token, user_id):
		req = http.HTTPRequest.get("/v1/users/%016x/invitations/inbox" %user_id)
		response = await self.request(req, access_token)
		return response.json

	async def get_invitation_group(self, access_token, invitation_group_id):
		req = http.HTTPRequest.get("/v1/invitation_groups/%i" %invitation_group_id)
		response = await self.request(req, access_token)
		return response.json
	
	async def mark_as_read(self, access_token, ids):
		req = http.HTTPRequest.patch("/v1/invitations")
		req.form = {
			"read": "true",
			"ids": ",".join("%016x" %id for id in ids)
		}
		await self.request(req, access_token)
	
	async def mark_all_as_read(self, access_token, user_id):
		req = http.HTTPRequest.patch("/v1/users/%016x/invitations/mark_as_read" %user_id)
		await self.request(req, access_token)

	async def send_invitation(
		self, access_token, receivers, application_id, application_group_id,
		application_data, messages, application_id_match=False,
		acd_index=0
	):
		# Sanity checks
		if len(receivers) > 16:
			raise ValueError("Too many receiver ids")
		for language, message in messages.items():
			if language not in LANGUAGES:
				raise ValueError("'%s' is not a valid language" %language)
			if len(message) >= 0xC0:
				raise ValueError("Message for language '%s' is too long" %language)
		if len(application_data) > 0x400:
			raise ValueError("Application data is too large")
		
		req = http.HTTPRequest.post("/v1/invitation_groups")
		req.json = {
			"receiver_ids": ["%016x" %id for id in receivers],
			"application_id": "%016x" %application_id,
		}

		if self.system_version >= 1900:
			req.json["acd_index"] = acd_index
		
		req.json["application_group_id"] = "%016x" %application_group_id
		
		if application_data:
			req.json["application_data"] = base64.b64encode(application_data).decode()
		
		req.json["messages"] = messages
		for language in LANGUAGES:
			if language in messages:
				req.json["messages"][language] = messages[language]
		req.json["application_id_match"] = application_id_match
		
		req.json_options["ensure_ascii"] = False
		
		response = await self.request(req, access_token)
		return response.json
