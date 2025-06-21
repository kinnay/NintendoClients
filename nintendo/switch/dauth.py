
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from anynet import tls, http
from nintendo import resources
import base64
import json
import time

import logging
logger = logging.getLogger(__name__)


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
	1600: "CusHY#00100000#k_VrW8iX7QgupPlYZYhg3dLEVDhqGN_iXW5Mm0VYEvQ=",
	1601: "CusHY#00100001#qHay53MkzVLOUU_Iy7_kyPlUMnaoi7HXCAmESYTft_c=",
	1602: "CusHY#00100002#qjeCnaxVt5NjGjxosJOMVw-ZyR219B3qgAB3YtSil6g=",
	1603: "CusHY#00100003#Lis4m_Z4pXlDAaBBxeRO66_glyu92IAf2-dHKNxYAJs=",
	1610: "CusHY#00100100#3kOLHmbuMWa-kHN-SMtCkgNvwdwBHIb2b4f60BNNmrw=",
	1700: "CusHY#00110000#ntMZ00Jmb7Rdu18Fy1FPZo7RO3h_MYIqxozbQQDcVaA=",
	1701: "CusHY#00110001#7CmXEDXEN8wnVu-e7WY6Cv5CvmzjuG6EnKEkf1_jaC8=",
	1800: "CusHY#00120000#U531L4Si9RbhOVeyVppe18WHkJ0k4_KzrNtygsekMNo=",
	1801: "CusHY#00120001#chuxR_O35JFyJq7dIlT8yP1A-j1yBcF-iU4iVDjHt9g=",
	1810: "CusHY#00120100#7pfwz-8raijuW2lv4UOi4Hukp-DuY898HEK6hEYUjSM=",
	1900: "CusHY#00130000#x2jf5al2EkqJmdvmnTFaL6s4ic7X68N0dY9jnwwcL98=",
	1901: "CusHY#00130001#6I1eeoSqDdjA7eXPDrsWBbdM-VxVhveQYiG1oNfNSt0=",
}

SYSTEM_VERSION_HEX = {
	2000: "7147e1386c9b6c15d8f14e6ed68c4b9a7f28fb9b",
	2001: "0b2540e5cd7498dd61f6caeca5136c73d9b1d21a",
	2010: "fa9b24a1d97b9adf5fe462f7f0ee97e6ed6294d0",
	2011: "9ffad64d79dd150490201461bdf66c8db963f57d",
	2015: "0605c36a7aa2535fb8989a0d133a0b96b0d97a12"
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
	1600: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 16.2.0.0)",
	1601: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 16.2.0.0)",
	1602: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 16.2.0.0)",
	1603: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 16.2.0.0)",
	1610: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 16.2.0.0)",
	1700: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 17.5.0.0)",
	1701: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 17.5.0.0)",
	1800: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 18.3.0.0)",
	1801: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 18.3.0.0)",
	1810: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 18.3.0.0)",
	1900: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 19.3.0.0)",
	1901: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 19.3.0.0)",
	2000: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2001: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2010: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2011: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2015: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
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
	1600: 16,
	1601: 16,
	1602: 16,
	1603: 16,
	1610: 16,
	1700: 17,
	1701: 17,
	1800: 17,
	1801: 17,
	1810: 17,
	1900: 19,
	1901: 19,
	2000: 20,
	2001: 20,
	2010: 20,
	2011: 20,
	2015: 20,
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
	1600: 7,
	1601: 7,
	1602: 7,
	1603: 7,
	1610: 7,
	1700: 7,
	1701: 7,
	1800: 7,
	1801: 7,
	1810: 7,
	1900: 7,
	1901: 7,
	2000: 8,
	2001: 8,
	2010: 8,
	2011: 8,
	2015: 8,
}

LATEST_VERSION = 2015


CLIENT_ID_SCSI = 0x146C8AC7B8A0DB52
CLIENT_ID_ER = 0x16E96F76850156D1
CLIENT_ID_ATUM = 0x3117B250CAB38F45
CLIENT_ID_ESHOP = 0x41F4A6491028E3C4
CLIENT_ID_BCAT = 0x67BF9945B45248C6
CLIENT_ID_SATA = 0x6AC5A6873FE5F68C
CLIENT_ID_ACCOUNT_APPLET = 0x75FE236362FF5F8B
CLIENT_ID_ACCOUNT = 0x81333C548B2E876D
CLIENT_ID_NPNS = 0x83B72B05DC3278D7
CLIENT_ID_BAAS = 0x8F849B5D34778D8E
CLIENT_ID_BEACH = 0x93AF0ACB26258DE9
CLIENT_ID_SPROFILE = 0xBAD8156F44AC935A
CLIENT_ID_DRAGONS = 0xD5B6CAC2C1514C56
CLIENT_ID_SCSI_POLICY = 0xD98185ACB55994B4
CLIENT_ID_PCTL = 0xDC656EA03B63CF68
CLIENT_ID_PREPO = 0xDF51C436BC01C437
CLIENT_ID_PENNE = 0xE58171FE439390CE


