
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from anynet import tls, http
from nintendo import resources
import struct
import base64

import logging
logger = logging.getLogger(__name__)


RSA_MODULUS =  int(
	"2903599220185509629948246004681271806662185201109683699434876284"
	"9306378942456577312580648895443616535088601867223713942187399041"
	"4854872772034425863387471719375473684104853507768450203982749294"
	"8967945831738920699512732919046223059402955082098739033920491649"
	"6879108565068863591362496844602988110766097564477545097467537357"
	"3183749964356608012071405755940871989007021731074728723470759285"
	"8155278592486462922448753256166071381157786436864032235809243318"
	"2591089355065715995209202752330511548478896205428626608544326862"
	"4782505679727111312756904637828438785474471375120478991907979820"
	"98870089661523253199182993983393803812441"
)

RSA_EXPONENT = 65537


USER_AGENT = {
	 900: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 901: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 910: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 920: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	1000: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1001: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1002: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1003: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1004: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1010: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1011: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1020: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1100: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 11.4.0.0; Add-on 11.4.0.0)",
	1101: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 11.4.0.0; Add-on 11.4.0.0)",
	1200: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1201: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1202: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1203: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1210: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 12.3.0.0; Add-on 12.3.0.0)",
	1300: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.3.0.0; Add-on 13.3.0.0)",
	1310: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1320: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1321: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 13.4.0.0; Add-on 13.4.0.0)",
	1400: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1410: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1411: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1412: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 14.3.0.0; Add-on 14.3.0.0)",
	1500: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)",
	1501: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 15.3.0.0; Add-on 15.3.0.0)",
	1600: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1601: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1602: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1603: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1610: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 16.2.0.0; Add-on 16.2.0.0)",
	1700: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 17.5.0.0; Add-on 17.5.0.0)",
	1701: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 17.5.0.0; Add-on 17.5.0.0)",
	1800: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 18.3.0.0; Add-on 18.3.0.0)",
	1801: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 18.3.0.0; Add-on 18.3.0.0)",
	1810: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 18.3.0.0; Add-on 18.3.0.0)",
	1900: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 19.3.0.0; Add-on 19.3.0.0)",
	1901: "libcurl (nnHttp; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 19.3.0.0; Add-on 19.3.0.0)",
}

API_VERSION = {
	 900: 3,
	 901: 3,
	 910: 3,
	 920: 3,
	1000: 3,
	1001: 3,
	1002: 3,
	1003: 3,
	1004: 3,
	1010: 3,
	1011: 3,
	1020: 3,
	1100: 3,
	1101: 3,
	1200: 3,
	1201: 3,
	1202: 3,
	1203: 3,
	1210: 3,
	1300: 3,
	1310: 3,
	1320: 3,
	1321: 3,
	1400: 3,
	1410: 3,
	1411: 3,
	1412: 3,
	1500: 4,
	1501: 4,
	1600: 4,
	1601: 4,
	1602: 4,
	1603: 4,
	1610: 4,
	1700: 4,
	1701: 4,
	1800: 4,
	1801: 4,
	1810: 4,
	1900: 5,
	1901: 5,
}

LATEST_VERSION = 1901


class AAuthError(Exception):
	DEVICE_TOKEN_EXPIRED = 103
	ROMID_BANNED = 105
	UNAUTHORIZED_APPLICATION = 106
	SERVICE_CLOSED = 109
	APPLICATION_UPDATE_REQUIRED = 111
	INTERNAL_SERVER_ERROR = 112
	GENERIC = 118
	REGION_MISMATCH = 121
	
	def __init__(self, response):
		self.response = response
		self.code = int(response.json["errors"][0]["code"])
		self.message = response.json["errors"][0]["message"]
	
	def __str__(self):
		return self.message


