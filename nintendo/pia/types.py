
from nintendo.nex.common import StationURL
import socket


class Range:
	def __init__(self, min=0, max=10):
		self.min = min
		self.max = max
	
	def __repr__(self):
		return "<Range: %i - %i>" %(self.min, self.max)
	
	def __contains__(self, value):
		return self.min <= value <= self.max


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


class Language:
	ENGLISH = 1
	
class PlayerInfo:
	def __init__(self):
		self.name = None
		self.nickname = None
		self.language = Language.ENGLISH
		self.play_history_key = bytes(64)
		self.info = 0

class IdentificationInfo:
	def __init__(self):
		self.token = None
		self.participants = 1
		self.players = []
		
		
class InetAddress:
	EMPTY = 2
	IPV4 = 6
	IPV6 = 18
	
	def __init__(self, host="0.0.0.0", port=0):
		self.host = host
		self.port = port
		
	def __bool__(self):
		return self.host != "0.0.0.0" or self.port == 0
		
	def get_type(self):
		if self.host == "0.0.0.0":
			return InetAddress.EMPTY
		return InetAddress.IPV4
		
	def encode(self, stream, type=IPV4):
		if type == InetAddress.IPV4:
			stream.write(socket.inet_aton(self.host))
		elif type == InetAddress.IPV6:
			stream.write(socket.inet_aton(self.host))
			stream.pad(12)
		elif type != InetAddress.EMPTY:
			raise ValueError("Invalid InetAddress type: %i" %type)
		stream.u16(self.port)
		
	def decode(self, stream, type=IPV4):
		if type == InetAddress.EMPTY:
			self.host = "0.0.0.0"
		elif type == InetAddress.IPV4:
			self.host = socket.inet_ntoa(stream.read(4))
		elif type == InetAddress.IPV6:
			self.host = socket.inet_ntoa(stream.read(4))
			if stream.read(12) != bytes(12):
				raise ValueError("IPv6 addresses are not supported")
		else:
			raise ValueError("Invalid InetAddress type: %i" %type)
		self.port = stream.u16()
		
		
class StationAddress:
	def __init__(self, host="0.0.0.0", port=0):
		self.address = InetAddress(host, port)
		self.extension_id = 0
		
	def encode(self, stream, type=InetAddress.IPV4):
		stream.add(self.address, type)
		if stream.settings.get("pia.station_extension"):
			stream.u16(self.extension_id)
			
	def decode(self, stream, type=InetAddress.IPV4):
		self.address = stream.extract(InetAddress, type)
		if stream.settings.get("pia.station_extension"):
			self.extension_id = stream.u16()
		
		
class StationLocation:
	def __init__(self):
		self.public = StationAddress()
		self.local = StationAddress()
		self.pid = 0
		self.cid = 0
		self.rvcid = 0
		self.url_type = 0
		self.sid = 0
		self.stream_type = 0
		self.natm = 0
		self.natf = 0
		self.type = 3
		self.probeinit = 0
		self.relay = InetAddress()
		
	def copy(self):
		copy = StationLocation()
		copy.set_station_url(self.get_station_url())
		return copy
		
	def set_station_url(self, url):
		self.public = StationAddress()
		self.local = StationAddress()
		
		if url["type"] == 0:
			self.local.address = InetAddress(url["address"], url["port"])
		else:
			self.public.address = InetAddress(url["address"], url["port"])
		
		self.pid = url["PID"]
		self.cid = url["CID"]
		self.rvcid = url["RVCID"]
		self.url_type = url.get_type_id()
		self.sid = url["sid"]
		self.stream_type = url["stream"]
		self.natm = url["natm"]
		self.natf = url["natf"]
		self.type = url["type"]
		self.probeinit = url["probeinit"]
		
		self.relay = InetAddress(url["Rsa"], url["Rsp"])
		
	def get_station_url(self):
		url = StationURL()
		url.set_type_id(self.url_type)
		if self.type == 0:
			url["address"] = self.local.address.host
			url["port"] = self.local.address.port
		else:
			url["address"] = self.public.address.host
			url["port"] = self.public.address.port
		url["PID"] = self.pid
		url["CID"] = self.cid
		url["RVCID"] = self.rvcid
		url["sid"] = self.sid
		url["stream"] = self.stream_type
		url["natm"] = self.natm
		url["natf"] = self.natf
		url["type"] = self.type
		url["probeinit"] = self.probeinit
		
		url["Rsa"] = self.relay.host
		url["Rsp"] = self.relay.port
		
		return url
		
	def encode(self, stream):
		if stream.settings.get("pia.version") < 51000:
			stream.add(self.public)
		else:
			type_public = InetAddress.IPV4
			type_local = InetAddress.IPV4
			if stream.settings.get("pia.version") >= 51100:
				type_public = self.public.address.get_type()
				type_local = self.local.address.get_type()
				stream.u8(type_public)
				stream.u8(type_local)
			stream.add(self.public, type_public)
			stream.add(self.local, type_local)
			stream.add(self.relay)
		stream.pid(self.pid)
		stream.u32(self.cid)
		stream.u32(self.rvcid)
		if stream.settings.get("pia.version") < 51000:
			stream.u8(self.url_type)
			stream.u8(self.sid)
			stream.u8(self.stream_type)
			stream.u8(self.natm)
			stream.u8(self.natf)
			stream.u8(self.type)
			stream.u8(self.probeinit)
			if stream.settings.get("pia.version") >= 50000:
				stream.add(self.relay)
		else:
			stream.u8((self.natm << 2) | self.natf)
			stream.u8(self.type)
			stream.u8(self.probeinit)
			stream.bool(self.type == 0)
		
	def decode(self, stream):
		if stream.settings.get("pia.version") < 51000:
			self.public = stream.extract(StationAddress)
		else:
			if stream.settings.get("pia.version") >= 51100:
				type_public = stream.u8()
				type_local = stream.u8()
			else:
				type_public = InetAddress.IPV4
				type_local = InetAddress.IPV4
			self.public = stream.extract(StationAddress, type_public)
			self.local = stream.extract(StationAddress, type_local)
			self.relay = stream.extract(InetAddress)
		self.pid = stream.pid()
		self.cid = stream.u32()
		self.rvcid = stream.u32()
		if stream.settings.get("pia.version") < 51000:
			self.url_type = stream.u8()
			self.sid = stream.u8()
			self.stream_type = stream.u8()
			self.natm = stream.u8()
			self.natf = stream.u8()
			self.type = stream.u8()
			self.probeinit = stream.u8()
			if stream.settings.get("pia.version") >= 50000:
				self.relay = stream.extract(InetAddress)
		else:
			natinfo = stream.u8()
			self.natm = natinfo >> 2
			self.natf = natinfo & 3
			self.type = stream.u8()
			self.probeinit = stream.u8()
			stream.skip(1)


class StationConnectionInfo:
	def __init__(self, location=None):
		if location:
			self.public = location.copy()
			self.local = location.copy()
		else:
			self.public = StationLocation()
			self.local = StationLocation()
		self.public.type = 3
		self.local.type = 0
		
	def encode(self, stream):
		stream.add(self.public)
		stream.add(self.local)
		
	def decode(self, stream):
		self.public = stream.extract(StationLocation)
		self.local = stream.extract(StationLocation)
