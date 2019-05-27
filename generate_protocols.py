
import string
import sys
import os


class Protocol:
	def __init__(self):
		self.id = None
		self.name = None
		self.methods = []
		self.structs = {}
		self.enums = {}
		
	def add_method(self, method):
		self.methods.append(method)
		method.id = len(self.methods)
		
	def add_struct(self, struct):
		self.structs[struct.name] = struct
		
	def add_enum(self, enum):
		self.enums[enum.name] = enum
		

class Method:
	def __init__(self):
		self.id = None
		self.name = None
		self.parameters = []
		self.response = None
		
	def add_parameter(self, param):
		self.parameters.append(param)
		
		
class Struct:
	def __init__(self):
		self.name = None
		self.parent = None
		self.vars = None
		
		
class VariableList:
	def __init__(self):
		self.fields = []
		
		
class VariableItem:
	FIELD = 0
	CONDITIONAL = 1
	REVISION = 2
	
	def __init__(self):
		self.obj = None
		
		
class Conditional:
	COMP_EQ = 0
	COMP_NE = 1
	COMP_LE = 2
	COMP_LT = 3
	COMP_GE = 4
	COMP_GT = 5

	def __init__(self):
		self.group = None
		self.setting = None
		self.comparison = None
		self.value = None
		self.body = None
		
	def get_operator(self):
		return ["==", "!=", "<=", "<", ">=", ">"][self.comparison]
		
		
class Revision:
	def __init__(self, revision):
		self.revision = revision
		
		
class Variable:
	def __init__(self):
		self.type = None
		self.name = None
		self.default = None
		
		
class Type:
	def __init__(self):
		self.name = None
		self.template = []
		
		
class Enum:
	def __init__(self):
		self.values = []
	
	def add(self, name, value):
		self.values.append((name, value))


class Token:
	
	NAME = 0
	NUMBER = 1
	STRING = 2
	SPECIAL = 3
	EOF = 4

	def __init__(self, type, value):
		self.type = type
		self.value = value


class Tokenizer:
	
	NameChars = string.ascii_letters + "_"
	NameTailChars = NameChars + string.digits
	NumberChars = string.digits
	SpecialChars = "{}()[]<>:;,.=!#"
	WhiteChars = " \t\r\n"
	
	def parse(self, data):
		self.tokens = []
		self.state = self.state_next
		for char in data:
			if not self.state(char):
				return False
		if self.state == self.state_name:
			self.add(Token.NAME, self.name)
		elif self.state == self.state_number:
			self.add(Token.NUMBER, int(self.number))
		self.add(Token.EOF, None)
		return True
		
	def add(self, type, name):
		self.tokens.append(Token(type, name))
			
	def state_next(self, char):
		if char in self.NameChars:
			self.state = self.state_name
			self.name = char
		elif char in self.NumberChars:
			self.state = self.state_number
			self.number = char
		elif char in self.SpecialChars:
			self.add(Token.SPECIAL, char)
		elif char == '"':
			self.state = self.state_string
			self.string = '"'
		elif char in self.WhiteChars:
			pass
		else:
			print("Unexpected character:", char)
			return False
		return True
			
	def state_name(self, char):
		if char in self.NameTailChars:
			self.name += char
		else:
			self.add(Token.NAME, self.name)
			self.state = self.state_next
			return self.state(char)
		return True
		
	def state_number(self, char):
		if char in self.NumberChars:
			self.number += char
		else:
			self.add(Token.NUMBER, int(self.number))
			self.state = self.state_next
			return self.state(char)
		return True
		
	def state_string(self, char):
		if char == '"':
			self.string += '"'
			self.add(Token.STRING, self.string)
			self.state = self.state_next
		else:
			self.string += char
		return True


