from nintendo.nex import (
	backend,
	rmc,
	common,
	authentication,
	kerberos,
	account,
	settings,
)
import pytest


HOST = "127.0.0.1"


class AuthenticationServer(authentication.AuthenticationServer):
	def __init__(self, settings):
		super().__init__()
		self.settings = settings

	async def login(self, client, username):
		assert username == "username"

		pid = 1001

		stick = kerberos.ServerTicket()
		stick.timestamp = common.DateTime.now()
		stick.source = pid
		stick.session_key = bytes(32)

		ctick = kerberos.ClientTicket()
		ctick.session_key = bytes(32)
		ctick.target = 100
		ctick.internal = stick.encrypt(b"testkey", self.settings)

		kerb = kerberos.KeyDerivationOld(65000, 1024)
		key = kerb.derive_key(b"password", pid)

		connection_data = authentication.RVConnectionData()
		connection_data.main_station = common.StationURL(
			address=HOST, port=12346, PID=100, sid=1
		)
		connection_data.special_protocols = []
		connection_data.special_station = common.StationURL()
		connection_data.server_time = common.DateTime.now()

		response = rmc.RMCResponse()
		response.result = common.Result.success()
		response.pid = pid
		response.ticket = ctick.encrypt(key, self.settings)
		response.connection_data = connection_data
		response.server_name = "server build name"
		return response


class AccountManagementServer(account.AccountServer):
	async def get_name(self, client, pid):
		assert pid == 1000
		return "test"


@pytest.mark.anyio
async def test_backend():
	s = settings.default()

	auth_servers = [AuthenticationServer(s)]
	secure_servers = [AccountManagementServer()]
	async with rmc.serve(s, auth_servers, HOST, 12345):
		async with rmc.serve(s, secure_servers, HOST, 12346, key=b"testkey"):
			async with backend.connect(s, HOST, 12345) as client:
				async with client.login("username", "password") as secure_client:
					act = account.AccountClient(secure_client)
					assert await act.get_name(1000) == "test"
