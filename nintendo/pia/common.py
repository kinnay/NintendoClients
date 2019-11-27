
import socket
import struct


class Range:
	def __init__(self, min=0, max=10):
		self.min = min
		self.max = max


class ResultRange:
	def __init__(self, offset=0, size=10):
		self.offset = offset
		self.size = size
		
	def encode(self, stream):
		stream.u32(self.offset)
		stream.u32(self.size)
		
	def decode(self, stream):
		self.offset = stream.u32()
		self.size = stream.u32()


class InetAddress:
	def __init__(self, host=None, port=None):
		self.host = host
		self.port = port
		
	def encode(self, stream):
		stream.write(socket.inet_aton(self.host))
		if stream.settings.get("pia.version") >= 51800:
			stream.write(bytes(12))
		stream.u16(self.port)
		
	def decode(self, stream):
		self.host = socket.inet_ntoa(stream.read(4))
		if stream.settings.get("pia.version") >= 51800:
			if stream.read(12) != bytes(12):
				raise ValueError("IPv6 addresses are not supported")
		self.port = stream.u16()

		
class StationAddress:
	def __init__(self, host=None, port=None):
		self.address = InetAddress(host, port)
		self.extension_id = 0
		
	def encode(self, stream):
		stream.add(self.address)
		if stream.settings.get("pia.station_extension"):
			stream.u16(self.extension_id)
			
	def decode(self, stream):
		self.address = stream.extract(InetAddress)
		if stream.settings.get("pia.station_extension"):
			self.extension_id = stream.u16()
