
from nintendo.common.stream import StreamOut, StreamIn

class NexStreamOut(StreamOut):
	def __init__(self, version):
		super().__init__()
		self.version = version

	def list(self, list, func):
		self.u32(len(list))
		super().list(list, func)
		
	def string(self, string):
		string += "\x00"
		self.u16(len(string))
		self.chars(string)
		
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
		return self.chars(self.u16())[:-1] #Remove null-terminator
		
	def substream(self):
		return NexStreamIn(self.read(self.u32()), self.version)
