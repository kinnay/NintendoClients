
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


class AuthenticationInfo(common.Data):
	def __init__(self):
		super().__init__()
		self.token = None
		self.ngs_version = 3
		self.token_type = 1
		self.server_version = 0
	
	def check_required(self, settings):
		for field in ['token']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.token = stream.string()
		self.ngs_version = stream.u32()
		self.token_type = stream.u8()
		self.server_version = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.token)
		stream.u32(self.ngs_version)
		stream.u8(self.token_type)
		stream.u32(self.server_version)
common.DataHolder.register(AuthenticationInfo, "AuthenticationInfo")


class NintendoLoginData(common.Data):
	def __init__(self):
		super().__init__()
		self.token = None
	
	def check_required(self, settings):
		for field in ['token']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.token = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.token)
common.DataHolder.register(NintendoLoginData, "NintendoLoginData")


class RVConnectionData(common.Structure):
	def __init__(self):
		super().__init__()
		self.main_station = None
		self.special_protocols = None
		self.special_station = None
		self.server_time = None
	
	def get_version(self, settings):
		version = 0
		if settings.get("nex.version") >= 30500:
			version = 1
		return version
	
	def check_required(self, settings):
		for field in ['main_station', 'special_protocols', 'special_station']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings.get("nex.version") >= 30500:
			for field in ['server_time']:
				if getattr(self, field) is None:
					raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.main_station = stream.stationurl()
		self.special_protocols = stream.list(stream.u8)
		self.special_station = stream.stationurl()
		if stream.settings.get("nex.version") >= 30500:
			self.server_time = stream.datetime()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.stationurl(self.main_station)
		stream.list(self.special_protocols, stream.u8)
		stream.stationurl(self.special_station)
		if stream.settings.get("nex.version") >= 30500:
			stream.datetime(self.server_time)


class ValidateAndRequestTicketParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.platform = 3
		self.username = None
		self.data = None
		self.unk = False
		self.nex_version = None
		self.client_version = None
	
	def check_required(self, settings):
		for field in ['username', 'data', 'nex_version', 'client_version']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.platform = stream.u32()
		self.username = stream.string()
		self.data = stream.anydata()
		self.unk = stream.bool()
		self.nex_version = stream.u32()
		self.client_version = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.platform)
		stream.string(self.username)
		stream.anydata(self.data)
		stream.bool(self.unk)
		stream.u32(self.nex_version)
		stream.u32(self.client_version)


class ValidateAndRequestTicketResult(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.ticket = None
		self.server_url = None
		self.server_time = None
		self.server_name = None
		self.ticket_key = None
	
	def check_required(self, settings):
		for field in ['pid', 'ticket', 'server_url', 'server_time', 'server_name', 'ticket_key']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.pid = stream.pid()
		self.ticket = stream.buffer()
		self.server_url = stream.stationurl()
		self.server_time = stream.datetime()
		self.server_name = stream.string()
		self.ticket_key = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.pid)
		stream.buffer(self.ticket)
		stream.stationurl(self.server_url)
		stream.datetime(self.server_time)
		stream.string(self.server_name)
		stream.string(self.ticket_key)


class AuthenticationProtocol:
	METHOD_LOGIN = 1
	METHOD_LOGIN_EX = 2
	METHOD_REQUEST_TICKET = 3
	METHOD_GET_PID = 4
	METHOD_GET_NAME = 5
	METHOD_LOGIN_WITH_PARAM = 6
	
	PROTOCOL_ID = 0xA