class Parser:
	def parse(self, tokens):
		self.protocols = []
		
		self.index = 0
		self.tokens = tokens
		return self.parse_file()
		
	def read(self):
		token = self.tokens[self.index]
		self.index += 1
		return token
		
	def peek(self):
		return self.tokens[self.index]
		
	def rewind(self):
		self.index -= 1
		
	def error(self, token):
		if token.type == Token.EOF:
			print("Unexpected end of file")
		else:
			print("Unexpected token:", token.value)
		return None
		
	def parse_file(self):
		while True:
			token = self.read()
			if token.type == Token.EOF:
				return True
			elif token.value == "protocol":
				protocol = self.parse_protocol()
				if not protocol:
					return False
				self.protocols.append(protocol)
			else:
				return self.error(token)
				
	def parse_protocol(self):
		protocol = Protocol()
		
		token = self.read()
		if token.type != Token.NAME:
			return self.error(token)
		protocol.name = token.value
		
		token = self.read()
		if token.value != ":":
			return self.error(token)
			
		token = self.read()
		if token.type != Token.NUMBER:
			return self.error(token)
		protocol.id = token.value
		
		token = self.read()
		if token.value != "{":
			return self.error(token)
			
		while True:
			token = self.read()
			if token.value == "}":
				return protocol
			elif token.value == "method":
				method = self.parse_method()
				if not method:
					return None
				protocol.add_method(method)
			elif token.value == "struct":
				struct = self.parse_struct()
				if not struct:
					return None
				protocol.add_struct(struct)
			elif token.value == "enum":
				enum = self.parse_enum(protocol)
				if not enum:
					return False
				protocol.add_enum(enum)
			else:
				return self.error(token)
				
	def parse_enum(self, protocol):
		enum = Enum()
		
		token = self.read()
		if token.type != Token.NAME:
			return self.error(token)
		enum.name = token.value
		
		token = self.read()
		if token.value != "{":
			return self.error(token)
		
		while True:
			token = self.read()
			if token.type != Token.NAME:
				return self.error(token)
			name = token.value
			
			token = self.read()
			if token.value != "=":
				return self.error(token)
				
			token = self.read()
			if token.type != Token.NUMBER:
				return self.error(token)
			enum.add(name, token.value)
			
			token = self.read()
			if token.value == "}":
				return enum
			elif token.value != ",":
				return self.error(token)
				
	def parse_struct(self):
		struct = Struct()
		
		token = self.read()
		if token.type != Token.NAME:
			return self.error(token)
		struct.name = token.value
		
		token = self.read()
		if token.value == ":":
			token = self.read()
			if token.type != Token.NAME:
				return self.error(token)
			struct.parent = token.value
		else:
			self.rewind()
		
		struct.vars = self.parse_variable_list()
		if not struct.vars:
			return None
	
		return struct
		
	def parse_type(self):
		type = Type()

		token = self.read()
		if token.type != Token.NAME:
			return self.error(token)
		type.name = token.value
		
		token = self.peek()
		if token.value == "<":
			if not self.parse_template_list(type):
				return None
		
		return type
		
	def parse_template_list(self, type):
		token = self.read()
		if token.value != "<":
			return self.error(token)
			
		token = self.peek()
		if token.value == ">":
			self.read()
			return True
			
		while True:
			subtype = self.parse_type()
			if not subtype:
				return False
			type.template.append(subtype)
			
			token = self.read()
			if token.value == ">":
				return True
			elif token.value != ",":
				return self.error(token)
				
	def parse_method(self):
		method = Method()
		
		token = self.read()
		if token.type != Token.NAME:
			return self.error(token)
		method.name = token.value
		
		token = self.read()
		if token.value == "(":
			self.rewind()
			if not self.parse_parameters(method):
				return False
			method.response = self.parse_variable_list()
			if not method.response:
				return False
		elif token.value != ";":
			return self.error(token)
		return method
		
	def parse_parameters(self, method):
		token = self.read()
		if token.value != "(":
			return self.error(token)
		
		token = self.peek()
		if token.value == ")":
			self.read()
			return True
		
		while True:
			param = Variable()
			
			param.type = self.parse_type()
			if not param.type:
				return False
				
			token = self.read()
			if token.type != Token.NAME:
				return self.error(token)
			param.name = token.value
			
			method.add_parameter(param)
			
			token = self.read()
			if token.value == ")":
				return True
			elif token.value != ",":
				return self.error(token)
			
	def parse_variable_list(self):
		list = VariableList()
	
		token = self.read()
		if token.value != "{":
			return self.error(token)
		
		while True:
			value = VariableItem()
			
			token = self.read()
			if token.value == "}":
				return list
			elif token.value == "[":
				value.type = VariableItem.CONDITIONAL
				value.obj = self.parse_conditional()
				if not value.obj:
					return None
			elif token.value == "#":
				token = self.read()
				if token.value != "revision":
					return self.error(token)
				token = self.read()
				if token.type != Token.NUMBER:
					return self.error(token)
				value.type = VariableItem.REVISION
				value.obj = Revision(token.value)
			else:
				self.rewind()
				value.type = VariableItem.FIELD
				value.obj = self.parse_variable()
				if not value.obj:
					return None
					
			list.fields.append(value)
					
	def parse_conditional(self):
		cond = Conditional()
			
		token = self.read()
		if token.type != Token.NAME:
			return self.error(token)
		cond.group = token.value
		
		token = self.read()
		if token.value != ".":
			return self.error(token)
			
		token = self.read()
		if token.type != Token.NAME:
			return self.error(token)
		cond.setting = token.value
		
		token = self.read()
		if token.value == ">":
			token = self.read()
			if token.value == "=":
				cond.comparison = Conditional.COMP_GE
			else:
				cond.comparison = Conditional.COMP_GT
				self.rewind()
		elif token.value == "<":
			token = self.read()
			if token.value == "=":
				cond.comparison = Conditional.COMP_LE
			else:
				cond.comparison = Conditional.COMP_LT
				self.rewind()
		elif token.value == "!":
			token = self.read()
			if token.value != "=":
				return self.error(token)
			cond.comparison = Conditional.COMP_NE
		elif token.value == "=":
			token = self.read()
			if token.value != "=":
				return self.error(token)
			cond.comparison = Conditional.COMP_EQ
		else:
			return self.error(token)
			
		token = self.read()
		if token.type != Token.NUMBER:
			return self.error(token)
		cond.value = token.value
		
		token = self.read()
		if token.value != "]":
			return self.error(token)
			
		cond.body = self.parse_variable_list()
		if not cond.body:
			return None
		return cond
		
	def parse_variable(self):
		value = Variable()
		
		value.type = self.parse_type()
		if not value.type:
			return None
		
		token = self.read()
		if token.type != Token.NAME:
			return self.error(token)
		value.name = token.value
		
		token = self.read()
		if token.value == "=":
			value.default = self.parse_default(value.type)
			if value.default is None:
				return None
			token = self.read()
		
		if token.value != ";":
			return self.error(token)
			
		return value
		
	def parse_default(self, type):
		if type.name in [
			"u8", "u16", "u32", "u64",
			"s8", "s16", "s32", "s64",
			"pid"
		]:
			token = self.read()
			if token.type != Token.NUMBER:
				return self.error(token)
			return token.value
		
		elif type.name == "datetime":
			token = self.read()
			if token.type != Token.NUMBER:
				return self.error(token)
			return "common.DateTime(%i)" %token.value
		
		elif type.name == "string":
			token = self.read()
			if token.type != Token.STRING:
				return self.error(token)
			return token.value
			
		elif type.name in ["buffer", "qbuffer"]:
			token = self.read()
			if token.type != Token.STRING:
				return self.error(token)
			return "b" + token.value
			
		elif type.name == "bool":
			token = self.read()
			if token.type != Token.NAME:
				return self.error(token)
			if token.value not in ["false", "true"]:
				return self.error(token)
			return token.value == "true"
			
		elif type.name == "list":
			if len(type.template) != 1:
				print("Unexpected template argument count")
				return None
				
			list = []
			subtype = type.template[0]
			
			token = self.read()
			if token.value != "[":
				return self.error(token)
				
			token = self.read()
			if token.value == "]":
				return list
			self.rewind()
			
			while True:
				list.append(self.parse_default(subtype))
				
				token = self.read()
				if token.value == "]":
					return list
				elif token.value != ",":
					return self.error(token)
		else:
			print("Don't know how to parse default value for %s" %type.name)

	
