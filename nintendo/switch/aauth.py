
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

from anynet import tls, http
from nintendo import resources
from typing import Any, Awaitable, Callable

import struct
import base64

import logging
logger = logging.getLogger(__name__)


type RequestCallback = Callable[..., Awaitable[http.HTTPResponse]]


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
	2000: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2001: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2010: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2011: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2015: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2020: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2030: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2040: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2050: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 20.5.4.0)",
	2100: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 21.4.0.0)",
	2101: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 21.4.0.0)",
	2110: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 21.4.0.0)",
	2120: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 21.4.0.0)",
	2200: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 22.2.0.0)",
	2210: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 22.2.0.0)",
	2250: "libcurl (nnDauth; 16f4553f-9eee-4e39-9b61-59bc7c99b7c8; SDK 22.2.0.0)",
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
	2000: 5,
	2001: 5,
	2010: 5,
	2011: 5,
	2015: 5,
	2020: 5,
	2030: 5,
	2040: 5,
	2050: 5,
	2100: 5,
	2101: 5,
	2110: 5,
	2120: 5,
	2200: 5,
	2210: 5,
	2250: 5,
}

LATEST_VERSION = 2250


class AAuthError(Exception):
	DEVICE_TOKEN_EXPIRED = 103
	ROMID_BANNED = 105
	UNAUTHORIZED_APPLICATION = 106
	SERVICE_CLOSED = 109
	APPLICATION_UPDATE_REQUIRED = 111
	INTERNAL_SERVER_ERROR = 112
	GENERIC = 118
	REGION_MISMATCH = 121

	response: http.HTTPResponse
	code: int
	message: str
	
	def __init__(self, response: http.HTTPResponse):
		self.response = response
		self.code = int(response.json["errors"][0]["code"])
		self.message = response.json["errors"][0]["message"]
	
	def __str__(self) -> str:
		return self.message


