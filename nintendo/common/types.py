
from collections import OrderedDict


class MappedDict:
	def __init__(self, value=None, **kwargs):
		self.dict = {} # Transformed key -> value
		self.keytable = {} # Transformed key -> original key
		self.update(value, **kwargs)
	
	@classmethod
	def fromkeys(cls, keys, value=None):
		return cls((key, value) for key in keys)
		
	def standard_dict(self):
		return {self.keytable[k]: v for k, v in self.dict.items()}
	def mapped_dict(self):
		return self.dict.copy()
	def transform_key(self, key):
		return key
	
	def __repr__(self):
		return repr(self.standard_dict())
	
	def __eq__(self, other):
		if isinstance(other, dict):
			other = self.__class__(other)
		if isinstance(other, MappedDict):
			return self.dict == other.dict
		return NotImplemented
	
	def __contains__(self, key):
		return self.transform_key(key) in self.keytable
	
	def __getitem__(self, key):
		return self.dict[self.transform_key(key)]
	def __setitem__(self, key, value):
		transformed = self.transform_key(key)
		self.dict[transformed] = value
		self.keytable[transformed] = key
	def __delitem__(self, key):
		key = self.transform_key(key)
		del self.dict[key]
		del self.keytable[key]
		
	def __iter__(self):
		return iter(self.keys())
	def __len__(self):
		return len(self.dict)
	
	def copy(self):
		return self.__class__(**self)
	
	def get(self, key, default=None):
		return self.dict.get(self.transform_key(key), default)
	
	def setdefault(self, key, value=None):
		if key not in self:
			self[key] = value
		return self[key]
	
	def pop(self, key, *args):
		key = self.transform_key(key)
		if key in self.dict:
			value = self.dict.pop(key)
			del self.keytable[key]
			return value
		return self.dict.pop(key, *args)
	
	def popitem(self):
		k, v = self.dict.popitem()
		return self.keytable.pop(k), v
	
	def keys(self): return self.keytable.values()
	def values(self): return self.dict.values()
	def items(self): return self.standard_dict().items()
	
	def clear(self):
		self.dict.clear()
		self.keytable.clear()
	
	def update(self, value=None, **kwargs):
		if value is not None:
			if hasattr(value, "keys"):
				for k in value:
					self[k] = value[k]
			else:
				for k, v in value:
					self[k] = v
		for k, v in kwargs.items():
			self[k] = v


class CaseInsensitiveDict(MappedDict):
	def transform_key(self, key):
		if type(key) != str:
			raise TypeError("Only strings are allowed as keys")
		return key.lower()