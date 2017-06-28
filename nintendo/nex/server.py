
class ProtocolServer:
	def init_callbacks(self, *methods):
		self.callbacks = {method: [] for method in methods}
		
	def add_callback(self, method_id, cb):
		self.callbacks[method_id].append(cb)
		
	def remove_callback(self, method_id, cb):
		self.callbacks[method_id].remove(cb)
		
	def callback(self, method_id, *args):
		for cb in self.callbacks[method_id]:
			cb(*args)
