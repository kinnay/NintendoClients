
from proto.nintendo.nex.stream import NexStreamOut
from proto.common.stream import Encoder


class NexEncoder(Encoder):
	version_map = {}

	def init_version(self, nex_version):
		if nex_version not in self.version_map:
			raise ValueError("%s does not support nex version %i" %(self.__class__.__name__, nex_version))
			
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
		30400: -1,
		30504: 0,
		30810: 0
	}
	
	def encode_old(self, stream): pass
	def encode_v0(self, stream): pass


class DataHolder(Encoder):
	def __init__(self, data):
		self.data = data
		
	def encode(self, stream):	
		stream.string(self.data.get_name())
		
		substream = NexStreamOut(stream.version)
		self.data.encode(substream)
		
		stream.u32(len(substream.buffer) + 4)
		stream.data(substream.buffer)
		
		
class StationUrl:
	def __init__(self, string):
		self.string = string
		
	@classmethod
	def make(cls, **kwargs):
		params = ["%s=%s" %(key, item) for key, item in kwargs.items()]
		return cls("prudp:/" + ";".join(params))
		
	def __str__(self): return self.string
		
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
	
	def __str__(self):
		return "%i-%i-%i %i:%02i:%02i" %(self.day(), self.month(), self.year(), self.hour(), self.minute(), self.second())
