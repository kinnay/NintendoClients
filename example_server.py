
from nintendo.nex import backend, service, kerberos, \
	authentication, secure, friends, common
from nintendo.settings import Settings
from nintendo.games import Friends
import collections
import itertools
import secrets
import time

import logging
logging.basicConfig(level=logging.INFO)


User = collections.namedtuple("User", "pid name password")

users = [
	User(2, "Quazal Rendez-Vous", "password"),
	User(100, "guest", "MMQea3n!fsik")
	#More accounts here
]

def get_user_by_name(name):
	for user in users:
		if user.name == name:
			return user
			
def get_user_by_pid(pid):
	for user in users:
		if user.pid == pid:
			return user
			
def derive_key(user):
	deriv = kerberos.KeyDerivationOld(65000, 1024)
	return deriv.derive_key(user.password.encode("ascii"), user.pid)

	
SECURE_SERVER = "Quazal Rendez-Vous"

class AuthenticationServer(authentication.AuthenticationServer):
	def __init__(self, settings):
		super().__init__()
		self.settings = settings
	
	def login(self, context, username):
		print("User trying to log in:", username)
		
		user = get_user_by_name(username)
		if not user:
			raise common.RMCError("RendezVous::InvalidUsername")
			
		server = get_user_by_name(SECURE_SERVER)
		
		url = common.StationURL(
			address="127.0.0.1", port=1224,
			PID = server.pid, CID = 1, type = 2,
			sid = 1, stream = 10
		)
		
		conn_data = authentication.RVConnectionData()
		conn_data.main_station = url
		conn_data.special_protocols = []
		conn_data.special_station = common.StationURL()
		
		response = common.RMCResponse()
		response.result = common.Result(0x10001) #Success
		response.pid = user.pid
		response.ticket = self.generate_ticket(user, server)
		response.connection_data = conn_data
		response.server_name = "Example server"
		return response
		
	def request_ticket(self, context, source, target):
		source = get_user_by_pid(source)
		target = get_user_by_pid(target)
		
		response = common.RMCResponse()
		response.result = common.Result(0x10001) #Success
		response.ticket = self.generate_ticket(source, target)
		return response
		
	def generate_ticket(self, source, target):
		settings = self.settings
		
		user_key = derive_key(source)
		server_key = derive_key(target)
		session_key = secrets.token_bytes(settings.get("kerberos.key_size"))
		
		internal = kerberos.ServerTicket()
		internal.expiration = common.DateTime.fromtimestamp(time.time() + 120)
		internal.source_pid = source.pid
		internal.session_key = session_key
		
		ticket = kerberos.ClientTicket()
		ticket.session_key = session_key
		ticket.target_pid = target.pid
		ticket.internal = internal.encrypt(server_key, settings)
		
		return ticket.encrypt(user_key, settings)
		
		
class SecureConnectionServer(secure.SecureConnectionServer):
	def __init__(self):
		super().__init__()
		self.connection_id = itertools.count(10)
	
	def register(self, context, urls):
		addr = context.client.remote_address()
		station = urls[0].copy()
		station["address"] = addr[0]
		station["port"] = addr[1]
		station["type"] = 3
		
		response = common.RMCResponse()
		response.result = common.Result(0x10001) #Success
		response.connection_id = next(self.connection_id)
		response.public_station = station
		return response
	
	def register_ex(self, context, urls, login_data):
		return self.register(context, urls)


class FriendsServer(friends.FriendsServer):
	pass #Implement friend server methods here


settings = Settings("friends.cfg")
settings.set("server.access_key", Friends.ACCESS_KEY)

auth_server = service.RMCServer(settings)
auth_server.register_protocol(AuthenticationServer(settings))
auth_server.start("", 1223)

server_key = derive_key(get_user_by_name("Quazal Rendez-Vous"))

secure_server = service.RMCServer(settings)
secure_server.register_protocol(SecureConnectionServer())
secure_server.register_protocol(FriendsServer())
secure_server.start("", 1224, key=server_key)

input("Press enter to exit...\n")
