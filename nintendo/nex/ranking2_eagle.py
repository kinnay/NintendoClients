
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class RankingMode:
	GLOBAL_AROUND_SELF = 1
	GLOBAL = 2
	FRIENDS = 3


class Ranking2CategorySetting(common.Structure):
	def __init__(self):
		super().__init__()
		self.min_score = None
		self.max_score = None
		self.lowest_rank = None
		self.reset_month = None
		self.reset_day = None
		self.reset_hour = None
		self.reset_mode = None
		self.max_seasons_to_go_back = None
		self.score_order = None
	
	def check_required(self, settings, version):
		for field in ['min_score', 'max_score', 'lowest_rank', 'reset_month', 'reset_day', 'reset_hour', 'reset_mode', 'max_seasons_to_go_back', 'score_order']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.min_score = stream.u32()
		self.max_score = stream.u32()
		self.lowest_rank = stream.u32()
		self.reset_month = stream.u16()
		self.reset_day = stream.u8()
		self.reset_hour = stream.u8()
		self.reset_mode = stream.u8()
		self.max_seasons_to_go_back = stream.u8()
		self.score_order = stream.bool()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.min_score)
		stream.u32(self.max_score)
		stream.u32(self.lowest_rank)
		stream.u16(self.reset_month)
		stream.u8(self.reset_day)
		stream.u8(self.reset_hour)
		stream.u8(self.reset_mode)
		stream.u8(self.max_seasons_to_go_back)
		stream.bool(self.score_order)


class Ranking2ChartInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.create_time = None
		self.index = None
		self.category = None
		self.season = None
		self.bins_size = None
		self.sampling_rate = None
		self.score_order = None
		self.estimate_length = None
		self.estimate_highest_score = None
		self.estimate_lowest_score = None
		self.estimate_median_score = None
		self.estimate_average_score = None
		self.highest_bins_score = None
		self.lowest_bins_score = None
		self.bins_width = None
		self.attribute1 = None
		self.attribute2 = None
		self.quantities = None
	
	def check_required(self, settings, version):
		for field in ['create_time', 'index', 'category', 'season', 'bins_size', 'sampling_rate', 'score_order', 'estimate_length', 'estimate_highest_score', 'estimate_lowest_score', 'estimate_median_score', 'estimate_average_score', 'highest_bins_score', 'lowest_bins_score', 'bins_width', 'attribute1', 'attribute2', 'quantities']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.create_time = stream.datetime()
		self.index = stream.u32()
		self.category = stream.u32()
		self.season = stream.s32()
		self.bins_size = stream.u8()
		self.sampling_rate = stream.u8()
		self.score_order = stream.bool()
		self.estimate_length = stream.u32()
		self.estimate_highest_score = stream.u32()
		self.estimate_lowest_score = stream.u32()
		self.estimate_median_score = stream.u32()
		self.estimate_average_score = stream.double()
		self.highest_bins_score = stream.u32()
		self.lowest_bins_score = stream.u32()
		self.bins_width = stream.u32()
		self.attribute1 = stream.u32()
		self.attribute2 = stream.u32()
		self.quantities = stream.list(stream.u32)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.datetime(self.create_time)
		stream.u32(self.index)
		stream.u32(self.category)
		stream.s32(self.season)
		stream.u8(self.bins_size)
		stream.u8(self.sampling_rate)
		stream.bool(self.score_order)
		stream.u32(self.estimate_length)
		stream.u32(self.estimate_highest_score)
		stream.u32(self.estimate_lowest_score)
		stream.u32(self.estimate_median_score)
		stream.double(self.estimate_average_score)
		stream.u32(self.highest_bins_score)
		stream.u32(self.lowest_bins_score)
		stream.u32(self.bins_width)
		stream.u32(self.attribute1)
		stream.u32(self.attribute2)
		stream.list(self.quantities, stream.u32)


class Ranking2ChartInfoInput(common.Structure):
	def __init__(self):
		super().__init__()
		self.chart_index = None
		self.seasons_to_go_back = None
	
	def check_required(self, settings, version):
		for field in ['chart_index', 'seasons_to_go_back']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.chart_index = stream.u32()
		self.seasons_to_go_back = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.chart_index)
		stream.u8(self.seasons_to_go_back)


class Ranking2CommonData(common.Structure):
	def __init__(self):
		super().__init__()
		self.username = None
		self.mii = None
		self.binary_data = None
	
	def check_required(self, settings, version):
		for field in ['username', 'mii', 'binary_data']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.username = stream.string()
		self.mii = stream.qbuffer()
		self.binary_data = stream.qbuffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.string(self.username)
		stream.qbuffer(self.mii)
		stream.qbuffer(self.binary_data)


