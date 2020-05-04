
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


class ApiCall(common.Structure):
	def __init__(self):
		super().__init__()
		self.name = None
		self.date = None
		self.pid = None
	
	def check_required(self, settings):
		for field in ['name', 'date', 'pid']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.name = stream.string()
		self.date = stream.datetime()
		self.pid = stream.pid()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.name)
		stream.datetime(self.date)
		stream.pid(self.pid)


class DebugProtocol:
	METHOD_ENABLE_API_RECORDER = 1
	METHOD_DISABLE_API_RECORDER = 2
	METHOD_IS_API_RECORDER_ENABLED = 3
	METHOD_GET_API_CALLS = 4
	
	PROTOCOL_ID = 0x74


class DebugClient(DebugProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def enable_api_recorder(self):
		logger.info("DebugClient.enable_api_recorder()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_ENABLE_API_RECORDER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DebugClient.enable_api_recorder -> done")
	
	def disable_api_recorder(self):
		logger.info("DebugClient.disable_api_recorder()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_DISABLE_API_RECORDER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DebugClient.disable_api_recorder -> done")
	
	def is_api_recorder_enabled(self):
		logger.info("DebugClient.is_api_recorder_enabled()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_IS_API_RECORDER_ENABLED, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DebugClient.is_api_recorder_enabled -> done")
		return result
	
	def get_api_calls(self, pids, unk2, unk3):
		logger.info("DebugClient.get_api_calls()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		stream.u64(unk2)
		stream.u64(unk3)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_API_CALLS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		calls = stream.list(ApiCall)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DebugClient.get_api_calls -> done")
		return calls


class DebugServer(DebugProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_ENABLE_API_RECORDER: self.handle_enable_api_recorder,
			self.METHOD_DISABLE_API_RECORDER: self.handle_disable_api_recorder,
			self.METHOD_IS_API_RECORDER_ENABLED: self.handle_is_api_recorder_enabled,
			self.METHOD_GET_API_CALLS: self.handle_get_api_calls,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_enable_api_recorder(self, context, input, output):
		logger.info("DebugServer.enable_api_recorder()")
		#--- request ---
		self.enable_api_recorder(context)
	
	def handle_disable_api_recorder(self, context, input, output):
		logger.info("DebugServer.disable_api_recorder()")
		#--- request ---
		self.disable_api_recorder(context)
	
	def handle_is_api_recorder_enabled(self, context, input, output):
		logger.info("DebugServer.is_api_recorder_enabled()")
		#--- request ---
		response = self.is_api_recorder_enabled(context)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	def handle_get_api_calls(self, context, input, output):
		logger.info("DebugServer.get_api_calls()")
		#--- request ---
		pids = input.list(input.pid)
		unk2 = input.u64()
		unk3 = input.u64()
		response = self.get_api_calls(context, pids, unk2, unk3)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	def enable_api_recorder(self, *args):
		logger.warning("DebugServer.enable_api_recorder not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def disable_api_recorder(self, *args):
		logger.warning("DebugServer.disable_api_recorder not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def is_api_recorder_enabled(self, *args):
		logger.warning("DebugServer.is_api_recorder_enabled not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_api_calls(self, *args):
		logger.warning("DebugServer.get_api_calls not implemented")
		raise common.RMCError("Core::NotImplemented")

