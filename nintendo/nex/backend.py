
from nintendo.nex import authentication, common, kerberos, rmc, settings
from anynet import tls
from dataclasses import dataclass
from typing import AsyncContextManager, AsyncIterator

import contextlib

import logging
logger = logging.getLogger(__name__)


@dataclass
class LoginResult:
	pid: int
	ticket: bytes
	source_key: bytes | None
	secure_station: common.StationURL


class BackEndClient:
	_settings: settings.Settings

	_auth_client: rmc.RMCClient
	_auth_host: str
	_auth_port: int

	_auth_proto: authentication.AuthenticationClient
	_auth_proto_nx: authentication.AuthenticationClientNX
	
	_key_derivation: kerberos.KeyDerivationOld | kerberos.KeyDerivationNew

	def __init__(
		self, settings: settings.Settings, client: rmc.RMCClient,
		host: str, port: int
	):
		self._settings = settings
		self._auth_client = client
		self._auth_host = host
		self._auth_port = port
		
		self._auth_proto = authentication.AuthenticationClient(client)
		self._auth_proto_nx = authentication.AuthenticationClientNX(client)
		
		if self._settings["kerberos.key_derivation"] == 0:
			self._key_derivation = kerberos.KeyDerivationOld(65000, 1024)
		else:
			self._key_derivation = kerberos.KeyDerivationNew(1, 1)
	
	@contextlib.asynccontextmanager
	async def login(
		self, username: str, password: str | None = None,
		auth_info: common.Structure | None = None,
		servers: list[rmc.RMCHandler] = []
	) -> AsyncIterator[rmc.RMCClient]:
		if self._settings["nex.version"] < 40000:
			result = await self._login_old(username, auth_info)
		elif self._settings["nex.version"] < 40400:
			result = await self._login_switch(username, auth_info)
		else:
			result = await self._login_with_param(username, auth_info)
		
		secure_station = result.secure_station
		
		kerberos_key = result.source_key
		if not kerberos_key:
			if password is None:
				raise ValueError("A password is required for this account")
			
			# Derive kerberos key from password
			kerberos_key = self._key_derivation.derive_key(
				password.encode(), result.pid
			)
		
		# Decrypt ticket from login response
		ticket = kerberos.ClientTicket.decrypt(
			result.ticket, kerberos_key, self._settings
		)
		if ticket.target != secure_station["PID"]:
			# Request ticket for secure server
			if self._settings["nex.version"] < 40000:
				response = await self._auth_proto.request_ticket(
					result.pid, secure_station["PID"]
				)
			else:
				response = await self._auth_proto_nx.request_ticket(
					result.pid, secure_station["PID"]
				)
			
			# Check for errors and decrypt ticket
			response.result.raise_if_error()
			ticket = kerberos.ClientTicket.decrypt(
				response.ticket, kerberos_key, self._settings
			)
		
		creds = kerberos.Credentials(ticket, result.pid, secure_station["CID"])
		
		# The secure server may reside at the same
		# address as the authentication server
		host = secure_station["address"]
		port = secure_station["port"]
		if host == "0.0.0.1":
			host, port = self._auth_host, self._auth_port

		# Connect to secure server
		stream_id = secure_station["sid"]
		
		context = tls.TLSContext()
		async with rmc.connect(
			self._settings, host, port, stream_id, context, creds, servers
		) as client:
			yield client
	
	async def _login_old(
		self, username: str, auth_info: common.Structure | None
	) -> LoginResult:
		if auth_info:
			response = await self._auth_proto.login_ex(username, auth_info)
		else:
			response = await self._auth_proto.login(username)
		response.result.raise_if_error()
		return LoginResult(
			response.pid, response.ticket, None,
			response.connection_data.main_station
		)
	
	async def _login_switch(
		self, username: str, auth_info: common.Structure | None
	) -> LoginResult:
		if auth_info:
			response = await self._auth_proto_nx.validate_and_request_ticket_with_custom_data(
				username, auth_info
			)
			response.result.raise_if_error()
			return LoginResult(
				response.pid, response.ticket, bytes.fromhex(response.source_key),
				response.connection_data.main_station
			)
		else:
			response = await self._auth_proto_nx.validate_and_request_ticket(username)
			response.result.raise_if_error()
			return LoginResult(
				response.pid, response.ticket, None,
				response.connection_data.main_station
			)
		
	async def _login_with_param(
		self, username: str, auth_info: common.Structure | None
	) -> LoginResult:
		param = authentication.ValidateAndRequestTicketParam()
		param.username = username
		if auth_info:
			param.data = auth_info
		else:
			param.data = common.NullData()
		param.nex_version = self._settings["nex.version"]
		param.client_version = self._settings["nex.client_version"]
		
		response = await self._auth_proto_nx.validate_and_request_ticket_with_param(param)
		return LoginResult(
			response.pid, response.ticket,
			bytes.fromhex(response.source_key),
			response.server_url
		)
	
	def login_guest(self) -> AsyncContextManager[rmc.RMCClient]:
		return self.login("guest", "MMQea3n!fsik")


@contextlib.asynccontextmanager
async def connect(settings, host, port):
	context = tls.TLSContext()
	async with rmc.connect(settings, host, port, context=context) as client:
		yield BackEndClient(settings, client, host, port)
