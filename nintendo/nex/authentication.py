
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class AuthenticationInfo(common.Data):
	def __init__(self):
		super().__init__()
		self.token = None
		self.ngs_version = 3
		self.token_type = 1
		self.server_version = 0
	
	def check_required(self, settings, version):
		for field in ['token']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.token = stream.string()
		self.ngs_version = stream.u32()
		self.token_type = stream.u8()
		self.server_version = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.string(self.token)
		stream.u32(self.ngs_version)
		stream.u8(self.token_type)
		stream.u32(self.server_version)
common.DataHolder.register(AuthenticationInfo, "AuthenticationInfo")


class RVConnectionData(common.Structure):
	def __init__(self):
		super().__init__()
		self.main_station = common.StationURL.parse("prudp:/")
		self.special_protocols = []
		self.special_station = common.StationURL.parse("prudp:/")
		self.server_time = common.DateTime(0)
	
	def max_version(self, settings):
		version = 0
		if settings["nex.version"] >= 30500:
			version = 1
		return version
	
	def check_required(self, settings, version):
		if settings["nex.version"] >= 30500:
			if version >= 1:
				pass
	
	def load(self, stream, version):
		self.main_station = stream.stationurl()
		self.special_protocols = stream.list(stream.u8)
		self.special_station = stream.stationurl()
		if stream.settings["nex.version"] >= 30500:
			if version >= 1:
				self.server_time = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.stationurl(self.main_station)
		stream.list(self.special_protocols, stream.u8)
		stream.stationurl(self.special_station)
		if stream.settings["nex.version"] >= 30500:
			if version >= 1:
				stream.datetime(self.server_time)


class ValidateAndRequestTicketParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.platform = 3
		self.username = None
		self.data = None
		self.skip_version_check = False
		self.nex_version = None
		self.client_version = None
	
	def check_required(self, settings, version):
		for field in ['username', 'data', 'nex_version', 'client_version']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.platform = stream.u32()
		self.username = stream.string()
		self.data = stream.anydata()
		self.skip_version_check = stream.bool()
		self.nex_version = stream.u32()
		self.client_version = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.platform)
		stream.string(self.username)
		stream.anydata(self.data)
		stream.bool(self.skip_version_check)
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
		self.source_key = None
	
	def check_required(self, settings, version):
		for field in ['pid', 'ticket', 'server_url', 'server_time', 'server_name', 'source_key']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.pid = stream.pid()
		self.ticket = stream.buffer()
		self.server_url = stream.stationurl()
		self.server_time = stream.datetime()
		self.server_name = stream.string()
		self.source_key = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.pid)
		stream.buffer(self.ticket)
		stream.stationurl(self.server_url)
		stream.datetime(self.server_time)
		stream.string(self.server_name)
		stream.string(self.source_key)


class AuthenticationProtocol:
	METHOD_LOGIN = 1
	METHOD_LOGIN_EX = 2
	METHOD_REQUEST_TICKET = 3
	METHOD_GET_PID = 4
	METHOD_GET_NAME = 5
	METHOD_LOGIN_WITH_CONTEXT = 6
	
	PROTOCOL_ID = 0xA


class AuthenticationProtocolNX:
	METHOD_VALIDATE_AND_REQUEST_TICKET = 1
	METHOD_VALIDATE_AND_REQUEST_TICKET_WITH_CUSTOM_DATA = 2
	METHOD_REQUEST_TICKET = 3
	METHOD_GET_PID = 4
	METHOD_GET_NAME = 5
	METHOD_VALIDATE_AND_REQUEST_TICKET_WITH_PARAM = 6
	
	PROTOCOL_ID = 0xA