BASIC_TYPES = [
	"u8", "u16", "u32", "u64",
	"s8", "s16", "s32", "s64",
	"float", "double", "bool",
	"pid", "result", "datetime",
	"string", "stationurl", "buffer",
	"qbuffer", "anydata"
]

COMMON_TYPES = [
	"ResultRange"
]

def generate_extract(protocol, type, stream="stream"):
	if type.name in BASIC_TYPES:
		return "%s.%s()" %(stream, type.name)
	elif type.name in protocol.structs:
		return "%s.extract(%s)" %(stream, type.name)
	elif type.name in COMMON_TYPES:
		return "%s.extract(common.%s)" %(stream, type.name)
	elif type.name == "list":
		if len(type.template) != 1:
			print("Unexpected template argument count")
			return "None"
		subtype = type.template[0]
		code = "%s.list(" %stream
		if subtype.name in BASIC_TYPES:
			code += "%s.%s" %(stream, subtype.name)
		elif subtype.name in protocol.structs:
			code += subtype.name
		elif subtype.name in COMMON_TYPES:
			code += "common.%s" %subtype.name
		else:
			print("Unknown type: %s" %subtype.name)
			return "None"
		return code + ")"
	else:
		print("Unknown type: %s" %type.name)
		return "None"
		
def generate_encode_func(protocol, type, stream="stream"):
	if type.name in BASIC_TYPES:
		return "%s.%s" %(stream, type.name)
	elif type.name in protocol.structs or type.name in COMMON_TYPES:
		return "%s.add" %stream
	else:
		print("Unknown type: %s" %type.name)
		return ""
		
