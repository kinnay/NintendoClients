
from nintendo.common.stream import StreamOut, StreamIn

class NexStreamOut(StreamOut):
	def __init__(self, version):
		super().__init__()
		self.version = version

	def list(self, list, func):
		self.u32(len(list))
		super().list(list, func)
		
	def string(self, string):
		if string is None:
			self.u16(0)
		else:
			data = (string + "\x00").encode("utf8")
			self.u16(len(data))
			self.write(data)
		
	def data(self, data):
		self.u32(len(data))
		self.write(data)
		
		
class NexStreamIn(StreamIn):
	def __init__(self, data, version):
		super().__init__(data)
		self.version = version

	def list(self, func):
		return super().list(func, self.u32())
		
	def string(self):
		length = self.u16()
		if length:
			return self.read(length).decode("utf8")[:-1] #Remove null-terminator
		
	def data(self):
		return self.read(self.u32())
		
	def substream(self):
		return NexStreamIn(self.data(), self.version)
