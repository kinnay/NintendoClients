
class Signal:
	def __init__(self):
		self.listeners = []
		
	def connect(self, callback):
		self.listeners.append(callback)
		
	def disconnect(self, callback):
		self.listeners.remove(callback)
		
	def emit(self, *args):
		for callback in self.listeners:
			callback(*args)
			
	def __call__(self, *args):
		self.emit(*args)
