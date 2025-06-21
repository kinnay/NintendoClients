
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class RankingOrderCalc:
	STANDARD = 0
	ORDINAL = 1


class RankingMode:
	GLOBAL = 0
	GLOBAL_AROUND_SELF = 1
	SELF = 4


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
		self.offset = 0
		self.count = 10
	
	def check_required(self, settings, version):
		pass
	
	def load(self, stream, version):
		self.order_calc = stream.u8()
		self.group_index = stream.u8()
		self.group_num = stream.u8()
		self.time_scope = stream.u8()
		self.offset = stream.u32()
		self.count = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
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
	
	def check_required(self, settings, version):
		for field in ['pid', 'unique_id', 'rank', 'category', 'score', 'groups', 'param', 'common_data']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings["nex.version"] >= 40000:
			for field in ['update_time']:
				if getattr(self, field) is None:
					raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.pid = stream.pid()
		self.unique_id = stream.u64()
		self.rank = stream.u32()
		self.category = stream.u32()
		self.score = stream.u32()
		self.groups = stream.list(stream.u8)
		self.param = stream.u64()
		self.common_data = stream.buffer()
		if stream.settings["nex.version"] >= 40000:
			self.update_time = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.pid)
		stream.u64(self.unique_id)
		stream.u32(self.rank)
		stream.u32(self.category)
		stream.u32(self.score)
		stream.list(self.groups, stream.u8)
		stream.u64(self.param)
		stream.buffer(self.common_data)
		if stream.settings["nex.version"] >= 40000:
			stream.datetime(self.update_time)


class RankingResult(common.Structure):
	def __init__(self):
		super().__init__()
		self.data = None
		self.total = None
		self.since_time = None
	
	def check_required(self, settings, version):
		for field in ['data', 'total', 'since_time']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data = stream.list(RankingRankData)
		self.total = stream.u32()
		self.since_time = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.list(self.data, stream.add)
		stream.u32(self.total)
		stream.datetime(self.since_time)


class RankingCachedResult(RankingResult):
	def __init__(self):
		super().__init__()
		self.created_time = None
		self.expired_time = None
		self.max_length = None
	
	def check_required(self, settings, version):
		for field in ['created_time', 'expired_time', 'max_length']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.created_time = stream.datetime()
		self.expired_time = stream.datetime()
		self.max_length = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.datetime(self.created_time)
		stream.datetime(self.expired_time)
		stream.u8(self.max_length)
common.DataHolder.register(RankingCachedResult, "RankingCachedResult")


class RankingStats(common.Structure):
	def __init__(self):
		super().__init__()
		self.stats = None
	
	def check_required(self, settings, version):
		for field in ['stats']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.stats = stream.list(stream.double)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.list(self.stats, stream.double)


class RankingScoreData(common.Structure):
	def __init__(self):
		super().__init__()
		self.category = None
		self.score = None
		self.order = None
		self.update_mode = None
		self.groups = None
		self.param = None
	
	def check_required(self, settings, version):
		for field in ['category', 'score', 'order', 'update_mode', 'groups', 'param']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.category = stream.u32()
		self.score = stream.u32()
		self.order = stream.u8()
		self.update_mode = stream.u8()
		self.groups = stream.list(stream.u8)
		self.param = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.category)
		stream.u32(self.score)
		stream.u8(self.order)
		stream.u8(self.update_mode)
		stream.list(self.groups, stream.u8)
		stream.u64(self.param)


class RankingChangeAttributesParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.flags = None
		self.groups = None
		self.param = None
	
	def check_required(self, settings, version):
		for field in ['flags', 'groups', 'param']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.flags = stream.u8()
		self.groups = stream.list(stream.u8)
		self.param = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u8(self.flags)
		stream.list(self.groups, stream.u8)
		stream.u64(self.param)


class CompetitionRankingInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.id = None
		self.num_participants = None
		self.team_scores = None
	
	def check_required(self, settings, version):
		for field in ['id', 'num_participants', 'team_scores']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.id = stream.u32()
		self.num_participants = stream.u32()
		self.team_scores = stream.list(stream.u32)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.id)
		stream.u32(self.num_participants)
		stream.list(self.team_scores, stream.u32)


class CompetitionRankingInfoGetParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.rank_order = None
		self.range = common.ResultRange()
	
	def check_required(self, settings, version):
		for field in ['rank_order']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.rank_order = stream.u8()
		self.range = stream.extract(common.ResultRange)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u8(self.rank_order)
		stream.add(self.range)


class CompetitionRankingUploadScoreParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.id = None
		self.season_id = None
		self.unk3 = None
		self.score = None
		self.team_id = None
		self.team_score = None
		self.is_first_upload = None
		self.metadata = None
	
	def check_required(self, settings, version):
		for field in ['id', 'season_id', 'unk3', 'score', 'team_id', 'team_score', 'is_first_upload', 'metadata']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.id = stream.u32()
		self.season_id = stream.u32()
		self.unk3 = stream.u32()
		self.score = stream.u32()
		self.team_id = stream.u8()
		self.team_score = stream.u32()
		self.is_first_upload = stream.bool()
		self.metadata = stream.qbuffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.id)
		stream.u32(self.season_id)
		stream.u32(self.unk3)
		stream.u32(self.score)
		stream.u8(self.team_id)
		stream.u32(self.team_score)
		stream.bool(self.is_first_upload)
		stream.qbuffer(self.metadata)


class RankingProtocolMK8:
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
	METHOD_GET_COMPETITION_RANKING_SCORE = 14
	METHOD_UPLOAD_COMPETITION_RANKING_SCORE = 15
	METHOD_GET_COMPETITION_INFO = 16
	
	PROTOCOL_ID = 0x70


