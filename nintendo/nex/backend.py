
from nintendo.nex.authentication import AuthenticationClient
from nintendo.nex.secure import SecureClient


class BackEndClient:
	def __init__(self, access_key, version):
		self.access_key = access_key.encode("ascii")
		self.version = version
		
		self.auth_client = None
		self.secure_client = None
		
	def connect(self, host, port):
		self.auth_client = AuthenticationClient(self, self.access_key)
		self.auth_client.connect(host, port)
		
	def close(self):
		self.auth_client.close()
		if self.secure_client:
			self.secure_client.close()
		
	def login(self, username, password, token=None):
		if token:
			self.auth_client.login_ex(username, password, token)
		else:
			self.auth_client.login(username, password)
		ticket = self.auth_client.request_ticket()
		host = self.auth_client.secure_station["address"]
		port = int(self.auth_client.secure_station["port"])
		
		self.secure_client = SecureClient(self, self.access_key, ticket, self.auth_client)
		self.secure_client.connect(host, port)
		self.secure_client.register()
