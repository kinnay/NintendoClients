
from nintendo.nex import common
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
		self.inet = InetAddress(host, port)
		self.extension_id = 0
		
	def encode(self, stream, type=InetAddress.IPV4):
		stream.add(self.inet, type)
		if stream.settings["pia.version"] < 500:
			stream.u16(self.extension_id)
			
	def decode(self, stream, type=InetAddress.IPV4):
		self.inet = stream.extract(InetAddress, type)
		if stream.settings["pia.version"] < 500:
			self.extension_id = stream.u16()
		
		
class StationLocation:
	url_types = {
		None: 0,
		"prudp": 1,
		"prudps": 2,
		"udp": 3
	}
	
	url_schemes = {
		0: None,
		1: "prudp",
		2: "prudps",
		3: "udp"
	}
	
	def __init__(self):
		self.public = StationAddress()
		self.local = StationAddress()
		self.pid = 0
		self.cid = 0
		self.rvcid = 0
		self.scheme = 0
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
			self.local.inet = InetAddress(url["address"], url["port"])
		else:
			self.public.inet = InetAddress(url["address"], url["port"])
		
		self.pid = url["PID"]
		self.cid = url["CID"]
		self.rvcid = url["RVCID"]
		self.scheme = self.url_types[url.scheme()]
		self.sid = url["sid"]
		self.stream_type = url["stream"]
		self.natm = url["natm"]
		self.natf = url["natf"]
		self.type = url["type"]
		self.probeinit = url["probeinit"]
		
		self.relay = InetAddress(url["Rsa"], url["Rsp"])
		
	def get_station_url(self):
		url = common.StationURL(self.url_schemes[self.scheme])
		if self.type == 0:
			url["address"] = self.local.inet.host
			url["port"] = self.local.inet.port
		else:
			url["address"] = self.public.inet.host
			url["port"] = self.public.inet.port
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
		if stream.settings["pia.version"] < 510:
			stream.add(self.public)
		else:
			type_public = InetAddress.IPV4
			type_local = InetAddress.IPV4
			if stream.settings["pia.version"] >= 511:
				type_public = self.public.inet.get_type()
				type_local = self.local.inet.get_type()
				stream.u8(type_public)
				stream.u8(type_local)
			stream.add(self.public, type_public)
			stream.add(self.local, type_local)
			stream.add(self.relay)
		stream.pid(self.pid)
		stream.u32(self.cid)
		stream.u32(self.rvcid)
		if stream.settings["pia.version"] < 510:
			stream.u8(self.scheme)
			stream.u8(self.sid)
			stream.u8(self.stream_type)
			stream.u8(self.natm)
			stream.u8(self.natf)
			stream.u8(self.type)
			stream.u8(self.probeinit)
			if stream.settings["pia.version"] >= 500:
				stream.add(self.relay)
		else:
			stream.u8((self.natm << 2) | self.natf)
			stream.u8(self.type)
			stream.u8(self.probeinit)
			stream.bool(self.type == 0)
		
	def decode(self, stream):
		if stream.settings["pia.version"] < 510:
			self.public = stream.extract(StationAddress)
		else:
			if stream.settings["pia.version"] >= 511:
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
		if stream.settings["pia.version"] < 510:
			self.scheme = stream.u8()
			self.sid = stream.u8()
			self.stream_type = stream.u8()
			self.natm = stream.u8()
			self.natf = stream.u8()
			self.type = stream.u8()
			self.probeinit = stream.u8()
			if stream.settings["pia.version"] >= 500:
				self.relay = stream.extract(InetAddress)
		else:
			natinfo = stream.u8()
			self.natm = natinfo >> 2
			self.natf = natinfo & 3
			self.type = stream.u8()
			self.probeinit = stream.u8()
			stream.skip(1)
