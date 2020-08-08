
from nintendo.nex import rmc, kerberos, friends, \
	authentication, common, settings
from nintendo.games import Friends
import collections
import secrets

import aioconsole
import asyncio

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
	
	async def login(self, client, username):
		print("User trying to log in:", username)
		
		user = get_user_by_name(username)
		if not user:
			raise common.RMCError("RendezVous::InvalidUsername")
			
		server = get_user_by_name(SECURE_SERVER)
		
		url = common.StationURL(
			scheme="prudps", address="127.0.0.1", port=1224,
			PID = server.pid, CID = 1, type = 2,
			sid = 1, stream = 10
		)
		
		conn_data = authentication.RVConnectionData()
		conn_data.main_station = url
		conn_data.special_protocols = []
		conn_data.special_station = common.StationURL()
		
		response = rmc.RMCResponse()
		response.result = common.Result.success()
		response.pid = user.pid
		response.ticket = self.generate_ticket(user, server)
		response.connection_data = conn_data
		response.server_name = "Example server"
		return response
		
	def generate_ticket(self, source, target):
		settings = self.settings
		
		user_key = derive_key(source)
		server_key = derive_key(target)
		session_key = secrets.token_bytes(settings["kerberos.key_size"])
		
		internal = kerberos.ServerTicket()
		internal.timestamp = common.DateTime.now()
		internal.source = source.pid
		internal.session_key = session_key
		
		ticket = kerberos.ClientTicket()
		ticket.session_key = session_key
		ticket.target = target.pid
		ticket.internal = internal.encrypt(server_key, settings)
		
		return ticket.encrypt(user_key, settings)
		

class FriendsServer(friends.FriendsServerV1):
	pass #Implement friend server methods here


async def main():
	s = settings.load("friends")
	s.configure(Friends.ACCESS_KEY, Friends.NEX_VERSION)
	
	auth_servers = [
		AuthenticationServer(s)
	]
	secure_servers = [
		FriendsServer()
	]
	
	server_key = derive_key(get_user_by_name(SECURE_SERVER))
	async with rmc.serve(s, auth_servers, "127.0.0.1", 1223):
		async with rmc.serve(s, secure_servers, "127.0.0.1", 1224, key=server_key):
			await aioconsole.ainput("Press enter to exit...\n")

asyncio.run(main())