class RankingClientMK8(RankingProtocolMK8):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def upload_score(self, score_data, unique_id):
		logger.info("RankingClientMK8.upload_score()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(score_data)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPLOAD_SCORE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.upload_score -> done")
	
	async def delete_score(self, category, unique_id):
		logger.info("RankingClientMK8.delete_score()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(category)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_SCORE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.delete_score -> done")
	
	async def delete_all_scores(self, unique_id):
		logger.info("RankingClientMK8.delete_all_scores()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_ALL_SCORES, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.delete_all_scores -> done")
	
	async def upload_common_data(self, common_data, unique_id):
		logger.info("RankingClientMK8.upload_common_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.buffer(common_data)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPLOAD_COMMON_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.upload_common_data -> done")
	
	async def delete_common_data(self, unique_id):
		logger.info("RankingClientMK8.delete_common_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_COMMON_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.delete_common_data -> done")
	
	async def get_common_data(self, unique_id):
		logger.info("RankingClientMK8.get_common_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_COMMON_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		data = stream.buffer()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.get_common_data -> done")
		return data
	
	async def change_attributes(self, category, param, unique_id):
		logger.info("RankingClientMK8.change_attributes()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(category)
		stream.add(param)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CHANGE_ATTRIBUTES, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.change_attributes -> done")
	
	async def change_all_attributes(self, param, unique_id):
		logger.info("RankingClientMK8.change_all_attributes()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CHANGE_ALL_ATTRIBUTES, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.change_all_attributes -> done")
	
	async def get_ranking(self, mode, category, order, unique_id, pid):
		logger.info("RankingClientMK8.get_ranking()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u8(mode)
		stream.u32(category)
		stream.add(order)
		stream.u64(unique_id)
		stream.pid(pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_RANKING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.extract(RankingResult)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.get_ranking -> done")
		return result
	
	async def get_approx_order(self, category, order, score, unique_id, pid):
		logger.info("RankingClientMK8.get_approx_order()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(category)
		stream.add(order)
		stream.u32(score)
		stream.u64(unique_id)
		stream.pid(pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_APPROX_ORDER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		order = stream.u32()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.get_approx_order -> done")
		return order
	
	async def get_stats(self, category, order, flags):
		logger.info("RankingClientMK8.get_stats()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(category)
		stream.add(order)
		stream.u32(flags)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_STATS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		stats = stream.extract(RankingStats)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.get_stats -> done")
		return stats
	
	async def get_ranking_by_pid_list(self, pids, mode, category, order, unique_id):
		logger.info("RankingClientMK8.get_ranking_by_pid_list()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		stream.u8(mode)
		stream.u32(category)
		stream.add(order)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_RANKING_BY_PID_LIST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.extract(RankingResult)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.get_ranking_by_pid_list -> done")
		return result
	
	async def get_ranking_by_unique_id_list(self, ids, mode, category, order, unique_id):
		logger.info("RankingClientMK8.get_ranking_by_unique_id_list()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(ids, stream.u64)
		stream.u8(mode)
		stream.u32(category)
		stream.add(order)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_RANKING_BY_UNIQUE_ID_LIST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.extract(RankingResult)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.get_ranking_by_unique_id_list -> done")
		return result
	
	async def upload_competition_ranking_score(self, param):
		logger.info("RankingClientMK8.upload_competition_ranking_score()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPLOAD_COMPETITION_RANKING_SCORE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.upload_competition_ranking_score -> done")
		return result
	
	async def get_competition_info(self, param):
		logger.info("RankingClientMK8.get_competition_info()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_COMPETITION_INFO, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.list(CompetitionRankingInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RankingClientMK8.get_competition_info -> done")
		return info


class RankingServerMK8(RankingProtocolMK8):
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
			self.METHOD_GET_COMPETITION_RANKING_SCORE: self.handle_get_competition_ranking_score,
			self.METHOD_UPLOAD_COMPETITION_RANKING_SCORE: self.handle_upload_competition_ranking_score,
			self.METHOD_GET_COMPETITION_INFO: self.handle_get_competition_info,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on RankingServerMK8: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_upload_score(self, client, input, output):
		logger.info("RankingServerMK8.upload_score()")
		#--- request ---
		score_data = input.extract(RankingScoreData)
		unique_id = input.u64()
		await self.upload_score(client, score_data, unique_id)
	
	async def handle_delete_score(self, client, input, output):
		logger.info("RankingServerMK8.delete_score()")
		#--- request ---
		category = input.u32()
		unique_id = input.u64()
		await self.delete_score(client, category, unique_id)
	
	async def handle_delete_all_scores(self, client, input, output):
		logger.info("RankingServerMK8.delete_all_scores()")
		#--- request ---
		unique_id = input.u64()
		await self.delete_all_scores(client, unique_id)
	
	async def handle_upload_common_data(self, client, input, output):
		logger.info("RankingServerMK8.upload_common_data()")
		#--- request ---
		common_data = input.buffer()
		unique_id = input.u64()
		await self.upload_common_data(client, common_data, unique_id)
	
	async def handle_delete_common_data(self, client, input, output):
		logger.info("RankingServerMK8.delete_common_data()")
		#--- request ---
		unique_id = input.u64()
		await self.delete_common_data(client, unique_id)
	
	async def handle_get_common_data(self, client, input, output):
		logger.info("RankingServerMK8.get_common_data()")
		#--- request ---
		unique_id = input.u64()
		response = await self.get_common_data(client, unique_id)
		
		#--- response ---
		if not isinstance(response, bytes):
			raise RuntimeError("Expected bytes, got %s" %response.__class__.__name__)
		output.buffer(response)
	
	async def handle_change_attributes(self, client, input, output):
		logger.info("RankingServerMK8.change_attributes()")
		#--- request ---
		category = input.u32()
		param = input.extract(RankingChangeAttributesParam)
		unique_id = input.u64()
		await self.change_attributes(client, category, param, unique_id)
	
	async def handle_change_all_attributes(self, client, input, output):
		logger.info("RankingServerMK8.change_all_attributes()")
		#--- request ---
		param = input.extract(RankingChangeAttributesParam)
		unique_id = input.u64()
		await self.change_all_attributes(client, param, unique_id)
	
	async def handle_get_ranking(self, client, input, output):
		logger.info("RankingServerMK8.get_ranking()")
		#--- request ---
		mode = input.u8()
		category = input.u32()
		order = input.extract(RankingOrderParam)
		unique_id = input.u64()
		pid = input.pid()
		response = await self.get_ranking(client, mode, category, order, unique_id, pid)
		
		#--- response ---
		if not isinstance(response, RankingResult):
			raise RuntimeError("Expected RankingResult, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_approx_order(self, client, input, output):
		logger.info("RankingServerMK8.get_approx_order()")
		#--- request ---
		category = input.u32()
		order = input.extract(RankingOrderParam)
		score = input.u32()
		unique_id = input.u64()
		pid = input.pid()
		response = await self.get_approx_order(client, category, order, score, unique_id, pid)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u32(response)
	
	async def handle_get_stats(self, client, input, output):
		logger.info("RankingServerMK8.get_stats()")
		#--- request ---
		category = input.u32()
		order = input.extract(RankingOrderParam)
		flags = input.u32()
		response = await self.get_stats(client, category, order, flags)
		
		#--- response ---
		if not isinstance(response, RankingStats):
			raise RuntimeError("Expected RankingStats, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_ranking_by_pid_list(self, client, input, output):
		logger.info("RankingServerMK8.get_ranking_by_pid_list()")
		#--- request ---
		pids = input.list(input.pid)
		mode = input.u8()
		category = input.u32()
		order = input.extract(RankingOrderParam)
		unique_id = input.u64()
		response = await self.get_ranking_by_pid_list(client, pids, mode, category, order, unique_id)
		
		#--- response ---
		if not isinstance(response, RankingResult):
			raise RuntimeError("Expected RankingResult, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_ranking_by_unique_id_list(self, client, input, output):
		logger.info("RankingServerMK8.get_ranking_by_unique_id_list()")
		#--- request ---
		ids = input.list(input.u64)
		mode = input.u8()
		category = input.u32()
		order = input.extract(RankingOrderParam)
		unique_id = input.u64()
		response = await self.get_ranking_by_unique_id_list(client, ids, mode, category, order, unique_id)
		
		#--- response ---
		if not isinstance(response, RankingResult):
			raise RuntimeError("Expected RankingResult, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_competition_ranking_score(self, client, input, output):
		logger.warning("RankingServerMK8.get_competition_ranking_score is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_upload_competition_ranking_score(self, client, input, output):
		logger.info("RankingServerMK8.upload_competition_ranking_score()")
		#--- request ---
		param = input.extract(CompetitionRankingUploadScoreParam)
		response = await self.upload_competition_ranking_score(client, param)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_get_competition_info(self, client, input, output):
		logger.info("RankingServerMK8.get_competition_info()")
		#--- request ---
		param = input.extract(CompetitionRankingInfoGetParam)
		response = await self.get_competition_info(client, param)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def upload_score(self, *args):
		logger.warning("RankingServerMK8.upload_score not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_score(self, *args):
		logger.warning("RankingServerMK8.delete_score not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_all_scores(self, *args):
		logger.warning("RankingServerMK8.delete_all_scores not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def upload_common_data(self, *args):
		logger.warning("RankingServerMK8.upload_common_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_common_data(self, *args):
		logger.warning("RankingServerMK8.delete_common_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_common_data(self, *args):
		logger.warning("RankingServerMK8.get_common_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def change_attributes(self, *args):
		logger.warning("RankingServerMK8.change_attributes not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def change_all_attributes(self, *args):
		logger.warning("RankingServerMK8.change_all_attributes not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_ranking(self, *args):
		logger.warning("RankingServerMK8.get_ranking not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_approx_order(self, *args):
		logger.warning("RankingServerMK8.get_approx_order not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_stats(self, *args):
		logger.warning("RankingServerMK8.get_stats not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_ranking_by_pid_list(self, *args):
		logger.warning("RankingServerMK8.get_ranking_by_pid_list not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_ranking_by_unique_id_list(self, *args):
		logger.warning("RankingServerMK8.get_ranking_by_unique_id_list not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def upload_competition_ranking_score(self, *args):
		logger.warning("RankingServerMK8.upload_competition_ranking_score not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_competition_info(self, *args):
		logger.warning("RankingServerMK8.get_competition_info not implemented")
		raise common.RMCError("Core::NotImplemented")