def generate_encode(protocol, type, name, stream="stream"):
	if type.name == "list":
		if len(type.template) != 1:
			print("Unexpected template argument count")
			return ""
		subtype = type.template[0]
		func = generate_encode_func(protocol, subtype, stream)
		if func:
			return "%s.list(%s, %s)" %(stream, name, func)
	else:
		func = generate_encode_func(protocol, type, stream)
		if func:
			return "%s(%s)" %(func, name)
	return ""
			
def generate_struct_init(protocol, vars, tabs):
	code = ""
	for field in vars.fields:
		if field.type == VariableItem.FIELD:
			value = field.obj.default
			if field.obj.type.name in protocol.structs:
				value = "%s()" %field.obj.type.name
			elif field.obj.type.name in COMMON_TYPES:
				value = "common.%s()" %field.obj.type.name
			code += "\t" * tabs + "self.%s = %s\n" %(field.obj.name, value)
		elif field.type == VariableItem.CONDITIONAL:
			code += generate_struct_init(protocol, field.obj.body, tabs)
	return code
	
def generate_condition(cond, prefix="stream."):
	operator = cond.get_operator()
	return "if %ssettings.get(\"%s.%s\") %s %s:\n" %(prefix, cond.group, cond.setting, operator, cond.value)
	
def generate_struct_version_body(vars, tabs):
	code = ""
	for field in vars.fields:
		if field.type == VariableItem.REVISION:
			code += "\t" * tabs + "version = %i\n" %field.obj.revision
		elif field.type == VariableItem.CONDITIONAL:
			subbody = generate_struct_version_body(field.obj.body, tabs + 1)
			if subbody:
				code += "\t" * tabs + generate_condition(field.obj, "")
				code += subbody
	return code
	
def generate_struct_version(protocol, vars):
	body = generate_struct_version_body(vars, 2)
	if body:
		code = "\tdef get_version(self, settings):\n"
		code += "\t\tversion = 0\n"
		code += body
		code += "\t\treturn version\n\n"
		return code
	return ""
	
