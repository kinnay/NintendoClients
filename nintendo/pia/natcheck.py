
import socket
import struct
import time

primary_url = "nncs1.app.nintendowifi.net"
secondary_url = "nncs2.app.nintendowifi.net"

primary_port = 10025
secondary_port = 10125


class NATProperties:
	def __init__(self, public_address, nat_filtering, nat_mapping, lag):
		self.public_address = public_address
		self.nat_filtering = nat_filtering
		self.nat_mapping = nat_mapping
		self.lag = lag


class NatDetecter:
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.s.settimeout(1)
		
	def send_message(self, dest, a, b, c, d):	
		#PIA sends each messages 5 times for some reason
		#Maybe because UDP doesn't assure packet arrival?
		data = struct.pack(">IIII", a, b, c, d)
		for i in range(5):
			self.s.sendto(data, dest)

	def recv_message(self):
		request, port, host, unk = struct.unpack(">II4sI", self.s.recvfrom(16)[0])
		return request, socket.inet_ntoa(host), port
		
	def get_nat_properties(self):
		#I've only tested this at home. If you have a different
		#NAT setup this function might fail or return incorrect
		#values. Any help/testing would be appreciated.
		
		import time
		start_time = time.time()

		self.send_message((primary_url, primary_port), 101, 0, 0, 0)
		self.send_message((primary_url, primary_port), 102, 0, 0, 0)
		self.send_message((primary_url, secondary_port), 103, 0, 0, 0)

		#Receive up to 15 (3x5) messages. A timeout is used because
		#the response to request 102 may be filtered out by the nat
		#device.
		messages = {}
		lag = None
		for i in range(15):
			try:
				request, host, port = self.recv_message()
				messages[request] = host, port
				
				if not lag:
					lag = int((time.time() - start_time) * 1000)
			except socket.timeout:
				break
		
		#We should always get a response to request 101 and 103
		if not 101 in messages or not 103 in messages:
			raise TimeoutError

		public_address = messages[103]
		nat_filtering = 1 if 102 in messages else 2
		nat_mapping = 1 if messages[101][1] == messages[103][1] else 2
		return NATProperties(public_address, nat_filtering, nat_mapping, lag)
