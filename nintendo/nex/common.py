
from nintendo.nex.errors import error_names, error_codes
from nintendo.nex import streams
import datetime, time

import logging
logger = logging.getLogger(__name__)


ERROR_MASK = 1 << 31

class RMCError(Exception):
	def __init__(self, code="Core::Unknown"):
		self.res = Result.error(code)
	
	def __str__(self):
		return str(self.res)
	
	def result(self):
		return self.res
		
	def name(self):
		return self.res.name()
	
	def code(self):
		return self.res.code()

	
class Result:
	def __init__(self, code=0x10001):
		self.error_code = code
	
	def __str__(self):
		return "%s (0x%08X)" %(self.name(), self.code())
		
	@staticmethod
	def success(code="Core::Unknown"):
		if type(code) == str:
			code = error_codes[code]
		return Result(code & ~ERROR_MASK)
		
	@staticmethod
	def error(code="Core::Unknown"):
		if type(code) == str:
			code = error_codes[code]
		return Result(code | ERROR_MASK)
	
	def is_success(self):
		return not self.error_code & ERROR_MASK
		
	def is_error(self):
		return bool(self.error_code & ERROR_MASK)
	
	def code(self):
		return self.error_code
		
	def name(self):
		if self.is_success():
			return "success"
		return error_names.get(self.error_code & ~ERROR_MASK, "unknown error")
		
	def raise_if_error(self):
		if self.is_error():
			raise RMCError(self.error_code)


# Black magic going on here
class Structure:
	def max_version(self, settings): return 0
			
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
			if stream.settings["nex.struct_header"]:
				version = cls.max_version(self, stream.settings)
				
				substream = streams.StreamOut(stream.settings)
				cls.save(self, substream, version)
				
				stream.u8(version)
				stream.buffer(substream.get())
			else:
				cls.save(self, stream, 0)

	def decode(self, stream):
		hierarchy = self.get_hierarchy()
		for cls in hierarchy:
			if stream.settings["nex.struct_header"]:
				max_version = cls.max_version(self, stream.settings)
				
				version = stream.u8()
				if version > max_version:
					logger.warning(
						"Struct %s version is higher than expected (%i > %i)",
						cls.__name__, version, max_version
					)
					
				substream = stream.substream()
				cls.load(self, substream, version)
				
				if not substream.eof():
					logger.warning(
						"Struct %s has unexpected size (got %i bytes, but only %i were read)",
						cls.__name__, substream.size(), substream.tell()
					)
			else:
				cls.load(self, stream, 0)
				
	def load(self, stream, version): raise NotImplementedError("%s.load()" %self.__class__.__name__)
	def save(self, stream, version): raise NotImplementedError("%s.save()" %self.__class__.__name__)
	
	
class Data(Structure):
	def save(self, stream, version): pass
	def load(self, stream, version): pass


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
	def save(self, stream, version): pass
	def load(self, stream, version): pass
DataHolder.register(NullData, "NullData")
		
		
class StationURL:

	str_params = ["address", "Uri", "Rsa", "Ra", "Ntrpa"]
	int_params = [
		"port", "stream", "sid", "PID", "CID", "type", "RVCID",
		"natm", "natf", "upnp", "pmp", "probeinit", "PRID",
		"fastproberesponse", "NodeID", "R", "Rsp", "Rp",
		"Tpt", "Pl", "Ntrpp"
	]

	def __init__(self, scheme="prudp", **kwargs):
		self.urlscheme = scheme
		self.params = kwargs

	def __repr__(self):
		params = ";".join(
			["%s=%s" %(key, value) for key, value in self.params.items()]
		)
		if self.urlscheme:
			return "%s:/%s" %(self.urlscheme, params)
		return params
		
	def __getitem__(self, field):
		if field in self.str_params:
			return str(self.params.get(field, ""))
		if field in self.int_params:
			return int(self.params.get(field, 0))
		raise KeyError(field)
		
	def __setitem__(self, field, value):
		self.params[field] = value
	
	def scheme(self):
		return self.urlscheme
		
	def address(self):
		return self["address"], self["port"]
		
	def is_public(self): return bool(self["type"] & 2)
	def is_behind_nat(self): return bool(self["type"] & 1)
	def is_global(self): return self.is_public() and not self.is_behind_nat()
		
	def copy(self):
		return StationURL(self.urlscheme, **self.params)
		
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
		self.val = value
		
	def second(self): return self.val & 63
	def minute(self): return (self.val >> 6) & 63
	def hour(self): return (self.val >> 12) & 31
	def day(self): return (self.val >> 17) & 31
	def month(self): return (self.val >> 22) & 15
	def year(self): return self.val >> 26
	
	def value(self): return self.val

	def standard_datetime(self):
		return datetime.datetime(
			self.year(), self.month(), self.day(),
			self.hour(), self.minute(), self.second(),
			tzinfo=datetime.timezone.utc
		)
	
	def timestamp(self):
		return int(self.standard_datetime().replace(tzinfo=None).timestamp())
	
	def __repr__(self):
		return "%i-%i-%i %i:%02i:%02i" %(self.day(), self.month(), self.year(), self.hour(), self.minute(), self.second())
		
	@classmethod
	def never(cls):
		return cls(0)
	
	@classmethod
	def future(cls):
		return cls.make(9999, 12, 31, 23, 59, 59)
		
	@classmethod
	def make(cls, year, month=1, day=1, hour=0, minute=0, second=0):
		return cls(second | (minute << 6) | (hour << 12) | (day << 17) | (month << 22) | (year << 26))
		
	@classmethod
	def fromtimestamp(cls, timestamp):
		dt = datetime.datetime.fromtimestamp(timestamp)
		return cls.make(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
	
	@classmethod
	def now(cls):
		return cls.fromtimestamp(time.time())
		
		
class ResultRange(Structure):
	def __init__(self, offset=0, size=10):
		self.offset = offset
		self.size = size

	def load(self, stream, version):
		self.offset = stream.u32()
		self.size = stream.u32()
	
	def save(self, stream, version):
		stream.u32(self.offset)
		stream.u32(self.size)
