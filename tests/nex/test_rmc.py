
from nintendo.nex import rmc, authentication, settings
import pytest


HOST = "127.0.0.1"


class AuthenticationServer(authentication.AuthenticationServer):
	async def get_name(self, client, pid):
		return str(pid)


@pytest.mark.anyio
async def test_simple():
	s = settings.default()
	
	servers = [AuthenticationServer()]
	async with rmc.serve(s, servers, HOST, 12345):
		async with rmc.connect(s, HOST, 12345) as client:
			assert client.remote_address() == (HOST, 12345)
			
			auth = authentication.AuthenticationClient(client)
			result = await auth.get_name(12345)
			assert result == "12345"
