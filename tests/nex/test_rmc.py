
from nintendo.nex import rmc, common, authentication, settings
import pytest
import anyio


HOST = "127.0.0.1"


class AuthenticationServer(authentication.AuthenticationServer):
	def __init__(self):
		super().__init__()
		self.flag = False
	
	async def logout(self, client):
		self.flag = True
	
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


@pytest.mark.anyio
async def test_unimplemented_protocol():
	s = settings.default()
	
	servers = []
	async with rmc.serve(s, servers, HOST, 12345):
		async with rmc.connect(s, HOST, 12345) as client:
			assert client.remote_address() == (HOST, 12345)
			
			auth = authentication.AuthenticationClient(client)
			try:
				result = await auth.get_name(12345)
			except common.RMCError as e:
				assert e.result().name() == "Core::NotImplemented"
				
				
@pytest.mark.anyio
async def test_logout_event():
	s = settings.default()
	
	server = AuthenticationServer()
	async with rmc.serve(s, [server], HOST, 12345):
		async with rmc.connect(s, HOST, 12345) as client:
			assert not server.flag
		await anyio.sleep(.1) # Wait a bit
		assert server.flag