def generate_struct_check(protocol, vars, tabs):
	code = ""
	unconditional = [
		f.obj.name for f in vars.fields if \
		f.type == VariableItem.FIELD and \
		f.obj.type.name not in protocol.structs and \
		f.obj.type.name not in COMMON_TYPES and \
		f.obj.default is None
	]
	if unconditional:
		code += "\t" * tabs + "for field in %s:\n" %unconditional
		code += "\t" * tabs + "\tif getattr(self, field) is None:\n"
		code += "\t" * tabs + "\t\traise ValueError(\"No value assigned to required field: %s\" %field)\n"
	conditional = [f for f in vars.fields if f.type == VariableItem.CONDITIONAL]
	for cond in conditional:
		code += "\t" * tabs + generate_condition(cond.obj, "")
		code += generate_struct_check(protocol, cond.obj.body, tabs + 1)
	if not unconditional and not conditional:
		code += "\t" * tabs + "pass\n"
	return code
	
def generate_struct_load(protocol, vars, tabs, prefix):
	code = ""
	for field in vars.fields:
		if field.type == VariableItem.FIELD:
			code += "\t" * tabs
			code += "%s.%s = %s\n" %(prefix, field.obj.name, generate_extract(protocol, field.obj.type))
		elif field.type == VariableItem.CONDITIONAL:
			code += "\t" * tabs
			code += generate_condition(field.obj)
			code += generate_struct_load(protocol, field.obj.body, tabs + 1, prefix)
	return code
	
def generate_struct_save(protocol, vars, tabs):
	code = ""
	for field in vars.fields:
		if field.type == VariableItem.FIELD:
			code += "\t" * tabs
			code += generate_encode(protocol, field.obj.type, "self." + field.obj.name) + "\n"
		elif field.type == VariableItem.CONDITIONAL:
			code += "\t" * tabs
			code += generate_condition(field.obj)
			code += generate_struct_save(protocol, field.obj.body, tabs + 1)
	return code
	
def generate_struct(protocol, struct):
	if not struct.parent:
		code = "class %s(common.Structure):\n" %struct.name
	elif struct.parent == "Data":
		code = "class %s(common.Data):\n" %struct.name
	else:
		code = "class %s(%s):\n" %(struct.name, struct.parent)
	
	code += "\tdef __init__(self):\n"
	code += "\t\tsuper().__init__()\n"
	code += generate_struct_init(protocol, struct.vars, 2)
	code += "\n"
	code += generate_struct_version(protocol, struct.vars)
	code += "\tdef check_required(self, settings):\n"
	code += generate_struct_check(protocol, struct.vars, 2)
	code += "\n"
	code += "\tdef load(self, stream):\n"
	code += generate_struct_load(protocol, struct.vars, 2, "self")
	code += "\n"
	code += "\tdef save(self, stream):\n"
	code += "\t\tself.check_required(stream.settings)\n"
	code += generate_struct_save(protocol, struct.vars, 2)
	
	if struct.parent:
		code += "common.DataHolder.register(%s, \"%s\")\n" %(struct.name, struct.name)
	
	return code + "\n\n"
		
def generate_structs(protocol):
	structs = []
	for name in sorted(protocol.structs):
		struct = protocol.structs[name]
		structs.append(generate_struct(protocol, struct))
	return "".join(structs)
	

def generate_enum(protocol, enum):
	code = "class %s:\n" %enum.name
	for name, value in enum.values:
		code += "\t%s = %i\n" %(name, value)
	code += "\n\n"
	return code
	
def generate_enums(protocol):
	enums = []
	for name in sorted(protocol.enums):
		enum = protocol.enums[name]
		enums.append(generate_enum(protocol, enum))
	return "".join(enums)
	
	
