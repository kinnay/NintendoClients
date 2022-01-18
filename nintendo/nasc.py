
from anynet import http, tls
import pkg_resources
import datetime
import base64

import logging
logger = logging.getLogger(__name__)


CA = pkg_resources.resource_filename("nintendo", "files/cert/CACERT_NINTENDO_CA_G3.der")
CERT = pkg_resources.resource_filename("nintendo", "files/cert/ctr-common-1-cert.der")
KEY = pkg_resources.resource_filename("nintendo", "files/cert/ctr-common-1-key.der")


def b64decode(text):
	text = text.replace(".", "+").replace("-", "/").replace("*", "=")
	return base64.b64decode(text).decode()

def b64encode(text):
	text = base64.b64encode(text).decode()
	return text.replace("+", ".").replace("/", "-").replace("=", "*")

def decode_form(form):
	return {key: b64decode(value) for key, value in form.items()}

def encode_form(form):
	return {key: b64encode(value) for key, value in form.items()}


class NASCError(Exception):
	def __init__(self, status_code, form):
		self.status_code = status_code
		self.form = form
	
	def __str__(self):
		if "returncd" in self.form:
			return "NASC request failed: %s" %self.form["returncd"]
		else:
			return "NASC request failed with status %i" %self.status_code


class NASCLocator:
	def __init__(self):
		self.host = None
		self.port = None

	@classmethod
	def parse(cls, locator):
		host, port = locator.split(":")

		inst = cls()
		inst.host = host
		inst.port = port
		return inst


class NASCResponse:
	def __init__(self):
		self.locator = None
		self.retry = None
		self.returncd = None
		self.token = None
		self.datetime = None

	@classmethod
	def parse(cls, form):
		inst = cls()
		inst.locator = NASCLocator.parse(form.get("locator"))
		inst.retry = form.get("retry")
		inst.return_code = form.get("returncd")
		inst.token = form.get("token")
		inst.datetime = form.get("datetime")
		return inst


class NASCClient:
	def __init__(self):
		self.url = "nasc.nintendowifi.net"
		
		ca = tls.TLSCertificate.load(CA, tls.TYPE_DER)
		cert = tls.TLSCertificate.load(CERT, tls.TYPE_DER)
		key = tls.TLSPrivateKey.load(KEY, tls.TYPE_DER)

		self.context = tls.TLSContext()
		self.context.set_authority(ca)
		self.context.set_certificate(cert, key)
		
		self.game_server_id = None
		self.title_id = None
		self.title_version = None
		self.title_product_code = None

		self.fcdcert = None
		self.serial_number = None
		self.device_name = "NintendoClients" # Doesn't matter
		self.current_access_point_slot = "01:0000000000"  # Doesn't matter
		self.mac_address = None
		self.bss_id = ""  # Doesn't matter
		self.fpd_version = "000F"
		self.environment = "L1"

		# These don't matter
		self.sdk_version = "000000"
		self.media_type = "0"
		self.maker_cd = "00"
		self.unit_cd = "2"
		
		self.pid = None
		self.pid_hmac = None
		
		self.language = "01"
		self.region = "01"
	
	def set_device(self, serial_number, mac_address, fcdcert):
		self.serial_number = serial_number
		self.mac_address = mac_address
		self.fcdcert = fcdcert
		
	def set_locale(self, region, language):
		self.region = region
		self.language = language
		
	def set_fpd_version(self, version): self.fpd_version = version
	def set_environment(self, environment): self.environment = environment
	
	def set_title(self, title_id, title_version, title_product_code):
		self.title_id = title_id
		self.title_version = title_version
		self.title_product_code = title_product_code

	def set_user(self, pid, pid_hmac):
		self.pid = pid
		self.pid_hmac = pid_hmac

	async def request(self, req):
		# Apply Nintendo's custom base64 encoding
		req.form = encode_form(req.form)
		
		# Must manually decode form here since server doesn't return correct content-type
		response = await http.request(self.url, req, self.context)
		response.form = decode_form(http.formdecode(response.text))
		
		if response.error():
			raise NASCError(response.status_code, response.form)

		if not response.form.get("locator"):
			raise NASCError(response.status_code, response.form)

		return response

	async def login(self, game_server_id):
		req = http.HTTPRequest.post("/ac")
		req.headers["Host"] = self.url
		req.headers["X-GameId"] = "%08X" % game_server_id
		req.headers["User-Agent"] = "CTR FPD/%s" %self.fpd_version
		req.headers["Content-Type"] = "application/x-www-form-urlencoded"

		now = datetime.datetime.now()
		device_time = now.strftime("%y%m%d%H%M%S")

		req.form = {
			"gameid": "%08X" %game_server_id,
			"sdkver": self.sdk_version,
			"titleid": "%016X" % self.title_id,
			"gamecd":  self.title_product_code,
			"gamever": "%04X" % self.title_version,
			"mediatype": self.media_type,
			"makercd": self.maker_cd,
			"unitcd": self.unit_cd,
			"macadr": self.mac_address,
			"bssid": self.bss_id,
			"apinfo": self.current_access_point_slot,
			"fcdcert": self.fcdcert,
			"devname": self.device_name,
			"servertype": self.environment,
			"fpdver": self.fpd_version,
			"devtime": device_time,
			"lang": self.language,
			"region": self.region,
			"csnum": self.serial_number,
			"uidhmac": self.pid_hmac,
			"userid": "%i" % self.pid,
			"action": "LOGIN",
			"ingamesn": ""
		}

		response = await self.request(req)
		
		return NASCResponse.parse(response.form)
