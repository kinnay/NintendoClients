
from anynet import streams
from nintendo.nex import common, settings
from typing import Any, Callable


List = list
Settings = settings.Settings


class StreamOut(streams.StreamOut):
	settings: Settings

	def __init__(self, settings: Settings):
		super().__init__("<")
		self.settings = settings
		
	def pid(self, value: int) -> None:
		if self.settings["nex.pid_size"] == 8:
			self.u64(value)
		else:
			self.u32(value)
			
	def result(self, result: common.Result) -> None:
		self.u32(result.code())

	def list[T](self, list: List[T], func: Callable[[T], None]) -> None:
		self.u32(len(list))
		self.repeat(list, func)
		
	def map[K, V](
		self, map: dict[K, V], keyfunc: Callable[[K], None],
		valuefunc: Callable[[V], None]
	) -> None:
		self.u32(len(map))
		for key, value in map.items():
			keyfunc(key)
			valuefunc(value)
	
	def string(self, string: str) -> None:
		if string is None:
			self.u16(0)
		else:
			data = (string + "\0").encode("utf8")
			self.u16(len(data))
			self.write(data)
			
	def stationurl(self, url: common.StationURL) -> None:
		self.string(str(url))
	
	def datetime(self, datetime: common.DateTime) -> None:
		self.u64(datetime.value())
		
	def buffer(self, data: bytes) -> None:
		self.u32(len(data))
		self.write(data)
		
	def qbuffer(self, data: bytes) -> None:
		self.u16(len(data))
		self.write(data)
		
	def add(self, inst: common.Structure) -> None:
		inst.encode(self)
		
	def anydata(self, inst: common.Data) -> None:
		holder = common.DataHolder()
		holder.data = inst
		holder.encode(self)
	
	def variant(self, value: Any) -> None:
		# We have to check for bool before int,
		# because bool is a subclass of int
		if value is None: self.u8(0)
		elif isinstance(value, bool):
			self.u8(3)
			self.bool(value)
		elif isinstance(value, int):
			if value < 0:
				self.u8(1)
				self.s64(value)
			else:
				self.u8(6)
				self.u64(value)
		elif isinstance(value, float):
			self.u8(2)
			self.double(value)
		elif isinstance(value, str):
			self.u8(4)
			self.string(value)
		elif isinstance(value, common.DateTime):
			self.u8(5)
			self.datetime(value)
		else:
			raise TypeError("Type is not compatible with 'variant'")
		
		
class StreamIn(streams.StreamIn):
	def __init__(self, data: bytes, settings: settings.Settings):
		super().__init__(data, "<")
		self.settings = settings
		
	def pid(self) -> int:
		if self.settings["nex.pid_size"] == 8:
			return self.u64()
		return self.u32()
		
	def result(self) -> common.Result:
		return common.Result(self.u32())

	def list[T](self, func: Callable[[], T]) -> List[T]:
		return self.repeat(func, self.u32())
		
	def map[K, V](
		self, keyfunc: Callable[[], K], valuefunc: Callable[[], V]
	) -> dict[K, V]:
		map = {}
		for i in range(self.u32()):
			key = self.callback(keyfunc)
			value = self.callback(valuefunc)
			map[key] = value
		return map
		
	def repeat(self, func: Callable[[], Any], count: int) -> List[Any]:
		return [self.callback(func) for i in range(count)]
		
	def callback(self, func: Callable[[], Any]) -> Any:
		if isinstance(func, type) and issubclass(func, common.Structure):
			return self.extract(func)
		return func()
		
	def string(self) -> str:
		length = self.u16()
		if length:
			return self.read(length).decode("utf8")[:-1] #Remove null-terminator
		return ""
			
	def stationurl(self) -> common.StationURL:
		return common.StationURL.parse(self.string())
		
	def datetime(self) -> common.DateTime:
		return common.DateTime(self.u64())
		
	def buffer(self) -> bytes:
		return self.read(self.u32())
	
	def qbuffer(self) -> bytes:
		return self.read(self.u16())
		
	def substream(self) -> StreamIn:
		return StreamIn(self.buffer(), self.settings)
	
	def extract[T: common.Structure](self, cls: type[T]) -> T:
		inst = cls()
		inst.decode(self)
		return inst
		
	def anydata(self) -> common.Structure:
		data = common.DataHolder()
		data.decode(self)
		return data.data
	
	def variant(self) -> Any:
		type = self.u8()
		if type == 0: return None
		elif type == 1: return self.s64()
		elif type == 2: return self.double()
		elif type == 3: return self.bool()
		elif type == 4: return self.string()
		elif type == 5: return self.datetime()
		elif type == 6: return self.u64()
		raise ValueError("Variant has invalid type id")
