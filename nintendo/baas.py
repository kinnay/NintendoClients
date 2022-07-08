
from anynet import tls, http
from enum import Enum
import json

import logging
logger = logging.getLogger(__name__)


USER_AGENT = {
	 900: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 901: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 910: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 920: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	1000: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1001: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1002: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1003: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1004: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1010: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1011: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1020: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1100: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 11.4.0.0; Add-on 11.4.0.0)",
	1101: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 11.4.0.0; Add-on 11.4.0.0)",
	1200: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1201: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1202: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1203: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1210: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1300: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.3.0.0; Add-on 13.3.0.0)",
	1310: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1320: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1321: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1400: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1410: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1411: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1412: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
}

LATEST_VERSION = 1412


class BAASError(Exception):
	def __init__(self, error):
		self.status = error["status"]
		self.name = error["errorCode"]
		self.title = error["title"]
		self.detail = error["detail"]
		self.instance = error["instance"]
		self.type = error["type"]

class PresenceState(Enum):
	INACTIVE = "INACTIVE"
	ONLINE = "ONLINE"
	PLAYING = "PLAYING"

class PresenceOperation:
	def __init__(self, op : str, path : str, value : str):

		if op not in ['add', 'replace']:
			raise ValueError("Operation must be 'add' or 'replace'")

		self.op = op
		self.path = path
		self.value = value
	
	def encode(self) -> dict:
		return {
			"op": self.op,
			"path": self.path,
			"value": self.value
		}
		

class BAASClient:
	def __init__(self):
		self.url = "e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com"
		self.user_agent = USER_AGENT[LATEST_VERSION]
		self.power_state = "FA"
		
		self.context = tls.TLSContext()
	
	def set_url(self, url): self.url = url
	def set_user_agent(self, user_agent): self.user_agent = user_agent
	def set_power_state(self, state): self.power_state = state
	def set_context(self, context): self.context = context
	
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		self.user_agent = USER_AGENT[version]
		
	async def request(self, req, token, use_power_state):
		req.headers["Host"] = self.url
		req.headers["User-Agent"] = self.user_agent
		req.headers["Accept"] = "*/*"
		if token:
			req.headers["Authorization"] = "Bearer " + token
		if use_power_state:
			req.headers["X-Nintendo-PowerState"] = self.power_state
		if req.method == "POST":
			req.headers["Content-Length"] = 0
			req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		
		response = await http.request(self.url, req, self.context)
		if response.error():
			logger.warning("BAAS request returned error: %s" %response.json)
			raise BAASError(response.json)
		return response
		
	async def authenticate(self, device_token):
		req = http.HTTPRequest.post("/1.0.0/application/token")
		req.form = {
			"grantType": "public_client",
			"assertion": device_token
		}

		response = await self.request(req, None, True)
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
			
		response = await self.request(req, access_token, True)
		return response.json
	
	async def register(self, access_token):
		req = http.HTTPRequest.post("/1.0.0/users")
		
		response = await self.request(req, access_token, False)
		return response.json

	async def set_presence(self, baas_id : int, user_id : int, baasLoginAccessToken, state : PresenceState, title_id : int):
		# Respect header ordering.
		req = http.HTTPRequest.patch("/1.0.0/users/%016x/device_accounts/%016x" % (user_id, baas_id))
		req.headers["Content-Type"] = "application/json-patch+json"

		op_pres_state = PresenceOperation("replace", "/presence/state", state.name).encode()
		op_app_field = PresenceOperation("add", "/presence/extras/friends/appField", "{}").encode()
		op_app_id = PresenceOperation("add", "/presence/extras/friends/appInfo:appId", "%016x" % title_id).encode()
		op_group_id = PresenceOperation("add", "/presence/extras/friends/appInfo:presenceGroupId", "%016x" % title_id).encode()

		list_ops = [op_pres_state, op_app_field, op_app_id, op_group_id]
		req.body = bytes(json.dumps(list_ops), encoding="ascii")

		response = await self.request(req, baasLoginAccessToken, False)
		return response.json
