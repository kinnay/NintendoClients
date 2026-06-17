
from anynet import http, tls
from nintendo import resources
import datetime
import secrets
import base64

import logging
logger = logging.getLogger(__name__)


MEDIA_TYPE_SYSTEM = 0
MEDIA_TYPE_DIGITAL = 1
MEDIA_TYPE_CARTRIDGE = 2


def b64decode(text: str) -> bytes:
	text = text.replace(".", "+").replace("-", "/").replace("*", "=")
	return base64.b64decode(text)

def b64encode(text: str | bytes) -> str:
	# Convert to bytes if necessary
	if isinstance(text, str):
		text = text.encode()
	
	text = base64.b64encode(text).decode()
	return text.replace("+", ".").replace("/", "-").replace("=", "*")

def decode_form(form: dict[str, str]) -> dict[str, bytes]:
	return {key: b64decode(value) for key, value in form.items()}

def encode_form(form: dict[str, str | bytes]) -> dict[str, str]:
	return {key: b64encode(value) for key, value in form.items()}

def parse_date(text: str) -> datetime.datetime:
	return datetime.datetime.strptime(text, "%Y%m%d%H%M%S")


# Known error codes:
#	001: success
#   109: missing or malformed parameter in request
#   110: game server is no longer available
#   119: fpd version is outdated
#   121: device certificate is invalid
#   122: uid hmac is invalid
#   125: game id is invalid

class NASCError(Exception):
	status_code: int
	return_code: int | None
	retry: bool
	datetime: datetime.datetime

	def __init__(self, status_code: int, form: dict[str, bytes]):
		self.status_code = status_code
		
		returncd = form["returncd"].decode()
		self.return_code = None if returncd == "null" else int(returncd)
		self.retry = bool(int(form["retry"].decode()))
		self.datetime = parse_date(form["datetime"].decode())
	
	def __str__(self) -> str:
		if self.return_code is None:
			return "NASC request failed with error code null"
		return "NASC request failed with error code %i" %self.return_code


class LoginResponse:
	host: str
	port: int
	token: str
	datetime: datetime.datetime

	def __init__(self, form: dict[str, bytes]):
		host, port = form["locator"].decode().split(":")
		
		self.host = host
		self.port = int(port)
		self.token = b64encode(form["token"])
		self.datetime = parse_date(form["datetime"].decode())


