
from collections import OrderedDict


class CaseInsensitiveDict:
	def __init__(self):
		self.dict = OrderedDict()
		
	def __repr__(self):
		return str(list(self.dict.values()))
		
	def __getitem__(self, key):
		return self.dict[key.lower()][1]
		
	def __setitem__(self, key, value):
		self.dict[key.lower()] = (key, value)
		
	def __contains__(self, key):
		return key.lower() in self.dict
		
	def get(self, key, default=None):
		if key.lower() in self.dict:
			return self.dict[key.lower()][1]
		return default
		
	def items(self):
		return self.dict.values()