class AuthenticationClient(AuthenticationProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def login(self, username):
		logger.info("AuthenticationClient.login()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(username)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_LOGIN, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.result()
		obj.pid = stream.pid()
		obj.ticket = stream.buffer()
		obj.connection_data = stream.extract(RVConnectionData)
		obj.server_name = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.login -> done")
		return obj
	
	async def login_ex(self, username, extra_data):
		logger.info("AuthenticationClient.login_ex()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(username)
		stream.anydata(extra_data)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_LOGIN_EX, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.result()
		obj.pid = stream.pid()
		obj.ticket = stream.buffer()
		obj.connection_data = stream.extract(RVConnectionData)
		obj.server_name = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.login_ex -> done")
		return obj
	
	async def request_ticket(self, source, target):
		logger.info("AuthenticationClient.request_ticket()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(source)
		stream.pid(target)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REQUEST_TICKET, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.result()
		obj.ticket = stream.buffer()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.request_ticket -> done")
		return obj
	
	async def get_pid(self, username):
		logger.info("AuthenticationClient.get_pid()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(username)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		pid = stream.pid()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.get_pid -> done")
		return pid
	
	async def get_name(self, pid):
		logger.info("AuthenticationClient.get_name()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_NAME, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		name = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.get_name -> done")
		return name
	
	async def login_with_context(self, login_data):
		logger.info("AuthenticationClient.login_with_context()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.anydata(login_data)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_LOGIN_WITH_CONTEXT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.result()
		obj.pid = stream.pid()
		obj.ticket = stream.buffer()
		obj.connection_data = stream.extract(RVConnectionData)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClient.login_with_context -> done")
		return obj


class AuthenticationClientNX(AuthenticationProtocolNX):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def validate_and_request_ticket(self, username):
		logger.info("AuthenticationClientNX.validate_and_request_ticket()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(username)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_VALIDATE_AND_REQUEST_TICKET, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.result()
		obj.pid = stream.pid()
		obj.ticket = stream.buffer()
		obj.connection_data = stream.extract(RVConnectionData)
		obj.server_name = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClientNX.validate_and_request_ticket -> done")
		return obj
	
	async def validate_and_request_ticket_with_custom_data(self, username, extra_data):
		logger.info("AuthenticationClientNX.validate_and_request_ticket_with_custom_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(username)
		stream.anydata(extra_data)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_VALIDATE_AND_REQUEST_TICKET_WITH_CUSTOM_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.result()
		obj.pid = stream.pid()
		obj.ticket = stream.buffer()
		obj.connection_data = stream.extract(RVConnectionData)
		obj.server_name = stream.string()
		obj.source_key = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClientNX.validate_and_request_ticket_with_custom_data -> done")
		return obj
	
	async def request_ticket(self, source, target):
		logger.info("AuthenticationClientNX.request_ticket()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(source)
		stream.pid(target)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REQUEST_TICKET, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.result()
		obj.ticket = stream.buffer()
		obj.key = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClientNX.request_ticket -> done")
		return obj
	
	async def get_pid(self, username):
		logger.info("AuthenticationClientNX.get_pid()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(username)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		pid = stream.pid()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClientNX.get_pid -> done")
		return pid
	
	async def get_name(self, pid):
		logger.info("AuthenticationClientNX.get_name()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_NAME, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		name = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClientNX.get_name -> done")
		return name
	
	async def validate_and_request_ticket_with_param(self, param):
		logger.info("AuthenticationClientNX.validate_and_request_ticket_with_param()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_VALIDATE_AND_REQUEST_TICKET_WITH_PARAM, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.extract(ValidateAndRequestTicketResult)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AuthenticationClientNX.validate_and_request_ticket_with_param -> done")
		return result


class AuthenticationServer(AuthenticationProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_LOGIN: self.handle_login,
			self.METHOD_LOGIN_EX: self.handle_login_ex,
			self.METHOD_REQUEST_TICKET: self.handle_request_ticket,
			self.METHOD_GET_PID: self.handle_get_pid,
			self.METHOD_GET_NAME: self.handle_get_name,
			self.METHOD_LOGIN_WITH_CONTEXT: self.handle_login_with_context,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on AuthenticationServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_login(self, client, input, output):
		logger.info("AuthenticationServer.login()")
		#--- request ---
		username = input.string()
		response = await self.login(client, username)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'pid', 'ticket', 'connection_data', 'server_name']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.pid(response.pid)
		output.buffer(response.ticket)
		output.add(response.connection_data)
		output.string(response.server_name)
	
	async def handle_login_ex(self, client, input, output):
		logger.info("AuthenticationServer.login_ex()")
		#--- request ---
		username = input.string()
		extra_data = input.anydata()
		response = await self.login_ex(client, username, extra_data)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'pid', 'ticket', 'connection_data', 'server_name']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.pid(response.pid)
		output.buffer(response.ticket)
		output.add(response.connection_data)
		output.string(response.server_name)
	
	async def handle_request_ticket(self, client, input, output):
		logger.info("AuthenticationServer.request_ticket()")
		#--- request ---
		source = input.pid()
		target = input.pid()
		response = await self.request_ticket(client, source, target)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'ticket']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.buffer(response.ticket)
	
	async def handle_get_pid(self, client, input, output):
		logger.info("AuthenticationServer.get_pid()")
		#--- request ---
		username = input.string()
		response = await self.get_pid(client, username)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.pid(response)
	
	async def handle_get_name(self, client, input, output):
		logger.info("AuthenticationServer.get_name()")
		#--- request ---
		pid = input.pid()
		response = await self.get_name(client, pid)
		
		#--- response ---
		if not isinstance(response, str):
			raise RuntimeError("Expected str, got %s" %response.__class__.__name__)
		output.string(response)
	
	async def handle_login_with_context(self, client, input, output):
		logger.info("AuthenticationServer.login_with_context()")
		#--- request ---
		login_data = input.anydata()
		response = await self.login_with_context(client, login_data)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'pid', 'ticket', 'connection_data']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.pid(response.pid)
		output.buffer(response.ticket)
		output.add(response.connection_data)
	
	async def login(self, *args):
		logger.warning("AuthenticationServer.login not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def login_ex(self, *args):
		logger.warning("AuthenticationServer.login_ex not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def request_ticket(self, *args):
		logger.warning("AuthenticationServer.request_ticket not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_pid(self, *args):
		logger.warning("AuthenticationServer.get_pid not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_name(self, *args):
		logger.warning("AuthenticationServer.get_name not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def login_with_context(self, *args):
		logger.warning("AuthenticationServer.login_with_context not implemented")
		raise common.RMCError("Core::NotImplemented")


class AuthenticationServerNX(AuthenticationProtocolNX):
	def __init__(self):
		self.methods = {
			self.METHOD_VALIDATE_AND_REQUEST_TICKET: self.handle_validate_and_request_ticket,
			self.METHOD_VALIDATE_AND_REQUEST_TICKET_WITH_CUSTOM_DATA: self.handle_validate_and_request_ticket_with_custom_data,
			self.METHOD_REQUEST_TICKET: self.handle_request_ticket,
			self.METHOD_GET_PID: self.handle_get_pid,
			self.METHOD_GET_NAME: self.handle_get_name,
			self.METHOD_VALIDATE_AND_REQUEST_TICKET_WITH_PARAM: self.handle_validate_and_request_ticket_with_param,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on AuthenticationServerNX: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_validate_and_request_ticket(self, client, input, output):
		logger.info("AuthenticationServerNX.validate_and_request_ticket()")
		#--- request ---
		username = input.string()
		response = await self.validate_and_request_ticket(client, username)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'pid', 'ticket', 'connection_data', 'server_name']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.pid(response.pid)
		output.buffer(response.ticket)
		output.add(response.connection_data)
		output.string(response.server_name)
	
	async def handle_validate_and_request_ticket_with_custom_data(self, client, input, output):
		logger.info("AuthenticationServerNX.validate_and_request_ticket_with_custom_data()")
		#--- request ---
		username = input.string()
		extra_data = input.anydata()
		response = await self.validate_and_request_ticket_with_custom_data(client, username, extra_data)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'pid', 'ticket', 'connection_data', 'server_name', 'source_key']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.pid(response.pid)
		output.buffer(response.ticket)
		output.add(response.connection_data)
		output.string(response.server_name)
		output.string(response.source_key)
	
	async def handle_request_ticket(self, client, input, output):
		logger.info("AuthenticationServerNX.request_ticket()")
		#--- request ---
		source = input.pid()
		target = input.pid()
		response = await self.request_ticket(client, source, target)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'ticket', 'key']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.buffer(response.ticket)
		output.string(response.key)
	
	async def handle_get_pid(self, client, input, output):
		logger.info("AuthenticationServerNX.get_pid()")
		#--- request ---
		username = input.string()
		response = await self.get_pid(client, username)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.pid(response)
	
	async def handle_get_name(self, client, input, output):
		logger.info("AuthenticationServerNX.get_name()")
		#--- request ---
		pid = input.pid()
		response = await self.get_name(client, pid)
		
		#--- response ---
		if not isinstance(response, str):
			raise RuntimeError("Expected str, got %s" %response.__class__.__name__)
		output.string(response)
	
	async def handle_validate_and_request_ticket_with_param(self, client, input, output):
		logger.info("AuthenticationServerNX.validate_and_request_ticket_with_param()")
		#--- request ---
		param = input.extract(ValidateAndRequestTicketParam)
		response = await self.validate_and_request_ticket_with_param(client, param)
		
		#--- response ---
		if not isinstance(response, ValidateAndRequestTicketResult):
			raise RuntimeError("Expected ValidateAndRequestTicketResult, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def validate_and_request_ticket(self, *args):
		logger.warning("AuthenticationServerNX.validate_and_request_ticket not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def validate_and_request_ticket_with_custom_data(self, *args):
		logger.warning("AuthenticationServerNX.validate_and_request_ticket_with_custom_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def request_ticket(self, *args):
		logger.warning("AuthenticationServerNX.request_ticket not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_pid(self, *args):
		logger.warning("AuthenticationServerNX.get_pid not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_name(self, *args):
		logger.warning("AuthenticationServerNX.get_name not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def validate_and_request_ticket_with_param(self, *args):
		logger.warning("AuthenticationServerNX.validate_and_request_ticket_with_param not implemented")
		raise common.RMCError("Core::NotImplemented")

