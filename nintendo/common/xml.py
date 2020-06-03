
from nintendo.common.textstream import TextStream
from nintendo.common import types
import string


NAME_CHARS = string.ascii_letters + string.digits + ":-_"


def decode_entities(s):
	s = s.replace("&quot;", '"')
	s = s.replace("&apos;", "'")
	s = s.replace("&lt;", "<")
	s = s.replace("&gt;", ">")
	s = s.replace("&amp;", "&")
	return s

def encode_entities(s):
	s = s.replace("&", "&amp;")
	s = s.replace("'", "&quot;")
	s = s.replace('"', "&apos;")
	s = s.replace("<", "&lt;")
	s = s.replace(">", "&gt;")
	return s


class XMLTree:
	def __init__(self):
		self.children = []
		self.attrs = types.OrderedDict()
		
		self.value = None
		self.name = None
		
	def set_header(self, header): self.header = header
	def set_name(self, name): self.name = name
	def set_value(self, value): self.value = value
	def set_attr(self, name, value): self.attrs[name] = value
	
	def __str__(self):
		return self.encode()
	
	def __contains__(self, name):
		for node in self.children:
			if node.name == name:
				return True
		return False
	
	def __getitem__(self, name):
		for node in self.children:
			if node.name == name:
				return node
		raise KeyError(name)
		
	def __iter__(self):
		return iter(self.children)
		
	def find(self, name):
		nodes = []
		for node in self.children:
			if node.name == name:
				nodes.append(node)
		return nodes
	
	def add(self, name, value=None, attrs={}):
		node = XMLTree()
		node.value = value
		node.attrs = types.OrderedDict(attrs)
		self.children.append(node)
		return node
	
	def encode(self):
		data = "<%s" %self.name
		for name, value in self.attrs.items():
			data += ' %s="%s"' %(name, encode_entities(value))
		data += ">"
		
		for child in self.children:
			data += child.encode()

		if self.value is not None:
			data += encode_entities(str(self.value))
		
		data += "</%s>" %self.name
		return data
		
		
class XMLParser:
	def parse(self, text):
		stream = TextStream(text)
		self.parse_declaration(stream)
		
		stream.skip_whitespace()
		
		tree = self.parse_tree(stream)
		
		stream.skip_whitespace()
		if not stream.eof():
			raise ValueError("XML document has data behind root tag")
		return tree
		
	def parse_declaration(self, stream):
		if stream.peek(6) == "<?xml ":
			stream.read(6)
			
			self.parse_declaration_attribs(stream)
			
			if stream.read() != "?":
				raise ValueError("XML declaration is invalid")
			stream.skip_whitespace()
			
			if stream.read() != ">":
				raise ValueError("XML declaration is invalid")
			
	def parse_declaration_attribs(self, stream):
		version = self.parse_fixed_attribute(stream, "version")
		if version != "1.0":
			raise ValueError("XML version must be 1.0")
		if stream.peek() == "?": return
		
		encoding = self.parse_fixed_attribute(stream, "encoding")
		if stream.peek() == "?": return
		
		standalone = self.parse_fixed_attribute(stream, "standalone")
		if standalone not in ["yes", "no"]:
			raise ValueError("standalone must be either yes of no")
			
	def parse_tree(self, stream):
		if stream.read() != "<":
			raise ValueError("Unexpected character in XML document")
			
		stream.skip_whitespace()
		
		tree = XMLTree()
		tree.name = self.parse_name(stream)
		
		stream.skip_whitespace()
		
		char = stream.peek()
		while char not in "/>":
			name, value = self.parse_attribute(stream)
			if name in tree.attrs:
				raise ValueError("Duplicate attributein XML document")
			tree.attrs[name] = value
			char = stream.peek()
		
		char = stream.read()
		if char == "/":
			if stream.read() != ">":
				raise ValueError("Unexpected character in XML document")
			return tree
			
		tree.value = ""
		
		chars = stream.peek(2)
		while chars != "</":
			if chars[0] == "<":
				tree.children.append(self.parse_tree(stream))
			else:
				tree.value += chars[0]
				stream.skip()
			chars = stream.peek(2)
			
		tree.value = decode_entities(tree.value)
			
		stream.skip(2)
		stream.skip_whitespace()
		
		name = self.parse_name(stream)
		if name != tree.name:
			raise ValueError(
				"Closing tag has unexpected name: '%s' (expected '%s')" %(name, tree.name)
			)
			
		stream.skip_whitespace()
		if stream.read() != ">":
			raise ValueError("Unexpected character in XML document")
		
		return tree	
			
	def parse_fixed_attribute(self, stream, attr):
		name, value = self.parse_attribute(stream)
		if name != attr:
			raise ValueError("Expected '%s' attribute, not '%s'" %(attr, name))
		return value
		
	def parse_attribute(self, stream):
		stream.skip_whitespace()
		key = self.parse_name(stream)
		stream.skip_whitespace()
		if stream.read() != "=":
			raise ValueError("Expected '=' after attribute name")
		stream.skip_whitespace()
		value = self.parse_string(stream)
		stream.skip_whitespace()
		return key, value
		
	def parse_string(self, stream):
		strchar = stream.read()
		if strchar not in ["'", '"']:
			raise ValueError("Expected string attribute")
		
		string = ""
		char = stream.read()
		while char != strchar:
			string += char
			char = stream.read()
		
		string = " ".join(string.split())
		string = decode_entities(string)
		return string
		
	def parse_name(self, stream):
		name = ""
		char = stream.peek()
		while char in NAME_CHARS:
			name += char
			stream.skip()
			char = stream.peek()
		return name
		
		
def parse(text):
	parser = XMLParser()
	return parser.parse(text)
