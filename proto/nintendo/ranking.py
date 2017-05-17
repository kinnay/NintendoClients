
from proto.common.stream import StreamOut, Encoder

import logging
logger = logging.getLogger(__name__)


class RankingOrderParam(Encoder):

	STANDARD = 0
	ORDINAL = 1

	def __init__(self, order_calc, filter_idx, filter_num, time_scope, base_rank, count):
		self.order_calc = order_calc
		self.filter_idx = filter_idx
		self.filter_num = filter_num
		self.time_scope = time_scope
		self.base_rank = base_rank
		self.count = count
		
	def encode(self, stream):
		stream.u8(self.order_calc)
		stream.u8(self.filter_idx)
		stream.u8(self.filter_num)
		stream.u8(self.time_scope)
		stream.u32(self.base_rank)
		stream.u8(self.count)
		
		
class RankingRankData(Encoder):
	def decode(self, stream):
		self.user_id = stream.u32()
		self.unk1 = stream.u64()
		self.rank = stream.u32()
		self.group_id = stream.u32()
		self.score = stream.u32()
		self.data = stream.read(stream.u32())
		self.file_id = stream.u64()
		self.name = stream.string(stream.u32)
		
		
class RankingResult(Encoder):
	def decode(self, stream):
		self.datas = stream.list(lambda: RankingRankData.from_stream(stream), stream.u32)
		self.total = stream.u32()
		self.datetime = stream.u64()


class RankingScoreData(Encoder):
	def __init__(self, group_id, score, unk3, unk4, data, file_id):
		self.group_id = group_id
		self.score = score
		self.unk3 = unk3
		self.unk4 = unk4
		self.data = data
		self.file_id = file_id

	def encode(self, stream):
		stream.u32(self.group_id)
		stream.u32(self.score)
		stream.u8(self.unk3)
		stream.u8(self.unk4)
		stream.data(self.data, stream.u32)
		stream.u64(self.file_id)
		

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
	METHOD_GET_CACHED_TOP_RANKING = 14
	METHOD_GET_CACHED_TOP_RANKINGS = 15

	PROTOCOL_ID = 0x70
	
	MODE_GLOBAL = 0
	MODE_GLOBAL_ME = 1 #Global rankings around me
	MODE_ME = 4 #Me ranking only

	def __init__(self, back_end):
		self.back_end = back_end
		self.client = self.back_end.secure_client
		
	#Untested, rankings should never be cheated
	def upload_score(self, score_data, arg): #Donkey Kong passes 0 as arg
		#--- request ---
		stream = StreamOut()
		call_id = self.client.init_message(stream, self.PROTOCOL_ID, self.METHOD_UPLOAD_SCORE)
		score_data.encode(stream)
		stream.u64(arg)
		self.client.send_message(stream)
		
		#--- response ---
		self.client.get_response(call_id)
		
	#Untested, I don't want to ruin my scores
	def delete_all_scores(self, arg):
		logger.info("Deleting all scores [%016X]", arg)
		#--- request ---
		stream = StreamOut()
		call_id = self.client.init_message(stream, self.PROTOCOL_ID, self.METHOD_DELETE_ALL_SCORES)
		stream.u64(arg)
		self.client.send_message(stream)
		
		#--- response ---
		self.client.get_response(call_id)
		
	def get_common_data(self, arg):
		logger.info("Ranking.get_common_data(%016X)", arg)
		#--- request ---
		stream = StreamOut()
		call_id = self.client.init_message(stream, self.PROTOCOL_ID, self.METHOD_GET_COMMON_DATA)
		stream.u64(arg)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		return stream.read(stream.u32())
		
	def get_ranking(self, mode, group_id, order, arg1, arg2):
		logger.info("Retrieving rankings [%i, %08X, %i - %i]", mode, group_id, order.base_rank + 1, order.base_rank + order.count)
		#--- request ---
		stream = StreamOut()
		call_id = self.client.init_message(stream, self.PROTOCOL_ID, self.METHOD_GET_RANKING)
		stream.u8(mode)
		stream.u32(group_id)
		order.encode(stream)
		stream.u64(arg1)
		stream.u32(arg2)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		return RankingResult.from_stream(stream)
		
	def get_stats(self, arg1, order, arg3):
		#--- request ---
		stream = StreamOut()
		call_id = self.client.init_message(stream, self.PROTOCOL_ID, self.METHOD_GET_STATS)
		stream.u32(arg1)
		order.encode(stream)
		stream.u32(arg3)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		return stream.list(stream.double, stream.u32)
