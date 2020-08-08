
from nintendo.common import util, socketutils
import contextlib
import socket
import anyio

import logging
logger = logging.getLogger(__name__)


class TCPClient:
	def __init__(self, stream):
		self.stream = stream
	
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tr):
		await self.close()
	
	async def send(self, data):
		await self.stream.send_all(data)
	async def recv(self, num=65536):
		data = await self.stream.receive_some(num)
		if not data:
			raise anyio.exceptions.ClosedResourceError
		return data
	
	async def close(self): await self.stream.close()
	async def abort(self): await self.stream.close()
	
	def local_address(self):
		return self.stream.address
	def remote_address(self):
		return self.stream.peer_address
		
		
class TCPServer:
	def __init__(self, handler, server, group):
		self.handler = handler
		self.server = server
		self.group = group
	
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tr):
		await self.group.cancel_scope.cancel()
		await self.server.close()
	
	async def start(self):
		await self.group.spawn(self.serve)
		
	async def serve(self):
		while True:
			client = TCPClient(await self.server.accept())
			
			host, port = client.remote_address()
			logger.debug("New TCP connection: %s:%i", host, port)
			
			await self.group.spawn(self.handle, client)
			
	async def handle(self, client):
		with util.catch_all():
			async with client:
				await self.handler(client)

@contextlib.asynccontextmanager
async def connect(host, port):
	logger.debug("Connecting TCP client to %s:%i", host, port)
	stream = await anyio.connect_tcp(host, port)
	async with TCPClient(stream) as client:
		yield client
	logger.debug("TCP client is closed")

@contextlib.asynccontextmanager
async def serve(handler, host="", port=0):
	if not host:
		host = util.local_address()
	logger.info("Starting TCP server at %s:%i", host, port)
	server = await anyio.create_tcp_server(port, host)
	async with anyio.create_task_group() as group:
		async with TCPServer(handler, server, group) as server:
			await server.start()
			yield
	logger.info("TCP server is closed")
