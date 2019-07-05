
from nintendo.nex.errors import error_names, error_codes
from nintendo.nex import streams
import datetime, time

import logging
logger = logging.getLogger(__name__)


class RMCError(Exception):
	def __init__(self, code):
		if type(code) == str:
			code = error_codes[code]
		self.error_code = code
		self.error_name = error_names[code]
		
	def __str__(self):
		return "%s (0x%08X)" %(self.error_name, self.error_code)


class RMCResponse:
	pass

	
class Result:
	def __init__(self, code):
		if type(code) == str:
			code = error_codes[code]
		self.error_code = code
		
	def is_success(self):
		return self.error_code == 0x10001
		
	def is_error(self):
		return self.error_code != 0x10001
	
	def code(self):
		return self.error_code
		
	def name(self):
		if self.is_success():
			return "success"
		return error_names.get(self.error_code, "unknown error")
		
	def raise_if_error(self):
		if self.is_error():
			raise RMCError(self.error_code)
	

# Black magic going on here
class Structure:
	def init_version(self, cls, settings):
		nex_version = settings.get("server.version")
		if nex_version < 30500:
			return -1
		else:
			return cls.get_version(self, settings)
			
	def get_version(self, settings): return 0
			
	def get_hierarchy(self):
		hierarchy = []
		cls = self.__class__
		while cls != Structure:
			hierarchy.append(cls)
			cls = cls.__bases__[0]
		return hierarchy[::-1]
	
	def encode(self, stream):
		hierarchy = self.get_hierarchy()
		for cls in hierarchy:
			version = self.init_version(cls, stream.settings)
			if version == -1:
				cls.save(self, stream)
			else:
				substream = streams.StreamOut(stream.settings)
				cls.save(self, substream)
				
				stream.u8(version)
				stream.buffer(substream.get())

	def decode(self, stream):
		hierarchy = self.get_hierarchy()
		for cls in hierarchy:
			expected_version = self.init_version(cls, stream.settings)
			if expected_version == -1:
				cls.load(self, stream)
			else:
				version = stream.u8()
				if version != expected_version:
					logger.warning("Struct %s version (%i) doesn't match expected version (%i)" % (cls.__name__, version, expected_version))
				cls.load(self, stream.substream())
				
	def load(self, stream): raise NotImplementedError("%s.load()" %self.__class__.__name__)
	def save(self, stream): raise NotImplementedError("%s.save()" %self.__class__.__name__)
	
	
class Data(Structure):
	def save(self, stream): pass
	def load(self, stream): pass


class DataHolder:

	object_map = {}

	def __init__(self):
		self.data = None
		
	def encode(self, stream):	
		stream.string(self.data.__class__.__name__)
		
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
		
		
class NullData(Data):
	def save(self, stream): pass
	def load(self, stream): pass
DataHolder.register(NullData, "NullData")
		
		
class StationURL:

	str_params = ["address"]
	int_params = ["port", "stream", "sid", "PID", "CID", "type", "RVCID",
				  "natm", "natf", "upnp", "pmp", "probeinit", "PRID"]
				  
	url_types = {
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

	def __init__(self, scheme="prudp", **kwargs):
		self.scheme = scheme
		self.params = kwargs

	def __repr__(self):
		params = ";".join(
			["%s=%s" %(key, value) for key, value in self.params.items()]
		)
		if self.scheme:
			return "%s:/%s" %(self.scheme, params)
		return params
		
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
		return self.url_types[self.scheme]
		
	def set_type_id(self, id):
		self.scheme = self.url_schemes[id]
		
	def is_public(self): return bool(self["type"] & 2)
	def is_behind_nat(self): return bool(self["type"] & 1)
	def is_global(self): return self.is_public() and not self.is_behind_nat()
		
	def copy(self):
		return StationURL(self.scheme, **self.params)
		
	@classmethod
	def parse(cls, string):
		if string:
			scheme, fields = string.split(":/")
			params = {}
			if fields:
				params = dict(field.split("=") for field in fields.split(";"))
			return cls(scheme, **params)
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
	
	def timestamp(self):
		dt = datetime.datetime(
			self.year(), self.month(), self.day(),
			self.hour(), self.minute(), self.second()
		)
		return dt.timestamp()
	
	def __repr__(self):
		return "%i-%i-%i %i:%02i:%02i" %(self.day(), self.month(), self.year(), self.hour(), self.minute(), self.second())
		
	@classmethod
	def make(cls, day, month, year, hour, minute, second):
		return cls(second | (minute << 6) | (hour << 12) | (day << 17) | (month << 22) | (year << 26))
		
	@classmethod
	def fromtimestamp(cls, timestamp):
		dt = datetime.datetime.fromtimestamp(timestamp)
		return cls.make(dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second)
		
	@classmethod
	def now(cls):
		return cls.fromtimestamp(time.time())
		
		
class ResultRange(Structure):
	def __init__(self, offset, size):
		self.offset = offset
		self.size = size
	
	def save(self, stream):
		stream.u32(self.offset)
		stream.u32(self.size)
