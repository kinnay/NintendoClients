
from nintendo.common import util, socketutils
import contextlib
import socket
import anyio

import logging
logger = logging.getLogger(__name__)


class UDPSocket:
	def __init__(self, sock):
		self.sock = sock
	
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tr):
		await self.close()
	
	async def send(self, data, addr):
		await self.sock.send(data, addr[0], addr[1])
	async def recv(self, num=65536):
		return await self.sock.receive(num)
	
	async def close(self): await self.sock.close()
	async def abort(self): await self.sock.close()
	
	async def broadcast(self, data, port):
		host = util.broadcast_address()
		await self.send(data, (host, port))
	
	def local_address(self):
		return self.sock.address


class UDPClient:
	def __init__(self, sock, addr):
		self.sock = sock
		self.addr = addr
	
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tr):
		await self.close()
	
	async def send(self, data):
		await self.sock.send(data, self.addr[0], self.addr[1])
	async def recv(self, num=65536):
		return (await self.sock.receive(num))[0]
	
	async def close(self): await self.sock.close()
	async def abort(self): await self.sock.close()
	
	def local_address(self):
		return self.sock.address
	def remote_address(self):
		return self.addr
		
		
class UDPServerClient:
	def __init__(self, server, addr):
		self.server = server
		self.addr = addr
		
		self.packets = socketutils.PacketQueue()
		self.closed = False
	
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tr):
		await self.close()
	
	async def handle(self, data):
		await self.packets.put(data)
	
	async def send(self, data):
		if self.closed:
			raise anyio.exceptions.ClosedResourceError
		await self.server.send(data, self.addr)
	
	async def recv(self):
		return await self.packets.get()
	
	async def close(self): await self.abort()
	async def abort(self):
		if not self.closed:
			self.closed = True
			self.server.unregister(self.addr)
			await self.packets.close()
	
	def local_address(self): return self.server.local_address()
	def remote_address(self): return self.addr


class UDPServer:
	def __init__(self, handler, sock, group):
		self.handler = handler
		self.sock = sock
		self.group = group
		
		self.table = {}
	
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tr):
		await self.group.cancel_scope.cancel()
		await self.sock.close()
	
	async def start(self):
		await self.group.spawn(self.serve)
	
	async def serve(self):
		while True:
			data, addr = await self.sock.recv()
			logger.debug("Received %i bytes from %s", len(data), addr)
			if addr not in self.table:
				client = UDPServerClient(self, addr)
				self.table[addr] = client
				
				host, port = client.remote_address()
				logger.debug("New UDP connection: %s:%i", host, port)
				
				await self.group.spawn(self.handle, client)
			await self.table[addr].handle(data)
	
	async def handle(self, client):
		with util.catch_all():
			async with client:
				await self.handler(client)
	
	async def send(self, data, addr):
		await self.sock.send(data, addr)
	
	def unregister(self, addr):
		del self.table[addr]


@contextlib.asynccontextmanager
async def bind(host="", port=0):
	if not host:
		host = util.local_address()
	
	logger.debug("Creating UDP socket at %s:%i", host, port)
	
	sock = await anyio.create_udp_socket(interface=host, port=port)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
	
	async with UDPSocket(sock) as sock:
		yield sock
	
	logger.debug("UDP socket is closed")

@contextlib.asynccontextmanager
async def connect(host, port):
	logger.debug("Connecting UDP client to %s:%i", host, port)
	sock = await anyio.create_udp_socket(target_host=host, target_port=port)
	async with UDPClient(sock, (host, port)) as client:
		yield client
	logger.debug("UDP client is closed")

@contextlib.asynccontextmanager
async def serve(handler, host="", port=0):
	logger.info("Starting UDP server at %s:%i", host, port)
	async with bind(host, port) as sock:
		async with anyio.create_task_group() as group:
			async with UDPServer(handler, sock, group) as server:
				await server.start()
				yield
	logger.info("UDP server is closed")
