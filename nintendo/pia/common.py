
import collections
import socket
import struct

class InetAddress(collections.namedtuple("InetAddress", "host port")):
	@classmethod
	def deserialize(cls, data):
		host = socket.inet_ntoa(data[:4])
		port = struct.unpack_from(">H", data, 4)[0]
		return cls(host, port)
		
	def serialize(self):
		return socket.inet_aton(self.host) + struct.pack(">H", self.port)

	@staticmethod
	def sizeof(): return 6


class StationAddress(collections.namedtuple("StationAddress", "address extension_id")):
	@classmethod
	def deserialize(cls, data):
		address = InetAddress.deserialize(data)
		extid = struct.unpack_from(">H", data, address.sizeof())[0]
		return cls(address, extid)
		
	def serialize(self):
		return self.address.serialize() + struct.pack(">H", self.extension_id)
		
	@staticmethod
	def sizeof(): return InetAddress.sizeof() + 2
