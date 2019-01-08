
class XMLTree:
	def __init__(self):
		self.nodes = []
		self.value = None
		self.name = None
		
	def add(self, key, value):
		if "/" in key:
			name, path = key.split("/", 1)
			self.find(name).add(path, value)
		else:
			self.find(key).value = value
			
	def find(self, name):
		for node in self.nodes:
			if node.name == name:
				return node
		node = XMLTree()
		node.name = name
		self.nodes.append(node)
		return node

	def build(self):
		data = ""
		for node in self.nodes:
			data += "<%s>" %node.name
			data += node.build()
			data += "</%s>" %node.name
		data += str(self.value)
		return data