class AAuthClient:
	_request_callback: RequestCallback

	_context: tls.TLSContext
	_context_overridden: bool

	_host_overridden: bool

	_power_state: str

	_system_version: int
	_user_agent: str
	_api_version: int

	def __init__(self):
		self._request_callback = http.request
		
		self._context = tls.TLSContext()
		self._context_overridden = False
		
		self._host_overridden = False

		self._power_state = "FA"

		self.set_system_version(LATEST_VERSION)

	def set_request_callback(self, callback: RequestCallback) -> None:
		self._request_callback = callback

	def set_context(self, context: tls.TLSContext) -> None:
		self._context = context
		self._context_overridden = True
	
	def set_certificate(
		self, cert: tls.TLSCertificate, key: tls.TLSPrivateKey
	) -> None:
		self._context.set_certificate(cert, key)
	
	def set_host(self, host: str) -> None:
		self._host = host
		self._host_overridden = True
	
	def set_power_state(self, state: str) -> None:
		self._power_state = state
	
	def set_system_version(self, version: int) -> None:
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		
		self._system_version = version
		self._user_agent = USER_AGENT[version]
		self._api_version = API_VERSION[version]

		if version >= 2000:
			caname = "Nintendo_Root_CA_G4.der"
			host = "aauth.hac.lp1.ndas.srv.nintendo.net"
		else:
			caname = "Nintendo_CA_G3.der"
			host = "aauth-lp1.ndas.srv.nintendo.net"
		
		if not self._context_overridden:
			ca = resources.certificate(caname)
			self._context.set_authority(ca)
		
		if not self._host_overridden:
			self._host = host
	
	async def _request(
		self, req: http.HTTPRequest, use_power_state: bool
	) -> http.HTTPResponse:
		if self._system_version < 1800:
			req.headers["Host"] = self._host
			req.headers["User-Agent"] = self._user_agent
			req.headers["Accept"] = "*/*"
			if use_power_state:
				req.headers["X-Nintendo-PowerState"] = self._power_state
			req.headers["Content-Length"] = 0
			req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		elif self._system_version < 2000:
			req.headers["Host"] = self._host
			req.headers["Accept"] = "*/*"
			req.headers["Content-Type"] = "application/x-www-form-urlencoded"	
			if use_power_state:
				req.headers["X-Nintendo-PowerState"] = self._power_state
			req.headers["Content-Length"] = 0
		else:
			req.headers["Host"] = self._host
			req.headers["Accept"] = "*/*"
			req.headers["User-Agent"] = self._user_agent
			req.headers["Content-Type"] = "application/x-www-form-urlencoded"
			if use_power_state:
				req.headers["X-Nintendo-PowerState"] = self._power_state
			req.headers["Content-Length"] = 0
		
		response = await self._request_callback(self._host, req, self._context)
		if response.json and "errors" in response.json:
			logger.error("AAuth server returned errors:")
			for error in response.json["errors"]:
				logger.error("  (%s) %s", error["code"], error["message"])
			raise AAuthError(response)
		response.raise_if_error()
		return response
	
	def _verify_ticket(self, ticket: bytes, title_id: int) -> None:
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
	
	async def get_time(self) -> tuple[int, str]:
		req = http.HTTPRequest.get("/v1/time")
		req.headers["Host"] = self._host
		req.headers["Accept"] = "*/*"
		
		response = await http.request(self._host, req, self._context)
		response.raise_if_error()
		
		time = int(response.headers["X-NINTENDO-UNIXTIME"])
		ip = response.headers["X-NINTENDO-GLOBAL-IP"]
		return time, ip
	
	async def challenge(self, device_token: str) -> Any:
		param_name = "&device_auth_token" if self._system_version < 1800 \
			else "device_auth_token"

		req = http.HTTPRequest.post(f"/v{self._api_version}/challenge")
		req.rawform = {
			param_name: device_token
		}
		
		response = await self._request(req, False)
		return response.json

	async def auth_nocert(
		self, title_id: int, title_version: int, device_token: str
	) -> Any:
		"""
		WARNING: do not use auth_nocert on a production server. It will
		immediately ban your Switch.
		"""

		auth_type = "media_type" if self._api_version < 5 else "auth_type"

		req = http.HTTPRequest.post(
			f"/v{self._api_version}/application_auth_token"
		)
		req.form = {
			"application_id": f"{title_id:016x}",
			"application_version": f"{title_version:08x}",
			"device_auth_token": device_token,
			auth_type: "NO_CERT"
		}
		
		response = await self._request(req, True)
		return response.json

	async def auth_system(
		self, title_id: int, title_version: int, device_token: str
	) -> Any:
		auth_type = "media_type" if self._api_version < 5 else "auth_type"

		req = http.HTTPRequest.post(
			f"/v{self._api_version}/application_auth_token"
		)
		req.form = {
			"application_id": f"{title_id:016x}",
			"application_version": f"{title_version:08x}",
			"device_auth_token": device_token,
			auth_type: "SYSTEM"
		}

		response = await self._request(req, True)
		return response.json

	async def auth_digital(
		self, title_id: int, title_version: int, device_token: str,
		cert: bytes | str
	) -> Any:
		auth_type = "media_type" if self._api_version < 5 else "auth_type"

		req = http.HTTPRequest.post(
			f"/v{self._api_version}/application_auth_token"
		)
		req.form = {
			"application_id": f"{title_id:016x}",
			"application_version": f"{title_version:08x}",
			"device_auth_token": device_token,
			auth_type: "DIGITAL"
		}
		
		if self._api_version == 3:
			if not isinstance(cert, bytes):
				raise TypeError(
					"'cert' must be a bytes object in the selected system " \
					"version"
				)
			
			self._verify_ticket(cert, title_id)
			
			plain_key = get_random_bytes(16)
			
			aes = AES.new(plain_key, AES.MODE_CBC, iv=bytes(16))
			encrypted_ticket = aes.encrypt(pad(cert, 16))
			
			rsa_key = RSA.construct((RSA_MODULUS, RSA_EXPONENT))
			rsa = PKCS1_OAEP.new(rsa_key, SHA256)
			encrypted_key = rsa.encrypt(plain_key)
		
			req.form["cert"] = \
				base64.b64encode(encrypted_ticket, b"-_").decode().rstrip("=")
			req.form["cert_key"] = \
				base64.b64encode(encrypted_key, b"-_").decode().rstrip("=")
		
		elif self._api_version >= 4:
			if not isinstance(cert, str) or cert.count(".") != 2:
				raise ValueError("'cert' must contain a valid JWT")
			
			req.form["cert"] = cert
		
		response = await self._request(req, True)
		return response.json

	async def auth_gamecard(
		self, title_id: int, title_version: int, device_token: str, cert: bytes,
		gvt: bytes, challenge: str | None = None,
		challenge_src: str | None = None
	):
		auth_type = "media_type" if self._api_version < 5 else "auth_type"

		req = http.HTTPRequest.post(
			f"/v{self._api_version}/application_auth_token"
		)
		req.form = {
			"application_id": f"{title_id:016x}",
			"application_version": f"{title_version:08x}",
			"device_auth_token": device_token,
			auth_type: "GAMECARD",
			"gvt": base64.b64encode(gvt, b"-_").decode().rstrip("="),
			"cert": base64.b64encode(cert, b"-_").decode().rstrip("=")
		}

		if self._api_version >= 5:
			req.form["challenge"] = challenge
			req.form["challenge_src"] = challenge_src

		response = await self._request(req, True)
		return response.json