class NASCClient:
	_url: str

	_context: tls.TLSContext

	_sdk_version_major: int
	_sdk_version_minor: int

	_title_id: int | None
	_title_version: int | None
	_product_code: str
	_maker_code: str
	_media_type: int
	_rom_id: bytes | None

	_serial_number: str | None
	_mac_address: str | None
	_fcd_cert: bytes | None
	_device_name: str
	_unit_code: str

	_bss_id: str
	_ap_info: str

	_region: int
	_language: int

	_pid: int | None
	_pid_hmac: str | None
	_password: str | None

	_fpd_version: int
	_environment: str

	def __init__(self):
		self._url = "nasc.nintendowifi.net"

		ca = resources.certificate("Nintendo_CA_G3.der")
		cert = resources.certificate("CTR_Common_Prod_1.der")
		key = resources.private_key("CTR_Common_Prod_1.key")

		self._context = tls.TLSContext()
		self._context.set_authority(ca)
		self._context.set_certificate(cert, key)
		
		self._sdk_version_major = 0
		self._sdk_version_minor = 0
		
		self._title_id = None
		self._title_version = None
		self._product_code = "----"
		self._maker_code = "00"
		self._media_type = MEDIA_TYPE_SYSTEM
		self._rom_id = None
		
		self._serial_number = None
		self._mac_address = None
		self._fcd_cert = None
		self._device_name = ""
		self._unit_code = "2"
		
		self._bss_id = secrets.token_hex(6)
		self._ap_info = "01:0000000000"
		
		self._region = 3
		self._language = 2
		
		self._pid = None
		self._pid_hmac = None
		self._password = None
		
		self._fpd_version = 16
		self._environment = "L1"
	
	def set_context(self, context: tls.TLSContext) -> None:
		self._context = context
	
	def set_url(self, url: str) -> None:
		self._url = url
	
	def set_sdk_version(self, major_version: int, minor_version: int) -> None:
		self._sdk_major_version = major_version
		self._sdk_minor_version = minor_version
	
	def set_title(
		self, title_id: int, title_version: int, product_code: str = "----",
		maker_code: str = "00", media_type: int = MEDIA_TYPE_SYSTEM,
		rom_id: bytes | None = None
	):
		if media_type == MEDIA_TYPE_CARTRIDGE and rom_id is None:
			raise ValueError("Rom ID is required for cartridge media type")
		
		self._title_id = title_id
		self._title_version = title_version
		self._product_code = product_code
		self._maker_code = maker_code
		self._media_type = media_type
		self._rom_id = rom_id
	
	def set_device(
		self, serial_number: str, mac_address: str, fcd_cert: bytes,
		name: str = "", unit_code: str = "2"
	) -> None:
		self._serial_number = serial_number
		self._mac_address = mac_address
		self._fcd_cert = fcd_cert
		self._device_name = name
		self._unit_code = unit_code
	
	def set_network(self, bss_id: str, ap_info: str) -> None:
		self._bss_id = bss_id
		self._ap_info = ap_info
	
	def set_locale(self, region: int, language: int) -> None:
		self._region = region
		self._language = language
	
	def set_user(self, pid: int, pid_hmac: str) -> None:
		self._pid = pid
		self._pid_hmac = pid_hmac
		self._password = None
		
	def set_password(self, password: str) -> None:
		self._pid = None
		self._pid_hmac = None
		self._password = password
	
	def set_fpd_version(self, version: int) -> None:
		self._fpd_version = version
	
	def set_environment(self, environment: str) -> None:
		self._environment = environment

	async def request(self, req: http.HTTPRequest) -> http.HTTPResponse:
		# Apply Nintendo's custom base64 encoding
		req.form = encode_form(req.form)
		
		# Must manually decode form here since server doesn't return correct
		# content-type
		response = await http.request(self._url, req, self._context)
		response.form = decode_form(http.formdecode(response.text))
		
		return_code = response.form["returncd"].decode()
		if return_code == "null" or int(return_code) != 1:
			raise NASCError(response.status_code, response.form)
		
		return response

	async def login(
		self, game_server_id: int, nickname: str = ""
	) -> LoginResponse:
		if self._title_id is None:
			raise ValueError("Please configure the title (set_title)")
		if self._serial_number is None:
			raise ValueError("Please configure the device (set_device)")
		if self._pid is None and self._password is None:
			raise ValueError(
				"Please configure a user id or password " \
				"(set_user / set_password)"
			)
		
		req = http.HTTPRequest.post("/ac")
		req.headers["Host"] = self._url
		req.headers["X-GameId"] = f"{game_server_id:08X}"
		req.headers["User-Agent"] = f"CTR FPD/{self._fpd_version:04X}"
		
		# The real 3DS seems to add this header twice for some reason
		req.headers.add("Content-Type", "application/x-www-form-urlencoded")
		req.headers.add("Content-Type", "application/x-www-form-urlencoded")

		now = datetime.datetime.now()
		device_time = now.strftime("%y%m%d%H%M%S")

		req.form = {}
		req.form["gameid"] = f"{game_server_id:08X}"
		req.form["sdkver"] = \
			f"{self._sdk_version_major:03}{self._sdk_version_minor:03}"
		req.form["titleid"] = f"{self._title_id:016X}"
		req.form["gamecd"] = self._product_code
		req.form["gamever"] = f"{self._title_version:04X}"
		req.form["mediatype"] = str(self._media_type)
		if self._media_type == MEDIA_TYPE_CARTRIDGE:
			req.form["romid"] = self._rom_id
		req.form["makercd"] = self._maker_code
		req.form["unitcd"] = self._unit_code
		req.form["macadr"] = self._mac_address
		req.form["bssid"] = self._bss_id
		req.form["apinfo"] = self._ap_info
		req.form["fcdcert"] = self._fcd_cert
		req.form["devname"] = self._device_name.encode("utf-16-le")
		req.form["servertype"] = self._environment
		req.form["fpdver"] = f"{self._fpd_version:04X}"
		req.form["devtime"] = device_time
		req.form["lang"] = f"{self._language:02X}"
		req.form["region"] = f"{self._region:02X}"
		req.form["csnum"] = self._serial_number
		if self._pid_hmac is not None:
			req.form["uidhmac"] = self._pid_hmac
			req.form["userid"] = str(self._pid)
		else:
			req.form["passwd"] = self._password
		req.form["action"] = "LOGIN"
		req.form["ingamesn"] = nickname
		
		response = await self.request(req)
		return LoginResponse(response.form)