PRELOADED_DEVICE_TOKENS = [
	CLIENT_ID_BAAS,
	CLIENT_ID_PCTL,
	CLIENT_ID_BEACH,
	CLIENT_ID_PREPO,
	CLIENT_ID_ER,
	CLIENT_ID_PENNE,
	CLIENT_ID_ACCOUNT,
	CLIENT_ID_ACCOUNT_APPLET,
	CLIENT_ID_SCSI,
	CLIENT_ID_DRAGONS,
	CLIENT_ID_SPROFILE
]

PRELOADED_EDGE_TOKENS = [
	(CLIENT_ID_BEACH, "akamai"),
	(CLIENT_ID_BCAT, "akamai"),
	(CLIENT_ID_SCSI_POLICY, "akamai"),
	(CLIENT_ID_SCSI, "akamai"),
	(CLIENT_ID_ESHOP, "akamai"),
	(CLIENT_ID_ATUM, "akamai"),
	(CLIENT_ID_ATUM, "fastly")
]


class DAuthError(Exception):
	UNAUTHORIZED_DEVICE = 4
	SYSTEM_UPDATE_REQUIRED = 7
	BANNED_DEVICE = 8
	INTERNAL_SERVER_ERROR = 9
	GENERIC = 14
	CHALLENGE_EXPIRED = 15
	WRONG_MAC = 16
	BROKEN_DEVICE = 17
	
	def __init__(self, response):
		self.response = response
		self.code = int(response.json["errors"][0]["code"])
		self.message = response.json["errors"][0]["message"]
	
	def __str__(self):
		return self.message