def generate_protocol(protocol):
	code = "class %sProtocol:\n" %protocol.name
	for method in protocol.methods:
		code += "\tMETHOD_%s = %i\n" %(method.name.upper(), method.id)
	code += "\n\tPROTOCOL_ID = 0x%X\n\n\n" %protocol.id
	return code


def generate_client_method(protocol, method):
	if method.response is None:
		return ""

	code = "\tdef %s(self" %method.name
	for param in method.parameters:
		code += ", %s" %param.name
	code += "):\n"
	
	code += "\t\tlogger.info(\"%sClient.%s()\")\n" %(protocol.name, method.name)
	code += "\t\t#--- request ---\n"
	code += "\t\tstream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_%s)\n" %method.name.upper()
	for param in method.parameters:
		code += "\t\t%s\n" %generate_encode(protocol, param.type, param.name)
	code += "\t\tself.client.send_message(stream)\n\n"
	
	code += "\t\t#--- response ---\n"
	if len(method.response.fields) > 1:
		code += "\t\tstream = self.client.get_response(call_id)\n"
		code += "\t\tobj = common.RMCResponse()\n"
		code += generate_struct_load(protocol, method.response, 2, "obj")
		code += "\t\tlogger.info(\"%sClient.%s -> done\")\n" %(protocol.name, method.name)
		code += "\t\treturn obj"
	elif len(method.response.fields) == 1:
		item = method.response.fields[0]
		if item.type == VariableItem.FIELD:
			value = item.obj
			code += "\t\tstream = self.client.get_response(call_id)\n"
			code += "\t\t%s = %s\n" %(value.name, generate_extract(protocol, value.type))
			code += "\t\tlogger.info(\"%sClient.%s -> done\")\n" %(protocol.name, method.name)
			code += "\t\treturn %s" %value.name
	else:
		code += "\t\tself.client.get_response(call_id)\n"
		code += "\t\tlogger.info(\"%sClient.%s -> done\")" %(protocol.name, method.name)
	return code

def generate_client(protocol):
	code = "class %sClient(%sProtocol):\n" %(protocol.name, protocol.name)
	code += "\tdef __init__(self, client):\n"
	code += "\t\tself.client = client\n\n"
	for method in protocol.methods:
		method_code = generate_client_method(protocol, method)
		if method_code:
			code += method_code + "\n\n"
	return code + "\n"


def get_python_type(type):
	if type.name in [
		"u8", "u16", "u32", "u64",
		"s8", "s16", "s32", "s64",
		"pid"
	]: return "int"
	elif type.name in ["float", "double"]:
		return "float"
	elif type.name == "bool": return "bool"
	elif type.name == "string": return "str"
	elif type.name in ["buffer", "qbuffer"]:
		return "bytes"
	elif type.name == "list": return "list"
	elif type.name == "datetime": return "common.DateTime"
	elif type.name == "stationurl": return "common.StationURL"
	elif type.name == "result": return "common.Result"
	elif type.name == "anydata": return "common.Data"
	elif type.name in COMMON_TYPES:
		return "common.%s" %type.name
	return type.name

