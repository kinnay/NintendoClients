
from anynet import tls, http

import logging
logger = logging.getLogger(__name__)


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
}

LATEST_VERSION = 1501


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
	ACCOUNT = "nnAccount"
	FRIENDS = "nnFriends"
	
	def __init__(self):
		self.request_callback = http.request
		
		self.context = tls.TLSContext()
		
		self.host = "e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com"
		self.user_agent_account = USER_AGENT[LATEST_VERSION] %self.ACCOUNT
		self.user_agent_friends = USER_AGENT[LATEST_VERSION] %self.FRIENDS
		self.power_state = "FA"
	
	def set_request_callback(self, callback): self.request_callback = callback
	def set_context(self, context): self.context = context
	
	def set_host(self, host): self.host = host
	def set_power_state(self, state): self.power_state = state
	
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		self.user_agent_account = USER_AGENT[version] %self.ACCOUNT
		self.user_agent_friends = USER_AGENT[version] %self.FRIENDS
		
	async def request(self, req, token, user_agent, *, use_power_state=False):
		req.headers["Host"] = self.host
		req.headers["User-Agent"] = user_agent
		req.headers["Accept"] = "*/*"
		if token:
			req.headers["Authorization"] = "Bearer " + token
		if use_power_state:
			req.headers["X-Nintendo-PowerState"] = self.power_state
		if req.method == "POST":
			req.headers["Content-Length"] = 0
			req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		
		response = await self.request_callback(self.host, req, self.context)
		if response.json and "errorCode" in response.json:
			logger.warning("BAAS server returned an error: %s" %response.json)
			raise BAASError(response)
		response.raise_if_error()
		return response
		
	async def authenticate(self, device_token):
		req = http.HTTPRequest.post("/1.0.0/application/token")
		req.form = {
			"grantType": "public_client",
			"assertion": device_token
		}

		response = await self.request(req, None, self.user_agent_account, use_power_state=True)
		return response.json
	
	async def login(self, id, password, access_token, app_token=None, skip_verification=False):
		req = http.HTTPRequest.post("/1.0.0/login")
		req.form = {
			"id": "%016x" %id,
			"password": password
		}
		
		if app_token:
			req.form["appAuthNToken"] = app_token
		if skip_verification:
			req.form["skipOp2Verification"] = "1"
			
		response = await self.request(req, access_token, self.user_agent_account, use_power_state=True)
		return response.json
	
	async def register(self, access_token):
		req = http.HTTPRequest.post("/1.0.0/users")
		
		response = await self.request(req, access_token, self.user_agent_account)
		return response.json
