
from anynet import tls, http
from nintendo import resources
from nintendo.switch import common, dauth
from typing import Any, Awaitable, Callable

import base64

import logging
logger = logging.getLogger(__name__)


type RequestCallback = Callable[..., Awaitable[http.HTTPResponse]]


USER_AGENT = "NintendoSDK Firmware/%s (platform:NX; did:%016x; eid:lp1)"

API_VERSION = {
	 900: 1,
	 901: 1,
	 910: 1,
	 920: 1,
	1000: 1,
	1001: 1,
	1002: 1,
	1003: 1,
	1004: 1,
	1010: 1,
	1011: 1,
	1020: 1,
	1100: 1,
	1101: 1,
	1200: 1,
	1201: 1,
	1202: 1,
	1203: 1,
	1210: 1,
	1300: 1,
	1310: 1,
	1320: 1,
	1321: 1,
	1400: 1,
	1410: 1,
	1411: 1,
	1412: 1,
	1500: 1,
	1501: 1,
	1600: 1,
	1601: 1,
	1602: 1,
	1603: 1,
	1610: 1,
	1700: 1,
	1701: 1,
	1800: 1,
	1801: 1,
	1810: 1,
	1900: 1,
	1901: 1,
	2000: 2,
	2001: 2,
	2010: 2,
	2011: 2,
	2015: 2,
	2020: 2,
	2030: 2,
	2040: 2,
	2050: 2,
	2100: 2,
	2101: 2,
	2110: 2,
	2120: 2,
	2200: 2,
	2210: 2,
	2250: 2,
}

LATEST_VERSION = 2250


class DragonsError(Exception):
	response: http.HTTPResponse

	type: str
	name: str
	title: str
	detail: str
	status: int
	invalid_params: Any

	def __init__(self, response: http.HTTPResponse):
		self.response = response
		
		self.type = response.json["type"]
		self.name = response.json["type"].split("/")[-1]
		self.title = response.json["title"]
		self.detail = response.json["detail"]
		self.status = response.json["number"]
		self.invalid_params = response.json.get("invalid-params")
	
	def __str__(self) -> str:
		return self.title


