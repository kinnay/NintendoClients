
from nintendo.common.http import HTTPClient, HTTPRequest
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
import base64

import logging
logger = logging.getLogger(__name__)


class DAuthError(Exception): pass


DAUTH_SOURCE = bytes.fromhex("8be45abcf987021523ca4f5e2300dbf0")

class DAuthClient:
	def __init__(self, keyset):
		self.client = HTTPClient()
		self.keyset = keyset
		
		self.cert = None
		self.region = 1
		
		self.client_id = 0x8F849B5D34778D8E
		
		self.url = "dauth-lp1.ndas.srv.nintendo.net"
		self.user_agent = "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 9.3.0.0)"
		self.system_digest = "CusHY#00090100#vIPNrRbf30SoU8ZJ6uGklMqKAkyjHfdE9m6yLFeChkE="
		
		self.power_state = "FA"
		
		self.key_generation = 11
		
	def set_certificate(self, cert, key): self.cert = cert, key
	
	def set_platform_region(self, region): self.region = region
	def set_client_id(self, id): self.client_id = id
	
	def set_url(self, url): self.url = url
	def set_user_agent(self, agent): self.user_agent = agent
	def set_system_digest(self, digest): self.system_digest = digest
	
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
		
		data = base64.b64decode(challenge["data"].encode(), b"-_")
		
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
		return response.json["device_auth_token"]
		
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
		return base64.b64encode(mac.digest(), b"-_").decode().rstrip("=")
