
import socket
import struct


class Range:
	def __init__(self, min=None, max=None):
		self.min = min
		self.max = max


class ResultRange:
	def __init__(self, offset=None, size=None):
		self.offset = offset
		self.size = size


class InetAddress:
	def __init__(self, host=None, port=None):
		self.host = host
		self.port = port
		
	def encode(self, stream):
		stream.write(socket.inet_aton(self.host))
		stream.u16(self.port)
		
	def decode(self, stream):
		self.host = socket.inet_ntoa(stream.read(4))
		self.port = stream.u16()

		
class StationAddress:
	def __init__(self):
		self.address = InetAddress()
		self.extension_id = None
		
	def encode(self, stream):
		stream.add(self.address)
		if stream.settings.get("pia.station_extension"):
			stream.u16(self.extension_id)
			
	def decode(self, stream):
		self.address = stream.extract(InetAddress)
		if stream.settings.get("pia.station_extension"):
			self.extension_id = stream.u16()