class AAuthClient:
	def __init__(self):
		self.request_callback = http.request
		
		ca = resources.certificate("CACERT_NINTENDO_CA_G3.der")
		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		
		self.host = "aauth-lp1.ndas.srv.nintendo.net"
		self.power_state = "FA"

		self.system_version = LATEST_VERSION
		self.user_agent = USER_AGENT[self.system_version]
		self.api_version = API_VERSION[self.system_version]
	
	def set_request_callback(self, callback): self.request_callback = callback
	def set_context(self, context): self.context = context
	
	def set_host(self, host): self.host = host
	def set_power_state(self, state): self.power_state = state
	
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		self.system_version = version
		self.user_agent = USER_AGENT[version]
		self.api_version = API_VERSION[version]
	
	async def request(self, req, use_power_state):
		if self.system_version < 1800:
			req.headers["Host"] = self.host
			req.headers["User-Agent"] = self.user_agent
			req.headers["Accept"] = "*/*"
			if use_power_state:
				req.headers["X-Nintendo-PowerState"] = self.power_state
			req.headers["Content-Length"] = 0
			req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		else:
			req.headers["Host"] = self.host
			req.headers["Accept"] = "*/*"
			req.headers["Content-Type"] = "application/x-www-form-urlencoded"	
			if use_power_state:
				req.headers["X-Nintendo-PowerState"] = self.power_state
			req.headers["Content-Length"] = 0
		
		response = await self.request_callback(self.host, req, self.context)
		if response.json and "errors" in response.json:
			logger.error("AAuth server returned errors:")
			for error in response.json["errors"]:
				logger.error("  (%s) %s", error["code"], error["message"])
			raise AAuthError(response)
		response.raise_if_error()
		return response
	
	def verify_ticket(self, ticket, title_id):
		# Verify ticket, in case someone accidentally
		# provides the wrong ticket
		if len(ticket) != 0x2C0:
			raise ValueError("Ticket has unexpected size")
		if struct.unpack_from("<I", ticket)[0] != 0x10004:
			raise ValueError("Ticket has invalid signature type")
		if struct.unpack_from(">Q", ticket, 0x2A0)[0] != title_id:
			raise ValueError("Ticket has different title id")
		if struct.unpack_from(">Q", ticket, 0x2A8)[0] != ticket[0x285]:
			raise ValueError("Ticket has inconsistent master key revision")
	
	def verify_token(self, token):
		# Just a basic check, to make sure that people do not
		# accidentally pass a ticket instead of a JWT
		if not isinstance(token, str) or token.count(".") != 2:
			raise ValueError("Cert must contain a valid JWT")
	
	async def get_time(self):
		req = http.HTTPRequest.get("/v1/time")
		req.headers["Host"] = self.host
		req.headers["Accept"] = "*/*"
		
		response = await http.request(self.host, req, self.context)
		response.raise_if_error()
		
		time = int(response.headers["X-NINTENDO-UNIXTIME"])
		ip = response.headers["X-NINTENDO-GLOBAL-IP"]
		return time, ip
	
	async def challenge(self, device_token):
		param_name = "&device_auth_token" if self.system_version < 1800 else "device_auth_token"

		req = http.HTTPRequest.post("/v%i/challenge" %self.api_version)
		req.rawform = {
			param_name: device_token
		}
		
		response = await self.request(req, False)
		return response.json

	# Warning: do not use auth_nocert on a production server.
	# It will immediately ban your Switch.
	async def auth_nocert(self, title_id, title_version, device_token):
		auth_type = "media_type" if self.api_version < 5 else "auth_type"

		req = http.HTTPRequest.post("/v%i/application_auth_token" %self.api_version)
		req.form = {
			"application_id": "%016x" %title_id,
			"application_version": "%08x" %title_version,
			"device_auth_token": device_token,
			auth_type: "NO_CERT"
		}
		
		response = await self.request(req, True)
		return response.json

	async def auth_system(self, title_id, title_version, device_token):
		auth_type = "media_type" if self.api_version < 5 else "auth_type"

		req = http.HTTPRequest.post("/v%i/application_auth_token" %self.api_version)
		req.form = {
			"application_id": "%016x" %title_id,
			"application_version": "%08x" %title_version,
			"device_auth_token": device_token,
			auth_type: "SYSTEM"
		}

		response = await self.request(req, True)
		return response.json

	async def auth_digital(self, title_id, title_version, device_token, cert):
		auth_type = "media_type" if self.api_version < 5 else "auth_type"

		req = http.HTTPRequest.post("/v%i/application_auth_token" %self.api_version)
		req.form = {
			"application_id": "%016x" %title_id,
			"application_version": "%08x" %title_version,
			"device_auth_token": device_token,
			auth_type: "DIGITAL"
		}
		
		if self.api_version == 3:
			self.verify_ticket(cert, title_id)
			
			plain_key = get_random_bytes(16)
			
			aes = AES.new(plain_key, AES.MODE_CBC, iv=bytes(16))
			encrypted_ticket = aes.encrypt(pad(cert, 16))
			
			rsa_key = RSA.construct((RSA_MODULUS, RSA_EXPONENT))
			rsa = PKCS1_OAEP.new(rsa_key, SHA256)
			encrypted_key = rsa.encrypt(plain_key)
		
			req.form["cert"] = base64.b64encode(encrypted_ticket, b"-_").decode().rstrip("=")
			req.form["cert_key"] = base64.b64encode(encrypted_key, b"-_").decode().rstrip("=")
		
		elif self.api_version >= 4:
			self.verify_token(cert)
			
			req.form["cert"] = cert
		
		response = await self.request(req, True)
		return response.json

	async def auth_gamecard(self, title_id, title_version, device_token, cert, gvt, challenge=None, challenge_src=None):
		auth_type = "media_type" if self.api_version < 5 else "auth_type"

		req = http.HTTPRequest.post("/v%i/application_auth_token" %self.api_version)
		req.form = {
			"application_id": "%016x" %title_id,
			"application_version": "%08x" %title_version,
			"device_auth_token": device_token,
			auth_type: "GAMECARD",
			"gvt": base64.b64encode(gvt, b"-_").decode().rstrip("="),
			"cert": base64.b64encode(cert, b"-_").decode().rstrip("=")
		}

		if self.api_version >= 5:
			req.form["challenge"] = challenge
			req.form["challenge_src"] = challenge_src

		response = await self.request(req, True)
		return response.json
