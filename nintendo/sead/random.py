
class Random:
	def __init__(self, seed):
		multiplier = 0x6C078965
		
		temp = seed
		self.state = []
		for i in range(1, 5):
			temp ^= temp >> 30
			temp = (temp * multiplier + i) & 0xFFFFFFFF
			self.state.append(temp)

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
