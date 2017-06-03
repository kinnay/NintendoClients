
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
		
		
		
class StationUrl:
	def __init__(self, string):
		self.string = string
		
	@classmethod
	def make(cls, **kwargs):
		params = ["%s=%s" %(key, item) for key, item in kwargs.items()]
		return cls("prudp:/" + ";".join(params))
		
	def __repr__(self): return self.string
		
	def __getitem__(self, field):
		if field + "=" not in self.string:
			raise KeyError
			
		substr = self.string.split(field + "=")[1]
		return substr[:substr.find(";")] if ";" in substr else substr
		
		
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
