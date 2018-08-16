
from nintendo.nex import streams

import logging
logger = logging.getLogger(__name__)


# Black magic going on here
class Structure:
	def init_version(self, cls):
		if self.nex_version < 30500:
			self.version = -1
		else:
			self.version = cls.get_version(self)
			
	def get_version(self): return 0
			
	def get_hierarchy(self):
		hierarchy = []
		cls = self.__class__
		while cls != Structure:
			hierarchy.append(cls)
			cls = cls.__bases__[0]
		return hierarchy[::-1]
	
	def encode(self, stream):
		self.nex_version = stream.settings.get("server.version")
		hierarchy = self.get_hierarchy()
		for cls in hierarchy:
			self.init_version(cls)
			if self.version == -1:
				cls.save(self, stream)
			else:
				substream = streams.StreamOut(stream.settings)
				cls.save(self, substream)
				
				stream.u8(self.version)
				stream.buffer(substream.get())

	def decode(self, stream):
		self.nex_version = stream.settings.get("server.version")
		hierarchy = self.get_hierarchy()
		for cls in hierarchy:
			self.init_version(cls)
			if self.version == -1:
				cls.load(self, stream)
			else:
				version = stream.u8()
				if version != self.version:
					logger.warning("Struct version (%i) doesn't match expected version (%i)" %(version, self.version))
					self.version = version
				cls.load(self, stream.substream())
				
	def load(self, stream): raise NotImplementedError("%s.load()" %self.__class__.__name__)
	def save(self, stream): raise NotImplementedError("%s.save()" %self.__class__.__name__)
	
	
class Data(Structure):
	def save(self, stream): pass
	def load(self, stream): pass


class DataHolder:

	object_map = {}

	def __init__(self, data):
		self.data = data
		
	def encode(self, stream):	
		stream.string(self.data.get_name())
		
		substream = streams.StreamOut(stream.settings)
		substream.add(self.data)
		
		stream.u32(len(substream.get()) + 4)
		stream.buffer(substream.get())
		
	def decode(self, stream):
		name = stream.string()
		substream = stream.substream().substream()
		self.data = substream.extract(self.object_map[name])
		
	@classmethod
	def register(cls, object, name):
		cls.object_map[name] = object
		
		
class StationUrl:

	str_params = ["address"]
	int_params = ["port", "stream", "sid", "PID", "CID", "type", "RVCID",
				  "natm", "natf", "upnp", "pmp", "probeinit", "PRID"]
				  
	url_types = {
		"prudp": 1,
		"prudps": 2,
		"udp": 3
	}
	
	url_schemes = {
		1: "prudp",
		2: "prudps",
		3: "udp"
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
		
	def get_address(self):
		return self["address"], self["port"]
		
	def get_type_id(self):
		return self.url_types[self.url_type]
		
	def set_type_id(self, id):
		self.url_type = self.url_schemes[id]
		
	def is_public(self): return bool(self["type"] & 2)
	def is_behind_nat(self): return bool(self["type"] & 1)
	def is_global(self): return self.is_public() and not self.is_behind_nat()
		
	def copy(self):
		return StationUrl(self.url_type, **self.params)
		
	@classmethod
	def parse(cls, string):
		if string:
			url_type, fields = string.split(":/")
			params = {}
			if fields:
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
		
		
class ResultRange(Structure):
	def __init__(self, offset, size):
		self.offset = offset
		self.size = size
	
	def save(self, stream):
		stream.u32(self.offset)
		stream.u32(self.size)
