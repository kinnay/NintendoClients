
import struct


class StreamOut:
	def __init__(self):
		self.buffer = b""
		
	def u8(self, value): self.buffer += struct.pack("B", value)
	def u16(self, value): self.buffer += struct.pack("H", value)
	def u32(self, value): self.buffer += struct.pack("I", value)
	def u64(self, value): self.buffer += struct.pack("Q", value)
	
	def double(self, value): self.buffer += struct.pack("d", value)
	
	def bool(self, value): self.u8(1 if value else 0)
	
	def list(self, list, func, length_func):
		if length_func:
			length_func(len(list))
		for i in list:
			func(i)
	
	def string(self, string, length_func, null_terminate=True):
		if null_terminate:
			string += "\x00"
		self.data(string.encode("ascii"), length_func)
		
	def data(self, data, length_func):
		if length_func:
			length_func(len(data))
		self.buffer += data


class StreamIn:
	def __init__(self, data):
		self.buffer = data
		self.pos = 0
		
	def read(self, num):
		data = self.buffer[self.pos : self.pos + num]
		self.pos += num
		return data
		
	def u8(self): return self.read(1)[0]
	def u16(self): return struct.unpack("H", self.read(2))[0]
	def u32(self): return struct.unpack("I", self.read(4))[0]
	def u64(self): return struct.unpack("Q", self.read(8))[0]
	
	def double(self): return struct.unpack("d", self.read(8))[0]
	
	def bool(self): return bool(self.u8())
	
	def list(self, func, length_func):
		return [func() for i in range(length_func())]
	
	def string(self, length_func, null_terminated=True):
		data = self.read(length_func())
		if null_terminated:
			data = data[:-1]
		return data.decode("ascii")
	
	def substream(self):
		return StreamIn(self.read(self.u32()))
		
		
class Encoder:
	@classmethod
	def from_stream(cls, stream):
		instance = cls()
		instance.decode(stream)
		return instance

	@classmethod
	def from_data(cls, data):
		return cls.from_stream(StreamIn(data))
		
	def encode(self, stream): raise NotImplementedError
	def decode(self, stream): raise NotImplementedError
