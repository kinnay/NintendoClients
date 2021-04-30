
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class ApiCall(common.Structure):
	def __init__(self):
		super().__init__()
		self.name = None
		self.time = None
		self.pid = None
	
	def check_required(self, settings, version):
		for field in ['name', 'time', 'pid']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.name = stream.string()
		self.time = stream.datetime()
		self.pid = stream.pid()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.string(self.name)
		stream.datetime(self.time)
		stream.pid(self.pid)


class DebugProtocol:
	METHOD_ENABLE_API_RECORDER = 1
	METHOD_DISABLE_API_RECORDER = 2
	METHOD_IS_API_RECORDER_ENABLED = 3
	METHOD_GET_API_CALLS = 4
	METHOD_SET_EXCLUDE_JOINED_MATCHMAKE_SESSION = 5
	METHOD_GET_EXCLUDE_JOINED_MATCHMAKE_SESSION = 6
	METHOD_GET_API_CALL_SUMMARY = 7
	
	PROTOCOL_ID = 0x74


class DebugClient(DebugProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def enable_api_recorder(self):
		logger.info("DebugClient.enable_api_recorder()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_ENABLE_API_RECORDER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DebugClient.enable_api_recorder -> done")
	
	async def disable_api_recorder(self):
		logger.info("DebugClient.disable_api_recorder()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DISABLE_API_RECORDER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DebugClient.disable_api_recorder -> done")
	
	async def is_api_recorder_enabled(self):
		logger.info("DebugClient.is_api_recorder_enabled()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_IS_API_RECORDER_ENABLED, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		enabled = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DebugClient.is_api_recorder_enabled -> done")
		return enabled
	
	async def get_api_calls(self, pids, unk1, unk2):
		logger.info("DebugClient.get_api_calls()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		stream.datetime(unk1)
		stream.datetime(unk2)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_API_CALLS, stream.get())
		
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
			self.METHOD_SET_EXCLUDE_JOINED_MATCHMAKE_SESSION: self.handle_set_exclude_joined_matchmake_session,
			self.METHOD_GET_EXCLUDE_JOINED_MATCHMAKE_SESSION: self.handle_get_exclude_joined_matchmake_session,
			self.METHOD_GET_API_CALL_SUMMARY: self.handle_get_api_call_summary,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on DebugServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_enable_api_recorder(self, client, input, output):
		logger.info("DebugServer.enable_api_recorder()")
		#--- request ---
		await self.enable_api_recorder(client)
	
	async def handle_disable_api_recorder(self, client, input, output):
		logger.info("DebugServer.disable_api_recorder()")
		#--- request ---
		await self.disable_api_recorder(client)
	
	async def handle_is_api_recorder_enabled(self, client, input, output):
		logger.info("DebugServer.is_api_recorder_enabled()")
		#--- request ---
		response = await self.is_api_recorder_enabled(client)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_get_api_calls(self, client, input, output):
		logger.info("DebugServer.get_api_calls()")
		#--- request ---
		pids = input.list(input.pid)
		unk1 = input.datetime()
		unk2 = input.datetime()
		response = await self.get_api_calls(client, pids, unk1, unk2)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_set_exclude_joined_matchmake_session(self, client, input, output):
		logger.warning("DebugServer.set_exclude_joined_matchmake_session is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_get_exclude_joined_matchmake_session(self, client, input, output):
		logger.warning("DebugServer.get_exclude_joined_matchmake_session is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_get_api_call_summary(self, client, input, output):
		logger.warning("DebugServer.get_api_call_summary is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def enable_api_recorder(self, *args):
		logger.warning("DebugServer.enable_api_recorder not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def disable_api_recorder(self, *args):
		logger.warning("DebugServer.disable_api_recorder not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def is_api_recorder_enabled(self, *args):
		logger.warning("DebugServer.is_api_recorder_enabled not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_api_calls(self, *args):
		logger.warning("DebugServer.get_api_calls not implemented")
		raise common.RMCError("Core::NotImplemented")

