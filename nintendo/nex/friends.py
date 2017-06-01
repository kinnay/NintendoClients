
#This might be the 3DS version of the protocol, but until
#I'm sure about that I'm calling it the "friends" protocol,
#since it's only used by IOSU for friend services on Wii U

from nintendo.nex.common import NexEncoder
from nintendo.nex.backend import BackEndClient


class FriendsTitle:
	TITLE_ID_EUR = 0x10001C00
	TITLE_ID_USA = 0x10001C00
	TITLE_ID_JAP = 0x10001C00
	LATEST_VERSION = 0
	
	GAME_SERVER_ID = 0x3200
	ACCESS_KEY = "ridfebb9"
	NEX_VERSION = 0


class NintendoLoginData(NexEncoder):
	def init(self, token):
		self.token = token
		
	def get_name(self):
		return "NintendoLoginData"
		
	def encode_old(self, stream):
		stream.string(self.token)

		
class FriendsBackEnd(BackEndClient):
	def authenticate(self, username, password, token):
		self.auth_client.login(username, password)

	def register_urls(self, token):
		self.secure_client.register_ex(NintendoLoginData(token))