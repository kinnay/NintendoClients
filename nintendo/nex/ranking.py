
from nintendo.nex import common

import logging
logger = logging.getLogger(__name__)


class RankingOrderParam(common.Structure):
	STANDARD = 0 #1224 ranking
	ORDINAL = 1  #1234 ranking

	def __init__(self, order_calc, group_index, group_num, time_scope, offset, count):
		self.order_calc = order_calc
		self.group_index = group_index
		self.group_num = group_num
		self.time_scope = time_scope
		self.offset = offset
		self.count = count
		
	def save(self, stream):
		stream.u8(self.order_calc)
		stream.u8(self.group_index)
		stream.u8(self.group_num)
		stream.u8(self.time_scope)
		stream.u32(self.offset)
		stream.u8(self.count)


class RankingRankData(common.Structure):
	def load(self, stream):
		self.pid = stream.uint()
		self.unique_id = stream.u64()
		self.rank = stream.u32()
		self.category = stream.u32()
		self.score = stream.u32()
		self.groups = stream.list(stream.u8)
		self.param = stream.u64()
		self.common_data = stream.buffer()


class RankingResult(common.Structure):
	def load(self, stream):	
		self.datas = stream.list(RankingRankData)
		self.total = stream.u32()
		self.since_time = stream.datetime()
	
	
class RankingStats(common.Structure):
	def load(self, stream):
		self.stats = stream.list(stream.double)


class RankingClient:

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
	
	MODE_GLOBAL = 0
	MODE_GLOBAL_ME = 1 #Global rankings around me
	MODE_ME = 4 #Me ranking only
	
	STAT_RANKING_COUNT = 1
	STAT_TOTAL_SCORE = 2
	STAT_LOWEST_SCORE = 4
	STAT_HIGHEST_SCORE = 8
	STAT_AVERAGE_SCORE = 0x10

	def __init__(self, backend):
		self.client = backend.secure_client

	def delete_all_scores(self, unique_id):
		logger.info("Ranking.delete_all_scores(%016X)", unique_id)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_DELETE_ALL_SCORES)
		stream.u64(unique_id)
		self.client.send_message(stream)
		
		#--- response ---
		self.client.get_response(call_id)
		logger.info("Ranking.delete_all_scores -> done")
		
	def upload_common_data(self, data, unique_id):
		logger.info("Ranking.upload_common_data(...)")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_UPLOAD_COMMON_DATA)
		stream.data(data)
		stream.u64(unique_id)
		self.client.send_message(stream)
		
		#--- response ---
		self.client.get_response(call_id)
		logger.info("Ranking.upload_common_data -> done")
		
	def get_common_data(self, unique_id):
		logger.info("Ranking.get_common_data(%i)", unique_id)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_COMMON_DATA)
		stream.u64(unique_id)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		data = stream.buffer()
		logger.info("Ranking.get_common_data -> %s", data)
		return data
		
	def get_ranking(self, mode, category, order, unique_id, pid):
		logger.info("Ranking.get_ranking(%i, %08X, %i - %i, %016X, %08X)", mode, category, order.offset + 1,
					order.offset + order.count, unique_id, pid)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_RANKING)
		stream.u8(mode)
		stream.u32(category)
		stream.add(order)
		stream.u64(unique_id)
		stream.uint(pid)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		result = stream.extract(RankingResult)
		logger.info("Ranking.get_ranking -> %i results (out of %i total)", len(result.datas), result.total)
		return result
		
	def get_stats(self, category, order, flags=0x1F):
		logger.info("Ranking.get_stats(%08X, %i - %i, %02X)", category, order.offset + 1, order.offset + order.count, flags)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_STATS)
		stream.u32(category)
		stream.add(order)
		stream.u32(flags)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		result = stream.extract(RankingStats)
		logger.info("Ranking.get_stats -> %s", result.stats)
		
		stats = {}
		for i in range(5):
			if flags & (1 << i):
				stats[1 << i] = result.stats[i]
		return stats
	
	def get_ranking_by_pid_list(self, pids, mode, category, order, unique_id):
		logger.info("Ranking.get_ranking_by_pid_list(%s, %i, %08X, <order param>, %016X)", pids, mode, category, unique_id)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_RANKING_BY_PID_LIST)
		stream.list(pids, stream.u32)
		stream.u8(mode)
		stream.u32(category)
		stream.add(order)
		stream.u64(unique_id)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		result = stream.extract(RankingResult)
		logger.info("Ranking.get_ranking_by_pid_list -> %i results (out of %i total)", len(result.datas), result.total)
		return result
