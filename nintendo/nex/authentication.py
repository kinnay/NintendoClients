
from nintendo.nex import service, common, streams, kerberos, friends, errors
import hashlib
import struct

import logging
logger = logging.getLogger(__name__)


class AuthenticationError(Exception): pass


class AuthenticationInfo(common.Data):
	def __init__(self, token, server_version):
		self.token = token
		self.server_version = server_version
		
	def get_name(self):
		return "AuthenticationInfo"

	def streamin(self, stream):
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
		
	def streamin(self, stream):
		stream.string(self.token)
common.DataHolder.register(NintendoLoginData, "NintendoLoginData")
	
	
class RVConnectionData(common.Structure):
	def get_version(self, nex_version):
		return 1
	
	def streamout(self, stream):
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
		
	def login(self, username, password):
		logger.info("Authentication.login(%s, %s)", username, password)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_LOGIN)
		stream.string(username)
		self.send_message(stream)
		
		#--- response ---
		self.handle_login_result(call_id, password)
		
	def login_ex(self, username, password, auth_info):
		logger.info("Authentication.login_ex(%s, %s, %s)", username, password, auth_info.__class__.__name__)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_LOGIN_EX)
		stream.string(username)
		stream.add(common.DataHolder(auth_info))
		self.send_message(stream)
		
		#--- response ---
		self.handle_login_result(call_id, password)
		
	def handle_login_result(self, call_id, password):
		stream = self.get_response(call_id)
		result = stream.u32()
		if result & 0x80000000:
			raise AuthenticationError("NEX authentication failed (%s)" %errors.error_names.get(result, "unknown error"))
			
		self.pid = stream.u32()
		kerberos_data = stream.buffer()
		self.secure_station = stream.extract(RVConnectionData).main_station
		server_name = stream.string()
		
		kerberos_key = password.encode("ascii")
		for i in range(65000 + self.pid % 1024):
			kerberos_key = hashlib.md5(kerberos_key).digest()
		self.kerberos_encryption = kerberos.KerberosEncryption(kerberos_key)
		self.kerberos_encryption.decrypt(kerberos_data) #Validate kerberos key 

		logger.info("Authentication.login(_ex) -> (%08X, %s, %s)", self.pid, self.secure_station, server_name)
		
	def request_ticket(self):
		logger.info("Authentication.request_ticket()")
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_REQUEST_TICKET)
		stream.u32(self.pid)
		stream.u32(self.secure_station["PID"])
		self.send_message(stream)

		#--- response ---
		stream = self.get_response(call_id)
		result = stream.u32()
		
		key_length = 32
		if self.back_end.game_server_id == friends.FriendsTitle.GAME_SERVER_ID:
			key_length = 16
		
		encrypted_ticket = stream.buffer()
		ticket_data = streams.StreamIn(self.kerberos_encryption.decrypt(encrypted_ticket), stream.version)
		ticket_key = ticket_data.read(key_length)
		ticket_data.u32() #Unknown
		ticket_buffer = ticket_data.read(ticket_data.u32())

		logger.info("Authentication.request_ticket -> %s", ticket_key.hex())
		return kerberos.Ticket(ticket_key, ticket_buffer)
		
	def get_pid(self, name):
		logger.info("Authentication.get_pid(%s)", name)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_GET_PID)
		stream.string(name)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		pid = stream.u32()
		logger.info("Authentication.get_pid -> %i", pid)
		return pid
		
	def get_name(self, id):
		logger.info("Authentication.get_name(%i)", id)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_GET_NAME)
		stream.u32(id)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		name = stream.string()
		logger.info("Authentication.get_name -> %s", name)
		return name
