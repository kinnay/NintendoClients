
class RC4:
	def __init__(self, key, reset=False):
		self.reinit = reset
		self.set_key(key)
		
	def set_key(self, key):
		self.key = key
		self.reset()
		
	def reset(self):
		self.state = list(range(256))
		self.x = self.y = 0
		
		p = 0
		for i in range(256):
			p = (p + self.state[i] + self.key[i % len(self.key)]) % 256
			self.state[i], self.state[p] = self.state[p], self.state[i]
		
	def crypt(self, data):
		out = []
		for char in data:
			self.x = (self.x + 1) % 256
			self.y = (self.y + self.state[self.x]) % 256
			p, q = self.state[self.y], self.state[self.x]
			self.state[self.x], self.state[self.y] = p, q
			
			mask = self.state[(p + q) % 256]
			out.append(char ^ mask)
			
		if self.reinit:
			self.reset()

		return bytes(out)
