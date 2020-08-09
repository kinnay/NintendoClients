
from nintendo.common import tcp
import pytest


HOST = "127.0.0.1"


@pytest.mark.anyio
async def test_tcp():
	async def handler(client):
		assert await client.recv() == b"hi"
		await client.send(b"hello")
	
	async with tcp.serve(handler, HOST, 12345):
		async with tcp.connect(HOST, 12345) as client:
			assert client.remote_address() == (HOST, 12345)
			
			await client.send(b"hi")
			assert await client.recv() == b"hello"
