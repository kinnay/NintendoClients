
from anynet import tls, http
from nintendo import resources
from nintendo.switch import common

import logging
logger = logging.getLogger(__name__)


USER_AGENT = "NintendoSDK Firmware/%s (platform:NX; did:%016x; eid:lp1)"

LATEST_VERSION = 1901


class SunError(Exception):
	def __init__(self, response):
		self.response = response

		self.code = response.json["error"]["code"]
		self.message = response.json["error"]["message"]
	
	def __str__(self):
		return self.message


class SunClient:
	def __init__(self, device_id):
		self.device_id = device_id
		
		self.request_callback = http.request
		
		ca = resources.certificate("CACERT_NINTENDO_CLASS2_CA_G3.der")
		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		
		self.host = "sun.hac.lp1.d4c.nintendo.net"
		
		self.user_agent = USER_AGENT %(common.FIRMWARE_VERSIONS[LATEST_VERSION], self.device_id)
	
	def set_request_callback(self, callback): self.request_callback = callback
	
	def set_context(self, context): self.context = context
	def set_certificate(self, cert, key): self.context.set_certificate(cert, key)
	
	def set_host(self, host): self.host = host
	
	def set_system_version(self, version):
		if version not in common.FIRMWARE_VERSIONS:
			raise ValueError("Unknown system version: %i" %version)
		self.user_agent = USER_AGENT %(common.FIRMWARE_VERSIONS[version], self.device_id)
	
	async def request(self, req):
		req.headers["Host"] = self.host
		req.headers["User-Agent"] = self.user_agent
		req.headers["Accept"] = "application/json"
		
		response = await self.request_callback(self.host, req, self.context)
		if response.error() and response.json:
			logger.error("Sun server returned an error: %s" %response.json)
			raise SunError(response)
		response.raise_if_error()
		return response
	
	async def system_update_meta(self):
		req = http.HTTPRequest.get("/v1/system_update_meta")
		req.params = {
			"device_id": "%016x" %self.device_id
		}
		
		response = await self.request(req)
		return response.json
