
from anynet import tls, http
import json

import logging
logger = logging.getLogger(__name__)


MODULE_ACCOUNT = "nnAccount"
MODULE_FRIENDS = "nnFriends"

USER_AGENT = {
	 900: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 901: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 910: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 920: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	1000: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1001: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1002: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1003: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1004: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1010: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1011: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1020: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1100: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 11.4.0.0; Add-on 11.4.0.0)",
	1101: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 11.4.0.0; Add-on 11.4.0.0)",
	1200: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1201: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1202: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1203: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1210: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1300: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.3.0.0; Add-on 13.3.0.0)",
	1310: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1320: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1321: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1400: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1410: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1411: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1412: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1500: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)",
	1501: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)",
	1600: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1601: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1602: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1603: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1610: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1700: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 17.5.0.0; Add-on 17.5.0.0)",
	1701: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 17.5.0.0; Add-on 17.5.0.0)",
	1800: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 18.3.0.0; Add-on 18.3.0.0)",
	1801: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 18.3.0.0; Add-on 18.3.0.0)",
	1810: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 18.3.0.0; Add-on 18.3.0.0)",
	1900: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 19.3.0.0; Add-on 19.3.0.0)",
	1901: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 19.3.0.0; Add-on 19.3.0.0)",
}

LATEST_VERSION = 1901


class PresenceState:
	INACTIVE = "INACTIVE"
	ONLINE = "ONLINE"
	PLAYING = "PLAYING"


class BAASError(Exception):
	def __init__(self, response):
		self.response = response
		
		self.type = response.json["type"]
		self.name = response.json["errorCode"]
		self.title = response.json["title"]
		self.detail = response.json["detail"]
		self.status = response.json["status"]
		self.instance = response.json["instance"]
	
	def __str__(self):
		return self.title


class BAASClient:
	def __init__(self):
		self.request_callback = http.request
		
		self.context = tls.TLSContext()
		
		self.host = "e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com"
		self.power_state = "FA"

		self.system_version = LATEST_VERSION
		self.user_agent = USER_AGENT[LATEST_VERSION]
	
	def set_request_callback(self, callback): self.request_callback = callback
	def set_context(self, context): self.context = context
	
	def set_host(self, host): self.host = host
	def set_power_state(self, state): self.power_state = state
	
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		self.system_version = version
		self.user_agent = USER_AGENT[version]
		
	async def request(self, req, token, module, *, use_power_state=False):
		# This is somewhat complicated because we want to
		# put the headers in the correct order
		content_type = "application/x-www-form-urlencoded"
		if req.json is not None:
			content_type = "application/json-patch+json" if req.method == "PATCH" else "application/json"
		
		req.headers["Host"] = self.host
		req.headers["User-Agent"] = self.user_agent %module
		req.headers["Accept"] = "*/*"
		if module == MODULE_FRIENDS and req.json is not None:
			req.headers["Content-Type"] = content_type
		if token:
			req.headers["Authorization"] = "Bearer " + token
		if use_power_state:
			req.headers["X-Nintendo-PowerState"] = self.power_state
		
		if req.method != "GET":
			if req.json is None:
				req.headers["Content-Length"] = 0
				req.headers["Content-Type"] = content_type
			else:
				if module != MODULE_FRIENDS:
					req.headers["Content-Type"] = content_type
				req.headers["Content-Length"] = 0
		
		response = await self.request_callback(self.host, req, self.context)
		if response.json and "errorCode" in response.json:
			logger.warning("BAAS server returned an error: %s" %response.json)
			raise BAASError(response)
		response.raise_if_error()
		return response
	
	async def authenticate(self, device_token, penne_id=None):
		req = http.HTTPRequest.post("/1.0.0/application/token")
		req.form = {
			"grantType": "public_client",
			"assertion": device_token
		}
		if self.system_version >= 1900 and penne_id is not None:
			req.form["penneId"] = penne_id

		response = await self.request(req, None, MODULE_ACCOUNT, use_power_state=True)
		return response.json
	
	async def login(self, id, password, access_token, app_token=None, na_country=None, skip_verification=False):
		req = http.HTTPRequest.post("/1.0.0/login")
		req.form = {
			"id": "%016x" %id,
			"password": password
		}
		
		if app_token:
			req.form["appAuthNToken"] = app_token
		
		if self.system_version >= 1800:
			if na_country is None:
				raise ValueError("na_country parameter is required for system version 18.0.0 and later")
			req.form["naCountry"] = na_country
		
		if skip_verification:
			req.form["skipOp2Verification"] = "1"
			
		response = await self.request(req, access_token, MODULE_ACCOUNT, use_power_state=True)
		return response.json
	
	async def register(self, access_token):
		req = http.HTTPRequest.post("/1.0.0/users")
		
		response = await self.request(req, access_token, MODULE_ACCOUNT)
		return response.json
	
	async def update_presence(self, user_id, device_account_id, access_token, state, title_id, presence_group_id, app_fields={}, acd_index=0):
		app_fields = json.dumps(app_fields, separators=(",", ":"))
		
		req = http.HTTPRequest.patch("/1.0.0/users/%016x/device_accounts/%016x" %(user_id, device_account_id))
		req.json = [
			{"op": "replace", "path": "/presence/state", "value": state},
			{"op": "add", "path": "/presence/extras/friends/appField", "value": app_fields},
			{"op": "add", "path": "/presence/extras/friends/appInfo:appId", "value": "%016x" %title_id}
		]
		if self.system_version >= 1900:
			req.json.append({"op": "add", "path": "/presence/extras/friends/appInfo:acdIndex", "value": acd_index})
		req.json.append({"op": "add", "path": "/presence/extras/friends/appInfo:presenceGroupId", "value": "%016x" %presence_group_id})

		response = await self.request(req, access_token, MODULE_FRIENDS)
		return response.json
	
	async def get_friends(self, user_id, access_token, count=300):
		req = http.HTTPRequest.get("/2.0.0/users/%016x/friends" %user_id)
		req.params = {"count": count}
		response = await self.request(req, access_token, MODULE_FRIENDS)
		return response.json
