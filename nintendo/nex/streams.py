
from nintendo.nex import common
from anynet import streams


class StreamOut(streams.StreamOut):
	def __init__(self, settings):
		super().__init__("<")
		self.settings = settings
		
	def pid(self, value):
		if self.settings["nex.pid_size"] == 8:
			self.u64(value)
		else:
			self.u32(value)
			
	def result(self, result):
		self.u32(result.code())

	def list(self, list, func):
		self.u32(len(list))
		self.repeat(list, func)
		
	def map(self, map, keyfunc, valuefunc):
		self.u32(len(map))
		for key, value in map.items():
			keyfunc(key)
			valuefunc(value)
		
	def string(self, string):
		if string is None:
			self.u16(0)
		else:
			data = (string + "\0").encode("utf8")
			self.u16(len(data))
			self.write(data)
			
	def stationurl(self, url):
		self.string(str(url))
	
	def datetime(self, datetime):
		self.u64(datetime.value())
		
	def buffer(self, data):
		self.u32(len(data))
		self.write(data)
		
	def qbuffer(self, data):
		self.u16(len(data))
		self.write(data)
		
	def add(self, inst):
		inst.encode(self)
		
	def anydata(self, inst):
		holder = common.DataHolder()
		holder.data = inst
		self.add(holder)
		
	def variant(self, value):
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
	def __init__(self, data, settings):
		super().__init__(data, "<")
		self.settings = settings
		
	def pid(self):
		if self.settings["nex.pid_size"] == 8:
			return self.u64()
		return self.u32()
		
	def result(self):
		return common.Result(self.u32())

	def list(self, func):
		return self.repeat(func, self.u32())
		
	def map(self, keyfunc, valuefunc):
		map = {}
		for i in range(self.u32()):
			key = self.callback(keyfunc)
			value = self.callback(valuefunc)
			map[key] = value
		return map
		
	def repeat(self, func, count):
		return [self.callback(func) for i in range(count)]
		
	def callback(self, func):
		if isinstance(func, type) and issubclass(func, common.Structure):
			return self.extract(func)
		return func()
		
	def string(self):
		length = self.u16()
		if length:
			return self.read(length).decode("utf8")[:-1] #Remove null-terminator
			
	def stationurl(self):
		return common.StationURL.parse(self.string())
		
	def datetime(self):
		return common.DateTime(self.u64())
		
	def buffer(self): return self.read(self.u32())
	def qbuffer(self): return self.read(self.u16())
		
	def substream(self):
		return StreamIn(self.buffer(), self.settings)
	
	def extract(self, cls):
		inst = cls()
		inst.decode(self)
		return inst
		
	def anydata(self):
		return self.extract(common.DataHolder).data
		
	def variant(self):
		type = self.u8()
		if type == 0: return None
		elif type == 1: return self.s64()
		elif type == 2: return self.double()
		elif type == 3: return self.bool()
		elif type == 4: return self.string()
		elif type == 5: return self.datetime()
		elif type == 6: return self.u64()
		raise ValueError("Variant has invalid type id")
