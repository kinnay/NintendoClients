
from anynet import tls, http
from nintendo import resources
from nintendo.switch import common, dauth
import base64

import logging
logger = logging.getLogger(__name__)


USER_AGENT = "NintendoSDK Firmware/%s (platform:NX; did:%016x; eid:lp1)"

LATEST_VERSION = 1901


class DragonsError(Exception):
	def __init__(self, response):
		self.response = response
		
		self.type = response.json["type"]
		self.name = response.json["type"].split("/")[-1]
		self.title = response.json["title"]
		self.detail = response.json["detail"]
		self.status = response.json["number"]
		self.invalid_params = response.json.get("invalid-params")
	
	def __str__(self):
		return self.title


class DragonsClient:
	def __init__(self, device_id=None):
		self.device_id = device_id
		
		self.request_callback = http.request
		
		ca = resources.certificate("CACERT_NINTENDO_CLASS2_CA_G3.der")
		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		
		self.host_dragons = "dragons.hac.lp1.dragons.nintendo.net"
		self.host_dragonst = "dragonst.hac.lp1.dragons.nintendo.net"
		self.host_tigers = "tigers.hac.lp1.dragons.nintendo.net"
		
		self.system_version = LATEST_VERSION
		self.user_agent_nim = None
		if self.device_id is not None:
			self.user_agent_nim = USER_AGENT %(common.FIRMWARE_VERSIONS[LATEST_VERSION], self.device_id)
		self.user_agent_dauth = dauth.USER_AGENT[LATEST_VERSION]
	
	def set_request_callback(self, callback): self.request_callback = callback
	
	def set_context(self, context): self.context = context
	def set_certificate(self, cert, key): self.context.set_certificate(cert, key)
	
	def set_hosts(self, dragons, dragonst, tigers):
		self.host_dragons = dragons
		self.host_dragonst = dragonst
		self.host_tigers = tigers
	
	def set_system_version(self, version):
		if version not in common.FIRMWARE_VERSIONS:
			raise ValueError("Unknown system version: %i" %version)
		
		self.system_version = version
		if self.device_id is not None:
			self.user_agent_nim = USER_AGENT %(common.FIRMWARE_VERSIONS[version], self.device_id)
		self.user_agent_dauth = dauth.USER_AGENT[version]
	
	async def request(self, req, host, device_token, *, account_id=None):
		if self.user_agent_nim is None:
			raise ValueError("This request requires a device id")
		
		req.headers["Host"] = host
		req.headers["Accept"] = "*/*"
		req.headers["User-Agent"] = self.user_agent_nim
		req.headers["DeviceAuthorization"] = "Bearer " + device_token
		if account_id is not None:
			req.headers["Nintendo-Account-Id"] = "%016x" %account_id
		if req.json is not None:
			req.headers["Content-Type"] = "application/json"
			req.headers["Content-Length"] = 0
		else:
			req.headers["Content-Length"] = 0
			req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		
		response = await self.request_callback(host, req, self.context)
		if response.error() and response.json:
			logger.error("Dragons server returned an error: %s" %response.json)
			raise DragonsError(response)
		response.raise_if_error()
		return response
	
	async def request_dauth(self, req, device_token, title_id):
		req.headers["Host"] = self.host_dragons
		if self.system_version < 1800:
			req.headers["User-Agent"] = self.user_agent_dauth
		req.headers["Accept"] = "*/*"
		req.headers["Content-Type"] = "application/json"
		req.headers["DeviceAuthorization"] = "Bearer " + device_token
		req.headers["Nintendo-Application-Id"] = "%016x" %title_id
		req.headers["Content-Length"] = 0
		
		response = await self.request_callback(self.host_dragons, req, self.context)
		if response.error() and response.json:
			logger.error("Dragons server returned an error: %s" %response.json)
			raise DragonsError(response)
		response.raise_if_error()
		return response
	
	async def publish_elicense_archive(self, device_token, challenge, certificate, account_id):
		req = http.HTTPRequest.post("/v1/elicense_archives/publish")
		req.json = {
			"challenge": challenge,
			"certificate": base64.b64encode(certificate).decode()
		}
		
		response = await self.request(req, self.host_dragons, device_token, account_id=account_id)
		return response.json
	
	async def report_elicense_archive(self, device_token, elicense_archive_id, account_id):
		req = http.HTTPRequest.put("/v1/elicense_archives/%s/report" %elicense_archive_id)
		await self.request(req, self.host_dragons, device_token, account_id=account_id)
	
	async def publish_device_linked_elicenses(self, device_token):
		req = http.HTTPRequest.post("/v1/rights/publish_device_linked_elicenses")
		response = await self.request(req, self.host_dragons, device_token)
		return response.json
	
	async def exercise_elicense(self, device_token, elicense_ids, account_ids, current_account_id):
		req = http.HTTPRequest.post("/v1/elicenses/exercise")
		req.json = {
			"elicense_ids": elicense_ids,
			"account_ids": ["%016x" %i for i in account_ids]
		}
		await self.request(req, self.host_dragons, device_token, account_id=current_account_id)
	
	async def contents_authorization_token_for_aauth(self, device_token, elicense_id, na_id, title_id):
		if self.system_version < 1500:
			raise ValueError("contents_authorization_token_for_aauth was added in system version 15.0.0")
		
		req = http.HTTPRequest.post("/v1/contents_authorization_token_for_aauth/issue")
		req.json = {
			"elicense_id": elicense_id,
			"na_id": "%016x" %na_id
		}
		
		response = await self.request_dauth(req, device_token, title_id)
		return response.json
