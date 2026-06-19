
from anynet import tls, http
from nintendo import resources
from nintendo.switch import common
from typing import Awaitable, Callable

import logging
logger = logging.getLogger(__name__)


type RequestCallback = Callable[..., Awaitable[http.HTTPResponse]]


USER_AGENT = "NintendoSDK Firmware/%s (platform:NX; did:%016x; eid:lp1)"

LATEST_VERSION = 2250


class AtumnClient:
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
		
		self._host = "atumn.hac.lp1.d4c.nintendo.net"
		
		self._user_agent = USER_AGENT %(
			common.FIRMWARE_VERSIONS[LATEST_VERSION], self._device_id
		)
	
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
	
	def set_system_version(self, version: int) -> None:
		if version not in common.FIRMWARE_VERSIONS:
			raise ValueError(f"Unknown system version: {version}")
		self._user_agent = USER_AGENT %(
			common.FIRMWARE_VERSIONS[version], self._device_id
		)

	async def download_content_metadata(
		self, title_id: int, title_version: int, *, system_update: bool = False
	) -> bytes:
		content_type = "s" if system_update else "a"

		req = http.HTTPRequest.head(
			f"/t/{content_type}/{title_id:016x}/{title_version}"
		)
		req.params = {
			"device_id": f"{self._device_id:016x}"
		}

		response = await self._request(req)
		content_id = response.headers["X-Nintendo-Content-ID"]

		req = http.HTTPRequest.get(f"/c/{content_type}/{content_id}")
		response = await self._request(req)
		return response.body
	
	async def download_content(self, content_id: str) -> bytes:
		req = http.HTTPRequest.get(f"/c/c/{content_id}")
		response = await self._request(req)
		return response.body
	
	async def _request(self, req: http.HTTPRequest) -> http.HTTPResponse:
		req.headers["Host"] = self._host
		req.headers["Accept"] = "*/*"
		req.headers["User-Agent"] = self._user_agent
		
		response = await self._request_callback(self._host, req, self._context)
		response.raise_if_error()
		return response
