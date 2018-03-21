
from nintendo.nex import streams

import logging
logger = logging.getLogger(__name__)


class Structure:
	def init_version(self, nex_version):
		self.nex_version = nex_version
		if nex_version < 30500:
			self.version = -1
		else:
			self.version = self.get_version(nex_version)
			
	def get_version(self, nex_version):
		return 0

	def encode(self, stream):
		self.init_version(stream.settings.get("server.version"))
		if self.version == -1:
			self.streamin(stream)
		else:
			substream = streams.StreamOut(stream.settings)
			self.streamin(substream)
			
			stream.u8(self.version)
			stream.buffer(substream.data)

	def decode(self, stream):
		self.init_version(stream.settings.get("server.version"))
		if self.version == -1:
			self.streamout(stream)
			
		else:
			version = stream.u8()
			if version != self.version:
				logger.info("Structure version (%i) doesn't match expected version (%i)" %(version, self.version))
				self.version = version
			self.streamout(stream.substream())
			
	def streamin(self, stream): raise NotImplementedError("Structure.streamin")
	def streamout(self, stream): raise NotImplementedError("Structure.streamout")
	
	
class DataObj(Structure):
	def streamin(self, stream): pass
	def streamout(self, stream): pass
	
	
class Data(Structure):
	def encode(self, stream):
		stream.add(DataObj())
		super().encode(stream)
		
	def decode(self, stream):
		stream.extract(DataObj)
		super().decode(stream)


class DataHolder:

	object_map = {}

	def __init__(self, data):
		self.data = data
		
	def encode(self, stream):	
		stream.string(self.data.get_name())
		
		substream = streams.StreamOut(stream.settings)
		substream.add(self.data)
		
		stream.u32(len(substream.data) + 4)
		stream.buffer(substream.data)
		
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
