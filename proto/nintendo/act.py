
from bs4 import BeautifulSoup
import requests
import time
import os

import logging
logger = logging.getLogger(__name__)


CERT = os.path.join(os.path.dirname(__file__), "../files/wiiu_common_cert.pem")
KEY = os.path.join(os.path.dirname(__file__), "../files/wiiu_common_key.pem")

class Request:
	def __init__(self, api):
		self.api = api
		self.headers = api.headers.copy()
		
	def auth(self, token):
		self.headers["X-Nintendo-Client-ID"] = ""
		self.headers["X-Nintendo-Client-Secret"] = ""
		self.headers["Authorization"] = "Bearer %s" %token
		
	def format(self, url):
		return "https://account.nintendo.net/v1/api/%s" %url
		
	def get(self, url, data=None, params=None):
		req = requests.Request("GET", self.format(url), self.headers, data=data, params=params)
		return self.request(req)
		
	def request(self, req):
		prepped = req.prepare()
		response = self.api.session.send(prepped, verify=False, cert=(CERT, KEY))
		
		if response.status_code != 200:
			logger.error("HTTP request returned status code %i\n%s", response.status_code, response.text)
		
		return BeautifulSoup(response.text, "lxml")


class NexToken:
	def __init__(self, host, port, username, password, token):
		self.host = host
		self.port = port
		self.username = username
		self.password = password
		self.token = token
		
		
class AccountAPI:
	def __init__(self):
		self.headers = {
			"X-Nintendo-Platform-ID": "1",
			"X-Nintendo-Device-Type": "2",
			"X-Nintendo-Client-ID": "a2efa818a34fa16b8afbc8a74eba3eda",
			"X-Nintendo-Client-Secret": "c91cdb5658bd4954ade78533a339cf9a",
			"X-Nintendo-FPD-Version": "0000",
			"X-Nintendo-Environment": "L1"
		}
		self.session = requests.Session()
		
		self.access_token = None
		self.refresh_token = None
		self.refresh_time = None
		
	def set_device(self, device_id, serial_number, system_version, region, country):
		self.headers["X-Nintendo-Device-ID"] = str(device_id)
		self.headers["X-Nintendo-Serial-Number"] = serial_number
		self.headers["X-Nintendo-System-Version"] = "%04X" %system_version
		self.headers["X-Nintendo-Region"] = str(region)
		self.headers["X-Nintendo-Country"] = country
		
	def set_title(self, title_id, application_version):
		self.headers["X-Nintendo-Title-ID"] = "%016X" %title_id
		self.headers["X-Nintendo-Unique-ID"] = "%05X" %((title_id & 0xFFFFF00) >> 8)
		self.headers["X-Nintendo-Application-Version"] = "%04X" %application_version
		
	def get_access_token(self):
		if time.time() >= self.refresh_time:
			self.refresh_login()
		return self.access_token
		
	def login(self, username, password):
		request = Request(self)
		response = request.get(
			"oauth20/access_token/generate",
			data = {
				"grant_type": "password",
				"user_id": username,
				"password": password
			}
		)
		
		self.access_token = response.oauth20.access_token.token.text
		self.refresh_token = response.oauth20.access_token.refresh_token.text
		self.refresh_time = time.time() + int(response.oauth20.access_token.expires_in.text)
		
	def refresh_login(self):
		request = Request(self)
		response = request.get(
			"oauth20/access_token/generate",
			data = {
				"grant_type": "refresh_token",
				"refresh_token": self.refresh_token
			}
		)
		
		self.access_token = response.oauth20.access_token.token.text
		self.refresh_token = response.oauth20.access_token.refresh_token.text
		self.refresh_time = time.time() + int(response.oauth20.access_token.expires_in.text)
		
	def get_nex_token(self, game_server_id):
		request = Request(self)
		request.auth(self.get_access_token())
		response = request.get(
			"provider/nex_token/@me",
			params = {
				"game_server_id": "%08X" %game_server_id
			}
		)
		
		return NexToken(
			response.nex_token.host.text,
			int(response.nex_token.port.text),
			response.nex_token.pid.text,
			response.nex_token.nex_password.text,
			response.nex_token.token.text
		)
