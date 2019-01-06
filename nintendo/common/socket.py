
from nintendo.common import scheduler
import pkg_resources
import socket
import ssl

CERT = pkg_resources.resource_filename("nintendo", "files/server.crt")
KEY = pkg_resources.resource_filename("nintendo", "files/server.key")


TYPE_UDP = 0
TYPE_TCP = 1
TYPE_SSL = 2

class Socket:
	def __init__(self, type, sock=None):
		self.type = type
		
		self.s = sock
		if not self.s:
			if type == TYPE_UDP:
				self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			elif type == TYPE_TCP or type == TYPE_SSL:
				self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			
		self.remote_addr = None
		
		self.certfile = None
		self.keyfile = None
		
	def set_certificate(self, certfile, keyfile):
		self.certfile = certfile
		self.keyfile = keyfile
		
	def bind(self, host, port):
		self.s.bind((host, port))
		
	def connect(self, host, port, timeout=3):
		if self.type == TYPE_SSL:
			self.s = ssl.wrap_socket(self.s, self.keyfile, self.certfile)
		
		self.s.settimeout(timeout)
		try:
			self.s.connect((host, port))
		except socket.timeout:
			return False
		self.s.setblocking(False)
		self.remote_addr = host, port
		return True
	
	def listen(self):
		if self.type == TYPE_SSL:
			if not self.certfile or not self.keyfile:
				self.certfile = CERT
				self.keyfile = KEY
			self.s = ssl.wrap_socket(self.s, self.keyfile, self.certfile, True)
		
		self.s.listen()
		self.s.setblocking(False)
	
	def accept(self):
		try:
			sock, addr = self.s.accept()
			sock.setblocking(False)
			wrapper = Socket(self.type, sock)
			wrapper.remote_addr = addr
			return wrapper
		except BlockingIOError:
			pass

	def close(self): self.s.close()
	def send(self, data): self.s.sendall(data)
	def recv(self, num=4096):
		try:
			return self.s.recv(num)
		except (BlockingIOError, ssl.SSLWantReadError):
			pass
		except OSError:
			return b""
			
	def local_address(self): return self.s.getsockname()
	def remote_address(self): return self.remote_addr
	
	
class UDPServer:
	def __init__(self):
		self.s = self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.incoming = []
		self.packets = {}
		
	def bind(self, host, port):
		self.s.bind((host, port))
	
	def listen(self):
		self.s.setblocking(False)
		scheduler.add_callback(self.update)
		
	def remove(self, addr):
		del self.packets[addr]
		
	def recvfrom(self, addr):
		if self.packets[addr]:
			return self.packets[addr].pop(0)
	
	def sendto(self, addr, data):
		self.s.sendto(data, addr)
		
	def update(self):
		try:
			data, addr = self.s.recvfrom(4096)
			if addr not in self.packets:
				sock = UDPWrapper(self, addr)
				self.packets[addr] = []
				self.incoming.append(sock)
			self.packets[addr].append(data)
		except BlockingIOError:
			pass
			
	def accept(self):
		if self.incoming:
			return self.incoming.pop(0)
			
			
class UDPWrapper:
	def __init__(self, server, addr):
		self.server = server
		self.addr = addr
		
	def close(self):
		self.server.remove(self.addr)
		
	def recv(self):
		return self.server.recvfrom(self.addr)
		
	def send(self, data):
		self.server.sendto(self.addr, data)
	
	
class SocketServer:
	def __init__(self, type):
		self.type = type
		if type == TYPE_UDP:
			self.socket = UDPServer()
		else:
			self.socket = Socket(type)
		self.event = None
		
		self.certfile = None
		self.keyfile = None
		
		self.incoming = []
		
	def set_certificate(self, certfile, keyfile):
		self.certfile = certfile
		self.keyfile = keyfile
		
	def start(self, host, port):
		if self.type == TYPE_SSL:
			self.socket.set_certificate(self.certfile, self.keyfile)
		self.socket.bind(host, port)
		self.socket.listen()
		scheduler.add_server(self.incoming.append, self.socket)
		
	def accept(self):
		if self.incoming:
			return self.incoming.pop(0)
