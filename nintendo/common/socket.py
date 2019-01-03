
from nintendo.common import scheduler
import socket
import ssl

TYPE_UDP = 0
TYPE_TCP = 1
TYPE_SSL = 2

class Socket:
	def __init__(self, type):
		if type == TYPE_UDP:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		elif type == TYPE_TCP:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
		else:
			tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			self.s = ssl.wrap_socket(tcp)
			
		self.remote_addr = None
		
	def bind(self, host, port):
		self.s.bind((host, port))
		
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
		self.s.setblocking(False)
	
	def accept(self):
		try:
			sock, addr = self.s.accept()
			sock.remote_addr = addr
			return sock
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
	
	
class SocketServer:
	def __init__(self, type):
		self.socket = Socket(type)
		self.event = None
		
		self.incoming = []
		
	def start(self, host, port):
		self.socket.bind(host, port)
		self.socket.listen()
		scheduler.add_server(self.incoming.append, self.socket)
		
	def accept(self, client):
		if self.incoming:
			return self.incoming.pop(0)
