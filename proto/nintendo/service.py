
from proto.nintendo.prudp import PRUDP
from proto.nintendo.errors import errors
from proto.common.stream import StreamOut, StreamIn, Encoder
from proto.common.crypto import RC4

import struct
import time
import hashlib
import hmac
import random

import logging
logger = logging.getLogger(__name__)


class ServiceClient(PRUDP):
	def __init__(self, key):
		super().__init__(key)
		self.call_id = 0
		
		self.responses = {}
		
	def init_message(self, stream, protocol_id, method_id):
		self.call_id += 1
		stream.u8(protocol_id | 0x80)
		stream.u32(self.call_id)
		stream.u32(method_id)
		return self.call_id
		
	def send_message(self, stream):
		self.send(struct.pack("I", len(stream.buffer)) + stream.buffer)
		
	def get_response(self, call_id):
		while call_id not in self.responses:
			time.sleep(0.05)
			
		error, stream = self.responses.pop(call_id)
		if error:
			raise ConnectionError(error, "RMC failed (%s)" %errors.get(error, "unknown error"))
		return stream
		
	def on_data(self, data):
		stream = StreamIn(data)
		length = stream.u32()
		
		protocol_id = stream.u8()

		success = stream.u8()
		if not success:
			error_code = stream.u32()
			call_id = stream.u32()

			logger.error("RMC failed with error code %08X", error_code)
			self.responses[call_id] = (error_code, None)

		else:
			call_id = stream.u32()
			method_id = stream.u32()
			logger.debug("Received RMC response: protocol=%i, call=%i, method=%i", protocol_id, call_id, method_id)

			self.responses[call_id] = (0, stream)
		
		
class KerberosEncryption:
	def __init__(self, key):
		self.key = key
		self.rc4 = RC4(key)
		
	def decrypt(self, buffer):
		data = buffer[:-0x10] #Remove checksum
		return self.rc4.crypt(data)
		
	def encrypt(self, buffer):
		encrypted = self.rc4.crypt(buffer)
		mac = hmac.HMAC(self.key)
		mac.update(encrypted)
		return encrypted + mac.digest()

	
class AuthenticationInfo(Encoder):
	def __init__(self, token=None):
		self.token = token
		
	def encode(self, stream):
		stream.string("AuthenticationInfo", stream.u16)
		
		substream = StreamOut()
		substream.string(self.token, substream.u16)
		substream.u32(3)
		substream.u8(1)
		substream.u32(3)
		stream.data(struct.pack("I", len(substream.buffer)) + substream.buffer, stream.u32)
	
	
class RVConnectionData(Encoder):
	def decode(self, stream):
		self.main_station = stream.string(stream.u16)
		self.unk_list = stream.list(stream.u8, stream.u32)
		self.unk_station = stream.string(stream.u16)
		
	def get(self, field):
		substr = self.main_station.split(field + "=")[1]
		return substr[:substr.find(";")] if ";" in substr else substr
		
		
class ConnectionData(Encoder):
	def decode(self, stream):	
		self.station = stream.string(stream.u16)
		self.connection_id = stream.u32()


class Ticket:
	def __init__(self, key, data):
		self.key = key
		self.data = data
	
	
class AuthenticationClient(ServiceClient):
	
	METHOD_LOGIN = 1
	METHOD_LOGIN_EX = 2
	METHOD_REQUEST_TICKET = 3
	METHOD_GET_PID = 4
	METHOD_GET_NAME = 5
	METHOD_LOGIN_WITH_CONTEXT = 6
	
	PROTOCOL_ID = 0xA
	
	def login(self, username, password):
		logger.info("Logging in with username (%s) and password (%s)", username, password)
		#--- request ---
		stream = StreamOut()
		call_id = self.init_message(stream, self.PROTOCOL_ID, self.METHOD_LOGIN)
		stream.string(username, stream.u16)
		self.send_message(stream)
		
		#--- response ---
		self.handle_login_result(call_id, password)

	def login_ex(self, username, password, token):
		logger.info("Logging in with username(%s), password(%s) and token", username, password)
		#--- request ---
		stream = StreamOut()
		call_id = self.init_message(stream, self.PROTOCOL_ID, self.METHOD_LOGIN_EX)
		stream.string(username, stream.u16)
		AuthenticationInfo(token).encode(stream)
		self.send_message(stream)
		
		#--- response ---
		self.handle_login_result(call_id, password)
		
	def handle_login_result(self, call_id, password):
		stream = self.get_response(call_id)
		result = stream.u32()
		self.user_id = stream.u32()
		kerberos_data = stream.read(stream.u32()) #Used to validate kerberos key
		self.connection_data = RVConnectionData.from_stream(stream)
		server_name = stream.string(stream.u16)

		kerberos_key = password.encode("ascii")
		for i in range(65000 + self.user_id % 1024):
			kerberos_key = hashlib.md5(kerberos_key).digest()
		self.kerberos_encryption = KerberosEncryption(kerberos_key)
		
		logger.info("Login result: user_id=%08X, station=%s, server=%s", self.user_id, self.connection_data.main_station, server_name)
		
	def request_ticket(self):
		logger.info("Requesting Kerberos ticket")
		#--- request ---
		stream = StreamOut()
		call_id = self.init_message(stream, self.PROTOCOL_ID, self.METHOD_REQUEST_TICKET)
		stream.u32(self.user_id)
		stream.u32(int(self.connection_data.get("PID")))
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		result = stream.u32()
		
		encrypted_ticket = stream.read(stream.u32())
		ticket_data = self.kerberos_encryption.decrypt(encrypted_ticket)
		ticket_key = ticket_data[:0x20]
		length = struct.unpack_from("I", ticket_data, 0x24)[0]
		ticket_buffer = ticket_data[0x28 : 0x28 + length]
		logger.info("Kerberos ticket key is %s", ticket_key.hex())
		return Ticket(ticket_key, ticket_buffer)
		
	def get_pid(self, name):
		logger.info("Requesting PID for %s", name)
		#--- request ---
		stream = StreamOut()
		call_id = self.init_message(stream, self.PROTOCOL_ID, self.METHOD_GET_PID)
		stream.string(name, stream.u16)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		pid = stream.u32()
		logger.info("PID response: %i", pid)
		return pid
		
	def get_name(self, id):
		logger.info("Requesting name for %i", id)
		#--- request ---
		stream = StreamOut()
		call_id = self.init_message(stream, self.PROTOCOL_ID, self.METHOD_GET_NAME)
		stream.u32(id)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		name = stream.string(stream.u16)
		logger.info("Name response: %s", name)
		return name
		
		
