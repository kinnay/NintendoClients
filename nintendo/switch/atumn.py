
from nintendo.switch import common
from anynet import tls, http
import pkg_resources

import logging
logger = logging.getLogger(__name__)


CA = pkg_resources.resource_filename("nintendo", "files/cert/CACERT_NINTENDO_CLASS2_CA_G3.der")


USER_AGENT = "NintendoSDK Firmware/%s (platform:NX; did:%016x; eid:lp1)"

LATEST_VERSION = 1700


class AtumnClient:
	def __init__(self, device_id):
		self.device_id = device_id
		
		self.request_callback = http.request
		
		ca = tls.TLSCertificate.load(CA, tls.TYPE_DER)
		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		
		self.host = "atumn.hac.lp1.d4c.nintendo.net"
		
		self.system_version = LATEST_VERSION
		self.user_agent = USER_AGENT %(common.FIRMWARE_VERSIONS[LATEST_VERSION], self.device_id)
	
	def set_request_callback(self, callback): self.request_callback = callback
	
	def set_context(self, context): self.context = context
	def set_certificate(self, cert, key): self.context.set_certificate(cert, key)
	
	def set_host(self, host): self.host = host
	
	def set_system_version(self, version):
		if version not in common.FIRMWARE_VERSIONS:
			raise ValueError("Unknown system version: %i" %version)
		
		self.system_version = version
		self.user_agent = USER_AGENT %(common.FIRMWARE_VERSIONS[version], self.device_id)
	
	async def request(self, req):
		req.headers["Host"] = self.host
		req.headers["Accept"] = "*/*"
		req.headers["User-Agent"] = self.user_agent
		
		response = await self.request_callback(self.host, req, self.context)
		response.raise_if_error()
		return response

	async def download_content_metadata(self, title_id, title_version, *, system_update=False):
		content_type = "s" if system_update else "a"

		req = http.HTTPRequest.head("/t/%c/%016x/%i" %(content_type, title_id, title_version))
		req.params = {
			"device_id": "%016x" %self.device_id
		}

		response = await self.request(req)
		content_id = response.headers["X-Nintendo-Content-ID"]

		req = http.HTTPRequest.get("/c/%s/%s" %(content_type, content_id))
		response = await self.request(req)
		return response.body
	
	async def download_content(self, content_id):
		req = http.HTTPRequest.get("/c/c/%s" %content_id)
		response = await self.request(req)
		return response.body
