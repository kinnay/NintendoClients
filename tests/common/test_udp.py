
from nintendo.common import udp
import pytest


HOST = "127.0.0.1"


@pytest.mark.anyio
async def test_socket():
	async with udp.bind(HOST, 12345) as sock1:
		async with udp.bind(HOST, 12346) as sock2:
			assert sock1.local_address() == (HOST, 12345)
			assert sock2.local_address() == (HOST, 12346)
			
			await sock1.send(b"hi", (HOST, 12346))
			await sock2.send(b"hello", (HOST, 12345))
			assert (await sock1.recv())[0] == b"hello"
			assert (await sock2.recv())[0] == b"hi"


@pytest.mark.anyio
async def test_udp():
	async def handler(client):
		assert await client.recv() == b"hi"
		await client.send(b"hello")
	
	async with udp.serve(handler, HOST, 12345):
		async with udp.connect(HOST, 12345) as client:
			assert client.remote_address() == (HOST, 12345)
			
			await client.send(b"hi")
			assert await client.recv() == b"hello"
