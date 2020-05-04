
import struct


class StreamOut:
	def __init__(self, endian="<"):
		self.endian = endian
		self.data = bytearray()
		self.pos = 0
		self.stack = []
		
	def push(self): self.stack.append(self.pos)
	def pop(self): self.pos = self.stack.pop()
		
	def get(self): return bytes(self.data)
	def size(self): return len(self.data)
	def tell(self): return self.pos
	def seek(self, pos):
		if pos > len(self.data):
			self.pad(len(self.data) - pos)
		self.pos = pos
	def skip(self, num): self.seek(self.pos + num)
	def align(self, num): self.skip((num - self.pos % num) % num)
	def eof(self): return self.pos >= len(self.data)
		
	def write(self, data):
		self.data[self.pos : self.pos + len(data)] = data
		self.pos += len(data)
		
	def pad(self, num, char=b"\0"):
		self.write(char * num)
		
	def ascii(self, data):
		self.write(data.encode("ascii"))
		
	def u8(self, value): self.write(bytes([value]))
	def u16(self, value): self.write(struct.pack(self.endian + "H", value))
	def u32(self, value): self.write(struct.pack(self.endian + "I", value))
	def u64(self, value): self.write(struct.pack(self.endian + "Q", value))
	
	def s8(self, value): self.write(struct.pack("b", value))
	def s16(self, value): self.write(struct.pack(self.endian + "h", value))
	def s32(self, value): self.write(struct.pack(self.endian + "i", value))
	def s64(self, value): self.write(struct.pack(self.endian + "q", value))
	
	def u24(self, value):
		if self.endian == ">":
			self.u16(value >> 8)
			self.u8(value & 0xFF)
		else:
			self.u8(value & 0xFF)
			self.u16(value >> 8)
			
	def float(self, value): self.write(struct.pack(self.endian + "f", value))
	def double(self, value): self.write(struct.pack(self.endian + "d", value))
	
	def bool(self, value): self.u8(1 if value else 0)
	def char(self, value): self.u8(ord(value))
	def wchar(self, value): self.u16(ord(value))
	
	def chars(self, data): self.repeat(data, self.char)
	def wchars(self, data): self.repeat(data, self.wchar)
	
	def repeat(self, list, func):
		for value in list:
			func(value)


class StreamIn:
	def __init__(self, data, endian="<"):
		self.endian = endian
		self.data = data
		self.pos = 0
		
	def get(self): return self.data
	def size(self): return len(self.data)
	def tell(self): return self.pos
	def seek(self, pos): self.pos = pos
	def skip(self, num): self.pos += num
	def align(self, num): self.pos += (num - self.pos % num) % num
	def eof(self): return self.pos >= len(self.data)
	def available(self): return len(self.data) - self.pos
	
	def peek(self, num):
		return self.data[self.pos : self.pos + num]
		
	def read(self, num):
		data = self.data[self.pos : self.pos + num]
		self.pos += num
		return data
		
	def readall(self):
		return self.read(self.available())
		
	def pad(self, num, char=b"\0"):
		if self.read(num) != char * num:
			raise ValueError("Incorrect padding")
			
	def ascii(self, num):
		return self.read(num).decode("ascii")
		
	def u8(self): return self.read(1)[0]
	def u16(self): return struct.unpack(self.endian + "H", self.read(2))[0]
	def u32(self): return struct.unpack(self.endian + "I", self.read(4))[0]
	def u64(self): return struct.unpack(self.endian + "Q", self.read(8))[0]
	
	def s8(self): return struct.unpack("b", self.read(1))[0]
	def s16(self): return struct.unpack(self.endian + "h", self.read(2))[0]
	def s32(self): return struct.unpack(self.endian + "i", self.read(4))[0]
	def s64(self): return struct.unpack(self.endian + "q", self.read(8))[0]
	
	def u24(self):
		if self.endian == ">":
			return (self.u16() << 8) | self.u8()
		return self.u8() | (self.u16() << 8)
	
	def float(self): return struct.unpack(self.endian + "f", self.read(4))[0]
	def double(self): return struct.unpack(self.endian + "d", self.read(8))[0]
	
	def bool(self): return bool(self.u8())
	def char(self): return chr(self.u8())
	def wchar(self): return chr(self.u16())
	
	def chars(self, num): return "".join(self.repeat(self.char, num))
	def wchars(self, num): return "".join(self.repeat(self.wchar, num))
	
	def repeat(self, func, count):
		return [func() for i in range(count)]
		
		
class BitStreamOut(StreamOut):
	def __init__(self, endian="<"):
		super().__init__(endian)
		self.bitpos = 0
		
	def push(self): self.stack.append((self.pos, self.bitpos))
	def pop(self): self.pos, self.bitpos = self.stack.pop()
	
	def seek(self, pos, bitpos=0):
		super().seek(pos)
		if bitpos > 0 and self.pos == len(self.data):
			self.data += b"\0"
		self.bitpos = bitpos
		
	def bytealign(self):
		if self.bitpos != 0:
			self.skip(1)
			self.bitpos = 0
			
	def align(self, num):
		self.bytealign()
		super().align(num)
		
	def bit(self, value):
		if self.pos == len(self.data):
			self.data += b"\0"

		byte = self.data[self.pos]
		mask = 1 << (7 - self.bitpos)
		if value:
			byte |= mask
		else:
			byte &= ~mask
		self.data[self.pos] = byte
		
		self.bitpos += 1
		if self.bitpos == 8:
			self.bitpos = 0
			self.pos += 1
			
	def bits(self, value, num):
		for i in range(num):
			self.bit((value >> (num - i - 1)) & 1)
			
	def write(self, data):
		if self.bitpos == 0: #Fast method
			super().write(data)
		else: #Slow method
			for value in data:
				self.bits(value, 8)
		
		
class BitStreamIn(StreamIn):
	def __init__(self, data, endian="<"):
		super().__init__(data, endian)
		self.bitpos = 0
		
	def push(self): self.stack.append((self.pos, self.bitpos))
	def pop(self): self.pos, self.bitpos = self.stack.pop()
	
	def seek(self, pos, bitpos=0):
		self.pos = pos
		self.bitpos = bitpos
		
	def bytealign(self):
		if self.bitpos != 0:
			self.pos += 1
			self.bitpos = 0
		
	def align(self, num):
		self.bytealign()
		super().align(num)
		
	def bit(self):
		byte = self.data[self.pos]
		value = (byte >> (7 - self.bitpos)) & 1
		
		self.bitpos += 1
		if self.bitpos == 8:
			self.bitpos = 0
			self.pos += 1
		
		return value
		
	def bits(self, num):
		value = 0
		for i in range(num):
			value = (value << 1) | self.bit()
		return value
		
	def read(self, num):
		if self.bitpos == 0: #Fast method
			return super().read(num)
		else: #Slow method
			data = []
			for i in range(num):
				data.append(self.bits(8))
			return bytes(data)
