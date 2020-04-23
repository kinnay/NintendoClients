
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from nintendo.common.http import HTTPRequest, HTTPClient
from nintendo.switch import b64encode, b64decode
import struct

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
	900:  "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	901:  "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	910:  "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	920:  "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	1000: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1001: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)"
}

LATEST_VERSION = 1001


class AAuthError(Exception): pass


class AAuthClient:
	def __init__(self):
		self.client = HTTPClient()
		
		self.url = "aauth-lp1.ndas.srv.nintendo.net"
		
		self.user_agent = USER_AGENT[LATEST_VERSION]
		self.power_state = "FA"
	
	def set_url(self, url): self.url = url
	def set_user_agent(self, agent): self.user_agent = agent
	def set_power_state(self, state): self.power_state = state
	
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		self.user_agent = USER_AGENT[version]
	
	def request(self, req, use_power_state):
		req.headers["Host"] = self.url
		req.headers["User-Agent"] = self.user_agent
		req.headers["Accept"] = "*/*"
		if use_power_state:
			req.headers["X-Nintendo-PowerState"] = self.power_state
		req.headers["Content-Length"] = 0
		req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		
		response = self.client.request(req, True)
		if response.status != 200:
			if response.json is not None:
				logger.error("AAuth request returned errors:")
				for error in response.json["errors"]:
					logger.error("  (%s) %s", error["code"], error["message"])
				raise AAuthError("AAuth request failed: %s" %response.json["errors"][0]["message"])
			else:
				logger.error("DAuth request returned status code %i", response.status)
				raise AAuthError("AAuth request failed with status %i" %response.status)
		return response
		
	def verify_ticket(self, ticket, title_id):
		if len(ticket) != 0x2C0:
			raise ValueError("Ticket has unexpected size")
		if struct.unpack_from("<I", ticket)[0] != 0x10004:
			raise ValueError("Ticket has invalid signature type")
		if struct.unpack_from(">Q", ticket, 0x2A0)[0] != title_id:
			raise ValueError("Ticket has different title id")
		if struct.unpack_from(">Q", ticket, 0x2A8)[0] != ticket[0x285]:
			raise ValueError("Ticket has inconsistent master key revision")
		
	def auth_digital(self, title_id, title_version, device_token, ticket):
		self.verify_ticket(ticket, title_id)
		
		plain_key = get_random_bytes(16)
		
		aes = AES.new(plain_key, AES.MODE_CBC, iv=bytes(16))
		encrypted_ticket = aes.encrypt(pad(ticket, 16))
		
		rsa_key = RSA.construct((RSA_MODULUS, RSA_EXPONENT))
		rsa = PKCS1_OAEP.new(rsa_key, SHA256)
		encrypted_key = rsa.encrypt(plain_key)
	
		req = HTTPRequest.post("/v3/application_auth_token")
		req.form["application_id"] = "%016x" %title_id
		req.form["application_version"] = "%08x" %title_version
		req.form["device_auth_token"] = device_token
		req.form["media_type"] = "DIGITAL"
		
		req.form["cert"] = b64encode(encrypted_ticket)
		req.form["cert_key"] = b64encode(encrypted_key)
	
		response = self.request(req, True)
		return response.json
