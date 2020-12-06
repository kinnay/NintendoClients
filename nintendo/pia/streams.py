
from anynet import streams


class StreamOut(streams.StreamOut):
	def __init__(self, settings):
		super().__init__(">")
		self.settings = settings
		
	def pid(self, value):
		if self.settings["common.pid_size"] == 8:
			self.u64(value)
		else:
			self.u32(value)
		
	def add(self, inst, *args):
		inst.encode(self, *args)
		
		
class StreamIn(streams.StreamIn):
	def __init__(self, data, settings):
		super().__init__(data, ">")
		self.settings = settings
		
	def pid(self):
		if self.settings["common.pid_size"] == 8:
			return self.u64()
		return self.u32()
		
	def extract(self, cls, *args):
		inst = cls()
		inst.decode(self, *args)
		return inst
