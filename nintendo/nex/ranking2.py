
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


class RankingMode:
	GLOBAL_AROUND_USER = 1
	GLOBAL = 2
	FRIENDS = 3


class Ranking2CategorySetting(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
		self.unk3 = None
		self.unk4 = None
		self.unk5 = None
		self.unk6 = None
		self.unk7 = None
		self.unk8 = None
		self.unk9 = None
	
	def check_required(self, settings):
		for field in ['unk1', 'unk2', 'unk3', 'unk4', 'unk5', 'unk6', 'unk7', 'unk8', 'unk9']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk1 = stream.u32()
		self.unk2 = stream.u32()
		self.unk3 = stream.u32()
		self.unk4 = stream.u16()
		self.unk5 = stream.u8()
		self.unk6 = stream.u8()
		self.unk7 = stream.u8()
		self.unk8 = stream.u8()
		self.unk9 = stream.bool()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.unk1)
		stream.u32(self.unk2)
		stream.u32(self.unk3)
		stream.u16(self.unk4)
		stream.u8(self.unk5)
		stream.u8(self.unk6)
		stream.u8(self.unk7)
		stream.u8(self.unk8)
		stream.bool(self.unk9)


class Ranking2CommonData(common.Structure):
	def __init__(self):
		super().__init__()
		self.username = None
		self.unk1 = None
		self.unk2 = None
	
	def check_required(self, settings):
		for field in ['username', 'unk1', 'unk2']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.username = stream.string()
		self.unk1 = stream.qbuffer()
		self.unk2 = stream.qbuffer()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.username)
		stream.qbuffer(self.unk1)
		stream.qbuffer(self.unk2)


class Ranking2GetParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = 0
		self.pid = 0
		self.category = None
		self.offset = 0
		self.count = 10
		self.unk2 = 0
		self.unk3 = 0
		self.mode = 2
		self.unk4 = 0
	
	def check_required(self, settings):
		for field in ['category']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk1 = stream.u64()
		self.pid = stream.pid()
		self.category = stream.u32()
		self.offset = stream.u32()
		self.count = stream.u32()
		self.unk2 = stream.u32()
		self.unk3 = stream.u32()
		self.mode = stream.u8()
		self.unk4 = stream.u8()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.unk1)
		stream.pid(self.pid)
		stream.u32(self.category)
		stream.u32(self.offset)
		stream.u32(self.count)
		stream.u32(self.unk2)
		stream.u32(self.unk3)
		stream.u8(self.mode)
		stream.u8(self.unk4)


class Ranking2Info(common.Structure):
	def __init__(self):
		super().__init__()
		self.data = None
		self.unk1 = None
		self.num_entries = None
		self.unk2 = None
	
	def check_required(self, settings):
		for field in ['data', 'unk1', 'num_entries', 'unk2']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data = stream.list(Ranking2RankData)
		self.unk1 = stream.u32()
		self.num_entries = stream.u32()
		self.unk2 = stream.s32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.list(self.data, stream.add)
		stream.u32(self.unk1)
		stream.u32(self.num_entries)
		stream.s32(self.unk2)


class Ranking2RankData(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
		self.pid = None
		self.rank = None
		self.score = None
		self.common_data = Ranking2CommonData()
	
	def check_required(self, settings):
		for field in ['unk1', 'unk2', 'pid', 'rank', 'score']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk1 = stream.u64()
		self.unk2 = stream.u64()
		self.pid = stream.pid()
		self.rank = stream.u32()
		self.score = stream.u32()
		self.common_data = stream.extract(Ranking2CommonData)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.unk1)
		stream.u64(self.unk2)
		stream.pid(self.pid)
		stream.u32(self.rank)
		stream.u32(self.score)
		stream.add(self.common_data)


class Ranking2Protocol:
	METHOD_PUT_SCORE = 1
	METHOD_GET_COMMON_DATA = 2
	METHOD_PUT_COMMON_DATA = 3
	METHOD_DELETE_COMMON_DATA = 4
	METHOD_GET_RANKING = 5
	METHOD_GET_RANKING_BY_PRINCIPAL_ID = 6
	METHOD_GET_CATEGORY_SETTING = 7
	
	PROTOCOL_ID = 0x7A


class Ranking2Client(Ranking2Protocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def get_ranking(self, param):
		logger.info("Ranking2Client.get_ranking()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_RANKING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(Ranking2Info)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.get_ranking -> done")
		return info
	
	def get_category_setting(self, category):
		logger.info("Ranking2Client.get_category_setting()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(category)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_CATEGORY_SETTING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		setting = stream.extract(Ranking2CategorySetting)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.get_category_setting -> done")
		return setting


class Ranking2Server(Ranking2Protocol):
	def __init__(self):
		self.methods = {
			self.METHOD_PUT_SCORE: self.handle_put_score,
			self.METHOD_GET_COMMON_DATA: self.handle_get_common_data,
			self.METHOD_PUT_COMMON_DATA: self.handle_put_common_data,
			self.METHOD_DELETE_COMMON_DATA: self.handle_delete_common_data,
			self.METHOD_GET_RANKING: self.handle_get_ranking,
			self.METHOD_GET_RANKING_BY_PRINCIPAL_ID: self.handle_get_ranking_by_principal_id,
			self.METHOD_GET_CATEGORY_SETTING: self.handle_get_category_setting,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_put_score(self, context, input, output):
		logger.warning("Ranking2Server.put_score is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_common_data(self, context, input, output):
		logger.warning("Ranking2Server.get_common_data is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_put_common_data(self, context, input, output):
		logger.warning("Ranking2Server.put_common_data is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_delete_common_data(self, context, input, output):
		logger.warning("Ranking2Server.delete_common_data is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_ranking(self, context, input, output):
		logger.info("Ranking2Server.get_ranking()")
		#--- request ---
		param = input.extract(Ranking2GetParam)
		response = self.get_ranking(context, param)
		
		#--- response ---
		if not isinstance(response, Ranking2Info):
			raise RuntimeError("Expected Ranking2Info, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_ranking_by_principal_id(self, context, input, output):
		logger.warning("Ranking2Server.get_ranking_by_principal_id is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_category_setting(self, context, input, output):
		logger.info("Ranking2Server.get_category_setting()")
		#--- request ---
		category = input.u32()
		response = self.get_category_setting(context, category)
		
		#--- response ---
		if not isinstance(response, Ranking2CategorySetting):
			raise RuntimeError("Expected Ranking2CategorySetting, got %s" %response.__class__.__name__)
		output.add(response)
	
	def get_ranking(self, *args):
		logger.warning("Ranking2Server.get_ranking not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_category_setting(self, *args):
		logger.warning("Ranking2Server.get_category_setting not implemented")
		raise common.RMCError("Core::NotImplemented")

