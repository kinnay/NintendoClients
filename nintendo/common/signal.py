
class Signal:
	def __init__(self):
		self.listeners = []
		
	def add(self, callback):
		self.listeners.append(callback)
		
	def remove(self, callback):
		self.listeners.remove(callback)
		
	def fire(self, *args):
		for callback in self.listeners:
			callback(*args)
			
	def __call__(self, *args):
		self.fire(*args)
