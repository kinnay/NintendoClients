
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class ReportCategory:
	INVALID = 0
	MIN = 1
	PERSONAL = 1
	CRIMINAL = 2
	IMMORAL = 3
	HARASSMENT = 4
	COMMERCIAL = 5
	SEXUALLY_EXPLICIT = 6
	OTHER = 7
	MAX = 7


class ScreeningDataStoreContentParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.content_data_id = None
		self.ugc_type = None
		self.language = None
		self.search_key = None
	
	def __key(self):
		return (self.data_id, self.content_data_id, self.ugc_type, self.language, self.search_key, )
	
	def __hash__(self):
		return hash(common.make_hashable(self.__key()))
	
	def __eq__(self, other):
		if type(self) is not type(other):
			return NotImplemented
		return self.__key() == other.__key()
	def check_required(self, settings, version):
		for field in ['data_id', 'content_data_id', 'ugc_type', 'language', 'search_key']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.content_data_id = stream.u64()
		self.ugc_type = stream.string()
		self.language = stream.string()
		self.search_key = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.u64(self.content_data_id)
		stream.string(self.ugc_type)
		stream.string(self.language)
		stream.string(self.search_key)


class ScreeningUgcViolationParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.category = None
		self.reason = None
		self.context = None
		self.screenshot_data_id = None
	
	def __key(self):
		return (self.category, self.reason, self.context, self.screenshot_data_id, )
	
	def __hash__(self):
		return hash(common.make_hashable(self.__key()))
	
	def __eq__(self, other):
		if type(self) is not type(other):
			return NotImplemented
		return self.__key() == other.__key()
	def check_required(self, settings, version):
		for field in ['category', 'reason', 'context', 'screenshot_data_id']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.category = stream.u32()
		self.reason = stream.string()
		self.context = stream.list(ScreeningContextInfo)
		self.screenshot_data_id = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.category)
		stream.string(self.reason)
		stream.list(self.context, stream.add)
		stream.u64(self.screenshot_data_id)


class ScreeningContextInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.key = None
		self.value = None
	
	def __key(self):
		return (self.key, self.value, )
	
	def __hash__(self):
		return hash(common.make_hashable(self.__key()))
	
	def __eq__(self, other):
		if type(self) is not type(other):
			return NotImplemented
		return self.__key() == other.__key()
	def check_required(self, settings, version):
		for field in ['key', 'value']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.key = stream.string()
		self.value = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.string(self.key)
		stream.string(self.value)


class ScreeningProtocol:
	METHOD_REPORT_DATA_STORE_CONTENT = 1
	METHOD_REPORT_USER = 2
	
	PROTOCOL_ID = 0x7C


class ScreeningClient(ScreeningProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def report_data_store_content(self, content_param, violation_param):
		logger.info("ScreeningClient.report_data_store_content()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(content_param)
		stream.add(violation_param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REPORT_DATA_STORE_CONTENT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("ScreeningClient.report_data_store_content -> done")


class ScreeningServer(ScreeningProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_REPORT_DATA_STORE_CONTENT: self.handle_report_data_store_content,
			self.METHOD_REPORT_USER: self.handle_report_user,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on ScreeningServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_report_data_store_content(self, client, input, output):
		logger.info("ScreeningServer.report_data_store_content()")
		#--- request ---
		content_param = input.extract(ScreeningDataStoreContentParam)
		violation_param = input.extract(ScreeningUgcViolationParam)
		await self.report_data_store_content(client, content_param, violation_param)
	
	async def handle_report_user(self, client, input, output):
		logger.warning("ScreeningServer.report_user is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def report_data_store_content(self, *args):
		logger.warning("ScreeningServer.report_data_store_content not implemented")
		raise common.RMCError("Core::NotImplemented")

