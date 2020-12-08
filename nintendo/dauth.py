
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from anynet import tls, http
from nintendo import switch
import pkg_resources

import logging
logger = logging.getLogger(__name__)


CA = pkg_resources.resource_filename("nintendo", "files/cert/CACERT_NINTENDO_CA_G3.der")


DAUTH_SOURCE = bytes.fromhex("8be45abcf987021523ca4f5e2300dbf0")

SYSTEM_VERSION_DIGEST = {
	900:  "CusHY#00090000#-80vwBkUjWLb5Kpb_cnuTjBZ0rHwZHhN7R1-vg0Ti5c=",
	901:  "CusHY#00090001#qVDSOCehwMDCHyDnkXiTSJ1wEJZHtpRV_CLMKgD-fSw=",
	910:  "CusHY#00090100#vIPNrRbf30SoU8ZJ6uGklMqKAkyjHfdE9m6yLFeChkE=",
	920:  "CusHY#00090200#Uxxmc8gYnfMqxzdZdygZ_OrKo98O7QA65s_EkZnGsDo=",
	1000: "CusHY#000a0000#EmdxOnZjZ9Ihf3Zskt_48pYgowAUeeJccU6tCBIweEc=",
	1001: "CusHY#000a0001#JEuSEdid24qqHqQzfW1tuNsCGcCk-86gcPq0I7M1x18=",
	1002: "CusHY#000a0002#BTOGo0giC7bbrNoi8JEm-FBzmXb2Kgpq4K3OzQrD5l8=",
	1003: "CusHY#000a0003#4mBbTFYnE0Rtmh8NLCVq61rbvx0kJPQUxXkDpwj0V84=",
	1004: "CusHY#000a0003#4mBbTFYnE0Rtmh8NLCVq61rbvx0kJPQUxXkDpwj0V84=",
	1010: "CusHY#000a0100#Vlw9dIEqjxE2F5jDOQPYWXs2p7wIGyDYWXXIyQGdxcE=",
	1011: "CusHY#000a0100#Vlw9dIEqjxE2F5jDOQPYWXs2p7wIGyDYWXXIyQGdxcE=",
	1020: "CusHY#000a0200#90k0dE_eO7hRcs6ByTZMvgUm4lhEoqAlik96WkznQcQ=",
	1100: "CusHY#000b0000#VyA0fsWi6ZBEOzVsseXIcEfFLqQMgW0tWzN2oJ7viqk="
}

USER_AGENT = {
	900:  "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 9.3.0.0)",
	901:  "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 9.3.0.0)",
	910:  "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 9.3.0.0)",
	920:  "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 9.3.0.0)",
	1000: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 10.4.0.0)",
	1001: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 10.4.0.0)",
	1002: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 10.4.0.0)",
	1003: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 10.4.0.0)",
	1004: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 10.4.0.0)",
	1010: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 10.4.0.0)",
	1011: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 10.4.0.0)",
	1020: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 10.4.0.0)",
	1100: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 11.4.0.0)"
}

KEY_GENERATION = {
	900:  10,
	901:  10,
	910:  11,
	920:  11,
	1000: 11,
	1001: 11,
	1002: 11,
	1003: 11,
	1004: 11,
	1010: 11,
	1011: 11,
	1020: 11,
	1100: 11
}

LATEST_VERSION = 1100


class DAuthError(switch.NDASError): pass


class DAuthClient:
	BCAT = 0x67BF9945B45248C6
	ACCOUNT = 0x81333C548B2E876D
	BAAS = 0x8F849B5D34778D8E
	BEACH = 0x93AF0ACB26258DE9
	DRAGONS = 0xD5B6CAC2C1514C56
	PREPO = 0xDF51C436BC01C437
	
	def __init__(self, keyset):
		self.keyset = keyset
		
		ca = tls.TLSCertificate.load(CA, tls.TYPE_DER)
		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		
		self.region = 1
		
		self.url = "dauth-lp1.ndas.srv.nintendo.net"
		self.user_agent = USER_AGENT[LATEST_VERSION]
		self.system_digest = SYSTEM_VERSION_DIGEST[LATEST_VERSION]
		self.key_generation = KEY_GENERATION[LATEST_VERSION]
		
		self.power_state = "FA"
		
	def set_certificate(self, cert, key):
		self.context.set_certificate(cert, key)
	def set_context(self, context):
		self.context = context
	
	def set_platform_region(self, region): self.region = region

	def set_url(self, url): self.url = url
	def set_user_agent(self, user_agent): self.user_agent = user_agent
	def set_system_digest(self, digest): self.system_digest = digest
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version: %i" %version)
		self.user_agent = USER_AGENT[version]
		self.system_digest = SYSTEM_VERSION_DIGEST[version]
		self.key_generation = KEY_GENERATION[version]
	
	def set_power_state(self, state): self.power_state = state
	def set_key_generation(self, keygen): self.key_generation = keygen
		
	async def request(self, req):
		req.headers["Host"] = self.url
		req.headers["User-Agent"] = self.user_agent
		req.headers["Accept"] = "*/*"
		req.headers["X-Nintendo-PowerState"] = self.power_state
		req.headers["Content-Length"] = 0
		req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		
		response = await http.request(self.url, req, self.context)
		if response.error():
			if response.json:
				logger.error("DAuth request returned errors:")
				errors = response.json["errors"]
				for error in errors:
					logger.error("  (%s) %s", error["code"], error["message"])
				raise DAuthError(response.status_code, errors)
			else:
				logger.error("DAuth request returned status code %i", response.status_code)
				raise DAuthError(response.status_code)
		return response
		
	async def challenge(self):
		req = http.HTTPRequest.post("/v6/challenge")
		req.plainform["key_generation"] = self.key_generation
		
		response = await self.request(req)
		return response.json
		
	async def device_token(self, client_id):
		challenge = await self.challenge()
		
		data = switch.b64decode(challenge["data"])
		
		req = http.HTTPRequest.post("/v6/device_auth_token")
		req.plainform["challenge"] = challenge["challenge"]
		req.plainform["client_id"] = "%016x" %client_id
		if self.region == 2:
			req.plainform["ist"] = "true"
		else:
			req.plainform["ist"] = "false"
		req.plainform["key_generation"] = self.key_generation
		req.plainform["system_version"] = self.system_digest
		
		string = http.formencode(req.plainform, False)
		req.plainform["mac"] = self.calculate_mac(string, data)
		
		response = await self.request(req)
		return response.json
		
	def get_master_key(self):
		keygen = self.key_generation
		keyname = "master_key_%02x" %(keygen - 1)
		return self.keyset[keyname]
		
	def decrypt_key(self, key, kek):
		aes = AES.new(kek, AES.MODE_ECB)
		return aes.decrypt(key)
		
	def calculate_mac(self, form, data):
		kek_source = self.keyset["aes_kek_generation_source"]
		master_key = self.get_master_key()
		
		key = self.decrypt_key(kek_source, master_key)
		key = self.decrypt_key(DAUTH_SOURCE, key)
		key = self.decrypt_key(data, key)
		
		mac = CMAC.new(key, ciphermod=AES)
		mac.update(form.encode())
		return switch.b64encode(mac.digest())
