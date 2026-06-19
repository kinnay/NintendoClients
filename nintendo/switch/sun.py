
from anynet import tls, http
from nintendo import resources
from nintendo.switch import common
from typing import Any, Awaitable, Callable

import logging
logger = logging.getLogger(__name__)


type RequestCallback = Callable[..., Awaitable[http.HTTPResponse]]


USER_AGENT = "NintendoSDK Firmware/%s (platform:NX; did:%016x; eid:lp1)"

LATEST_VERSION = 2250


class SunError(Exception):
	response: http.HTTPResponse

	code: str
	message: str

	def __init__(self, response: http.HTTPResponse):
		self.response = response

		self.code = response.json["error"]["code"]
		self.message = response.json["error"]["message"]
	
	def __str__(self) -> str:
		return self.message


class SunClient:
	_device_id: int
	_request_callback: RequestCallback
	_context: tls.TLSContext
	_host: str
	_user_agent: str

	def __init__(self, device_id: int):
		self._device_id = device_id
		
		self._request_callback = http.request
		
		ca = resources.certificate("Nintendo_Class_2_CA_G3.der")
		self._context = tls.TLSContext()
		self._context.set_authority(ca)
		
		self._host = "sun.hac.lp1.d4c.nintendo.net"
		
		self._user_agent = USER_AGENT %(
			common.FIRMWARE_VERSIONS[LATEST_VERSION], self._device_id
		)
	
	def set_request_callback(self, callback: RequestCallback) -> None:
		self._request_callback = callback
	
	def set_context(self, context: tls.TLSContext):
		self._context = context
	
	def set_certificate(
		self, cert: tls.TLSCertificate, key: tls.TLSPrivateKey
	) -> None:
		self._context.set_certificate(cert, key)
	
	def set_host(self, host: str) -> None:
		self._host = host
	
	def set_system_version(self, version: int) -> None:
		if version not in common.FIRMWARE_VERSIONS:
			raise ValueError("Unknown system version: {version}")
		self._user_agent = USER_AGENT %(
			common.FIRMWARE_VERSIONS[version], self._device_id
		)
	
	async def _request(self, req: http.HTTPRequest) -> http.HTTPResponse:
		req.headers["Host"] = self._host
		req.headers["User-Agent"] = self._user_agent
		req.headers["Accept"] = "application/json"
		
		response = await self._request_callback(self._host, req, self._context)
		if response.error() and response.json:
			logger.error(f"Sun server returned an error: {response.json}")
			raise SunError(response)
		response.raise_if_error()
		return response
	
	async def system_update_meta(self) -> Any:
		req = http.HTTPRequest.get("/v1/system_update_meta")
		req.params = {
			"device_id": f"{self._device_id:016x}"
		}
		
		response = await self._request(req)
		return response.json
