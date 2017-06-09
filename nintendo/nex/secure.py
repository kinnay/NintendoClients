
from nintendo.nex.service import ServiceClient
from nintendo.nex.kerberos import KerberosEncryption
from nintendo.nex.stream import NexStreamOut
from nintendo.nex.common import NexEncoder, DataHolder, StationUrl
import random

import logging
logger = logging.getLogger(__name__)


class ConnectionData(NexEncoder):
	version_map = {
		30504: 0,
		30810: 0
	}
	
	def decode_old(self, stream):
		self.station = StationUrl(stream.string())
		self.connection_id = stream.u32()
		
	decode_v0 = decode_old


class SecureClient(ServiceClient):
	
	METHOD_REGISTER = 1
	METHOD_REQUEST_CONNECTION_DATA = 2
	METHOD_REQUEST_URLS = 3
	METHOD_REGISTER_EX = 4
	METHOD_TEST_CONNECTIVITY = 5
	METHOD_UPDATE_URLS = 6
	METHOD_REPLACE_URL = 7
	METHOD_SEND_REPORT = 8
	
	PROTOCOL_ID = 0xB
	
	def __init__(self, back_end, key, ticket, auth_client):
		super().__init__(back_end, key)
		self.ticket = ticket
		self.auth_client = auth_client
		self.kerberos_encryption = KerberosEncryption(self.ticket.key)
		
		station_url = self.auth_client.secure_station
		self.connection_id = int(station_url["CID"])
		self.principal_id = int(station_url["PID"])
		
	def connect(self, host, port):
		stream = NexStreamOut(self.back_end.version)
		stream.data(self.ticket.data)
		
		substream = NexStreamOut(self.back_end.version)
		substream.u32(self.auth_client.user_id)
		substream.u32(self.connection_id)
		substream.u32(random.randint(0, 0xFFFFFFFF)) #Used to check connection response
		
		stream.data(self.kerberos_encryption.encrypt(substream.buffer))
		super().connect(host, port, stream.buffer)
		
		self.set_secure_key(self.ticket.key)
		
	def register(self):
		logger.info("Secure.register()")
		#--- request ---
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_REGISTER)
		client_url = str(StationUrl.make(address=self.s.get_address(), port=self.s.get_port(), sid=15, natm=0, natf=0, upnp=0, pmp=0))
		stream.list([client_url], lambda x: stream.string(x))
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		result = stream.u32()
		connection_id = stream.u32()
		client_station = stream.string()
		logger.info("Secure.register -> (%i, %s)", connection_id, client_station)
		return client_station
		
	def request_connection_data(self, cid, pid):
		logger.info("Secure.request_connection_data(%i, %i)", cid, pid)
		#--- request ---
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_REQUEST_CONNECTION_DATA)
		stream.u32(cid)
		stream.u32(pid)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		bool = stream.bool()
		connection_data = stream.list(lambda: ConnectionData.from_stream(stream))
		logger.info("Secure.request_connection_data -> (%i, %s)", bool, [dat.station for dat in connection_data])
		return bool, connection_data
		
	def request_urls(self, cid, pid):
		logger.info("Secure.request_urls(%i, %i)", cid, pid)
		#--- request ---
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_REQUEST_URLS)
		stream.u32(cid)
		stream.u32(pid)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		bool = stream.bool()
		urls = stream.list(lambda: StationUrl(stream.string()))
		logger.info("Secure.request_urls -> (%i, %s)", bool, urls)
		return bool, urls
		
	def register_ex(self, login_data):
		logger.info("Secure.register_ex(...)")
		#--- request ---
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_REGISTER_EX)
		client_url = str(StationUrl.make(address=self.s.get_address(), port=self.s.get_port(), sid=15, natm=0, natf=0, upnp=0, pmp=0))
		stream.list([client_url], lambda x: stream.string(x))
		DataHolder(login_data).encode(stream)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		result = stream.u32()
		connection_id = stream.u32()
		client_station = stream.string()
		logger.info("Secure.register_ex -> (%i, %s)", connection_id, client_station)
		return client_station
	
	def test_connectivity(self):
		logger.info("Secure.test_connectivity()")
		#--- request ---
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_TEST_CONNECTIVITY)
		self.send_message(stream)
		
		#--- response ---
		self.get_response(call_id)
		logger.info("Secure.test_connectivity -> done")
		
	def replace_url(self, url, new):
		logger.info("Secure.replace_url(%s, %s)", url, new)
		#--- request ---
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_REPLACE_URL)
		stream.string(url)
		stream.string(new)
		self.send_message(stream)
		
		#--- response ---
		self.get_response(call_id)
		logger.info("Secure.replace_url -> done")
		
	def send_report(self, unk, data):
		logger.info("Secure.send_report(%08X, ...)")
		#--- request ---
		stream, call_id = self.init_message(self.PROTOCOL_ID, self.METHOD_SEND_REPORT)
		stream.u32(unk)
		stream.u16(len(data))
		stream.write(data)
		self.send_message(stream)
		
		#--- response ---
		self.get_response(call_id)
		logger.info("Secure.send_report -> done")