class AuthenticationClient(AuthenticationProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def login(self, username):
		logger.info("AuthenticationClient.login()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(username)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_LOGIN, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.result = stream.result()
		obj.pid = stream.pid()
		obj.ticket = stream.buffer()
		obj.connection_data = stream.extract(RVConnectionData)
		obj.server_name = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.login -> done")
		return obj
	
	def login_ex(self, username, extra_data):
		logger.info("AuthenticationClient.login_ex()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(username)
		stream.anydata(extra_data)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_LOGIN_EX, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.result = stream.result()
		obj.pid = stream.pid()
		obj.ticket = stream.buffer()
		obj.connection_data = stream.extract(RVConnectionData)
		obj.server_name = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.login_ex -> done")
		return obj
	
	def request_ticket(self, source, target):
		logger.info("AuthenticationClient.request_ticket()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(source)
		stream.pid(target)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_REQUEST_TICKET, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.result = stream.result()
		obj.ticket = stream.buffer()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.request_ticket -> done")
		return obj
	
	def get_pid(self, username):
		logger.info("AuthenticationClient.get_pid()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(username)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_PID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		pid = stream.pid()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.get_pid -> done")
		return pid
	
	def get_name(self, pid):
		logger.info("AuthenticationClient.get_name()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_NAME, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		name = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.get_name -> done")
		return name
	
	def login_with_param(self, param):
		logger.info("AuthenticationClient.login_with_param()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_LOGIN_WITH_PARAM, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.extract(ValidateAndRequestTicketResult)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.login_with_param -> done")
		return result


class AuthenticationServer(AuthenticationProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_LOGIN: self.handle_login,
			self.METHOD_LOGIN_EX: self.handle_login_ex,
			self.METHOD_REQUEST_TICKET: self.handle_request_ticket,
			self.METHOD_GET_PID: self.handle_get_pid,
			self.METHOD_GET_NAME: self.handle_get_name,
			self.METHOD_LOGIN_WITH_PARAM: self.handle_login_with_param,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_login(self, context, input, output):
		logger.info("AuthenticationServer.login()")
		#--- request ---
		username = input.string()
		response = self.login(context, username)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'pid', 'ticket', 'connection_data', 'server_name']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.pid(response.pid)
		output.buffer(response.ticket)
		output.add(response.connection_data)
		output.string(response.server_name)
	
	def handle_login_ex(self, context, input, output):
		logger.info("AuthenticationServer.login_ex()")
		#--- request ---
		username = input.string()
		extra_data = input.anydata()
		response = self.login_ex(context, username, extra_data)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'pid', 'ticket', 'connection_data', 'server_name']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.pid(response.pid)
		output.buffer(response.ticket)
		output.add(response.connection_data)
		output.string(response.server_name)
	
	def handle_request_ticket(self, context, input, output):
		logger.info("AuthenticationServer.request_ticket()")
		#--- request ---
		source = input.pid()
		target = input.pid()
		response = self.request_ticket(context, source, target)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'ticket']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.buffer(response.ticket)
	
	def handle_get_pid(self, context, input, output):
		logger.info("AuthenticationServer.get_pid()")
		#--- request ---
		username = input.string()
		response = self.get_pid(context, username)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.pid(response)
	
	def handle_get_name(self, context, input, output):
		logger.info("AuthenticationServer.get_name()")
		#--- request ---
		pid = input.pid()
		response = self.get_name(context, pid)
		
		#--- response ---
		if not isinstance(response, str):
			raise RuntimeError("Expected str, got %s" %response.__class__.__name__)
		output.string(response)
	
	def handle_login_with_param(self, context, input, output):
		logger.info("AuthenticationServer.login_with_param()")
		#--- request ---
		param = input.extract(ValidateAndRequestTicketParam)
		response = self.login_with_param(context, param)
		
		#--- response ---
		if not isinstance(response, ValidateAndRequestTicketResult):
			raise RuntimeError("Expected ValidateAndRequestTicketResult, got %s" %response.__class__.__name__)
		output.add(response)
	
	def login(self, *args):
		logger.warning("AuthenticationServer.login not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def login_ex(self, *args):
		logger.warning("AuthenticationServer.login_ex not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def request_ticket(self, *args):
		logger.warning("AuthenticationServer.request_ticket not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_pid(self, *args):
		logger.warning("AuthenticationServer.get_pid not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_name(self, *args):
		logger.warning("AuthenticationServer.get_name not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def login_with_param(self, *args):
		logger.warning("AuthenticationServer.login_with_param not implemented")
		raise common.RMCError("Core::NotImplemented")

