
from nintendo.common import scheduler
from nintendo.nex import prudp, streams, kerberos, common
import random
import struct
import time

import logging
logger = logging.getLogger(__name__)


class ServiceClient:
	def __init__(self, settings):
		self.client = prudp.PRUDPClient(settings)
		
		self.settings = settings
		self.servers = {}

		self.call_id = 0
		self.responses = {}
		
	def register_server(self, server):
		if server.PROTOCOL_ID in self.servers:
			raise ValueError("Server with protocol id 0x%X already exists" %server.PROTOCOL_ID)
		self.servers[server.PROTOCOL_ID] = server
		
	def connect(self, host, port, stream_id, ticket=None):
		if ticket:
			check_value = random.randint(0, 0xFFFFFFFF)
			request = self.build_connection_request(check_value, ticket)
			response = self.connect_socket(host, port, stream_id, request)
			self.check_connection_response(response, check_value)
			
			self.client.set_session_key(ticket.session_key)
		else:
			self.connect_socket(host, port, stream_id, b"")
			
		self.socket_event = scheduler.add_socket(self.handle_recv, self.client)
		return self.client.connect_response
		
	def connect_socket(self, host, port, stream_id, payload):
		if not self.client.connect(host, port, stream_id, payload):
			raise ConnectionError("PRUDP connection failed")
		return self.client.connect_response
		
	def build_connection_request(self, check_value, ticket):
		kerb = kerberos.KerberosEncryption(ticket.session_key)
		
		stream = streams.StreamOut(self.settings)
		stream.buffer(ticket.internal)
		
		substream = streams.StreamOut(self.settings)
		substream.pid(ticket.source_pid)
		substream.u32(ticket.target_cid)
		substream.u32(check_value) #Used to check connection response
		
		stream.buffer(kerb.encrypt(substream.get()))
		return stream.get()
		
	def check_connection_response(self, response, check_value):
		stream = streams.StreamIn(response, self.settings)
		if stream.u32() != 4: raise ConnectionError("Invalid connection response size")
		if stream.u32() != (check_value + 1) & 0xFFFFFFFF:
			raise ConnectionError("Connection response check failed")
		
	def stream_id(self):
		return self.client.client_port
		
	def close(self):
		if self.is_connected():
			scheduler.remove(self.socket_event)
			self.client.close()
		
	def is_connected(self): return self.client.is_connected()
	def client_address(self): return self.client.client_address()
	def server_address(self): return self.client.server_address()
		
	def handle_recv(self, data):
		if not data:
			logger.debug("Connection was closed")
			scheduler.remove(self.socket_event)
			return

		stream = streams.StreamIn(data, self.settings)
		length = stream.u32()
		protocol_id = stream.u8()

		if protocol_id & 0x80:
			self.handle_request(protocol_id & 0x7F, stream)
		else:
			self.handle_response(protocol_id, stream)

	def init_request(self, protocol_id, method_id):
		self.call_id += 1
		stream = streams.StreamOut(self.settings)
		stream.u8(protocol_id | 0x80)
		stream.u32(self.call_id)
		stream.u32(method_id)
		return stream, self.call_id
		
	def init_response(self, protocol_id, call_id, method_id, error=None):
		stream = streams.StreamOut(self.settings)
		stream.u8(protocol_id)
		if error:
			stream.u8(0)
			stream.result(error)
			stream.u32(call_id)
		else:
			stream.u8(1)
			stream.u32(call_id)
			stream.u32(method_id | 0x8000)
		return stream
		
	def send_message(self, stream):
		if self.client.is_connected():
			self.client.send(struct.pack("I", len(stream.get())) + stream.get())
		else:
			raise RuntimeError("Can't send message on disconnected service client")
			
	def handle_request(self, protocol_id, stream):
		call_id = stream.u32()
		method_id = stream.u32()
		logger.debug("Received RMC request: protocol=%i, call=%i, method=%i", protocol_id, call_id, method_id)
		
		if protocol_id in self.servers:
			response = self.init_response(protocol_id, call_id, method_id)
			try:
				result = self.servers[protocol_id].handle(method_id, stream, response)
			except Exception as e:
				logger.error("Exception occurred while handling method call")
				import traceback
				traceback.print_exc()
				if isinstance(e, TypeError): result = common.Result("PythonCore::TypeError")
				elif isinstance(e, IndexError): result = common.Result("PythonCore::IndexError")
				elif isinstance(e, MemoryError): result = common.Result("PythonCore::MemoryError")
				elif isinstance(e, KeyError): result = common.Result("PythonCore::KeyError")
				else: result = common.Result("PythonCore::Exception")
		else:
			logger.warning("Received RMC request with unsupported protocol id: 0x%X", protocol_id)
			result = common.Result("Core::NotImplemented")
		
		if result and result.is_error():
			response = self.init_response(protocol_id, call_id, method_id, result)
			
		self.send_message(response)
			
	def handle_response(self, protocol_id, stream):
		success = stream.u8()
		if not success:
			result = stream.result()
			call_id = stream.u32()

			logger.warning("RMC failed with error code %08X", result.code())
			self.responses[call_id] = (result, None)

		else:
			call_id = stream.u32()
			method_id = stream.u32() & 0x7FFF
			logger.debug("Received RMC response: protocol=%i, call=%i, method=%i", protocol_id, call_id, method_id)

			self.responses[call_id] = (None, stream)
			
	def get_response(self, call_id, timeout=5):
		start = time.monotonic()
		while call_id not in self.responses:
			if not self.client.is_connected():
				raise ConnectionError("RMC failed because the PRUDP connection was closed")

			scheduler.update()
			
			now = time.monotonic()
			if now - start >= timeout:
				raise RuntimeError("RMC request timed out")
			
		result, stream = self.responses.pop(call_id)
		if result:
			result.raise_if_error()
		return stream
