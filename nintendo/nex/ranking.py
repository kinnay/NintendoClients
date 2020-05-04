
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


class RankingMode:
	GLOBAL = 0
	GLOBAL_AROUND_SELF = 1
	SELF = 4


class RankingOrderCalc:
	STANDARD = 0
	ORDINAL = 1


class RankingStatFlags:
	RANKING_COUNT = 1
	TOTAL_SCORE = 2
	LOWEST_SCORE = 4
	HIGHEST_SCORE = 8
	AVERAGE_SCORE = 16
	ALL = 31


class RankingOrderParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.order_calc = 0
		self.group_index = 255
		self.group_num = 0
		self.time_scope = 2
		self.offset = None
		self.count = None
	
	def check_required(self, settings):
		for field in ['offset', 'count']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.order_calc = stream.u8()
		self.group_index = stream.u8()
		self.group_num = stream.u8()
		self.time_scope = stream.u8()
		self.offset = stream.u32()
		self.count = stream.u8()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u8(self.order_calc)
		stream.u8(self.group_index)
		stream.u8(self.group_num)
		stream.u8(self.time_scope)
		stream.u32(self.offset)
		stream.u8(self.count)


class RankingRankData(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.unique_id = None
		self.rank = None
		self.category = None
		self.score = None
		self.groups = None
		self.param = None
		self.common_data = None
		self.update_time = None
	
	def check_required(self, settings):
		for field in ['pid', 'unique_id', 'rank', 'category', 'score', 'groups', 'param', 'common_data']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings.get("nex.version") >= 40000:
			for field in ['update_time']:
				if getattr(self, field) is None:
					raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.pid = stream.pid()
		self.unique_id = stream.u64()
		self.rank = stream.u32()
		self.category = stream.u32()
		self.score = stream.u32()
		self.groups = stream.list(stream.u8)
		self.param = stream.u64()
		self.common_data = stream.buffer()
		if stream.settings.get("nex.version") >= 40000:
			self.update_time = stream.datetime()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.pid)
		stream.u64(self.unique_id)
		stream.u32(self.rank)
		stream.u32(self.category)
		stream.u32(self.score)
		stream.list(self.groups, stream.u8)
		stream.u64(self.param)
		stream.buffer(self.common_data)
		if stream.settings.get("nex.version") >= 40000:
			stream.datetime(self.update_time)


class RankingResult(common.Structure):
	def __init__(self):
		super().__init__()
		self.data = None
		self.total = None
		self.since_time = None
	
	def check_required(self, settings):
		for field in ['data', 'total', 'since_time']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data = stream.list(RankingRankData)
		self.total = stream.u32()
		self.since_time = stream.datetime()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.list(self.data, stream.add)
		stream.u32(self.total)
		stream.datetime(self.since_time)


class RankingScoreData(common.Structure):
	def __init__(self):
		super().__init__()
		self.category = None
		self.score = None
		self.order = None
		self.update_mode = None
		self.groups = None
		self.param = None
	
	def check_required(self, settings):
		for field in ['category', 'score', 'order', 'update_mode', 'groups', 'param']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.category = stream.u32()
		self.score = stream.u32()
		self.order = stream.u8()
		self.update_mode = stream.u8()
		self.groups = stream.list(stream.u8)
		self.param = stream.u64()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.category)
		stream.u32(self.score)
		stream.u8(self.order)
		stream.u8(self.update_mode)
		stream.list(self.groups, stream.u8)
		stream.u64(self.param)


class RankingStats(common.Structure):
	def __init__(self):
		super().__init__()
		self.stats = None
	
	def check_required(self, settings):
		for field in ['stats']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.stats = stream.list(stream.double)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.list(self.stats, stream.double)


class RankingProtocol:
	METHOD_UPLOAD_SCORE = 1
	METHOD_DELETE_SCORE = 2
	METHOD_DELETE_ALL_SCORES = 3
	METHOD_UPLOAD_COMMON_DATA = 4
	METHOD_DELETE_COMMON_DATA = 5
	METHOD_GET_COMMON_DATA = 6
	METHOD_CHANGE_ATTRIBUTES = 7
	METHOD_CHANGE_ALL_ATTRIBUTES = 8
	METHOD_GET_RANKING = 9
	METHOD_GET_APPROX_ORDER = 10
	METHOD_GET_STATS = 11
	METHOD_GET_RANKING_BY_PID_LIST = 12
	METHOD_GET_RANKING_BY_UNIQUE_ID_LIST = 13
	METHOD_GET_CACHED_TOPX_RANKING = 14
	METHOD_GET_CACHED_TOPX_RANKINGS = 15
	
	PROTOCOL_ID = 0x70