def generate_server_method(protocol, method):
	code = "\tdef handle_%s(self, context, input, output):\n" %method.name
	if method.response is None: #Unsupported method
		code += "\t\tlogger.warning(\"%sSever.%s is unsupported\")\n" %(protocol.name, method.name)
		code += "\t\treturn common.Result(\"Core::NotImplemented\")\n\n"
		return code
	
	code += "\t\tlogger.info(\"%sServer.%s()\")\n" %(protocol.name, method.name)
	code += "\t\t#--- request ---\n"
	for param in method.parameters:
		code += "\t\t%s = %s\n" %(param.name, generate_extract(protocol, param.type, "input"))
		
	params = ""
	for param in method.parameters:
		params += ", " + param.name
	
	fields = [f.obj for f in method.response.fields if f.type == VariableItem.FIELD]
	if len(fields) > 1:
		field_names = [f.name for f in fields]
		code += "\t\tresponse = self.%s(context%s)\n\n" %(method.name, params)
		code += "\t\t#--- response ---\n"
		code += "\t\tif not isinstance(response, common.RMCResponse):\n"
		code += "\t\t\traise RuntimeError(\"Expected RMCResponse, got %s\" %response.__class__.__name__)\n"
		code += "\t\tfor field in %s:\n" %field_names
		code += "\t\t\tif not hasattr(response, field):\n"
		code += "\t\t\t\traise RuntimeError(\"Missing field in RMCResponse: %s\" %field)\n"
		for field in fields:
			code += "\t\t%s\n" %generate_encode(protocol, field.type, "response." + field.name, "output")
		code += "\n"
	elif len(fields) == 1:
		field = fields[0]
		expected = get_python_type(field.type)
		code += "\t\tresponse = self.%s(context%s)\n\n" %(method.name, params)
		code += "\t\t#--- response ---\n"
		code += "\t\tif not isinstance(response, %s):\n" %expected
		code += "\t\t\traise RuntimeError(\"Expected %s, got %%s\" %%response.__class__.__name__)\n" %expected
		code += "\t\t%s\n\n" %generate_encode(protocol, field.type, "response", "output")
	else:
		code += "\t\tself.%s(context%s)\n\n" %(method.name, params)
	return code
	
def generate_server_stub(protocol, method):
	if method.response is None:
		return ""
	code = "\tdef %s(self, *args):\n" %method.name
	code += "\t\tlogger.warning(\"%sServer.%s not implemented\")\n" %(protocol.name, method.name)
	code += "\t\traise common.RMCError(\"Core::NotImplemented\")\n"
	return code + "\n"

SERVER_TEMPLATE = """class %sServer(%sProtocol):
	def __init__(self):
		self.methods = {
%s		}

	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			return self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %sServer: %%i", method_id)
			raise common.RMCError("Core::NotImplemented")

"""
def generate_server(protocol):
	methods = ""
	for method in protocol.methods:
		methods += "\t\t\tself.METHOD_%s: self.handle_%s,\n" %(method.name.upper(), method.name)
	code = SERVER_TEMPLATE %(
		protocol.name, protocol.name,
		methods, protocol.name
	)
	for method in protocol.methods:
		code += generate_server_method(protocol, method)
	for method in protocol.methods:
		code += generate_server_stub(protocol, method)
	return code + "\n"


def generate_header(name):
	code = "\n# This file was generated automatically from %s.proto\n\n" %name
	code += "from nintendo.nex import common\n\n"
	code += "import logging\n"
	code += "logger = logging.getLogger(__name__)\n\n\n"
	return code

	
def parse(name, data):
	tokenizer = Tokenizer()
	if not tokenizer.parse(data):
		return
	
	parser = Parser()
	if not parser.parse(tokenizer.tokens):
		return
	
	code = generate_header(name)
	for protocol in parser.protocols:
		code += generate_enums(protocol)
	for protocol in parser.protocols:
		code += generate_structs(protocol)
	for protocol in parser.protocols:
		code += generate_protocol(protocol)
	for protocol in parser.protocols:
		code += generate_client(protocol)
	for protocol in parser.protocols:
		code += generate_server(protocol)
	return code.rstrip("\n") + "\n"

def generate(filename):
	if not os.path.isfile(filename):
		print("File not found: %s" %filename)
	else:
		print("Parsing %s" %filename)
		with open(filename) as f:
			data = f.read()
		name = os.path.splitext(os.path.basename(filename))[0]
		code = parse(name, data)
		if code:
			with open("nintendo/nex/%s.py" %name, "w") as f:
				f.write(code)

if len(sys.argv) < 2:
	print("Usage: python generate_protocols.py <protocol...>")
else:
	protocols = []
	if "all" in sys.argv:
		for filename in os.listdir("nintendo/files/proto"):
			protocols.append(filename.split(".proto")[0])
	else:
		protocols = sys.argv[1:]
		
	for proto in protocols:
		generate("nintendo/files/proto/%s.proto" %proto)