class DragonsClient:
	_device_id: int | None

	_request_callback: RequestCallback

	_context: tls.TLSContext

	_host_dragons: str
	_host_dragonst: str
	_host_tigers: str

	_system_version: int
	_user_agent_nim: str | None
	_user_agent_dauth: str
	_api_version: int

	def __init__(self, device_id: int | None = None):
		self._device_id = device_id
		
		self._request_callback = http.request
		
		ca = resources.certificate("Nintendo_Class_2_CA_G3.der")
		self._context = tls.TLSContext()
		self._context.set_authority(ca)
		
		self._host_dragons = "dragons.hac.lp1.dragons.nintendo.net"
		self._host_dragonst = "dragonst.hac.lp1.dragons.nintendo.net"
		self._host_tigers = "tigers.hac.lp1.dragons.nintendo.net"
		
		self._system_version = LATEST_VERSION
		self._user_agent_nim = None
		if self._device_id is not None:
			self._user_agent_nim = USER_AGENT %(
				common.FIRMWARE_VERSIONS[LATEST_VERSION], self._device_id
			)
		self._user_agent_dauth = dauth.USER_AGENT[LATEST_VERSION]
		self._api_version = API_VERSION[self._system_version]
	
	def set_request_callback(self, callback: RequestCallback) -> None:
		self._request_callback = callback
	
	def set_context(self, context: tls.TLSContext) -> None:
		self._context = context
	
	def set_certificate(
		self, cert: tls.TLSCertificate, key: tls.TLSPrivateKey
	) -> None:
		self._context.set_certificate(cert, key)
	
	def set_hosts(self, dragons: str, dragonst: str, tigers: str) -> None:
		self._host_dragons = dragons
		self._host_dragonst = dragonst
		self._host_tigers = tigers
	
	def set_system_version(self, version: int) -> None:
		if version not in common.FIRMWARE_VERSIONS:
			raise ValueError("Unknown system version: %i" %version)
		
		self._system_version = version
		if self._device_id is not None:
			self._user_agent_nim = USER_AGENT %(
				common.FIRMWARE_VERSIONS[version], self._device_id
			)
		self._user_agent_dauth = dauth.USER_AGENT[version]
		self._api_version = API_VERSION[self._system_version]
	
	async def _request(
		self, req: http.HTTPRequest, host: str, device_token: str, *,
		account_id: int | None = None
	) -> http.HTTPResponse:
		if self._user_agent_nim is None:
			raise ValueError("This request requires a device id")
		
		req.headers["Host"] = host
		req.headers["Accept"] = "*/*"
		req.headers["User-Agent"] = self._user_agent_nim
		req.headers["DeviceAuthorization"] = "Bearer " + device_token
		if account_id is not None:
			req.headers["Nintendo-Account-Id"] = f"{account_id:016x}"
		if req.json is not None:
			req.headers["Content-Type"] = "application/json"
			req.headers["Content-Length"] = 0
		else:
			req.headers["Content-Length"] = 0
			req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		
		response = await self._request_callback(host, req, self._context)
		if response.error() and response.json:
			logger.error("Dragons server returned an error: %s" %response.json)
			raise DragonsError(response)
		response.raise_if_error()
		return response
	
	async def _request_dauth(
		self, req: http.HTTPRequest, device_token: str, title_id: int
	) -> http.HTTPResponse:
		req.headers["Host"] = self._host_dragons
		if self._system_version < 1800:
			req.headers["User-Agent"] = self._user_agent_dauth
		req.headers["Accept"] = "*/*"
		if self._system_version >= 2000:
			req.headers["User-Agent"] = self._user_agent_dauth
		req.headers["Content-Type"] = "application/json"
		req.headers["DeviceAuthorization"] = "Bearer " + device_token
		req.headers["Nintendo-Application-Id"] = f"{title_id:016x}"
		req.headers["Content-Length"] = 0
		
		response = await self._request_callback(
			self._host_dragons, req, self._context
		)
		if response.error() and response.json:
			logger.error("Dragons server returned an error: %s" %response.json)
			raise DragonsError(response)
		response.raise_if_error()
		return response
	
	async def publish_elicense_archive(
		self, device_token: str, challenge: str, certificate: bytes,
		account_id: int
	):
		req = http.HTTPRequest.post(
			f"/v{self._api_version}/elicense_archives/publish"
		)
		req.json = {
			"challenge": challenge,
			"certificate": base64.b64encode(certificate).decode()
		}
		
		response = await self._request(
			req, self._host_dragons, device_token, account_id=account_id
		)
		return response.json
	
	async def report_elicense_archive(
		self, device_token: str, elicense_archive_id: str, account_id: int
	) -> None:
		req = http.HTTPRequest.put(
			f"/v{self._api_version}/elicense_archives/{elicense_archive_id}/" \
				"report"
		)
		await self._request(
			req, self._host_dragons, device_token, account_id=account_id
		)
	
	async def publish_device_linked_elicenses(self, device_token: str) -> Any:
		req = http.HTTPRequest.post(
			f"/v{self._api_version}/rights/publish_device_linked_elicenses"
		)
		response = await self._request(req, self._host_dragons, device_token)
		return response.json
	
	async def exercise_elicense(
		self, device_token: str, elicense_ids: list[str],
		account_ids: list[int], current_account_id: int
	) -> None:
		req = http.HTTPRequest.post(f"/v{self._api_version}/elicenses/exercise")
		req.json = {
			"elicense_ids": elicense_ids,
			"account_ids": [f"{i:016x}" for i in account_ids]
		}
		await self._request(
			req, self._host_dragons, device_token,
			account_id=current_account_id
		)
	
	async def contents_authorization_token_for_aauth(
		self, device_token: str, elicense_id: str, na_id: int, title_id: int
	) -> Any:
		if self._system_version < 1500:
			raise ValueError(
				"contents_authorization_token_for_aauth was added in system " \
				"version 15.0.0"
			)
		
		req = http.HTTPRequest.post(
			f"/v{self._api_version}/contents_authorization_token_for_aauth/" \
				"issue"
		)
		req.json = {
			"elicense_id": elicense_id,
			"na_id": f"{na_id:016x}"
		}
		
		response = await self._request_dauth(req, device_token, title_id)
		return response.json
