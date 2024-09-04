
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


def b64decode(text):
	text = text.replace(".", "+").replace("-", "/").replace("*", "=")
	return base64.b64decode(text)

def b64encode(text):
	# Convert to bytes if necessary
	if isinstance(text, str):
		text = text.encode()
	
	text = base64.b64encode(text).decode()
	return text.replace("+", ".").replace("/", "-").replace("=", "*")

def decode_form(form):
	return {key: b64decode(value) for key, value in form.items()}

def encode_form(form):
	return {key: b64encode(value) for key, value in form.items()}

def parse_date(text):
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
	def __init__(self, status_code, form):
		self.status_code = status_code
		
		returncd = form["returncd"].decode()
		self.return_code = None if returncd == "null" else int(returncd)
		self.retry = bool(int(form["retry"].decode()))
		self.datetime = parse_date(form["datetime"].decode())
	
	def __str__(self):
		if self.return_code is None:
			return "NASC request failed with error code null"
		return "NASC request failed with error code %i" %self.return_code


class LoginResponse:
	def __init__(self):
		self.host = None
		self.port = None
		self.token = None
		self.datetime = None

	@classmethod
	def parse(cls, form):
		host, port = form["locator"].decode().split(":")
		
		inst = cls()
		inst.host = host
		inst.port = int(port)
		inst.token = b64encode(form["token"])
		inst.datetime = parse_date(form["datetime"].decode())
		return inst


class NASCClient:
	def __init__(self):
		self.url = "nasc.nintendowifi.net"

		ca = resources.certificate("CACERT_NINTENDO_CA_G3.der")
		cert = resources.certificate("ctr-common-1-cert.der")
		key = resources.private_key("ctr-common-1-key.der")

		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		self.context.set_certificate(cert, key)
		
		self.sdk_version_major = 0
		self.sdk_version_minor = 0
		
		self.title_id = None
		self.title_version = None
		self.product_code = "----"
		self.maker_code = "00"
		self.media_type = MEDIA_TYPE_SYSTEM
		self.rom_id = None
		
		self.serial_number = None
		self.mac_address = None
		self.fcd_cert = None
		self.device_name = ""
		self.unit_code = "2"
		
		self.bss_id = secrets.token_hex(6)
		self.ap_info = "01:0000000000"
		
		self.region = 3
		self.language = 2
		
		self.pid = None
		self.pid_hmac = None
		self.password = None
		
		self.fpd_version = 16
		self.environment = "L1"
	
	def set_context(self, context):
		self.context = context
	
	def set_url(self, url): self.url = url
	
	def set_sdk_version(self, major_version, minor_version):
		self.sdk_major_version = major_version
		self.sdk_minor_version = minor_version
	
	def set_title(
		self, title_id, title_version, product_code="----", maker_code="00",
		media_type=MEDIA_TYPE_SYSTEM, rom_id=None
	):
		if media_type == MEDIA_TYPE_CARTRIDGE and rom_id is None:
			raise ValueError("Rom ID is required for cartridge media type")
		
		self.title_id = title_id
		self.title_version = title_version
		self.product_code = product_code
		self.maker_code = maker_code
		self.media_type = media_type
		self.rom_id = rom_id
	
	def set_device(self, serial_number, mac_address, fcd_cert, name="", unit_code="2"):
		self.serial_number = serial_number
		self.mac_address = mac_address
		self.fcd_cert = fcd_cert
		self.device_name = name
		self.unit_code = unit_code
	
	def set_network(self, bss_id, ap_info):
		self.bss_id = bss_id
		self.ap_info = ap_info
	
	def set_locale(self, region, language):
		self.region = region
		self.language = language
	
	def set_user(self, pid, pid_hmac):
		self.pid = pid
		self.pid_hmac = pid_hmac
		self.password = None
		
	def set_password(self, password):
		self.pid = None
		self.pid_hmac = None
		self.password = password
	
	def set_fpd_version(self, version): self.fpd_version = version
	def set_environment(self, environment): self.environment = environment

	async def request(self, req):
		# Apply Nintendo's custom base64 encoding
		req.form = encode_form(req.form)
		
		# Must manually decode form here since server doesn't return correct content-type
		response = await http.request(self.url, req, self.context)
		response.form = decode_form(http.formdecode(response.text))
		
		return_code = response.form["returncd"].decode()
		if return_code == "null" or int(return_code) != 1:
			raise NASCError(response.status_code, response.form)
		
		return response

	async def login(self, game_server_id, nickname=""):
		if self.title_id is None:
			raise ValueError("Please configure the title (set_title)")
		if self.serial_number is None:
			raise ValueError("Please configure the device (set_device)")
		if self.pid is None and self.password is None:
			raise ValueError("Please configure a user id or password (set_user / set_password)")
		
		req = http.HTTPRequest.post("/ac")
		req.headers["Host"] = self.url
		req.headers["X-GameId"] = "%08X" %game_server_id
		req.headers["User-Agent"] = "CTR FPD/%04X" %self.fpd_version
		
		# The real 3DS seems to add this header twice for some reason
		req.headers.add("Content-Type", "application/x-www-form-urlencoded")
		req.headers.add("Content-Type", "application/x-www-form-urlencoded")

		now = datetime.datetime.now()
		device_time = now.strftime("%y%m%d%H%M%S")

		req.form = {}
		req.form["gameid"] = "%08X" %game_server_id
		req.form["sdkver"] = "%03i%03i" %(self.sdk_version_major, self.sdk_version_minor)
		req.form["titleid"] = "%016X" %self.title_id
		req.form["gamecd"] = self.product_code
		req.form["gamever"] = "%04X" %self.title_version
		req.form["mediatype"] = str(self.media_type)
		if self.media_type == MEDIA_TYPE_CARTRIDGE:
			req.form["romid"] = self.rom_id
		req.form["makercd"] = self.maker_code
		req.form["unitcd"] = self.unit_code
		req.form["macadr"] = self.mac_address
		req.form["bssid"] = self.bss_id
		req.form["apinfo"] = self.ap_info
		req.form["fcdcert"] = self.fcd_cert
		req.form["devname"] = self.device_name.encode("utf-16-le")
		req.form["servertype"] = self.environment
		req.form["fpdver"] = "%04X" %self.fpd_version
		req.form["devtime"] = device_time
		req.form["lang"] = "%02X" %self.language
		req.form["region"] = "%02X" %self.region
		req.form["csnum"] = self.serial_number
		if self.pid_hmac is not None:
			req.form["uidhmac"] = self.pid_hmac
			req.form["userid"] = str(self.pid)
		else:
			req.form["passwd"] = self.password
		req.form["action"] = "LOGIN"
		req.form["ingamesn"] = nickname
		
		response = await self.request(req)
		return LoginResponse.parse(response.form)
