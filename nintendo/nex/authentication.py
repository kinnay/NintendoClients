
# This file was generated automatically from authentication.proto

from nintendo.nex import common

import logging
logger = logging.getLogger(__name__)


class AuthenticationInfo(common.Data):
	def __init__(self):
		super().__init__()
		self.token = None
		self.ngs_version = 3
		self.token_type = 1
		self.server_version = None

	def check_required(self, settings):
		for field in ['token', 'server_version']:
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
		if settings.get("server.version") >= 30500:
			version = 1
		return version

	def check_required(self, settings):
		for field in ['main_station', 'special_protocols', 'special_station']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings.get("server.version") >= 30500:
			for field in ['server_time']:
				if getattr(self, field) is None:
					raise ValueError("No value assigned to required field: %s" %field)

	def load(self, stream):
		self.main_station = stream.stationurl()
		self.special_protocols = stream.list(stream.u8)
		self.special_station = stream.stationurl()
		if stream.settings.get("server.version") >= 30500:
						self.server_time = stream.datetime()

	def save(self, stream):
		self.check_required(stream.settings)
		stream.stationurl(self.main_station)
		stream.list(self.special_protocols, stream.u8)
		stream.stationurl(self.special_station)
		if stream.settings.get("server.version") >= 30500:
						stream.datetime(self.server_time)


class AuthenticationProtocol:
	METHOD_LOGIN = 1
	METHOD_LOGIN_EX = 2
	METHOD_REQUEST_TICKET = 3
	METHOD_GET_PID = 4
	METHOD_GET_NAME = 5

	PROTOCOL_ID = 0xA


class AuthenticationClient(AuthenticationProtocol):
	def __init__(self, client):
		self.client = client

	def login(self, username):
		logger.info("AuthenticationClient.login()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_LOGIN)
		stream.string(username)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		obj = common.ResponseObject()
		obj.result = stream.result()
		obj.pid = stream.pid()
		obj.ticket = stream.buffer()
		obj.connection_data = stream.extract(RVConnectionData)
		obj.server_name = stream.string()
		logger.info("AuthenticationClient.login -> done")
		return obj

	def login_ex(self, username, extra_data):
		logger.info("AuthenticationClient.login_ex()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_LOGIN_EX)
		stream.string(username)
		stream.anydata(extra_data)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		obj = common.ResponseObject()
		obj.result = stream.result()
		obj.pid = stream.pid()
		obj.ticket = stream.buffer()
		obj.connection_data = stream.extract(RVConnectionData)
		obj.server_name = stream.string()
		logger.info("AuthenticationClient.login_ex -> done")
		return obj

	def request_ticket(self, source, target):
		logger.info("AuthenticationClient.request_ticket()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_REQUEST_TICKET)
		stream.pid(source)
		stream.pid(target)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		obj = common.ResponseObject()
		obj.result = stream.result()
		obj.ticket = stream.buffer()
		logger.info("AuthenticationClient.request_ticket -> done")
		return obj

	def get_pid(self, username):
		logger.info("AuthenticationClient.get_pid()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_PID)
		stream.string(username)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		pid = stream.pid()
		logger.info("AuthenticationClient.get_pid -> done")
		return pid

	def get_name(self, pid):
		logger.info("AuthenticationClient.get_name()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_NAME)
		stream.pid(pid)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		name = stream.string()
		logger.info("AuthenticationClient.get_name -> done")
		return name


class AuthenticationServer(AuthenticationProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_LOGIN: self.handle_login,
			self.METHOD_LOGIN_EX: self.handle_login_ex,
			self.METHOD_REQUEST_TICKET: self.handle_request_ticket,
			self.METHOD_GET_PID: self.handle_get_pid,
			self.METHOD_GET_NAME: self.handle_get_name,
		}

	def handle(self, caller_id, method_id, input, output):
		if method_id in self.methods:
			return self.methods[method_id](caller_id, input, output)
		logger.warning("Unknown method called on AuthenticationServer: %i", method_id)
		return common.Result("Core::NotImplemented")

	def handle_login(self, caller_id, input, output):
		logger.info("AuthenticationServer.login()")
		#--- request ---
		username = input.string()
		response = common.ResponseObject()
		self.login(caller_id, response, username)

		#--- response ---
		for field in ['result', 'pid', 'ticket', 'connection_data', 'server_name']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in response object: %s" %field)
		output.result(response.result)
		output.pid(response.pid)
		output.buffer(response.ticket)
		output.add(response.connection_data)
		output.string(response.server_name)

	def handle_login_ex(self, caller_id, input, output):
		logger.info("AuthenticationServer.login_ex()")
		#--- request ---
		username = input.string()
		extra_data = input.anydata()
		response = common.ResponseObject()
		self.login_ex(caller_id, response, username, extra_data)

		#--- response ---
		for field in ['result', 'pid', 'ticket', 'connection_data', 'server_name']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in response object: %s" %field)
		output.result(response.result)
		output.pid(response.pid)
		output.buffer(response.ticket)
		output.add(response.connection_data)
		output.string(response.server_name)

	def handle_request_ticket(self, caller_id, input, output):
		logger.info("AuthenticationServer.request_ticket()")
		#--- request ---
		source = input.pid()
		target = input.pid()
		response = common.ResponseObject()
		self.request_ticket(caller_id, response, source, target)

		#--- response ---
		for field in ['result', 'ticket']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in response object: %s" %field)
		output.result(response.result)
		output.buffer(response.ticket)

	def handle_get_pid(self, caller_id, input, output):
		logger.info("AuthenticationServer.get_pid()")
		#--- request ---
		username = input.string()
		response = self.get_pid(username)

		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.pid(response)

	def handle_get_name(self, caller_id, input, output):
		logger.info("AuthenticationServer.get_name()")
		#--- request ---
		pid = input.pid()
		response = self.get_name(pid)

		#--- response ---
		if not isinstance(response, str):
			raise RuntimeError("Expected str, got %s" %response.__class__.__name__)
		output.string(response)

	def login(self, *args):
		logger.warning("AuthenticationServer.login not implemented")
		return common.Result("Core::NotImplemented")

	def login_ex(self, *args):
		logger.warning("AuthenticationServer.login_ex not implemented")
		return common.Result("Core::NotImplemented")

	def request_ticket(self, *args):
		logger.warning("AuthenticationServer.request_ticket not implemented")
		return common.Result("Core::NotImplemented")

	def get_pid(self, *args):
		logger.warning("AuthenticationServer.get_pid not implemented")
		return common.Result("Core::NotImplemented")

	def get_name(self, *args):
		logger.warning("AuthenticationServer.get_name not implemented")
		return common.Result("Core::NotImplemented")
