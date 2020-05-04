
from nintendo.common.http import HTTPClient, HTTPRequest
from nintendo.switch import b64encode, b64decode
from Crypto.Hash import CMAC
from Crypto.Cipher import AES

import logging
logger = logging.getLogger(__name__)


class DAuthError(Exception): pass


DAUTH_SOURCE = bytes.fromhex("8be45abcf987021523ca4f5e2300dbf0")

SYSTEM_VERSION_DIGEST = {
	900:  "CusHY#00090000#-80vwBkUjWLb5Kpb_cnuTjBZ0rHwZHhN7R1-vg0Ti5c=",
	901:  "CusHY#00090001#qVDSOCehwMDCHyDnkXiTSJ1wEJZHtpRV_CLMKgD-fSw=",
	910:  "CusHY#00090100#vIPNrRbf30SoU8ZJ6uGklMqKAkyjHfdE9m6yLFeChkE=",
	920:  "CusHY#00090200#Uxxmc8gYnfMqxzdZdygZ_OrKo98O7QA65s_EkZnGsDo=",
	1000: "CusHY#000a0000#EmdxOnZjZ9Ihf3Zskt_48pYgowAUeeJccU6tCBIweEc=",
	1001: "CusHY#000a0001#JEuSEdid24qqHqQzfW1tuNsCGcCk-86gcPq0I7M1x18=",
	1002: "CusHY#000a0002#BTOGo0giC7bbrNoi8JEm-FBzmXb2Kgpq4K3OzQrD5l8="
}

USER_AGENT = {
	900:  "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 9.3.0.0)",
	901:  "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 9.3.0.0)",
	910:  "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 9.3.0.0)",
	920:  "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 9.3.0.0)",
	1000: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 10.4.0.0)",
	1001: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 10.4.0.0)",
	1002: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 10.4.0.0)"
}

KEY_GENERATION = {
	900:  10,
	901:  10,
	910:  11,
	920:  11,
	1000: 11,
	1001: 11,
	1002: 11
}

LATEST_VERSION = 1002


class DAuthClient:
	def __init__(self, keyset):
		self.client = HTTPClient()
		self.keyset = keyset
		
		self.cert = None
		self.region = 1
		
		self.client_id = 0x8F849B5D34778D8E
		
		self.url = "dauth-lp1.ndas.srv.nintendo.net"
		self.user_agent = USER_AGENT[LATEST_VERSION]
		self.system_digest = SYSTEM_VERSION_DIGEST[LATEST_VERSION]
		self.key_generation = KEY_GENERATION[LATEST_VERSION]
		
		self.power_state = "FA"
		
	def set_certificate(self, cert, key): self.cert = cert, key
	
	def set_platform_region(self, region): self.region = region
	def set_client_id(self, id): self.client_id = id
	
	def set_url(self, url): self.url = url
	def set_user_agent(self, agent): self.user_agent = agent
	def set_system_digest(self, digest): self.system_digest = digest
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		self.user_agent = USER_AGENT[version]
		self.system_digest = SYSTEM_VERSION_DIGEST[version]
		self.key_generation = KEY_GENERATION[version]
	
	def set_power_state(self, state): self.power_state = state
	
	def set_key_generation(self, keygen): self.key_generation = keygen
		
	def request(self, req):
		req.certificate = self.cert
		
		req.headers["Host"] = self.url
		req.headers["User-Agent"] = self.user_agent
		req.headers["Accept"] = "*/*"
		req.headers["X-Nintendo-PowerState"] = self.power_state
		req.headers["Content-Length"] = 0
		req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		
		response = self.client.request(req, True)
		if response.status != 200:
			if response.json is not None:
				logger.error("DAuth request returned errors:")
				for error in response.json["errors"]:
					logger.error("  (%s) %s", error["code"], error["message"])
				raise DAuthError("DAuth request failed: %s" %response.json["errors"][0]["message"])
			else:
				logger.error("DAuth request returned status code %i", response.status)
				raise DAuthError("DAuth request failed with status %i" %response.status)
		return response
		
	def challenge(self):
		req = HTTPRequest.post("/v6/challenge")
		req.form["key_generation"] = self.key_generation
		
		response = self.request(req)
		return response.json
		
	def device_token(self):
		challenge = self.challenge()
		
		data = b64decode(challenge["data"])
		
		req = HTTPRequest.post("/v6/device_auth_token")
		req.form["challenge"] = challenge["challenge"]
		req.form["client_id"] = "%016x" %self.client_id
		if self.region == 2:
			req.form["ist"] = "true"
		else:
			req.form["ist"] = "false"
		req.form["key_generation"] = self.key_generation
		req.form["system_version"] = self.system_digest
		req.form["mac"] = self.calculate_mac(req.form.encode(), data)
		
		response = self.request(req)
		return response.json
		
	def get_master_key(self):
		keygen = self.key_generation
		keyname = "master_key_%02x" %(keygen - 1)
		return self.keyset.get(keyname)
		
	def decrypt_key(self, key, kek):
		aes = AES.new(kek, AES.MODE_ECB)
		return aes.decrypt(key)
		
	def calculate_mac(self, form, data):
		kek_source = self.keyset.get("aes_kek_generation_source")
		master_key = self.get_master_key()
		
		key = self.decrypt_key(kek_source, master_key)
		key = self.decrypt_key(DAUTH_SOURCE, key)
		key = self.decrypt_key(data, key)
		
		mac = CMAC.new(key, ciphermod=AES)
		mac.update(form.encode())
		return b64encode(mac.digest())
