
import socket


class Socket:

	TCP = 0
	UDP = 1

	def __init__(self, type):
		if type == self.TCP:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
		else:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.s.setblocking(False)
		
	def connect(self, host, port): self.s.connect((host, port))
	def close(self): self.s.close()
	def send(self, data): self.s.sendall(data)
	def recv(self, num):
		try:
			return self.s.recv(num)
		except BlockingIOError:
			pass
			
	def bind(self, addr=("", 0)): self.s.bind(addr)
	def sendto(self, data, addr): self.s.sendto(data, addr)
	def recvfrom(self, num):
		try:
			return self.s.recvfrom(num)
		except BlockingIOError:
			return None, None
			
	def get_address(self): return self.s.getsockname()[0]
	def get_port(self): return self.s.getsockname()[1]