class Ranking2EstimateScoreRankInput(common.Structure):
	def __init__(self):
		super().__init__()
		self.category = None
		self.seasons_to_go_back = None
		self.score = None
	
	def check_required(self, settings, version):
		for field in ['category', 'seasons_to_go_back', 'score']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.category = stream.u32()
		self.seasons_to_go_back = stream.u8()
		self.score = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.category)
		stream.u8(self.seasons_to_go_back)
		stream.u32(self.score)


class Ranking2EstimateScoreRankOutput(common.Structure):
	def __init__(self):
		super().__init__()
		self.rank = None
		self.length = None
		self.score = None
		self.category = None
		self.season = None
		self.sampling_rate = None
	
	def check_required(self, settings, version):
		for field in ['rank', 'length', 'score', 'category', 'season', 'sampling_rate']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.rank = stream.u32()
		self.length = stream.u32()
		self.score = stream.u32()
		self.category = stream.u32()
		self.season = stream.s32()
		self.sampling_rate = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.rank)
		stream.u32(self.length)
		stream.u32(self.score)
		stream.u32(self.category)
		stream.s32(self.season)
		stream.u8(self.sampling_rate)


class Ranking2GetByListParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.category = None
		self.offset = None
		self.length = None
		self.sort_flags = None
		self.option_flags = None
		self.seasons_to_go_back = None
	
	def check_required(self, settings, version):
		for field in ['category', 'offset', 'length', 'sort_flags', 'option_flags', 'seasons_to_go_back']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.category = stream.u32()
		self.offset = stream.u32()
		self.length = stream.u32()
		self.sort_flags = stream.u32()
		self.option_flags = stream.u32()
		self.seasons_to_go_back = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.category)
		stream.u32(self.offset)
		stream.u32(self.length)
		stream.u32(self.sort_flags)
		stream.u32(self.option_flags)
		stream.u8(self.seasons_to_go_back)


class Ranking2GetParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.unique_id = 0
		self.pid = 0
		self.category = None
		self.offset = 0
		self.count = 10
		self.sort_flags = 0
		self.option_flags = 0
		self.mode = 2
		self.seasons_to_go_back = 0
	
	def check_required(self, settings, version):
		for field in ['category']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.unique_id = stream.u64()
		self.pid = stream.pid()
		self.category = stream.u32()
		self.offset = stream.u32()
		self.count = stream.u32()
		self.sort_flags = stream.u32()
		self.option_flags = stream.u32()
		self.mode = stream.u8()
		self.seasons_to_go_back = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.unique_id)
		stream.pid(self.pid)
		stream.u32(self.category)
		stream.u32(self.offset)
		stream.u32(self.count)
		stream.u32(self.sort_flags)
		stream.u32(self.option_flags)
		stream.u8(self.mode)
		stream.u8(self.seasons_to_go_back)


class Ranking2Info(common.Structure):
	def __init__(self):
		super().__init__()
		self.data = None
		self.lowest_rank = None
		self.num_entries = None
		self.season = None
	
	def check_required(self, settings, version):
		for field in ['data', 'lowest_rank', 'num_entries', 'season']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data = stream.list(Ranking2RankData)
		self.lowest_rank = stream.u32()
		self.num_entries = stream.u32()
		self.season = stream.s32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.list(self.data, stream.add)
		stream.u32(self.lowest_rank)
		stream.u32(self.num_entries)
		stream.s32(self.season)


class Ranking2RankData(common.Structure):
	def __init__(self):
		super().__init__()
		self.misc = None
		self.unique_id = None
		self.pid = None
		self.rank = None
		self.score = None
		self.common_data = Ranking2CommonData()
	
	def check_required(self, settings, version):
		for field in ['misc', 'unique_id', 'pid', 'rank', 'score']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.misc = stream.u64()
		self.unique_id = stream.u64()
		self.pid = stream.pid()
		self.rank = stream.u32()
		self.score = stream.u32()
		self.common_data = stream.extract(Ranking2CommonData)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.misc)
		stream.u64(self.unique_id)
		stream.pid(self.pid)
		stream.u32(self.rank)
		stream.u32(self.score)
		stream.add(self.common_data)


class Ranking2ScoreData(common.Structure):
	def __init__(self):
		super().__init__()
		self.misc = None
		self.category = None
		self.score = None
	
	def check_required(self, settings, version):
		for field in ['misc', 'category', 'score']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.misc = stream.u64()
		self.category = stream.u32()
		self.score = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.misc)
		stream.u32(self.category)
		stream.u32(self.score)


