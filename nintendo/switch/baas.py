
from anynet import tls, http
from typing import Any, Awaitable, Callable

import json

import logging
logger = logging.getLogger(__name__)


type RequestCallback = Callable[..., Awaitable[http.HTTPResponse]]


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
	2000: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2001: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2010: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2011: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2015: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2020: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2030: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2040: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2050: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2100: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 21.4.0.0; Add-on 21.4.0.0)",
	2101: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 21.4.0.0; Add-on 21.4.0.0)",
	2110: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 21.4.0.0; Add-on 21.4.0.0)",
	2120: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 21.4.0.0; Add-on 21.4.0.0)",
	2220: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 22.2.0.0; Add-on 22.2.0.0)",
	2210: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 22.2.0.0; Add-on 22.2.0.0)",
	2250: "libcurl (%s; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 22.2.0.0; Add-on 22.2.0.0)",
}

LATEST_VERSION = 2250


class PresenceState:
	INACTIVE = "INACTIVE"
	ONLINE = "ONLINE"
	PLAYING = "PLAYING"


class BAASError(Exception):
	response: http.HTTPResponse

	type: str
	name: str
	title: str
	detail: str
	status: int
	instance: str

	def __init__(self, response: http.HTTPResponse):
		self.response = response
		
		self.type = response.json["type"]
		self.name = response.json["errorCode"]
		self.title = response.json["title"]
		self.detail = response.json["detail"]
		self.status = response.json["status"]
		self.instance = response.json["instance"]
	
	def __str__(self) -> str:
		return self.title


