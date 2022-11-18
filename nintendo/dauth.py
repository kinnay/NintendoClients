
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from anynet import tls, http
import pkg_resources
import base64

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
	1100: "CusHY#000b0000#VyA0fsWi6ZBEOzVsseXIcEfFLqQMgW0tWzN2oJ7viqk=",
	1101: "CusHY#000b0001#iI0rZ0Q2dg3Evhd-8GoYmp-KTE8malKe0GOJgXa-XG8=",
	1200: "CusHY#000c0000#C-BynYNPXdQJNBZjx02Hizi8lRUSIKLwPGa5p8EY1uo=",
	1201: "CusHY#000c0001#YXsU5FTbkUh18QH27L3woGqw5n1gIDpMGbPXM8oACzY=",
	1202: "CusHY#000c0002#6tB3UVnmvT_nsNBMPSD-K1oe0IA1cYvYDyqDCjy2W_I=",
	1203: "CusHY#000c0003#E8Ph6vISWsJtN0E3hsfVRoZMG1Qqkc-qGRlAp-Bs2SI=",
	1210: "CusHY#000c0100#Hzs8Gtp6yKgGKMb732-5Q-NvbQcHCgBh_LQrrpg0bIs=",
	1300: "CusHY#000d0000#r1xneESd4PiTRYIhVIl0bK1ST5L5BUmv_uGPLqc4PPo=",
	1310: "CusHY#000d0100#plps6S3C43QHhkI2oNvYIFjNxQjTcLdUX2_biEI5w2w=",
	1320: "CusHY#000d0200#JFVNVuG9x3V5tRshdD9FdJjgHOmzsrgXHocEPvW5eMM=",
	1321: "CusHY#000d0201#V1i7M7oEhkDaH1lcGlHhGAnyHONMAnTAA6pGdZ7MFqc=",
	1400: "CusHY#000e0000#35hWb15SBXTnbUfTMLBz9sCnfheuRGis0OTZqa7l8yw=",
	1410: "CusHY#000e0100#ctIxSPR4jenzQNGc6y4zXIvzvF75ty53jN0T15Rjtmk=",
	1411: "CusHY#000e0101#uTt4IVydkYqwYArOFR3BzOCmw0MkEeF_tZxHENYDh4E=",
	1412: "CusHY#000e0102#jHk6_VwXVPPl3ijRZ5jRy5MIAcUW_Q2uFdfJ0vrjhCA=",
	1500: "CusHY#000f0000#MJE7we0zvVhAnXN9uCU7fQAM7GiqGHpR5ECuC9G_nuU=",
	1501: "CusHY#000f0001#TMqizZGvUaBZApmHHQE0Uo7vQ6xWuQxZ8JH87_HnnqI=",
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
	1100: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 11.4.0.0)",
	1101: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 11.4.0.0)",
	1200: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 12.3.0.0)",
	1201: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 12.3.0.0)",
	1202: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 12.3.0.0)",
	1203: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 12.3.0.0)",
	1210: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 12.3.0.0)",
	1300: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 13.3.0.0)",
	1310: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 13.4.0.0)",
	1320: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 13.4.0.0)",
	1321: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 13.4.0.0)",
	1400: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 14.3.0.0)",
	1410: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 14.3.0.0)",
	1411: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 14.3.0.0)",
	1412: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 14.3.0.0)",
	1500: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 15.3.0.0)",
	1501: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 15.3.0.0)",
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
	1100: 11,
	1101: 11,
	1200: 11,
	1201: 11,
	1202: 11,
	1203: 11,
	1210: 11,
	1300: 13,
	1310: 13,
	1320: 13,
	1321: 13,
	1400: 14,
	1410: 14,
	1411: 14,
	1412: 14,
	1500: 15,
	1501: 15,
}

API_VERSION = {
	900: 6,
	901: 6,
	910: 6,
	920: 6,
	1000: 6,
	1001: 6,
	1002: 6,
	1003: 6,
	1004: 6,
	1010: 6,
	1011: 6,
	1020: 6,
	1100: 6,
	1101: 6,
	1200: 6,
	1201: 6,
	1202: 6,
	1203: 6,
	1210: 6,
	1300: 7,
	1310: 7,
	1320: 7,
	1321: 7,
	1400: 7,
	1410: 7,
	1411: 7,
	1412: 7,
	1500: 7,
	1501: 7,
}

LATEST_VERSION = 1501


class DAuthError(Exception):
	UNAUTHORIZED_DEVICE = 4
	SYSTEM_UPDATE_REQUIRED = 7
	BANNED_DEIVCE = 8
	INTERNAL_SERVER_ERROR = 9
	GENERIC = 14
	CHALLENGE_EXPIRED = 15
	WRONG_MAC = 16
	BROKEN_DEVICE = 17
	
	def __init__(self, response):
		self.response = response
		self.code = response.json["errors"][0]["code"]
		self.message = response.json["errors"][0]["message"]
	
	def __str__(self):
		return self.message


