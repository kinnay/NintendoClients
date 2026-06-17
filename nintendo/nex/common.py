
from nintendo.nex.errors import error_names, error_codes
from nintendo.nex import settings, streams
from typing import Self

import datetime
import time

import logging
logger = logging.getLogger(__name__)


ERROR_MASK = 1 << 31


class RMCError(Exception):
	_result: Result

	def __init__(self, code: str | int = "Core::Unknown"):
		self._result = Result.error(code)
	
	def __str__(self) -> str:
		return str(self._result)
	
	def result(self) -> Result:
		return self._result
		
	def name(self) -> str:
		return self._result.name()
	
	def code(self) -> int:
		return self._result.code()


class Result:
	_code: int

	def __init__(self, code: int = 0x10001):
		self._code = code
	
	def __str__(self):
		return f"{self.name()} (0x{self.code():08X})"
		
	@classmethod
	def success(cls, code: str | int = "Core::Unknown") -> Self:
		if isinstance(code, str):
			code = error_codes[code]
		return cls(code & ~ERROR_MASK)
		
	@classmethod
	def error(cls, code: str | int = "Core::Unknown") -> Self:
		if isinstance(code, str):
			code = error_codes[code]
		return cls(code | ERROR_MASK)
	
	def is_success(self) -> bool:
		return not self._code & ERROR_MASK
		
	def is_error(self) -> bool:
		return bool(self._code & ERROR_MASK)
	
	def code(self) -> int:
		return self._code
		
	def name(self) -> str:
		if self.is_success():
			return "success"
		return error_names.get(self._code & ~ERROR_MASK, "unknown error")
		
	def raise_if_error(self) -> None:
		if self.is_error():
			raise RMCError(self._code)


# Black magic going on here
class Structure:
	def max_version(self, settings: settings.Settings) -> int:
		return 0
			
	def _get_hierarchy(self) -> list[type[Structure]]:
		hierarchy = []
		cls = self.__class__
		while cls != Structure:
			hierarchy.append(cls)
			cls = cls.__bases__[0]
		return hierarchy[::-1]
	
	def encode(self, stream: streams.StreamOut) -> None:
		hierarchy = self._get_hierarchy()
		for cls in hierarchy:
			if stream.settings["nex.struct_header"]:
				version = cls.max_version(self, stream.settings)
				
				substream = streams.StreamOut(stream.settings)
				cls.save(self, substream, version)
				
				stream.u8(version)
				stream.buffer(substream.get())
			else:
				cls.save(self, stream, 0)

	def decode(self, stream: streams.StreamIn) -> None:
		hierarchy = self._get_hierarchy()
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
				
	def load(self, stream: streams.StreamIn, version: int) -> None:
		raise NotImplementedError("%s.load()" %self.__class__.__name__)
	
	def save(self, stream: streams.StreamOut, version: int) -> None:
		raise NotImplementedError("%s.save()" %self.__class__.__name__)
	
	
class Data(Structure):
	def save(self, stream: streams.StreamOut, version: int) -> None:
		pass

	def load(self, stream: streams.StreamIn, version: int) -> None:
		pass


class DataHolder:
	_object_map: dict[str, type[Structure]] = {}

	data: Structure

	def __init__(self):
		self.data = Data()
		
	def encode(self, stream: streams.StreamOut):
		stream.string(self.data.__class__.__name__)
		
		substream = streams.StreamOut(stream.settings)
		substream.add(self.data)
		
		stream.u32(len(substream.get()) + 4)
		stream.buffer(substream.get())
		
	def decode(self, stream: streams.StreamIn) -> None:
		name = stream.string()
		substream = stream.substream().substream()
		self.data = substream.extract(self._object_map[name])
		
	@classmethod
	def register(cls, object: type[Structure], name: str) -> None:
		cls._object_map[name] = object
		
		
class NullData(Data):
	def load(self, stream: streams.StreamIn, version: int) -> None: pass
	def save(self, stream: streams.StreamOut, version: int) -> None: pass
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
	_value: int

	def __init__(self, value: int):
		self._value = value
		
	def second(self) -> int: return self._value & 63
	def minute(self) -> int: return (self._value >> 6) & 63
	def hour(self) -> int: return (self._value >> 12) & 31
	def day(self) -> int: return (self._value >> 17) & 31
	def month(self) -> int: return (self._value >> 22) & 15
	def year(self) -> int: return self._value >> 26
	
	def value(self) -> int: return self._value

	def standard_datetime(self) -> datetime.datetime:
		return datetime.datetime(
			self.year(), self.month(), self.day(),
			self.hour(), self.minute(), self.second(),
			tzinfo=datetime.UTC
		)
	
	def timestamp(self) -> int:
		return int(self.standard_datetime().timestamp())
	
	def __repr__(self) -> str:
		return "%i-%i-%i %i:%02i:%02i" %(
			self.day(), self.month(), self.year(),
			self.hour(), self.minute(), self.second()
		)

	@classmethod
	def never(cls) -> Self:
		return cls(0)
	
	@classmethod
	def future(cls) -> Self:
		return cls.make(9999, 12, 31, 23, 59, 59)
		
	@classmethod
	def make(
		cls, year: int, month: int = 1, day: int = 1, hour: int = 0,
		minute: int = 0, second: int = 0
	) -> Self:
		return cls(second | (minute << 6) | (hour << 12) | (day << 17) | (month << 22) | (year << 26))
		
	@classmethod
	def fromtimestamp(cls, timestamp: float) -> Self:
		dt = datetime.datetime.fromtimestamp(timestamp, datetime.UTC)
		return cls.make(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
	
	@classmethod
	def now(cls) -> Self:
		return cls.fromtimestamp(time.time())
		
		
class ResultRange(Structure):
	offset: int
	size: int

	def __init__(self, offset: int = 0, size: int = 10):
		self.offset = offset
		self.size = size

	def load(self, stream: streams.StreamIn, version: int) -> None:
		self.offset = stream.u32()
		self.size = stream.u32()
	
	def save(self, stream: streams.StreamOut, version: int) -> None:
		stream.u32(self.offset)
		stream.u32(self.size)
