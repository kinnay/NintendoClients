
from anynet import tls, http
from nintendo import resources
from typing import Any, Awaitable, Callable
import base64

import logging
logger = logging.getLogger(__name__)


type RequestCallback = Callable[..., Awaitable[http.HTTPResponse]]


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
	2000: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2001: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2010: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2011: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2015: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2020: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2030: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2040: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2050: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 20.5.4.0; Add-on 20.5.4.0)",
	2100: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 21.4.0.0; Add-on 21.4.0.0)",
	2101: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 21.4.0.0; Add-on 21.4.0.0)",
	2110: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 21.4.0.0; Add-on 21.4.0.0)",
	2120: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 21.4.0.0; Add-on 21.4.0.0)",
	2200: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 22.2.0.0; Add-on 22.2.0.0)",
	2210: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 22.2.0.0; Add-on 22.2.0.0)",
	2250: "libcurl (nnFriends; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 22.2.0.0; Add-on 22.2.0.0)",
}

LATEST_VERSION = 2250

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

	response: http.HTTPResponse

	code: int
	message: str
	
	def __init__(self, response: http.HTTPResponse):
		self.response = response
		
		self.code = int(response.json["error"]["code"])
		self.message = response.json["error"]["message"]
	
	def __str__(self) -> str:
		return self.message


class FiveClient:
	_request_callback: RequestCallback

	_context: tls.TLSContext

	_host: str

	_system_version: int
	_user_agent: str

	def __init__(self):
		self._request_callback = http.request
		
		ca = resources.certificate("Nintendo_CA_G3.der")
		self._context = tls.TLSContext()
		self._context.set_authority(ca)
		
		self._host = "app.lp1.five.nintendo.net"
		
		self._system_version = LATEST_VERSION
		self._user_agent = USER_AGENT[LATEST_VERSION]
	
	def set_request_callback(self, callback: RequestCallback) -> None:
		self._request_callback = callback
	
	def set_context(self, context: tls.TLSContext) -> None:
		self._context = context
	
	def set_host(self, host: str) -> None:
		self._host = host
	
	def set_system_version(self, version: int) -> None:
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		self._system_version = version
		self._user_agent = USER_AGENT[version]
	
	async def _request(
		self, req: http.HTTPRequest, access_token: str
	) -> http.HTTPResponse:
		req.headers["Host"] = self._host
		req.headers["User-Agent"] = self._user_agent
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
		
		response = await self._request_callback(self._host, req, self._context)
		if response.json and "error" in response.json:
			logger.warning("Five server returned an error: %s" %response.json)
			raise FiveError(response)
		response.raise_if_error()
		return response
	
	async def get_unread_invitation_count(
		self, access_token: str, user_id: int
	) -> int:
		if self._system_version < 2000:
			req = http.HTTPRequest.get(
				f"/v1/users/{user_id:016x}/invitations/inbox"
			)
			req.params = {
				"fields": "count",
				"read": "false"
			}
		else:
			req = http.HTTPRequest.get(
				f"/v2/users/{user_id:016x}/invitations/inbox"
			)
			req.params = {
				"fields": "count",
				"read": "false",
				"invitation_types": "friend"
			}
		response = await self._request(req, access_token)
		return response.json["count"]
	
	async def get_inbox(self, access_token: str, user_id: int) -> Any:
		if self._system_version < 2000:
			req = http.HTTPRequest.get(
				f"/v1/users/{user_id:016x}/invitations/inbox"
			)
		else:
			req = http.HTTPRequest.get(
				f"/v2/users/{user_id:016x}/invitations/inbox"
			)
			req.params = {
				"invitation_types": "friend"
			}
		response = await self._request(req, access_token)
		return response.json

	async def get_invitation_group(
		self, access_token: str, invitation_group_id: int
	) -> Any:
		req = http.HTTPRequest.get(
			f"/v1/invitation_groups/{invitation_group_id}"
		)
		response = await self._request(req, access_token)
		return response.json
	
	async def mark_as_read(self, access_token: str, ids: list[int]) -> None:
		req = http.HTTPRequest.patch("/v1/invitations")
		req.form = {
			"read": "true",
			"ids": ",".join(f"{id:016x}" for id in ids)
		}
		await self._request(req, access_token)
	
	async def mark_all_as_read(self, access_token: str, user_id: int) -> None:
		req = http.HTTPRequest.patch(
			f"/v1/users/{user_id:016x}/invitations/mark_as_read"
		)
		await self._request(req, access_token)

	async def send_invitation(
		self, access_token: str, receivers: list[int], application_id: int,
		application_group_id: int, application_data: bytes,
		messages: dict[str, str], application_id_match: bool = False,
		acd_index: int = 0
	) -> Any:
		# Sanity checks
		if len(receivers) > 16:
			raise ValueError("Too many receiver ids")
		
		for language, message in messages.items():
			if language not in LANGUAGES:
				raise ValueError(f"'{language}' is not a valid language")
			if len(message) >= 0xC0:
				raise ValueError(
					f"Message for language '{language}' is too long"
				)
		
		if len(application_data) > 0x400:
			raise ValueError("Application data is too large")
		
		url = "/v1/invitation_groups"
		if self._system_version >= 2000:
			url = "/v2/invitation_groups"
		
		req = http.HTTPRequest.post(url)

		req.json = {
			"receiver_ids": [f"{id:016x}" for id in receivers],
		}

		if self._system_version >= 2000:
			req.json["invitation_type"] = "friend"
		
		req.json["application_id"] = f"{application_id:016x}"

		if self._system_version >= 1900:
			req.json["acd_index"] = acd_index
		
		req.json["application_group_id"] = f"{application_group_id:016x}"
		
		if application_data:
			req.json["application_data"] = \
				base64.b64encode(application_data).decode()
		
		req.json["messages"] = messages
		for language in LANGUAGES:
			if language in messages:
				req.json["messages"][language] = messages[language]
		req.json["application_id_match"] = application_id_match
		
		req.json_options["ensure_ascii"] = False
		
		response = await self._request(req, access_token)
		return response.json
