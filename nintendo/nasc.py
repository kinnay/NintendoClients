
from anynet import http, tls
import pkg_resources
import datetime
import base64

import logging
logger = logging.getLogger(__name__)


# These still work here
# But should probably be changed out for the 3DS ones
CA = pkg_resources.resource_filename("nintendo", "files/cert/CACERT_NINTENDO_CA_G3.der")
CERT = pkg_resources.resource_filename("nintendo", "files/cert/WIIU_COMMON_1_CERT.der")
KEY = pkg_resources.resource_filename("nintendo", "files/cert/WIIU_COMMON_1_RSA_KEY.der")


def nintendo_base64_decode(input):
	input = input.replace('.', '+').replace('-', '/').replace('*', '=').encode()
	return base64.b64decode(input).decode()

def nintendo_base64_encode(input):
	return base64.b64encode(input.encode()).decode().replace('+', '.').replace('/', '-').replace('=', '*')


class NASCError(Exception):
	def __init__(self, status_code, form):
		self.status_code = status_code
		self.form = form
	
	def __str__(self):
		if "returncd" in self.form:
			return "NASC request failed: %s" %nintendo_base64_decode(self.form.get("returncd"))
		else:
			return "NASC request failed with status %i" %self.status_code


class NASCLocator:
	def __init__(self):
		self.host = None
		self.port = None

	@classmethod
	def parse(cls, locator):
		host, port = nintendo_base64_decode(locator).split(":")

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
		inst.retry = nintendo_base64_decode(form.get("retry"))
		inst.return_code = nintendo_base64_decode(form.get("returncd"))
		inst.token = form.get("token")
		inst.datetime = nintendo_base64_decode(form.get("datetime"))
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
		response = await http.request(self.url, req, self.context)
		response.form = http.formdecode(response.text) # Must manually decode here since server doesn't return correct content-type

		if response.error():
			raise NASCError(response.status_code, response.form)

		if not response.form.get("locator"):
			raise NASCError(response.status_code, response.form)

		return response

	async def get_nasc_data(self, game_server_id):
		req = http.HTTPRequest.post("/ac")
		req.headers["Host"] = self.url
		req.headers["X-GameId"] = "%08X" % game_server_id
		req.headers["User-Agent"] = "CTR FPD/%s" %self.fpd_version
		req.headers["Content-Type"] = "application/x-www-form-urlencoded"

		now = datetime.datetime.now()
		device_time = now.strftime("%y%m%d%H%M%S")

		req.form = {
			"gameid": nintendo_base64_encode("%08X" % game_server_id),
			"sdkver": nintendo_base64_encode(self.sdk_version),
			"titleid": nintendo_base64_encode("%016X" % self.title_id),
			"gamecd":  nintendo_base64_encode(self.title_product_code),
			"gamever": nintendo_base64_encode("%04X" % self.title_version),
			"mediatype": nintendo_base64_encode(self.media_type),
			"makercd": nintendo_base64_encode(self.maker_cd),
			"unitcd": nintendo_base64_encode(self.unit_cd),
			"macadr": nintendo_base64_encode(self.mac_address),
			"bssid": nintendo_base64_encode(self.bss_id),
			"apinfo": nintendo_base64_encode(self.current_access_point_slot),
			"fcdcert": self.fcdcert,
			"devname": nintendo_base64_encode(self.device_name),
			"servertype": nintendo_base64_encode(self.environment),
			"fpdver": nintendo_base64_encode(self.fpd_version),
			"devtime": nintendo_base64_encode(device_time),
			"lang": nintendo_base64_encode(self.language),
			"region": nintendo_base64_encode(self.region),
			"csnum": nintendo_base64_encode(self.serial_number),
			"uidhmac": nintendo_base64_encode(self.pid_hmac),
			"userid": nintendo_base64_encode("%i" % self.pid),
			"action": nintendo_base64_encode("LOGIN"),
			"ingamesn": ""
		}

		response = await self.request(req)
		
		return NASCResponse.parse(response.form)
