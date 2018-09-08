
import socket

import logging
logger = logging.getLogger(__name__)


class P2PSocket:
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

	def bind(self, host, port):
		logger.debug("Binding P2P socket to (%s, %i)", host, port)
		self.s.bind((host, port))
		self.s.setblocking(False)
		
	def close(self): self.s.close()
		
	def recv(self, num=4096):
		try:
			return self.s.recvfrom(num)
		except BlockingIOError:
			pass
		except OSError:
			return b""
			
	def send(self, data, addr):
		self.s.sendto(data, addr)
			
	def client_address(self): return self.s.getsockname()
