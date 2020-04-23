
from nintendo.common.http import HTTPClient, HTTPRequest

import logging
logger = logging.getLogger(__name__)


USER_AGENT = {
	900:  "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	901:  "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	910:  "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	920:  "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	1000: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1001: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)"
}

LATEST_VERSION = 1001


class BAASError(Exception): pass


class BAASClient:
	def __init__(self):
		self.client = HTTPClient()
		
		self.url = "e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com"
		self.user_agent = USER_AGENT[LATEST_VERSION]
		self.power_state = "FA"
		
		self.access_token = None
		self.login_token = None
		
	def set_url(self, url): self.url = url
	def set_user_agent(self, agent): self.user_agent = agent
	def set_power_state(self, state): self.power_state = state
	
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		self.user_agent = USER_AGENT[version]
		
	def request(self, req, token, use_power_state):
		req.headers["Host"] = self.url
		req.headers["User-Agent"] = self.user_agent
		req.headers["Accept"] = "*/*"
		if token:
			req.headers["Authorization"] = token
		if use_power_state:
			req.headers["X-Nintendo-PowerState"] = self.power_state
		req.headers["Content-Length"] = 0
		req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		
		response = self.client.request(req, True)
		if response.status not in [200, 201]:
			logger.warning("BAAS request returned error: %s" %response.json)
			raise BAASError("BAAS request failed: %s" %response.json["title"])
		return response
		
	def authenticate(self, device_token):
		req = HTTPRequest.post("/1.0.0/application/token")
		req.form["grantType"] = "public_client"
		req.form["assertion"] = device_token
		
		response = self.request(req, False, True)
		self.access_token = response.json["tokenType"] + " " + response.json["accessToken"]
		return response.json
		
	def login(self, id, password, app_token=None):
		req = HTTPRequest.post("/1.0.0/login")
		req.form["id"] = id
		req.form["password"] = password
		if app_token:
			req.form["appAuthNToken"] = app_token
			
		response = self.request(req, self.access_token, True)
		self.login_token = response.json["tokenType"] + " " + response.json["accessToken"]
		return response.json
		
	def register(self):
		req = HTTPRequest.post("/1.0.0/users")
		response = self.request(req, self.access_token, False)
		return response.json
