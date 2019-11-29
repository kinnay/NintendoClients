
from nintendo.common import scheduler
import socket

import logging
logger = logging.getLogger(__name__)


class SocketWrapper:
	def __init__(self, sock):
		self.s = sock
		
		self.remote_addr = None
		
	def fd(self): return self.s
		
	def bind(self, host, port):
		self.s.bind((host, port))
		self.s.setblocking(False)
	
	def connect(self, host, port, timeout=3):
		self.s.settimeout(timeout)
		try:
			self.s.connect((host, port))
		except socket.timeout:
			return False
		self.s.setblocking(False)
		self.remote_addr = host, port
		return True
	
	def listen(self):
		self.s.listen()
	
	def accept(self):
		try:
			sock, addr = self.s.accept()
			sock.setblocking(False)
			wrapper = SocketWrapper(sock)
			wrapper.remote_addr = addr
			return wrapper
		except BlockingIOError:
			pass

	def close(self): self.s.close()
	
	def send(self, data): self.s.sendall(data)
	def recv(self, num=4096):
		try:
			return self.s.recv(num)
		except BlockingIOError:
			pass
		except OSError:
			return b""
	
	def sendto(self, data, addr): self.s.sendto(data, addr)
	def recvfrom(self, num=4096):
		try:
			return self.s.recvfrom(num)
		except (BlockingIOError, ConnectionResetError):
			pass
			
	def local_address(self): return self.s.getsockname()
	def remote_address(self): return self.remote_addr


class UDPSocket:
	def __init__(self, sock=None):
		self.s = sock
		if not self.s:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
			self.s = SocketWrapper(sock)
			
	def bind(self, host, port): self.s.bind(host, port)
	
	def send(self, data, addr): self.s.sendto(data, addr)
	def recv(self, num=4096): return self.s.recvfrom(num)
	
	def close(self): self.s.close()
	
	def fd(self): return self.s.fd()
	def local_address(self): return self.s.local_address()
	def remote_address(self): return self.s.remote_address()
	
	
class UDPClient:
	def __init__(self, sock=None):
		self.s = sock
		if not self.s:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			self.s = SocketWrapper(sock)
			
	def connect(self, host, port, timeout=3):
		return self.s.connect(host, port, timeout)
		
	def send(self, data): self.s.send(data)
	def recv(self, num=4096):
		return self.s.recv(num)
	
	def close(self): self.s.close()
			
	def fd(self): return self.s.fd()
	def local_address(self): return self.s.local_address()
	def remote_address(self): return self.s.remote_address()


class TCPClient:
	def __init__(self, sock=None):
		self.s = sock
		if not self.s:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			self.s = SocketWrapper(sock)
			
	def connect(self, host, port, timeout=3):
		return self.s.connect(host, port, timeout)
		
	def send(self, data): self.s.send(data)
	def recv(self, num=4096):
		return self.s.recv(num)
	
	def close(self): self.s.close()
			
	def fd(self): return self.s.fd()
	def local_address(self): return self.s.local_address()
	def remote_address(self): return self.s.remote_address()


class TCPServer:
	def __init__(self, sock=None):
		self.s = sock
		if not self.s:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			self.s = SocketWrapper(sock)
		
		self.incoming = []
	
	def fd(self): return self.s.fd()
	
	def start(self, host, port):
		self.s.bind(host, port)
		self.s.listen()
		scheduler.add_server(self.incoming.append, self.s)
		
	def accept(self):
		if self.incoming:
			return self.incoming.pop(0)
			
			
class UDPServerClient:
	def __init__(self, server, addr):
		self.server = server
		self.addr = addr
		
		self.packets = []
		
	def handle(self, data):
		self.packets.append(data)
	
	def send(self, data): self.server.send(data, self.addr)
	def recv(self, num=4096):
		if self.packets:
			return self.packets.pop(0)
	
	def close(self): self.server.close(self.addr)
			
	def fd(self): return self.server.fd()
	def local_address(self): return self.server.local_address()
	def remote_address(self): return self.addr
			
			
class UDPServer:
	def __init__(self, sock=None):
		self.s = sock
		if not self.s:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			self.s = SocketWrapper(sock)
		
		self.incoming = []
		self.clients = {}
	
	def fd(self): return self.s.fd()
	
	def start(self, host, port):
		self.s.bind((host, port))
		scheduler.add_callback(self.update)
		
	def accept(self):
		if self.incoming:
			return self.incoming.pop(0)
			
	def close(self, addr):
		del self.clients[addr]
		
	def send(self, data, addr):
		self.s.sendto(data, addr)
			
	def update(self):
		try:
			data, addr = self.s.recvfrom(4096)
			if addr not in self.clients:
				client = UDPServerClient(self, addr)
				self.clients[addr] = client
				self.incoming.append(client)
			self.clients[addr].handle(data)
		except (BlockingIOError, ConnectionResetError):
			pass
