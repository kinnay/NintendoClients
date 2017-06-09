
from nintendo.nex.prudp import PRUDP
from nintendo.nex.errors import error_names
from nintendo.nex.stream import NexStreamOut, NexStreamIn
import struct
import time

import logging
logger = logging.getLogger(__name__)


class ServiceClient(PRUDP):
	def __init__(self, back_end, key):
		super().__init__(key)
		self.back_end = back_end

		self.call_id = 0		
		self.responses = {}
		
	def init_message(self, protocol_id, method_id):
		self.call_id += 1
		stream = NexStreamOut(self.back_end.version)
		stream.u8(protocol_id | 0x80)
		stream.u32(self.call_id)
		stream.u32(method_id)
		return stream, self.call_id
		
	def init_response(self, protocol_id, call_id, method_id, error=None):
		stream = NexStreamOut(self.back_end.version)
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
		self.send(struct.pack("I", len(stream.buffer)) + stream.buffer)
		
	def get_response(self, call_id):
		while call_id not in self.responses:
			time.sleep(0.05)
			
		error, stream = self.responses.pop(call_id)
		if error != -1:
			raise ConnectionError(error, "RMC failed (%s)" %error_names.get(error, "unknown error"))
		return stream
		
	def on_data(self, data):
		stream = NexStreamIn(data, self.back_end.version)
		length = stream.u32()
		protocol_id = stream.u8()

		if protocol_id & 0x80:
			self.handle_request(protocol_id & 0x7F, stream)
		else:
			self.handle_response(protocol_id, stream)
			
	def handle_request(self, protocol_id, stream):
		call_id = stream.u32()
		method_id = stream.u32()
		logger.debug("Received RMC request: protocol=%i, call=%i, method=%i", protocol_id, call_id, method_id)
		
		if protocol_id in self.back_end.protocol_map:
			response = self.back_end.protocol_map[protocol_id].handle_request(self, call_id, method_id, stream)
			if response:
				self.send_message(response)
		else:
			logger.warning("Received RMC request with unsupported protocol id: 0x%X", protocol_id)
			
	def handle_response(self, protocol_id, stream):
		success = stream.u8()
		if not success:
			error_code = stream.u32()
			call_id = stream.u32()

			logger.error("RMC failed with error code %08X", error_code)
			self.responses[call_id] = (error_code, None)

		else:
			call_id = stream.u32()
			method_id = stream.u32() & 0x7FFF
			logger.debug("Received RMC response: protocol=%i, call=%i, method=%i", protocol_id, call_id, method_id)

			self.responses[call_id] = (-1, stream)