class DAuthClient:
	SCSI = 0x146C8AC7B8A0DB52
	ATUM = 0x3117B250CAB38F45
	ESHOP = 0x41F4A6491028E3C4
	BCAT = 0x67BF9945B45248C6
	SATA = 0x6AC5A6873FE5F68C
	ACCOUNT = 0x81333C548B2E876D
	NPNS = 0x83B72B05DC3278D7
	BAAS = 0x8F849B5D34778D8E
	BEACH = 0x93AF0ACB26258DE9
	DRAGONS = 0xD5B6CAC2C1514C56
	PCTL = 0xDC656EA03B63CF68
	PREPO = 0xDF51C436BC01C437
	
	def __init__(self, keys):
		self.keys = keys
		
		self.request_callback = http.request
		
		ca = tls.TLSCertificate.load(CA, tls.TYPE_DER)
		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		
		self.host = "dauth-lp1.ndas.srv.nintendo.net"
		self.user_agent = USER_AGENT[LATEST_VERSION]
		self.system_digest = SYSTEM_VERSION_DIGEST[LATEST_VERSION]
		self.key_generation = KEY_GENERATION[LATEST_VERSION]
		self.api_version = API_VERSION[LATEST_VERSION]
		
		self.power_state = "FA"
		self.region = 1
		
	def set_request_callback(self, callback): self.request_callback = callback
	
	def set_context(self, context): self.context = context
	def set_certificate(self, cert, key): self.context.set_certificate(cert, key)
	
	def set_power_state(self, state): self.power_state = state
	def set_platform_region(self, region): self.region = region
	
	def set_host(self, host): self.host = host
	
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version: %i" %version)
		self.user_agent = USER_AGENT[version]
		self.system_digest = SYSTEM_VERSION_DIGEST[version]
		self.key_generation = KEY_GENERATION[version]
		self.api_version = API_VERSION[version]
		
	async def request(self, req):
		req.headers["Host"] = self.host
		req.headers["User-Agent"] = self.user_agent
		req.headers["Accept"] = "*/*"
		req.headers["X-Nintendo-PowerState"] = self.power_state
		req.headers["Content-Length"] = 0
		req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		
		response = await self.request_callback(self.host, req, self.context)
		if response.json and "errors" in response.json:
			logger.error("DAuth server returned errors:")
			for error in response.json["errors"]:
				logger.error("  (%s) %s", error["code"], error["message"])
			raise DAuthError(response, errors)
		response.raise_if_error()
		return response
		
	async def challenge(self):
		req = http.HTTPRequest.post("/v%i/challenge" %self.api_version)
		req.form = {
			"key_generation": self.key_generation
		}
		
		response = await self.request(req)
		return response.json
	
	async def device_token(self, client_id):
		challenge = await self.challenge()
		
		data = base64.b64decode(challenge["data"], "-_")
		
		req = http.HTTPRequest.post("/v%i/device_auth_token" %self.api_version)
		req.rawform = {
			"challenge": challenge["challenge"],
			"client_id": "%016x" %client_id,
			"ist": "true" if self.region == 2 else "false",
			"key_generation": self.key_generation,
			"system_version": self.system_digest
		}
		
		string = http.formencode(req.rawform, False)
		req.rawform["mac"] = self.calculate_mac(string, data)
		
		response = await self.request(req)
		return response.json
		
	async def edge_token(self, client_id, vendor_id="akamai"):
		challenge = await self.challenge()
		
		data = base64.b64decode(challenge["data"], "-_")
		
		req = http.HTTPRequest.post("/v%i/edge_token" %self.api_version)
		req.rawform = {
			"challenge": challenge["challenge"],
			"client_id": "%016x" %client_id,
			"ist": "true" if self.region == 2 else "false",
			"key_generation": self.key_generation,
			"system_version": self.system_digest
		}
		
		if self.api_version == 7:
			req.rawform["vendor_id"] = vendor_id
		
		string = http.formencode(req.rawform, False)
		req.rawform["mac"] = self.calculate_mac(string, data)
		
		response = await self.request(req)
		return response.json
		
	def get_master_key(self):
		keygen = self.key_generation
		keyname = "master_key_%02x" %(keygen - 1)
		return self.keys[keyname]
	
	def decrypt_key(self, key, kek):
		aes = AES.new(kek, AES.MODE_ECB)
		return aes.decrypt(key)
		
	def calculate_mac(self, form, data):
		kek_source = self.keys["aes_kek_generation_source"]
		master_key = self.get_master_key()
		
		key = self.decrypt_key(kek_source, master_key)
		key = self.decrypt_key(DAUTH_SOURCE, key)
		key = self.decrypt_key(data, key)
		
		mac = CMAC.new(key, ciphermod=AES)
		mac.update(form.encode())
		return base64.b64encode(mac.digest(), b"-_").decode().rstrip("=")
