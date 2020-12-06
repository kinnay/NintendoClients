
from nintendo.nex import prudp, settings, kerberos, common
import pytest


HOST = "127.0.0.1"


@pytest.mark.anyio
async def test_v0():
	s = settings.load("3ds")
	s["prudp.access_key"] = b"access key"
	
	async def handler(client):
		assert await client.recv() == b"ping"
		await client.send(b"pong")
	
	async with prudp.serve(handler, s, HOST, 12345):
		async with prudp.connect(s, HOST, 12345) as client:
			assert client.remote_address() == (HOST, 12345)
			
			await client.send(b"ping")
			assert await client.recv() == b"pong"


@pytest.mark.anyio
async def test_v1():
	s = settings.default()
	
	async def handler(client):
		assert await client.recv() == b"ping"
		await client.send(b"pong")
	
	async with prudp.serve(handler, s, HOST, 12345):
		async with prudp.connect(s, HOST, 12345) as client:
			await client.send(b"ping")
			assert await client.recv() == b"pong"


@pytest.mark.anyio
async def test_lite():
	s = settings.load("switch")
	
	async def handler(client):
		assert await client.recv() == b"ping"
		await client.send(b"pong")
	
	async with prudp.serve(handler, s, HOST, 12345):
		async with prudp.connect(s, HOST, 12345) as client:
			await client.send(b"ping")
			assert await client.recv() == b"pong"


@pytest.mark.anyio
async def test_v0_alt():
	s = settings.load("3ds")
	s["prudp_v0.signature_version"] = 1
	s["prudp_v0.flags_version"] = 0
	s["prudp_v0.checksum_version"] = 0
	
	async def handler(client):
		assert await client.recv() == b"ping"
		await client.send(b"pong")
	
	async with prudp.serve(handler, s, HOST, 12345):
		async with prudp.connect(s, HOST, 12345) as client:
			await client.send(b"ping")
			assert await client.recv() == b"pong"
			
			
@pytest.mark.anyio
async def test_compression():
	s = settings.default()
	s["prudp.compression"] = s.COMPRESSION_ZLIB
	
	async def handler(client):
		assert await client.recv() == b"ping"
		await client.send(b"pong")
	
	async with prudp.serve(handler, s, HOST, 12345):
		async with prudp.connect(s, HOST, 12345) as client:
			await client.send(b"ping")
			assert await client.recv() == b"pong"
			
			
@pytest.mark.anyio
async def test_fragmentation():
	s = settings.default()
	s["prudp.fragment_size"] = 10
	
	async def handler(client):
		assert await client.recv() == b"a" * 40
		await client.send(b"b" * 40)
	
	async with prudp.serve(handler, s, HOST, 12345):
		async with prudp.connect(s, HOST, 12345) as client:
			await client.send(b"a" * 40)
			assert await client.recv() == b"b" * 40
			
			
@pytest.mark.anyio
async def test_unreliable():
	s = settings.default()
	
	async def handler(client):
		assert await client.recv_unreliable() == b"ping"
		await client.send_unreliable(b"pong")
	
	async with prudp.serve(handler, s, HOST, 12345):
		async with prudp.connect(s, HOST, 12345) as client:
			await client.send_unreliable(b"ping")
			assert await client.recv_unreliable() == b"pong"
			
			
@pytest.mark.anyio
async def test_substreams():
	s = settings.default()
	s["prudp.max_substream_id"] = 1
	
	async def handler(client):
		assert await client.recv(0) == b"test1"
		assert await client.recv(0) == b"test3"
		assert await client.recv(1) == b"test2"
		await client.send(b"pong", 1)
	
	async with prudp.serve(handler, s, HOST, 12345):
		async with prudp.connect(s, HOST, 12345) as client:
			await client.send(b"test1", 0)
			await client.send(b"test2", 1)
			await client.send(b"test3", 0)
			assert await client.recv(1) == b"pong"
			
			
@pytest.mark.anyio
async def test_client_transport():
	s = settings.default()
	
	async def handler(client):
		data = await client.recv()
		await client.send(data[::-1])
	
	async with prudp.serve(handler, s, HOST, 12345):
		async with prudp.connect_transport(s, HOST, 12345) as transport:
			async with transport.connect(1) as client1:
				async with transport.connect(1) as client2:
					await client1.send(b"ping")
					await client2.send(b"test")
					assert await client1.recv() == b"gnip"
					assert await client2.recv() == b"tset"
			
			
@pytest.mark.anyio
async def test_server_transport():
	s = settings.default()
	
	async def handler1(client):
		assert await client.recv() == b"ping1"
		await client.send(b"pong1")
	
	async def handler2(client):
		assert await client.recv() == b"ping2"
		await client.send(b"pong2")
	
	async with prudp.serve_transport(s, HOST, 12345) as transport:
		async with transport.serve(handler1, 1):
			async with transport.serve(handler2, 2):
				async with prudp.connect(s, HOST, 12345, 1) as client:
					await client.send(b"ping1")
					assert await client.recv() == b"pong1"
				async with prudp.connect(s, HOST, 12345, 2) as client:
					await client.send(b"ping2")
					assert await client.recv() == b"pong2"


@pytest.mark.anyio
async def test_negotiation():
	s1 = settings.default()
	s1["prudp.minor_version"] = 2
	
	s2 = settings.default()
	s2["prudp.minor_version"] = 5
	
	async def handler(client):
		assert client.minor_version() == 2
	
	async with prudp.serve(handler, s1, HOST, 12345):
		async with prudp.connect(s2, HOST, 12345) as client:
			assert client.minor_version() == 2


@pytest.mark.anyio
async def test_pid():
	s = settings.default()
	
	async def handler(client):
		assert client.pid() is None
	
	async with prudp.serve(handler, s, HOST, 12345):
		async with prudp.connect(s, HOST, 12345) as client:
			assert client.pid() is None
	
	
@pytest.mark.anyio
async def test_credentials():
	s = settings.default()
	
	async def handler(client):
		assert client.pid() == 1000
	
	ticket = kerberos.ServerTicket()
	ticket.timestamp = common.DateTime.now()
	ticket.source = 1000
	ticket.session_key = bytes(32)
	data = ticket.encrypt(b"server key", s)
	
	ticket = kerberos.ClientTicket()
	ticket.session_key = bytes(32)
	ticket.target = 1001
	ticket.internal = data
	
	creds = kerberos.Credentials(ticket, 1000, 2000)
	async with prudp.serve(handler, s, HOST, 12345, key=b"server key"):
		async with prudp.connect(s, HOST, 12345, credentials=creds) as client:
			assert client.pid() == 1000