class SecureClient(ServiceClient):
	
	METHOD_REGISTER = 1
	METHOD_REQUEST_CONNECTION_DATA = 2
	METHOD_REQUEST_URLS = 3
	METHOD_REGISTER_EX = 4
	METHOD_TEST_CONNECTIVITY = 5
	
	PROTOCOL_ID = 0xB
	
	def __init__(self, key, ticket, auth_client):
		super().__init__(key)
		self.ticket = ticket
		self.auth_client = auth_client
		self.kerberos_encryption = KerberosEncryption(self.ticket.key)
		
		connection_info = self.auth_client.connection_data
		self.connection_id = int(connection_info.get("CID"))
		self.principal_id = int(connection_info.get("PID"))
		
	def connect(self, host, port):
		#--- request ---
		stream = StreamOut()
		stream.data(self.ticket.data, stream.u32)
		
		substream = StreamOut()
		substream.u32(self.auth_client.user_id)
		substream.u32(self.connection_id)
		substream.u32(random.randint(0, 0xFFFFFFFF)) #Used to check connection response
		
		stream.data(self.kerberos_encryption.encrypt(substream.buffer), stream.u32)
		super().connect(host, port, stream.buffer)
		
		self.set_secure_key(self.ticket.key)
		
	def register(self):
		#--- request ---
		stream = StreamOut()
		call_id = self.init_message(stream, self.PROTOCOL_ID, self.METHOD_REGISTER)
		client_url = "prudp:/address=%s;port=%d;sid=15;natm=0;natf=0;upnp=0;pmp=0" %(
			self.s.get_address(), self.s.get_port()
		)
		stream.list([client_url], lambda x: stream.string(x, stream.u16), stream.u32)
		logger.info("Registering client to secure server - %s", client_url)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		result = stream.u32()
		connection_id = stream.u32()
		client_station = stream.string(stream.u16)
		logger.info("Connection id: %i, client station: %s", connection_id, client_station)
		
	def request_connection_data(self, cid, pid):
		#--- request ---
		stream = StreamOut()
		call_id = self.init_message(stream, self.PROTOCOL_ID, self.METHOD_REQUEST_CONNECTION_DATA)
		stream.u32(cid)
		stream.u32(pid)
		self.send_message(stream)
		logger.info("Requesting connection data from secure server for (%i, %i)", self.connection_id, self.principal_id)
		
		#--- response ---
		stream = self.get_response(call_id)
		bool = stream.bool()
		connection_data = stream.list(lambda: ConnectionData.from_stream(stream), stream.u32)
		return bool, connection_data
		
	def request_urls(self, arg1, arg2):
		#--- request ---
		stream = StreamOut()
		call_id = self.init_message(stream, self.PROTOCOL_ID, self.METHOD_REQUEST_URLS)
		stream.u32(arg1)
		stream.u32(arg2)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		bool = stream.bool()
		urls = stream.list(lambda: stream.string(stream.u16), stream.u32)
		return bool, urls
		
		
	def test_connectivity(self):
		#--- request ---
		stream = StreamOut()
		call_id = self.init_message(stream, self.PROTOCOL_ID, self.METHOD_TEST_CONNECTIVITY)
		self.send_message(stream)
		
		#--- response ---
		self.get_response(call_id)
		
		
class BackEndClient:
	def __init__(self, access_key):
		self.access_key = access_key.encode("ascii")
		
		self.auth_client = None
		self.secure_client = None
		
	def connect(self, host, port):
		self.auth_client = AuthenticationClient(self.access_key)
		self.auth_client.connect(host, port)
		
	def close(self):
		self.auth_client.close()
		if self.secure_client:	
			self.secure_client.close()
		
	def login(self, username, password, token=None):
		if token:
			self.auth_client.login_ex(username, password, token)
		else:
			self.auth_client.login(username, password)
		ticket = self.auth_client.request_ticket()
		host = self.auth_client.connection_data.get("address")
		port = int(self.auth_client.connection_data.get("port"))
		
		self.secure_client = SecureClient(self.access_key, ticket, self.auth_client)
		self.secure_client.connect(host, port)
		self.secure_client.register()
