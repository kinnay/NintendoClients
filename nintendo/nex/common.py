
from nintendo.nex.stream import NexStreamOut
from nintendo.common.stream import Encoder


class NexEncoder(Encoder):
	version_map = {}

	def init_version(self, nex_version):
		if nex_version < 30500:
			self.version = -1
		else:
			self.version = self.version_map[nex_version]

	def encode(self, stream):
		self.init_version(stream.version)
		if self.version == -1:
			self.encode_old(stream)
			
		else:
			substream = NexStreamOut(stream.version)
			getattr(self, "encode_v%i" %self.version)(substream)

			stream.u8(self.version)
			stream.data(substream.buffer)
			
	def decode(self, stream):
		self.init_version(stream.version)
		if self.version == -1:
			self.decode_old(stream)
			
		else:
			version = stream.u8()
			if version != self.version:
				raise ValueError("Wrong version number in %s" %(self.__class__.__name__))
			getattr(self, "decode_v%i" %self.version)(stream.substream())
	
	
class NexData(NexEncoder):
	version_map = {
		30504: 0,
		30810: 0
	}
	
	def encode_old(self, stream): pass
	def encode_v0(self, stream): pass
	def decode_old(self, stream): pass
	def decode_v0(self, stream): pass
	
	
class NexDataEncoder(NexEncoder):
	def encode(self, stream):
		NexData().encode(stream)
		super().encode(stream)
		
	def decode(self, stream):
		NexData.from_stream(stream)
		super().decode(stream)


class DataHolder(Encoder):

	object_map = {}

	def init(self, data):
		self.data = data
		
	def encode(self, stream):	
		stream.string(self.data.get_name())
		
		substream = NexStreamOut(stream.version)
		self.data.encode(substream)
		
		stream.u32(len(substream.buffer) + 4)
		stream.data(substream.buffer)
		
	def decode(self, stream):
		name = stream.string()
		substream = stream.substream().substream()
		self.data = self.object_map[name].from_stream(substream)
		
	@classmethod
	def register(cls, object, name):
		cls.object_map[name] = object
		
		
class KeyValue(NexEncoder):
	version_map = {
		30504: 0
	}
	
	def decode_old(self, stream):
		self.key = stream.string()
		self.value = stream.string()
		
	decode_v0 = decode_old
		
		
class StationUrl:

	str_params = ["address"]
	int_params = ["port", "stream", "sid", "PID", "CID", "type", "RVCID",
				  "natm", "natf", "upnp", "pmp", "probeinit", "PRID"]
				  
	url_types = {
		"prudp": 1,
		"prudps": 2,
		"udp": 3
	}

	def __init__(self, url_type="prudp", **kwargs):
		self.url_type = url_type
		self.params = kwargs

	def __repr__(self):
		params = ["%s=%s" %(key, value) for key, value in self.params.items()]
		return self.url_type + ":/" + ";".join(params)
		
	def __getitem__(self, field):
		if field in self.str_params:
			return str(self.params.get(field, ""))
		if field in self.int_params:
			return int(self.params.get(field, 0))
		raise KeyError(field)
		
	def __setitem__(self, field, value):
		self.params[field] = value
		
	def get_type_id(self):
		return self.url_types[self.url_type]
		
	def copy(self):
		return StationUrl(self.url_type, **self.params)
		
	@classmethod
	def parse(cls, string):
		if string:
			url_type, fields = string.split(":/")
			params = dict(field.split("=") for field in fields.split(";"))
			return cls(url_type, **params)
		else:
			return cls()

		
class DateTime:
	def __init__(self, value):
		self.value = value
		
	def second(self): return self.value & 63
	def minute(self): return (self.value >> 6) & 63
	def hour(self): return (self.value >> 12) & 31
	def day(self): return (self.value >> 17) & 31
	def month(self): return (self.value >> 22) & 15
	def year(self): return self.value >> 26
	
	def __repr__(self):
		return "%i-%i-%i %i:%02i:%02i" %(self.day(), self.month(), self.year(), self.hour(), self.minute(), self.second())
		
	@classmethod
	def make(cls, day, month, year, hour, minute, second):
		return cls(second | (minute << 6) | (hour << 12) | (day << 17) | (month << 22) | (year << 26))