class Ranking2EstimateMyScoreRankInput(common.Structure):
	def __init__(self):
		super().__init__()
		self.category = None
		self.seasons_to_go_back = None
	
	def check_required(self, settings, version):
		for field in ['category', 'seasons_to_go_back']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.category = stream.u32()
		self.seasons_to_go_back = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.category)
		stream.u8(self.seasons_to_go_back)


class Ranking2Protocol:
	METHOD_PUT_SCORE = 1
	METHOD_GET_COMMON_DATA = 2
	METHOD_PUT_COMMON_DATA = 3
	METHOD_DELETE_COMMON_DATA = 4
	METHOD_GET_RANKING = 5
	METHOD_GET_RANKING_BY_PRINCIPAL_ID = 6
	METHOD_GET_CATEGORY_SETTING = 7
	METHOD_GET_RANKING_CHART = 8
	METHOD_GET_RANKING_CHARTS = 9
	METHOD_GET_ESTIMATE_SCORE_RANK = 10
	METHOD_GET_ESTIMATE_MY_SCORE_RANK = 11
	
	PROTOCOL_ID = 0x7A


class Ranking2Client(Ranking2Protocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def put_score(self, socres, unique_id):
		logger.info("Ranking2Client.put_score()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(socres, stream.add)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PUT_SCORE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.put_score -> done")
	
	async def get_common_data(self, option_flags, pid, unique_id):
		logger.info("Ranking2Client.get_common_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(option_flags)
		stream.pid(pid)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_COMMON_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		common_data = stream.extract(Ranking2CommonData)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.get_common_data -> done")
		return common_data
	
	async def put_common_data(self, data, unique_id):
		logger.info("Ranking2Client.put_common_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(data)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PUT_COMMON_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.put_common_data -> done")
	
	async def delete_common_data(self, unique_id):
		logger.info("Ranking2Client.delete_common_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(unique_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_COMMON_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.delete_common_data -> done")
	
	async def get_ranking(self, param):
		logger.info("Ranking2Client.get_ranking()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_RANKING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(Ranking2Info)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.get_ranking -> done")
		return info
	
	async def get_ranking_by_principal_id(self, param, pids):
		logger.info("Ranking2Client.get_ranking_by_principal_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		stream.list(pids, stream.pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_RANKING_BY_PRINCIPAL_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(Ranking2Info)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.get_ranking_by_principal_id -> done")
		return info
	
	async def get_category_setting(self, category):
		logger.info("Ranking2Client.get_category_setting()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(category)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_CATEGORY_SETTING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		setting = stream.extract(Ranking2CategorySetting)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.get_category_setting -> done")
		return setting
	
	async def get_ranking_chart(self, input):
		logger.info("Ranking2Client.get_ranking_chart()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(input)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_RANKING_CHART, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(Ranking2ChartInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.get_ranking_chart -> done")
		return info
	
	async def get_ranking_charts(self, inputs):
		logger.info("Ranking2Client.get_ranking_charts()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(inputs, stream.add)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_RANKING_CHARTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		infos = stream.list(Ranking2ChartInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.get_ranking_charts -> done")
		return infos
	
	async def get_estimate_score_rank(self, input):
		logger.info("Ranking2Client.get_estimate_score_rank()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(input)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_ESTIMATE_SCORE_RANK, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		output = stream.extract(Ranking2EstimateScoreRankOutput)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.get_estimate_score_rank -> done")
		return output
	
	async def get_estimate_my_score_rank(self, input):
		logger.info("Ranking2Client.get_estimate_my_score_rank()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(input)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_ESTIMATE_MY_SCORE_RANK, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		output = stream.extract(Ranking2EstimateScoreRankOutput)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("Ranking2Client.get_estimate_my_score_rank -> done")
		return output


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
			self.METHOD_GET_RANKING_CHART: self.handle_get_ranking_chart,
			self.METHOD_GET_RANKING_CHARTS: self.handle_get_ranking_charts,
			self.METHOD_GET_ESTIMATE_SCORE_RANK: self.handle_get_estimate_score_rank,
			self.METHOD_GET_ESTIMATE_MY_SCORE_RANK: self.handle_get_estimate_my_score_rank,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on Ranking2Server: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_put_score(self, client, input, output):
		logger.info("Ranking2Server.put_score()")
		#--- request ---
		socres = input.list(Ranking2ScoreData)
		unique_id = input.u64()
		await self.put_score(client, socres, unique_id)
	
	async def handle_get_common_data(self, client, input, output):
		logger.info("Ranking2Server.get_common_data()")
		#--- request ---
		option_flags = input.u32()
		pid = input.pid()
		unique_id = input.u64()
		response = await self.get_common_data(client, option_flags, pid, unique_id)
		
		#--- response ---
		if not isinstance(response, Ranking2CommonData):
			raise RuntimeError("Expected Ranking2CommonData, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_put_common_data(self, client, input, output):
		logger.info("Ranking2Server.put_common_data()")
		#--- request ---
		data = input.extract(Ranking2CommonData)
		unique_id = input.u64()
		await self.put_common_data(client, data, unique_id)
	
	async def handle_delete_common_data(self, client, input, output):
		logger.info("Ranking2Server.delete_common_data()")
		#--- request ---
		unique_id = input.u64()
		await self.delete_common_data(client, unique_id)
	
	async def handle_get_ranking(self, client, input, output):
		logger.info("Ranking2Server.get_ranking()")
		#--- request ---
		param = input.extract(Ranking2GetParam)
		response = await self.get_ranking(client, param)
		
		#--- response ---
		if not isinstance(response, Ranking2Info):
			raise RuntimeError("Expected Ranking2Info, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_ranking_by_principal_id(self, client, input, output):
		logger.info("Ranking2Server.get_ranking_by_principal_id()")
		#--- request ---
		param = input.extract(Ranking2GetByListParam)
		pids = input.list(input.pid)
		response = await self.get_ranking_by_principal_id(client, param, pids)
		
		#--- response ---
		if not isinstance(response, Ranking2Info):
			raise RuntimeError("Expected Ranking2Info, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_category_setting(self, client, input, output):
		logger.info("Ranking2Server.get_category_setting()")
		#--- request ---
		category = input.u32()
		response = await self.get_category_setting(client, category)
		
		#--- response ---
		if not isinstance(response, Ranking2CategorySetting):
			raise RuntimeError("Expected Ranking2CategorySetting, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_ranking_chart(self, client, input, output):
		logger.info("Ranking2Server.get_ranking_chart()")
		#--- request ---
		input = input.extract(Ranking2ChartInfoInput)
		response = await self.get_ranking_chart(client, input)
		
		#--- response ---
		if not isinstance(response, Ranking2ChartInfo):
			raise RuntimeError("Expected Ranking2ChartInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_ranking_charts(self, client, input, output):
		logger.info("Ranking2Server.get_ranking_charts()")
		#--- request ---
		inputs = input.list(Ranking2ChartInfoInput)
		response = await self.get_ranking_charts(client, inputs)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_estimate_score_rank(self, client, input, output):
		logger.info("Ranking2Server.get_estimate_score_rank()")
		#--- request ---
		input = input.extract(Ranking2EstimateScoreRankInput)
		response = await self.get_estimate_score_rank(client, input)
		
		#--- response ---
		if not isinstance(response, Ranking2EstimateScoreRankOutput):
			raise RuntimeError("Expected Ranking2EstimateScoreRankOutput, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_estimate_my_score_rank(self, client, input, output):
		logger.info("Ranking2Server.get_estimate_my_score_rank()")
		#--- request ---
		input = input.extract(Ranking2EstimateMyScoreRankInput)
		response = await self.get_estimate_my_score_rank(client, input)
		
		#--- response ---
		if not isinstance(response, Ranking2EstimateScoreRankOutput):
			raise RuntimeError("Expected Ranking2EstimateScoreRankOutput, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def put_score(self, *args):
		logger.warning("Ranking2Server.put_score not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_common_data(self, *args):
		logger.warning("Ranking2Server.get_common_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def put_common_data(self, *args):
		logger.warning("Ranking2Server.put_common_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_common_data(self, *args):
		logger.warning("Ranking2Server.delete_common_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_ranking(self, *args):
		logger.warning("Ranking2Server.get_ranking not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_ranking_by_principal_id(self, *args):
		logger.warning("Ranking2Server.get_ranking_by_principal_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_category_setting(self, *args):
		logger.warning("Ranking2Server.get_category_setting not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_ranking_chart(self, *args):
		logger.warning("Ranking2Server.get_ranking_chart not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_ranking_charts(self, *args):
		logger.warning("Ranking2Server.get_ranking_charts not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_estimate_score_rank(self, *args):
		logger.warning("Ranking2Server.get_estimate_score_rank not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_estimate_my_score_rank(self, *args):
		logger.warning("Ranking2Server.get_estimate_my_score_rank not implemented")
		raise common.RMCError("Core::NotImplemented")

