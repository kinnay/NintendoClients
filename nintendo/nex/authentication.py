
from nintendo.nex.service import ServiceClient
from nintendo.nex.stream import NexStreamOut
from nintendo.nex.common import NexEncoder, NexDataEncoder, DataHolder, StationUrl, DateTime
from nintendo.nex.kerberos import KerberosEncryption, Ticket
from nintendo.nex.friends import FriendsTitle
from nintendo.nex.errors import error_names
from nintendo.common.stream import StreamIn
import hashlib
import struct

import logging
logger = logging.getLogger(__name__)


class AuthenticationError(Exception): pass


class AuthenticationInfo(NexDataEncoder):
	version_map = {
		30504: 0
	}
	
	#As nex versions increase, these values increase as well
	nex_versions = {
		30400: 3,
		30504: 2002,
		30810: 3017
	}
	
	def init(self, token):
		self.token = token
		
	def get_name(self):
		return "AuthenticationInfo"
		
	def encode_old(self, stream):
		stream.string(self.token)
		stream.u32(3)
		stream.u8(1)
		stream.u32(self.nex_versions[stream.version])
		
	encode_v0 = encode_old
DataHolder.register(AuthenticationInfo, "AuthenticationInfo")
	
	
class ConnectionData(NexEncoder):
	version_map = {
		30504: 1
	}
	
	def decode_old(self, stream):
		self.main_station = StationUrl.parse(stream.string())
		self.unk_list = stream.list(stream.u8)
		self.unk_station = StationUrl.parse(stream.string())
		
	def decode_v1(self, stream):
		self.decode_old(stream)
		self.server_time = DateTime(stream.u64())


class AuthenticationClient(ServiceClient):
	
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
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_LOGIN)
		stream.string(username)
		self.send_message(stream)
		
		#--- response ---
		self.handle_login_result(call_id, password)
		
	def login_ex(self, username, password, token):
		logger.info("Authentication.login_ex(%s, %s, %s)", username, password, token)
		#--- request ---
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_LOGIN_EX)
		stream.string(username)
		DataHolder(AuthenticationInfo(token)).encode(stream)
		self.send_message(stream)
		
		#--- response ---
		self.handle_login_result(call_id, password)
		
	def handle_login_result(self, call_id, password):
		stream = self.get_response(call_id)
		result = stream.u32()
		if result & 0x80000000:
			raise AuthenticationError("NEX authentication failed (%s)" %error_names.get(result, "unknown error"))
			
		self.user_id = stream.u32()
		kerberos_data = stream.data()
		self.secure_station = ConnectionData.from_stream(stream).main_station
		server_name = stream.string()
		
		kerberos_key = password.encode("ascii")
		for i in range(65000 + self.user_id % 1024):
			kerberos_key = hashlib.md5(kerberos_key).digest()
		self.kerberos_encryption = KerberosEncryption(kerberos_key)
		self.kerberos_encryption.decrypt(kerberos_data) #Validate kerberos key 
		
		logger.info("Authentication.login(_ex) -> (%08X, %s, %s)", self.user_id, self.secure_station, server_name)
		
	def request_ticket(self):
		logger.info("Authentication.request_ticket()")
		#--- request ---
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_REQUEST_TICKET)
		stream.u32(self.user_id)
		stream.u32(self.secure_station["PID"])
		self.send_message(stream)

		#--- response ---
		stream = self.get_response(call_id)
		result = stream.u32()
		
		key_length = 32
		if self.back_end.version == FriendsTitle.NEX_VERSION:
			key_length = 16
		
		encrypted_ticket = stream.data()
		ticket_data = StreamIn(self.kerberos_encryption.decrypt(encrypted_ticket))
		ticket_key = ticket_data.read(key_length)
		ticket_data.u32() #Unknown
		ticket_buffer = ticket_data.read(ticket_data.u32())

		logger.info("Authentication.request_ticket -> %s", ticket_key.hex())
		return Ticket(ticket_key, ticket_buffer)
		
	def get_pid(self, name):
		logger.info("Authentication.get_pid(%s)", name)
		#--- request ---
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_GET_PID)
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
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_GET_NAME)
		stream.u32(id)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		name = stream.string()
		logger.info("Authentication.get_name -> %s", name)
		return name