class DAuthClient:
	def __init__(self, keys):
		self.keys = keys
		
		self.request_callback = http.request
		
		ca = resources.certificate("Nintendo_CA_G3.der")
		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		
		self.host = "dauth-lp1.ndas.srv.nintendo.net"
		
		self.power_state = "FA"
		self.region = 1

		self.system_version = LATEST_VERSION
		self.user_agent = USER_AGENT[self.system_version]
		self.system_version_hash = SYSTEM_VERSION_HEX[self.system_version]
		self.key_generation = KEY_GENERATION[self.system_version]
		self.api_version = API_VERSION[self.system_version]
		
	def set_request_callback(self, callback): self.request_callback = callback
	
	def set_context(self, context): self.context = context
	def set_certificate(self, cert, key): self.context.set_certificate(cert, key)
	
	def set_power_state(self, state): self.power_state = state
	def set_platform_region(self, region): self.region = region
	
	def set_host(self, host): self.host = host
	
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version: %i" %version)
		self.system_version = version
		self.user_agent = USER_AGENT[version]
		self.key_generation = KEY_GENERATION[version]
		self.api_version = API_VERSION[version]
		if self.api_version < 8:
			self.system_version_hash = SYSTEM_VERSION_DIGEST[version]
		else:
			self.system_version_hash = SYSTEM_VERSION_HEX[version]
		
	async def request(self, req):
		if self.system_version < 1800:
			req.headers["Host"] = self.host
			req.headers["User-Agent"] = self.user_agent
			req.headers["Accept"] = "*/*"
			req.headers["X-Nintendo-PowerState"] = self.power_state
			req.headers["Content-Length"] = 0
			req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		elif self.system_version < 2000:
			req.headers["Host"] = self.host
			req.headers["Accept"] = "*/*"
			req.headers["Content-Type"] = "application/x-www-form-urlencoded"
			req.headers["X-Nintendo-PowerState"] = self.power_state
			req.headers["Content-Length"] = 0
		else:
			req.headers["Host"] = self.host
			req.headers["Accept"] = "*/*"
			req.headers["User-Agent"] = self.user_agent
			if req.json:
				req.headers["Content-Type"] = "application/json"
			else:
				req.headers["Content-Type"] = "application/x-www-form-urlencoded"
			req.headers["X-Nintendo-PowerState"] = self.power_state
			req.headers["Content-Length"] = 0
		
		response = await self.request_callback(self.host, req, self.context)
		if response.json and "errors" in response.json:
			logger.error("DAuth server returned errors:")
			for error in response.json["errors"]:
				logger.error("  (%s) %s", error["code"], error["message"])
			raise DAuthError(response)
		response.raise_if_error()
		return response
		
	async def challenge(self):
		req = http.HTTPRequest.post("/v%i/challenge" %self.api_version)
		req.form = {
			"key_generation": self.key_generation
		}
		
		response = await self.request(req)
		return response.json
	
	async def request_token(self, client_id, vendor_id="akamai", *, edge_token):
		# This is a generic method to reduce code duplication between device_token and edge_token

		# On system version 20.0.0 and later, we use the new version of the API
		# Note: in this case, you probably want to use one of the preload functions instead,
		# to mimic the behavior of a real Switch.
		if self.system_version >= 2000:
			return await self.request_tokens([(client_id, vendor_id)], edge_tokens=edge_token)
		
		challenge = await self.challenge()
		data = base64.b64decode(challenge["data"] + "==", "-_")

		path = "/v%i/device_auth_token" %self.api_version
		if edge_token:
			path = "/v%i/edge_token" %self.api_version
		
		req = http.HTTPRequest.post(path)
		req.rawform = {
			"challenge": challenge["challenge"],
			"client_id": "%016x" %client_id,
			"ist": "true" if self.region == 2 else "false",
			"key_generation": self.key_generation,
			"system_version": self.system_version_hash
		}
		if self.api_version >= 7 and edge_token:
			req.rawform["vendor_id"] = vendor_id

		string = http.formencode(req.rawform, False)
		req.rawform["mac"] = self.calculate_mac(string, data)

		response = await self.request(req)
		return response.json
	
	async def request_tokens(self, token_requests, *, edge_tokens):
		# This is a generic method to reduce code duplication between device_tokens and edge_tokens

		if self.system_version < 2000:
			raise ValueError("This method is only available on system version 20.0.0 and above.")
		
		challenge = await self.challenge()
		data = base64.b64decode(challenge["data"] + "==", "-_")

		system_version = "00%02x%02x%02x" %(
			self.system_version // 100,
			(self.system_version // 10) % 10,
			self.system_version % 10
		)

		form = {
			"challenge": challenge["challenge"],
			"fw_revision": self.system_version_hash,
			"ist": "true" if self.region == 2 else "false",
			"key_generation": self.key_generation,
			"system_version": system_version,
			"token_requests": json.dumps(token_requests, separators=(",", ":"))
		}
		string = http.formencode(form, False)
		mac = self.calculate_mac(string, data)

		path = "/v%i/device_auth_tokens" %self.api_version
		if edge_tokens:
			path = "/v%i/edge_tokens" %self.api_version

		req = http.HTTPRequest.post(path)
		req.json = {
			"system_version": system_version,
			"fw_revision": self.system_version_hash,
			"ist": self.region == 2,
			"token_requests": token_requests,
			"key_generation": self.key_generation,
			"challenge": challenge["challenge"],
			"mac": mac
		}

		response = await self.request(req)
		return response.json
	
	async def device_token(self, client_id):
		return await self.request_token(client_id, edge_token=False)
	
	async def edge_token(self, client_id, vendor_id="akamai"):
		return await self.request_token(client_id, vendor_id, edge_token=True)
		
	async def device_tokens(self, client_ids):
		token_requests = [{"client_id": "%016x" %client_id} for client_id in client_ids]
		return await self.request_tokens(token_requests, edge_tokens=False)
	
	async def edge_tokens(self, token_requests):
		token_requests = [{"client_id": "%016x" %client_id, "vendor_id": vendor_id} for client_id, vendor_id in token_requests]
		return await self.request_tokens(token_requests, edge_tokens=True)
	
	async def preload_device_tokens(self):
		return await self.device_tokens(PRELOADED_DEVICE_TOKENS)
	
	async def preload_edge_tokens(self):
		return await self.edge_tokens(PRELOADED_EDGE_TOKENS)
		
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


class DAuthCache:
	def __init__(self, client, expiration=None):
		self.client = client
		self.expiration = expiration

		self.device_tokens = {}
		self.edge_tokens = {}
	
	async def device_token(self, client_id):
		now = time.time()
		if client_id in self.device_tokens and self.device_tokens[client_id][1] > now:
			return self.device_tokens[client_id][0]
		
		if client_id in PRELOADED_DEVICE_TOKENS:
			response = await self.client.preload_device_tokens()
		else:
			response = await self.client.device_tokens([client_id])
		
		for result in response["results"]:
			if self.expiration is not None:
				expiration = now + self.expiration
			else:
				expiration = now + result["expires_in"]
			self.device_tokens[int(result["client_id"], 16)] = (result["device_auth_token"], expiration)

		return self.device_tokens[client_id][0]

	async def edge_token(self, client_id, vendor_id="akamai"):
		now = time.time()
		key = (client_id, vendor_id)
		if key in self.edge_tokens and self.edge_tokens[key][1] > now:
			return self.edge_tokens[key][0]
		
		if key in PRELOADED_EDGE_TOKENS:
			response = await self.client.preload_edge_tokens()
		else:
			response = await self.client.edge_tokens([key])
		
		for result in response["results"]:
			result_key = (int(result["client_id"], 16), result["vendor_id"])
			if self.expiration is not None:
				expiration = now + self.expiration
			else:
				expiration = now + result["expires_in"]
			self.edge_tokens[result_key] = (result["dtoken"], expiration)
		
		return self.edge_tokens[key][0]
