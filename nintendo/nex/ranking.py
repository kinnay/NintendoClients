
# This file was generated automatically from ranking.proto

from nintendo.nex import common

import logging
logger = logging.getLogger(__name__)


class RankingMode:
	GLOBAL = 0
	GLOBAL_ME = 1
	ME = 4


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

	def check_required(self, settings):
		for field in ['pid', 'unique_id', 'rank', 'category', 'score', 'groups', 'param', 'common_data']:
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


class RankingResult(common.Structure):
	def __init__(self):
		super().__init__()
		self.datas = None
		self.total = None
		self.since_time = None

	def check_required(self, settings):
		for field in ['datas', 'total', 'since_time']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)

	def load(self, stream):
		self.datas = stream.list(RankingRankData)
		self.total = stream.u32()
		self.since_time = stream.datetime()

	def save(self, stream):
		self.check_required(stream.settings)
		stream.list(self.datas, stream.add)
		stream.u32(self.total)
		stream.datetime(self.since_time)


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
		self.client = client

	def get_common_data(self, unique_id):
		logger.info("RankingClient.get_common_data()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_COMMON_DATA)
		stream.u64(unique_id)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		data = stream.buffer()
		logger.info("RankingClient.get_common_data -> done")
		return data

	def get_ranking(self, mode, category, order, unique_id, pid):
		logger.info("RankingClient.get_ranking()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_RANKING)
		stream.u8(mode)
		stream.u32(category)
		stream.add(order)
		stream.u64(unique_id)
		stream.pid(pid)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		result = stream.extract(RankingResult)
		logger.info("RankingClient.get_ranking -> done")
		return result

	def get_stats(self, category, order, flags):
		logger.info("RankingClient.get_stats()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_STATS)
		stream.u32(category)
		stream.add(order)
		stream.u32(flags)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		stats = stream.extract(RankingStats)
		logger.info("RankingClient.get_stats -> done")
		return stats

	def get_ranking_by_pid_list(self, pids, mode, category, order, unique_id):
		logger.info("RankingClient.get_ranking_by_pid_list()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_RANKING_BY_PID_LIST)
		stream.list(pids, stream.pid)
		stream.u8(mode)
		stream.u32(category)
		stream.add(order)
		stream.u64(unique_id)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		result = stream.extract(RankingResult)
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

	def handle(self, caller_id, method_id, input, output):
		if method_id in self.methods:
			return self.methods[method_id](caller_id, input, output)
		logger.warning("Unknown method called on RankingServer: %i", method_id)
		return common.Result("Core::NotImplemented")

	def handle_upload_score(self, caller_id, input, output):
		logger.warning("RankingSever.upload_score is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_delete_score(self, caller_id, input, output):
		logger.warning("RankingSever.delete_score is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_delete_all_scores(self, caller_id, input, output):
		logger.warning("RankingSever.delete_all_scores is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_upload_common_data(self, caller_id, input, output):
		logger.warning("RankingSever.upload_common_data is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_delete_common_data(self, caller_id, input, output):
		logger.warning("RankingSever.delete_common_data is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_get_common_data(self, caller_id, input, output):
		logger.info("RankingServer.get_common_data()")
		#--- request ---
		unique_id = input.u64()
		response = self.get_common_data(unique_id)

		#--- response ---
		if not isinstance(response, bytes):
			raise RuntimeError("Expected bytes, got %s" %response.__class__.__name__)
		output.buffer(response)

	def handle_change_attributes(self, caller_id, input, output):
		logger.warning("RankingSever.change_attributes is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_change_all_attributes(self, caller_id, input, output):
		logger.warning("RankingSever.change_all_attributes is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_get_ranking(self, caller_id, input, output):
		logger.info("RankingServer.get_ranking()")
		#--- request ---
		mode = input.u8()
		category = input.u32()
		order = input.extract(RankingOrderParam)
		unique_id = input.u64()
		pid = input.pid()
		response = self.get_ranking(mode, category, order, unique_id, pid)

		#--- response ---
		if not isinstance(response, RankingResult):
			raise RuntimeError("Expected RankingResult, got %s" %response.__class__.__name__)
		output.add(response)

	def handle_get_approx_order(self, caller_id, input, output):
		logger.warning("RankingSever.get_approx_order is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_get_stats(self, caller_id, input, output):
		logger.info("RankingServer.get_stats()")
		#--- request ---
		category = input.u32()
		order = input.extract(RankingOrderParam)
		flags = input.u32()
		response = self.get_stats(category, order, flags)

		#--- response ---
		if not isinstance(response, RankingStats):
			raise RuntimeError("Expected RankingStats, got %s" %response.__class__.__name__)
		output.add(response)

	def handle_get_ranking_by_pid_list(self, caller_id, input, output):
		logger.info("RankingServer.get_ranking_by_pid_list()")
		#--- request ---
		pids = input.list(input.pid)
		mode = input.u8()
		category = input.u32()
		order = input.extract(RankingOrderParam)
		unique_id = input.u64()
		response = self.get_ranking_by_pid_list(pids, mode, category, order, unique_id)

		#--- response ---
		if not isinstance(response, RankingResult):
			raise RuntimeError("Expected RankingResult, got %s" %response.__class__.__name__)
		output.add(response)

	def handle_get_ranking_by_unique_id_list(self, caller_id, input, output):
		logger.warning("RankingSever.get_ranking_by_unique_id_list is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_get_cached_topx_ranking(self, caller_id, input, output):
		logger.warning("RankingSever.get_cached_topx_ranking is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_get_cached_topx_rankings(self, caller_id, input, output):
		logger.warning("RankingSever.get_cached_topx_rankings is unsupported")
		return common.Result("Core::NotImplemented")

	def get_common_data(self, *args):
		logger.warning("RankingServer.get_common_data not implemented")
		return common.Result("Core::NotImplemented")

	def get_ranking(self, *args):
		logger.warning("RankingServer.get_ranking not implemented")
		return common.Result("Core::NotImplemented")

	def get_stats(self, *args):
		logger.warning("RankingServer.get_stats not implemented")
		return common.Result("Core::NotImplemented")

	def get_ranking_by_pid_list(self, *args):
		logger.warning("RankingServer.get_ranking_by_pid_list not implemented")
		return common.Result("Core::NotImplemented")
