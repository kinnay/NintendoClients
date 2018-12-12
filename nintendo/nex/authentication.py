
from nintendo.nex import service, common, streams, kerberos, errors

import logging
logger = logging.getLogger(__name__)


class AuthenticationError(Exception): pass


class AuthenticationInfo(common.Data):
	def __init__(self, token, server_version):
		self.token = token
		self.server_version = server_version
		
	def get_name(self):
		return "AuthenticationInfo"

	def save(self, stream):
		stream.string(self.token)
		stream.u32(3)
		stream.u8(1)
		stream.u32(self.server_version)
common.DataHolder.register(AuthenticationInfo, "AuthenticationInfo")


class NintendoLoginData(common.Data):
	def __init__(self, token):
		self.token = token
		
	def get_name(self):
		return "NintendoLoginData"
		
	def save(self, stream):
		stream.string(self.token)
common.DataHolder.register(NintendoLoginData, "NintendoLoginData")
	
	
class RVConnectionData(common.Structure):
	def get_version(self):
		return 1
	
	def load(self, stream):
		self.main_station = stream.stationurl()
		self.special_protocols = stream.list(stream.u8)
		self.special_station = stream.stationurl()
		
		self.server_time = None
		if self.version >= 1:
			self.server_time = stream.datetime()


class AuthenticationClient(service.ServiceClient):
	
	METHOD_LOGIN = 1
	METHOD_LOGIN_EX = 2
	METHOD_REQUEST_TICKET = 3
	METHOD_GET_PID = 4
	METHOD_GET_NAME = 5
	METHOD_LOGIN_WITH_CONTEXT = 6
	
	PROTOCOL_ID = 0xA
	
	def __init__(self, backend):
		super().__init__(backend, service.ServiceClient.AUTHENTICATION)
		self.settings = backend.settings
		
	def login(self, username):
		logger.info("Authentication.login(%s)", username)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_LOGIN)
		stream.string(username)
		self.send_message(stream)
		
		#--- response ---
		return self.handle_login_result(call_id)
		
	def login_ex(self, username, auth_info):
		logger.info("Authentication.login_ex(%s, %s)", username, auth_info.__class__.__name__)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_LOGIN_EX)
		stream.string(username)
		stream.anydata(auth_info)
		self.send_message(stream)
		
		#--- response ---
		return self.handle_login_result(call_id)
		
	def handle_login_result(self, call_id):
		stream = self.get_response(call_id)
		result = stream.u32()
		if result & 0x80000000:
			raise AuthenticationError("Login failed (%s)" %errors.error_names.get(result, "unknown error"))
			
		self.pid = stream.pid()
		ticket_data = stream.buffer()
		self.secure_station = stream.extract(RVConnectionData).main_station
		server_name = stream.string()

		logger.info("Authentication.login(_ex) -> (%i, %s, %s)", self.pid, self.secure_station, server_name)
		return kerberos.Ticket(ticket_data)
		
	def request_ticket(self, source, target):
		logger.info("Authentication.request_ticket(%i, %i)", source, target)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_REQUEST_TICKET)
		stream.pid(source)
		stream.pid(target)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		result = stream.u32()
		if result & 0x80000000:
			raise AuthenticationError("Ticket request failed (%s)" %errors.error_names.get(result, "unknown error"))

		ticket_data = stream.buffer()
		logger.info("Authentication.request_ticket -> %i bytes" %len(ticket_data))
		return kerberos.Ticket(ticket_data)
		
	def get_pid(self, name):
		logger.info("Authentication.get_pid(%s)", name)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_GET_PID)
		stream.string(name)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		pid = stream.pid()
		logger.info("Authentication.get_pid -> %i", pid)
		return pid
		
	def get_name(self, id):
		logger.info("Authentication.get_name(%i)", id)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_GET_NAME)
		stream.pid(id)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		name = stream.string()
		logger.info("Authentication.get_name -> %s", name)
		return name
