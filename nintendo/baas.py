
from nintendo.common.http import HTTPClient, HTTPRequest

import logging
logger = logging.getLogger(__name__)


class BAASError(Exception): pass


class BAASClient:
	def __init__(self):
		self.client = HTTPClient()
		
		self.url = "e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com"
		self.user_agent = "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)"
		self.power_state = "FA"
		
		self.token = None
		
	def set_url(self, url): self.url = url
	def set_user_agent(self, agent): self.user_agent = agent
	def set_power_state(self, state): self.power_state = state
		
	def request(self, req):
		req.headers["Host"] = self.url
		req.headers["User-Agent"] = self.user_agent
		req.headers["Accept"] = "*/*"
		req.headers["X-Nintendo-PowerState"] = self.power_state
		req.headers["Content-Length"] = 0
		req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		
		response = self.client.request(req, True)
		if response.status != 200:
			logger.warning("BAAS request returned error: %s" %response.json)
			raise BAASError("BAAS request failed: %s" %response.json["title"])
		return response
		
	def authenticate(self, device_token):
		req = HTTPRequest.post("/1.0.0/application/token")
		req.form["grantType"] = "public_client"
		req.form["assertion"] = device_token
		
		response = self.request(req)
		self.token = response.json["tokenType"] + response.json["accessToken"]
		return response
