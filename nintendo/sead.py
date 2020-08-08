
class Random:
	def __init__(self, *param):
		if len(param) == 1: self.set_seed(param[0])
		elif len(param) == 4: self.set_state(*param)
		else:
			raise TypeError("Random.__init__ takes either 1 or 4 arguments")
			
	def set_seed(self, seed):
		multiplier = 0x6C078965
		
		temp = seed
		self.state = []
		for i in range(1, 5):
			temp ^= temp >> 30
			temp = (temp * multiplier + i) & 0xFFFFFFFF
			self.state.append(temp)
			
	def set_state(self, s0, s1, s2, s3):
		self.state = [s0, s1, s2, s3]

	def u32(self):
		temp = self.state[0]
		temp = (temp ^ (temp << 11)) & 0xFFFFFFFF
		temp ^= temp >> 8
		temp ^= self.state[3]
		temp ^= self.state[3] >> 19
		self.state[0] = self.state[1]
		self.state[1] = self.state[2]
		self.state[2] = self.state[3]
		self.state[3] = temp
		return temp
	
	def uint(self, max):
		return (self.u32() * max) >> 32