class BAASClient:
	_request_callback: RequestCallback

	_context: tls.TLSContext

	_host: str | None
	_power_state: str

	_system_version: int
	_user_agent: str

	def __init__(self):
		self._request_callback = http.request
		
		self._context = tls.TLSContext()
		
		self._host = None
		self._power_state = "FA"

		self._system_version = LATEST_VERSION
		self._user_agent = USER_AGENT[LATEST_VERSION]
	
	def set_request_callback(self, callback: RequestCallback) -> None:
		self._request_callback = callback
	
	def set_context(self, context: tls.TLSContext) -> None:
		self._context = context
	
	def set_certificate(
		self, cert: tls.TLSCertificate, key: tls.TLSPrivateKey
	) -> None:
		self._context.set_certificate(cert, key)
	
	def set_host(self, host: str) -> None:
		self._host = host
	
	def set_power_state(self, state: str) -> None:
		self._power_state = state
	
	def set_system_version(self, version: int) -> None:
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		self._system_version = version
		self._user_agent = USER_AGENT[version]
	
	def get_host(self, module: str) -> str:
		if self._host:
			return self._host
		
		if module == MODULE_ACCOUNT and self._system_version >= 2100:
			return "m-lp1.baas.nintendo.com"
		return "e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com"
	
	async def authenticate(
		self, device_token: str, penne_id: str | None = None
	) -> Any:
		req = http.HTTPRequest.post("/1.0.0/application/token")
		req.form = {
			"grantType": "public_client",
			"assertion": device_token
		}
		if self._system_version >= 1900 and penne_id is not None:
			req.form["penneId"] = penne_id

		response = await self._request(
			req, None, MODULE_ACCOUNT, use_power_state=True
		)
		return response.json
	
	async def login(
		self, id: int, password: str, access_token: str,
		app_token: str | None = None, na_country: str | None = None,
		skip_verification: bool = False, is_persistent: bool = True
	) -> Any:
		req = http.HTTPRequest.post("/1.0.0/login")
		req.form = {
			"id": f"{id:016x}",
			"password": password
		}
		
		if app_token:
			req.form["appAuthNToken"] = app_token
		
		if self._system_version >= 1800:
			if na_country is None:
				raise ValueError(
					"na_country parameter is required for system version " \
					"18.0.0 and later"
				)
			req.form["naCountry"] = na_country
		
		if self._system_version >= 2000:
			req.form["isPersistent"] = "true" if is_persistent else "false"
		
		if skip_verification:
			req.form["skipOp2Verification"] = "1"
			
		response = await self._request(
			req, access_token, MODULE_ACCOUNT, use_power_state=True
		)
		return response.json
	
	async def register(self, access_token: str) -> Any:
		req = http.HTTPRequest.post("/1.0.0/users")
		
		response = await self._request(req, access_token, MODULE_ACCOUNT)
		return response.json
	
	async def update_presence(
		self, user_id: int, device_account_id: int, access_token: str,
		state: str, title_id: int, presence_group_id: int,
		app_fields: dict[str, str] = {}, acd_index: int = 0
	) -> Any:
		app_fields_text = json.dumps(app_fields, separators=(",", ":"))
		
		req = http.HTTPRequest.patch(
			f"/1.0.0/users/{user_id:016x}/device_accounts/" \
			f"{device_account_id:016x}"
		)
		req.json = [
			{"op": "replace", "path": "/presence/state", "value": state},
			{
				"op": "add",
				"path": "/presence/extras/friends/appField",
				"value": app_fields_text
			},
			{
				"op": "add",
				"path": "/presence/extras/friends/appInfo:appId",
				"value": f"{title_id:016x}"
			}
		]
		if self._system_version >= 1900:
			req.json.append({
				"op": "add",
				"path": "/presence/extras/friends/appInfo:acdIndex",
				"value": acd_index}
			)
		
		req.json.append({
			"op": "add",
			"path": "/presence/extras/friends/appInfo:presenceGroupId",
			"value": f"{presence_group_id:016x}"
		})

		response = await self._request(req, access_token, MODULE_FRIENDS)
		return response.json
	
	async def get_friends(
		self, user_id: int, access_token: str, count: int = 300
	) -> Any:
		req = http.HTTPRequest.get(f"/2.0.0/users/{user_id:016x}/friends")
		req.params = {"count": count}
		response = await self._request(req, access_token, MODULE_FRIENDS)
		return response.json
	
	async def _request(
		self, req: http.HTTPRequest, token: str | None, module: str, *,
		use_power_state: bool = False
	) -> http.HTTPResponse:
		# This is somewhat complicated because we want to
		# put the headers in the correct order
		content_type = "application/x-www-form-urlencoded"
		if req.json is not None:
			if req.method == "PATCH":
				content_type = "application/json-patch+json"
			else:
				content_type = "application/json"
		
		req.headers["Host"] = self._host
		if module == MODULE_ACCOUNT and self._system_version >= 2100:
			req.headers["Accept"] = "*/*"
			req.headers["User-Agent"] = self._user_agent %module
			if req.method != "GET":
				req.headers["Content-Type"] = content_type
			if token:
				req.headers["Authorization"] = "Bearer " + token
			if use_power_state:
				req.headers["X-Nintendo-PowerState"] = self._power_state
			if req.method != "GET":
				req.headers["Content-Length"] = 0
		else:
			req.headers["User-Agent"] = self._user_agent %module
			req.headers["Accept"] = "*/*"
			if module == MODULE_FRIENDS and req.json is not None:
				req.headers["Content-Type"] = content_type
			if token:
				req.headers["Authorization"] = "Bearer " + token
			if use_power_state:
				req.headers["X-Nintendo-PowerState"] = self._power_state
			
			if req.method != "GET":
				if req.json is None:
					req.headers["Content-Length"] = 0
					req.headers["Content-Type"] = content_type
				else:
					if module != MODULE_FRIENDS:
						req.headers["Content-Type"] = content_type
					req.headers["Content-Length"] = 0
		
		response = await self._request_callback(self._host, req, self._context)
		if response.json and "errorCode" in response.json:
			logger.warning("BAAS server returned an error: %s" %response.json)
			raise BAASError(response)
		response.raise_if_error()
		return response
