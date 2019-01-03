
from nintendo.nex import account, authentication, common, datastore, \
	friends, kerberos, matchmaking, notification, ranking, secure, \
	service, nattraversal
import pkg_resources

import logging
logger = logging.getLogger(__name__)


class Settings:

	TRANSPORT_UDP = 0
	TRANSPORT_TCP = 1
	TRANSPORT_WEBSOCKET = 2
	
	field_types = {
		"prudp.transport": int,
		"prudp.version": int,
		"prudp.stream_type": int,
		"prudp.fragment_size": int,
		"prudp.resend_timeout": float,
		"prudp.resend_limit": int,
		"prudp.ping_timeout": float,
		"prudp.silence_timeout": float,
		"prudp.compression": int,
		
		"prudp_v0.signature_version": int,
		"prudp_v0.flags_version": int,
		"prudp_v0.checksum_version": int,

		"kerberos.key_size": int,
		"kerberos.key_derivation": int,
		
		"common.pid_size": int,
		
		"server.version": int,
		"server.access_key": str.encode
	}

	def __init__(self, filename=None):
		self.settings = {}
		self.reset()
		if filename:
			self.load(filename)
		
	def reset(self): self.load("default.cfg")
	def copy(self):
		copy = Settings()
		copy.settings = self.settings.copy()
		return copy
	
	def get(self, field): return self.settings[field]
	def set(self, field, value):
		if field not in self.field_types:
			raise ValueError("Unknown setting: %s" %field)
		self.settings[field] = self.field_types[field](value)

	def load(self, filename):
		filename = pkg_resources.resource_filename("nintendo", "files/%s" %filename)
		with open(filename) as f:
			linenum = 1
			for line in f:
				line = line.strip()
				if line:
					if "=" in line:
						field, value = line.split("=", 1)
						self.set(field.strip(), value.strip())
					else:
						raise ValueError("Syntax error at line %i" %linenum)
				linenum += 1


class BackEndClient:
	def __init__(self, access_key, version, settings=None):
		if settings:
			self.settings = settings.copy()
		else:
			self.settings = Settings()
		self.settings.set("server.access_key", access_key)
		self.settings.set("server.version", version)
		
		self.auth_client = service.RMCClient(self.settings)
		self.secure_client = service.RMCClient(self.settings)
		
		self.auth_proto = authentication.AuthenticationClient(self.auth_client)
		self.secure_proto = secure.SecureConnectionClient(self.secure_client)
		
		if self.settings.get("kerberos.key_derivation") == 0:
			self.key_derivation = kerberos.KeyDerivationOld(65000, 1024)
		else:
			self.key_derivation = kerberos.KeyDerivationNew(1, 1)
			
		self.my_pid = None
		self.local_station = None
		self.public_station = None
		
	def connect(self, host, port):
		# Connect to authentication server
		self.auth_client.connect(host, port, 1)
		
	def close(self):
		self.auth_client.close()
		self.secure_client.close()
		
	def login(self, username, password, auth_info=None, login_data=None):
		# Call login method on authentication protocol
		if auth_info:
			response = self.auth_proto.login_ex(username, auth_info)
		else:
			response = self.auth_proto.login(username)
			
		# Check for errors
		response.result.raise_if_error()
		
		self.my_pid = response.pid
		
		secure_station = response.connection_data.main_station

		# Derive kerberos key from password
		kerberos_key = self.key_derivation.derive_key(
			password.encode("ascii"), response.pid
		)
		
		# Decrypt ticket from login response
		ticket = kerberos.ClientTicket(response.ticket)
		ticket.decrypt(kerberos_key, self.settings)
		
		if ticket.target_pid != secure_station["PID"]:
			# Request ticket for secure server
			response = self.auth_proto.request_ticket(
				self.my_pid, secure_station["PID"]
			)
			
			# Check for errors and decrypt ticket
			response.result.raise_if_error()
			ticket = kerberos.ClientTicket(response.ticket)
			ticket.decrypt(kerberos_key, self.settings)
			
		ticket.source_pid = self.my_pid
		ticket.target_cid = secure_station["CID"]

		# The secure server may reside at the same
		# address as the authentication server
		host = secure_station["address"]
		port = secure_station["port"]
		if host == "0.0.0.1":
			host, port = self.auth_client.remote_address()
			
		# Connect to secure server
		server_sid = secure_station["sid"]
		self.secure_client.connect(host, port, server_sid, ticket)
		
		# Create a stationurl for our local client address
		client_addr = self.secure_client.local_address()
		self.local_station = common.StationUrl(
			address=client_addr[0], port=client_addr[1],
			sid=self.secure_client.stream_id(),
			natm=0, natf=0, upnp=0, pmp=0
		)
		
		# Register urls on secure server
		if login_data:
			response = self.secure_proto.register_ex([self.local_station], login_data)
		else:
			response = self.secure_proto.register([self.local_station])

		# Check for errors and update urls
		response.result.raise_if_error()
		self.public_station = response.public_station
		self.public_station["RVCID"] = response.connection_id
		self.local_station["RVCID"] = response.connection_id
		
	def login_guest(self):
		self.login("guest", "MMQea3n!fsik")
		
	def get_pid(self):
		return self.my_pid
