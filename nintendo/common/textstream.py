
import string

class TextStream:
	def __init__(self, text):
		self.text = text
		self.pos = 0
		
	def peek(self, size=1):
		if self.available() < size:
			raise OverflowError("Buffer overflow in text stream")
		return self.text[self.pos : self.pos + size]
		
	def read(self, size=1):
		if self.available() < size:
			raise OverflowError("Buffer overflow in text stream")
		text = self.text[self.pos : self.pos + size]
		self.pos += size
		return text
		
	def skip(self, size=1):
		self.pos += size
		
	def available(self): return len(self.text) - self.pos
		
	def eof(self):
		return self.pos == len(self.text)
		
	def skip_whitespace(self):
		while not self.eof():
			char = self.peek()
			if char not in string.whitespace:
				return
			self.skip(1)