class RankingClient(RankingProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def upload_score(self, score_data, unique_id):
		logger.info("RankingClient.upload_score()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(score_data)
		stream.u64(unique_id)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_UPLOAD_SCORE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClient.upload_score -> done")
	
	def get_common_data(self, unique_id):
		logger.info("RankingClient.get_common_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(unique_id)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_COMMON_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		data = stream.buffer()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClient.get_common_data -> done")
		return data
	
	def get_ranking(self, mode, category, order, unique_id, pid):
		logger.info("RankingClient.get_ranking()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u8(mode)
		stream.u32(category)
		stream.add(order)
		stream.u64(unique_id)
		stream.pid(pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_RANKING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.extract(RankingResult)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClient.get_ranking -> done")
		return result
	
	def get_stats(self, category, order, flags):
		logger.info("RankingClient.get_stats()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(category)
		stream.add(order)
		stream.u32(flags)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_STATS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		stats = stream.extract(RankingStats)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClient.get_stats -> done")
		return stats
	
	def get_ranking_by_pid_list(self, pids, mode, category, order, unique_id):
		logger.info("RankingClient.get_ranking_by_pid_list()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		stream.u8(mode)
		stream.u32(category)
		stream.add(order)
		stream.u64(unique_id)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_RANKING_BY_PID_LIST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.extract(RankingResult)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClient.get_ranking_by_pid_list -> done")
		return result


class RankingServer(RankingProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_UPLOAD_SCORE: self.handle_upload_score,
			self.METHOD_DELETE_SCORE: self.handle_delete_score,
			self.METHOD_DELETE_ALL_SCORES: self.handle_delete_all_scores,
			self.METHOD_UPLOAD_COMMON_DATA: self.handle_upload_common_data,
			self.METHOD_DELETE_COMMON_DATA: self.handle_delete_common_data,
			self.METHOD_GET_COMMON_DATA: self.handle_get_common_data,
			self.METHOD_CHANGE_ATTRIBUTES: self.handle_change_attributes,
			self.METHOD_CHANGE_ALL_ATTRIBUTES: self.handle_change_all_attributes,
			self.METHOD_GET_RANKING: self.handle_get_ranking,
			self.METHOD_GET_APPROX_ORDER: self.handle_get_approx_order,
			self.METHOD_GET_STATS: self.handle_get_stats,
			self.METHOD_GET_RANKING_BY_PID_LIST: self.handle_get_ranking_by_pid_list,
			self.METHOD_GET_RANKING_BY_UNIQUE_ID_LIST: self.handle_get_ranking_by_unique_id_list,
			self.METHOD_GET_CACHED_TOPX_RANKING: self.handle_get_cached_topx_ranking,
			self.METHOD_GET_CACHED_TOPX_RANKINGS: self.handle_get_cached_topx_rankings,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_upload_score(self, context, input, output):
		logger.info("RankingServer.upload_score()")
		#--- request ---
		score_data = input.extract(RankingScoreData)
		unique_id = input.u64()
		self.upload_score(context, score_data, unique_id)
	
	def handle_delete_score(self, context, input, output):
		logger.warning("RankingServer.delete_score is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_delete_all_scores(self, context, input, output):
		logger.warning("RankingServer.delete_all_scores is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_upload_common_data(self, context, input, output):
		logger.warning("RankingServer.upload_common_data is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_delete_common_data(self, context, input, output):
		logger.warning("RankingServer.delete_common_data is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_common_data(self, context, input, output):
		logger.info("RankingServer.get_common_data()")
		#--- request ---
		unique_id = input.u64()
		response = self.get_common_data(context, unique_id)
		
		#--- response ---
		if not isinstance(response, bytes):
			raise RuntimeError("Expected bytes, got %s" %response.__class__.__name__)
		output.buffer(response)
	
	def handle_change_attributes(self, context, input, output):
		logger.warning("RankingServer.change_attributes is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_change_all_attributes(self, context, input, output):
		logger.warning("RankingServer.change_all_attributes is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_ranking(self, context, input, output):
		logger.info("RankingServer.get_ranking()")
		#--- request ---
		mode = input.u8()
		category = input.u32()
		order = input.extract(RankingOrderParam)
		unique_id = input.u64()
		pid = input.pid()
		response = self.get_ranking(context, mode, category, order, unique_id, pid)
		
		#--- response ---
		if not isinstance(response, RankingResult):
			raise RuntimeError("Expected RankingResult, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_approx_order(self, context, input, output):
		logger.warning("RankingServer.get_approx_order is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_stats(self, context, input, output):
		logger.info("RankingServer.get_stats()")
		#--- request ---
		category = input.u32()
		order = input.extract(RankingOrderParam)
		flags = input.u32()
		response = self.get_stats(context, category, order, flags)
		
		#--- response ---
		if not isinstance(response, RankingStats):
			raise RuntimeError("Expected RankingStats, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_ranking_by_pid_list(self, context, input, output):
		logger.info("RankingServer.get_ranking_by_pid_list()")
		#--- request ---
		pids = input.list(input.pid)
		mode = input.u8()
		category = input.u32()
		order = input.extract(RankingOrderParam)
		unique_id = input.u64()
		response = self.get_ranking_by_pid_list(context, pids, mode, category, order, unique_id)
		
		#--- response ---
		if not isinstance(response, RankingResult):
			raise RuntimeError("Expected RankingResult, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_ranking_by_unique_id_list(self, context, input, output):
		logger.warning("RankingServer.get_ranking_by_unique_id_list is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_cached_topx_ranking(self, context, input, output):
		logger.warning("RankingServer.get_cached_topx_ranking is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_cached_topx_rankings(self, context, input, output):
		logger.warning("RankingServer.get_cached_topx_rankings is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def upload_score(self, *args):
		logger.warning("RankingServer.upload_score not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_common_data(self, *args):
		logger.warning("RankingServer.get_common_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_ranking(self, *args):
		logger.warning("RankingServer.get_ranking not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_stats(self, *args):
		logger.warning("RankingServer.get_stats not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_ranking_by_pid_list(self, *args):
		logger.warning("RankingServer.get_ranking_by_pid_list not implemented")
		raise common.RMCError("Core::NotImplemented")

