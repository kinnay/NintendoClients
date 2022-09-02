
from nintendo.nex import rmc, authentication, kerberos, common
from anynet import tls
import contextlib

import logging
logger = logging.getLogger(__name__)


class LoginResult:
	def __init__(self, pid, ticket, source_key, secure_station):
		self.pid = pid
		self.ticket = ticket
		self.source_key = source_key
		self.secure_station = secure_station


class BackEndClient:
	def __init__(self, settings, client, host, port):
		self.settings = settings
		self.auth_client = client
		self.auth_host = host
		self.auth_port = port
		
		if self.settings["nex.version"] < 40000:
			self.auth_proto = authentication.AuthenticationClient(client)
		else:
			self.auth_proto = authentication.AuthenticationClientNX(client)
		
		if self.settings["kerberos.key_derivation"] == 0:
			self.key_derivation = kerberos.KeyDerivationOld(65000, 1024)
		else:
			self.key_derivation = kerberos.KeyDerivationNew(1, 1)
	
	@contextlib.asynccontextmanager
	async def login(self, username, password=None, auth_info=None, servers=[]):
		if self.settings["nex.version"] < 40000:
			result = await self.login_old(username, auth_info)
		elif self.settings["nex.version"] < 40400:
			result = await self.login_switch(username, auth_info)
		else:
			result = await self.login_with_param(username, auth_info)
		
		secure_station = result.secure_station
		
		kerberos_key = result.source_key
		if not kerberos_key:
			if password is None:
				raise ValueError("A password is required for this account")
			
			# Derive kerberos key from password
			kerberos_key = self.key_derivation.derive_key(
				password.encode(), result.pid
			)
		
		# Decrypt ticket from login response
		ticket = kerberos.ClientTicket.decrypt(result.ticket, kerberos_key, self.settings)
		if ticket.target != secure_station["PID"]:
			# Request ticket for secure server
			response = await self.auth_proto.request_ticket(
				result.pid, secure_station["PID"]
			)
			
			# Check for errors and decrypt ticket
			response.result.raise_if_error()
			ticket = kerberos.ClientTicket.decrypt(response.ticket, kerberos_key, self.settings)
		
		creds = kerberos.Credentials(ticket, result.pid, secure_station["CID"])
		
		# The secure server may reside at the same
		# address as the authentication server
		host = secure_station["address"]
		port = secure_station["port"]
		if host == "0.0.0.1":
			host, port = self.auth_host, self.auth_port

		# Connect to secure server
		stream_id = secure_station["sid"]
		
		context = tls.TLSContext()
		async with rmc.connect(self.settings, host, port, stream_id, context, creds, servers) as client:
			yield client
	
	async def login_old(self, username, auth_info):
		if auth_info:
			response = await self.auth_proto.login_ex(username, auth_info)
		else:
			response = await self.auth_proto.login(username)
		response.result.raise_if_error()
		return LoginResult(
			response.pid, response.ticket, None,
			response.connection_data.main_station
		)
	
	async def login_switch(self, username, auth_info):
		if auth_info:
			response = await self.auth_proto.validate_and_request_ticket_with_custom_data(
				username, auth_info
			)
			response.result.raise_if_error()
			return LoginResult(
				response.pid, response.ticket, bytes.fromhex(response.source_key),
				response.connection_data.main_station
			)
		else:
			response = await self.auth_proto.validate_and_request_ticket(username)
			response.result.raise_if_error()
			return LoginResult(
				response.pid, response.ticket, None,
				response.connection_data.main_station
			)
		
	async def login_with_param(self, username, auth_info):
		param = authentication.ValidateAndRequestTicketParam()
		param.username = username
		if auth_info:
			param.data = auth_info
		else:
			param.data = common.NullData()
		param.nex_version = self.settings["nex.version"]
		param.client_version = self.settings["nex.client_version"]
		
		response = await self.auth_proto.validate_and_request_ticket_with_param(param)
		return LoginResult(
			response.pid, response.ticket,
			bytes.fromhex(response.source_key),
			response.server_url
		)
	
	def login_guest(self):
		return self.login("guest", "MMQea3n!fsik")


@contextlib.asynccontextmanager
async def connect(settings, host, port):
	context = tls.TLSContext()
	async with rmc.connect(settings, host, port, context=context) as client:
		yield BackEndClient(settings, client, host, port)
