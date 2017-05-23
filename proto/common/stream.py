
import struct


class StreamOut:
	def __init__(self):
		self.buffer = b""
		self.pos = 0
		
	def seek(self, pos): self.pos = pos
	def tell(self): return self.pos
		
	def write(self, data):
		self.buffer = self.buffer[:self.pos] + data + self.buffer[self.pos + len(data):]
		self.pos += len(data)
		
	def u8(self, value): self.write(bytes([value]))
	def u16(self, value): self.write(struct.pack("H", value))
	def u32(self, value): self.write(struct.pack("I", value))
	def u64(self, value): self.write(struct.pack("Q", value))
	
	def s8(self, value): self.write(struct.pack("b", value))
	def s16(self, value): self.write(struct.pack("h", value))
	def s32(self, value): self.write(struct.pack("i", value))
	def s64(self, value): self.write(struct.pack("q", value))
	
	def float(self, value): self.write(struct.pack("f", value))
	def double(self, value): self.write(struct.pack("d", value))
	
	def bool(self, value): self.u8(1 if value else 0)
	
	def list(self, list, func):
		for i in list:
			func(i)
	
	def ascii(self, data):
		self.write(data.encode("ascii"))


class StreamIn:
	def __init__(self, data):
		self.buffer = data
		self.pos = 0
		
	def seek(self, pos): self.pos = pos
	def tell(self): return self.pos
		
	def read(self, num):
		data = self.buffer[self.pos : self.pos + num]
		self.pos += num
		return data
		
	def u8(self): return self.read(1)[0]
	def u16(self): return struct.unpack("H", self.read(2))[0]
	def u32(self): return struct.unpack("I", self.read(4))[0]
	def u64(self): return struct.unpack("Q", self.read(8))[0]
	
	def s8(self): return struct.unpack("b", self.read(1))[0]
	def s16(self): return struct.unpack("h", self.read(2))[0]
	def s32(self): return struct.unpack("i", self.read(4))[0]
	def s64(self): return struct.unpack("q", self.read(8))[0]
	
	def float(self): return struct.unpack("f", self.read(4))[0]
	def double(self): return struct.unpack("d", self.read(8))[0]
	
	def bool(self): return bool(self.u8())
	
	def list(self, func, count):
		return [func() for i in range(count)]
	
	def ascii(self, num):
		return self.read(num).decode("ascii")
		
		
class Encoder:
	@classmethod
	def from_stream(cls, stream, *args):
		instance = cls()
		instance.decode(stream, *args)
		return instance
		
	def encode(self, stream, *args): raise NotImplementedError
	def decode(self, stream, *args): raise NotImplementedError
