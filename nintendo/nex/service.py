
from nintendo.common import scheduler
from nintendo.nex import prudp, errors, streams
import struct
import time

import logging
logger = logging.getLogger(__name__)


class ServiceClient:
	def __init__(self, backend):
		self.client = prudp.PRUDPClient(backend.settings)
		self.backend = backend

		self.call_id = 0
		self.responses = {}
		
	def connect(self, host, port, payload=b""):
		if not self.client.connect(host, port, payload):
			raise ConnectionError("Connection failed")
			
		self.socket_event = scheduler.add_socket(self.handle_recv, self.client)
		
	def close(self):
		scheduler.remove(self.socket_event)
		self.client.close()
		
	def handle_recv(self, data):
		if not data:
			logger.debug("Connection was closed")
			scheduler.remove(self.socket_event)
			return

		stream = streams.StreamIn(data, self.backend.settings)
		length = stream.u32()
		protocol_id = stream.u8()

		if protocol_id & 0x80:
			self.handle_request(protocol_id & 0x7F, stream)
		else:
			self.handle_response(protocol_id, stream)

	def init_request(self, protocol_id, method_id):
		self.call_id += 1
		stream = streams.StreamOut(self.backend.settings)
		stream.u8(protocol_id | 0x80)
		stream.u32(self.call_id)
		stream.u32(method_id)
		return stream, self.call_id
		
	def init_response(self, protocol_id, call_id, method_id, error=None):
		stream = streams.StreamOut(self.backend.settings)
		stream.u8(protocol_id)
		if error:
			stream.u8(0)
			stream.u32(error)
			stream.u32(call_id)
		else:
			stream.u8(1)
			stream.u32(call_id)
			stream.u32(method_id | 0x8000)
		return stream
		
	def send_message(self, stream):
		if self.client.is_connected():
			self.client.send(struct.pack("I", len(stream.data)) + stream.data)
		else:
			raise RuntimeError("Can't send message on disconnected service client")
			
	def handle_request(self, protocol_id, stream):
		call_id = stream.u32()
		method_id = stream.u32()
		logger.debug("Received RMC request: protocol=%i, call=%i, method=%i", protocol_id, call_id, method_id)
		
		if protocol_id in self.backend.protocol_map:
			self.backend.protocol_map[protocol_id].handle_request(self, call_id, method_id, stream)
		else:
			logger.warning("Received RMC request with unsupported protocol id: 0x%X", protocol_id)
			
	def handle_response(self, protocol_id, stream):
		success = stream.u8()
		if not success:
			error_code = stream.u32()
			call_id = stream.u32()

			logger.warning("RMC failed with error code %08X", error_code)
			self.responses[call_id] = (error_code, None)

		else:
			call_id = stream.u32()
			method_id = stream.u32() & 0x7FFF
			logger.debug("Received RMC response: protocol=%i, call=%i, method=%i", protocol_id, call_id, method_id)

			self.responses[call_id] = (-1, stream)
			
	def get_response(self, call_id):
		while call_id not in self.responses:
			if not self.client.is_connected():
				raise ConnectionError("RMC failed because the PRUDP connection was closed")
			time.sleep(0.05)
			
		error, stream = self.responses.pop(call_id)
		if error != -1:
			raise RuntimeError(error, "RMC failed (%s)" %errors.error_names.get(error, "unknown error"))
		return stream
