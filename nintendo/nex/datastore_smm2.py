
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


class ClearCondition:
	NORMAL = 0
	COLLECT_COINS = 4116396131
	KILL_SKIPSQUEAKS = 4042480826


class CourseDifficulty:
	EASY = 0
	STANDARD = 1
	EXPERT = 2
	SUPER_EXPERT = 3


class CourseOption:
	PLAY_STATS = 1
	RATINGS = 2
	TIME_STATS = 4
	COMMENT_STATS = 8
	UNK9 = 16
	UNK10 = 32
	UNK8 = 64
	ONE_SCREEN_THUMBNAIL = 128
	ENTIRE_THUMBNAIL = 256
	ALL = 511


class CourseTag:
	NONE = 0
	STANDARD = 1
	PUZZLE_SOLVING = 2
	SPEEDRUN = 3
	AUTOSCROLL = 4
	AUTO_MARIO = 5
	SHORT_AND_SWEET = 6
	MULTIPLAYER_VS = 7
	THEMED = 8
	MUSIC = 9


class CourseTheme:
	GROUND = 0
	UNDERGROUND = 1
	CASTLE = 2
	AIRSHIP = 3
	UNDERWATER = 4
	GHOST_HOUSE = 5
	SNOW = 6
	DESERT = 7
	SKY = 8
	FOREST = 9


class EventCourseOption:
	UNK3 = 1
	GET_INFO = 2
	BEST_TIME = 8
	ONE_SCREEN_THUMBNAIL = 16
	ENTIRE_THUMBNAIL = 32
	UNK1 = 64
	MEDAL_TIME = 256
	GHOST = 512
	ALL = 1023


class GameStyle:
	SMB1 = 0
	SMB3 = 1
	SMW = 2
	NSMBU = 3
	SM3DW = 4


class MultiplayerStatsKeys:
	MULTIPLAYER_SCORE = 0
	VERSUS_PLAYS = 2
	VERSUS_WINS = 3
	COOP_PLAYS = 10
	COOP_WINS = 11


class PlayStatsKeys:
	PLAYS = 0
	CLEARS = 1
	ATTEMPTS = 2
	DEATHS = 3


class UserOption:
	PLAY_STATS = 1
	MAKER_STATS = 2
	UNK2 = 4
	ENDLESS_MODE = 8
	MULTIPLAYER_STATS = 16
	BADGE_INFO = 32
	UNK8 = 64
	UNK9 = 128
	UNK1 = 512
	UNK7 = 1024
	UNK11 = 4096
	UNK13 = 8192
	UNK15 = 32768
	ALL = 65535


class BadgeInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
	
	def check_required(self, settings):
		for field in ['unk1', 'unk2']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk1 = stream.u16()
		self.unk2 = stream.u8()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u16(self.unk1)
		stream.u8(self.unk2)


class CommentInfo(common.Structure):
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
		self.unk10 = None
		self.unk11 = None
		self.unk12 = None
		self.unk13 = None
		self.unk14 = None
		self.unk15 = None
		self.picture = CommentPictureReqGetInfoWithoutHeaders()
		self.unk16 = None
		self.unk17 = None
	
	def check_required(self, settings):
		for field in ['unk1', 'unk2', 'unk3', 'unk4', 'unk5', 'unk6', 'unk7', 'unk8', 'unk9', 'unk10', 'unk11', 'unk12', 'unk13', 'unk14', 'unk15', 'unk16', 'unk17']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk1 = stream.u64()
		self.unk2 = stream.string()
		self.unk3 = stream.u8()
		self.unk4 = stream.u8()
		self.unk5 = stream.u64()
		self.unk6 = stream.u16()
		self.unk7 = stream.u16()
		self.unk8 = stream.u8()
		self.unk9 = stream.u8()
		self.unk10 = stream.u8()
		self.unk11 = stream.bool()
		self.unk12 = stream.bool()
		self.unk13 = stream.datetime()
		self.unk14 = stream.qbuffer()
		self.unk15 = stream.string()
		self.picture = stream.extract(CommentPictureReqGetInfoWithoutHeaders)
		self.unk16 = stream.u16()
		self.unk17 = stream.u8()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.unk1)
		stream.string(self.unk2)
		stream.u8(self.unk3)
		stream.u8(self.unk4)
		stream.u64(self.unk5)
		stream.u16(self.unk6)
		stream.u16(self.unk7)
		stream.u8(self.unk8)
		stream.u8(self.unk9)
		stream.u8(self.unk10)
		stream.bool(self.unk11)
		stream.bool(self.unk12)
		stream.datetime(self.unk13)
		stream.qbuffer(self.unk14)
		stream.string(self.unk15)
		stream.add(self.picture)
		stream.u16(self.unk16)
		stream.u8(self.unk17)


class CommentPictureReqGetInfoWithoutHeaders(common.Structure):
	def __init__(self):
		super().__init__()
		self.url = None
		self.data_type = None
		self.unk1 = None
		self.unk2 = None
		self.filename = None
	
	def check_required(self, settings):
		for field in ['url', 'data_type', 'unk1', 'unk2', 'filename']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.url = stream.string()
		self.data_type = stream.u8()
		self.unk1 = stream.u32()
		self.unk2 = stream.buffer()
		self.filename = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.url)
		stream.u8(self.data_type)
		stream.u32(self.unk1)
		stream.buffer(self.unk2)
		stream.string(self.filename)


class CourseInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.code = None
		self.owner_id = None
		self.name = None
		self.description = None
		self.game_style = None
		self.course_theme = None
		self.upload_time = None
		self.difficulty = None
		self.tag1 = None
		self.tag2 = None
		self.unk1 = None
		self.clear_condition = None
		self.clear_condition_magnitude = None
		self.unk2 = None
		self.unk3 = None
		self.play_stats = None
		self.ratings = None
		self.unk4 = None
		self.time_stats = CourseTimeStats()
		self.comment_stats = None
		self.unk9 = None
		self.unk10 = None
		self.unk11 = None
		self.unk12 = None
		self.one_screen_thumbnail = RelationObjectReqGetInfo()
		self.entire_thumbnail = RelationObjectReqGetInfo()
	
	def check_required(self, settings):
		for field in ['data_id', 'code', 'owner_id', 'name', 'description', 'game_style', 'course_theme', 'upload_time', 'difficulty', 'tag1', 'tag2', 'unk1', 'clear_condition', 'clear_condition_magnitude', 'unk2', 'unk3', 'play_stats', 'ratings', 'unk4', 'comment_stats', 'unk9', 'unk10', 'unk11', 'unk12']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data_id = stream.u64()
		self.code = stream.string()
		self.owner_id = stream.pid()
		self.name = stream.string()
		self.description = stream.string()
		self.game_style = stream.u8()
		self.course_theme = stream.u8()
		self.upload_time = stream.datetime()
		self.difficulty = stream.u8()
		self.tag1 = stream.u8()
		self.tag2 = stream.u8()
		self.unk1 = stream.u8()
		self.clear_condition = stream.u32()
		self.clear_condition_magnitude = stream.u16()
		self.unk2 = stream.u16()
		self.unk3 = stream.qbuffer()
		self.play_stats = stream.map(stream.u8, stream.u32)
		self.ratings = stream.map(stream.u8, stream.u32)
		self.unk4 = stream.map(stream.u8, stream.u32)
		self.time_stats = stream.extract(CourseTimeStats)
		self.comment_stats = stream.map(stream.u8, stream.u32)
		self.unk9 = stream.u8()
		self.unk10 = stream.u8()
		self.unk11 = stream.u8()
		self.unk12 = stream.u8()
		self.one_screen_thumbnail = stream.extract(RelationObjectReqGetInfo)
		self.entire_thumbnail = stream.extract(RelationObjectReqGetInfo)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)
		stream.string(self.code)
		stream.pid(self.owner_id)
		stream.string(self.name)
		stream.string(self.description)
		stream.u8(self.game_style)
		stream.u8(self.course_theme)
		stream.datetime(self.upload_time)
		stream.u8(self.difficulty)
		stream.u8(self.tag1)
		stream.u8(self.tag2)
		stream.u8(self.unk1)
		stream.u32(self.clear_condition)
		stream.u16(self.clear_condition_magnitude)
		stream.u16(self.unk2)
		stream.qbuffer(self.unk3)
		stream.map(self.play_stats, stream.u8, stream.u32)
		stream.map(self.ratings, stream.u8, stream.u32)
		stream.map(self.unk4, stream.u8, stream.u32)
		stream.add(self.time_stats)
		stream.map(self.comment_stats, stream.u8, stream.u32)
		stream.u8(self.unk9)
		stream.u8(self.unk10)
		stream.u8(self.unk11)
		stream.u8(self.unk12)
		stream.add(self.one_screen_thumbnail)
		stream.add(self.entire_thumbnail)


class CourseTimeStats(common.Structure):
	def __init__(self):
		super().__init__()
		self.first_completion = None
		self.world_record_holder = None
		self.world_record = None
		self.upload_time = None
	
	def check_required(self, settings):
		for field in ['first_completion', 'world_record_holder', 'world_record', 'upload_time']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.first_completion = stream.pid()
		self.world_record_holder = stream.pid()
		self.world_record = stream.u32()
		self.upload_time = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.first_completion)
		stream.pid(self.world_record_holder)
		stream.u32(self.world_record)
		stream.u32(self.upload_time)


class DataStoreCompletePostParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.success = None
	
	def check_required(self, settings):
		for field in ['data_id', 'success']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data_id = stream.u64()
		self.success = stream.bool()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)
		stream.bool(self.success)


class DataStoreGetMetaParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = 0
		self.persistence_target = DataStorePersistenceTarget()
		self.result_option = 0
		self.access_password = 0
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		self.data_id = stream.u64()
		self.persistence_target = stream.extract(DataStorePersistenceTarget)
		self.result_option = stream.u8()
		self.access_password = stream.u64()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)
		stream.add(self.persistence_target)
		stream.u8(self.result_option)
		stream.u64(self.access_password)


class DataStoreKeyValue(common.Structure):
	def __init__(self):
		super().__init__()
		self.key = None
		self.value = None
	
	def check_required(self, settings):
		for field in ['key', 'value']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.key = stream.string()
		self.value = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.key)
		stream.string(self.value)


class DataStoreMetaInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.owner_id = None
		self.size = None
		self.name = None
		self.data_type = None
		self.meta_binary = None
		self.permission = DataStorePermission()
		self.delete_permission = DataStorePermission()
		self.create_time = None
		self.update_time = None
		self.period = None
		self.status = None
		self.referred_count = None
		self.refer_data_id = None
		self.flag = None
		self.referred_time = None
		self.expire_time = None
		self.tags = None
		self.ratings = None
	
	def check_required(self, settings):
		for field in ['data_id', 'owner_id', 'size', 'name', 'data_type', 'meta_binary', 'create_time', 'update_time', 'period', 'status', 'referred_count', 'refer_data_id', 'flag', 'referred_time', 'expire_time', 'tags', 'ratings']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data_id = stream.u64()
		self.owner_id = stream.pid()
		self.size = stream.u32()
		self.name = stream.string()
		self.data_type = stream.u16()
		self.meta_binary = stream.qbuffer()
		self.permission = stream.extract(DataStorePermission)
		self.delete_permission = stream.extract(DataStorePermission)
		self.create_time = stream.datetime()
		self.update_time = stream.datetime()
		self.period = stream.u16()
		self.status = stream.u8()
		self.referred_count = stream.u32()
		self.refer_data_id = stream.u32()
		self.flag = stream.u32()
		self.referred_time = stream.datetime()
		self.expire_time = stream.datetime()
		self.tags = stream.list(stream.string)
		self.ratings = stream.list(DataStoreRatingInfoWithSlot)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)
		stream.pid(self.owner_id)
		stream.u32(self.size)
		stream.string(self.name)
		stream.u16(self.data_type)
		stream.qbuffer(self.meta_binary)
		stream.add(self.permission)
		stream.add(self.delete_permission)
		stream.datetime(self.create_time)
		stream.datetime(self.update_time)
		stream.u16(self.period)
		stream.u8(self.status)
		stream.u32(self.referred_count)
		stream.u32(self.refer_data_id)
		stream.u32(self.flag)
		stream.datetime(self.referred_time)
		stream.datetime(self.expire_time)
		stream.list(self.tags, stream.string)
		stream.list(self.ratings, stream.add)


class DataStorePasswordInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.access_password = None
		self.update_password = None
	
	def check_required(self, settings):
		for field in ['data_id', 'access_password', 'update_password']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data_id = stream.u64()
		self.access_password = stream.u64()
		self.update_password = stream.u64()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)
		stream.u64(self.access_password)
		stream.u64(self.update_password)


class DataStorePermission(common.Structure):
	def __init__(self):
		super().__init__()
		self.permission = 3
		self.recipients = []
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		self.permission = stream.u8()
		self.recipients = stream.list(stream.pid)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u8(self.permission)
		stream.list(self.recipients, stream.pid)


class DataStorePersistenceInitParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.persistence_id = 65535
		self.delete_last_object = True
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		self.persistence_id = stream.u16()
		self.delete_last_object = stream.bool()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u16(self.persistence_id)
		stream.bool(self.delete_last_object)


class DataStorePersistenceTarget(common.Structure):
	def __init__(self):
		super().__init__()
		self.owner_id = 0
		self.persistence_id = 65535
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		self.owner_id = stream.pid()
		self.persistence_id = stream.u16()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.owner_id)
		stream.u16(self.persistence_id)


class DataStorePrepareGetParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = 0
		self.lock_id = 0
		self.persistence_target = DataStorePersistenceTarget()
		self.access_password = 0
		self.extra_data = []
	
	def check_required(self, settings):
		if settings.get("nex.version") >= 30500:
			pass
	
	def load(self, stream):
		self.data_id = stream.u64()
		self.lock_id = stream.u32()
		self.persistence_target = stream.extract(DataStorePersistenceTarget)
		self.access_password = stream.u64()
		if stream.settings.get("nex.version") >= 30500:
			self.extra_data = stream.list(stream.string)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)
		stream.u32(self.lock_id)
		stream.add(self.persistence_target)
		stream.u64(self.access_password)
		if stream.settings.get("nex.version") >= 30500:
			stream.list(self.extra_data, stream.string)


class DataStorePrepareGetParamV1(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.lock_id = 0
	
	def check_required(self, settings):
		for field in ['data_id']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data_id = stream.u64()
		self.lock_id = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)
		stream.u32(self.lock_id)


class DataStorePreparePostParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.size = None
		self.name = ""
		self.data_type = 0
		self.meta_binary = b""
		self.permission = DataStorePermission()
		self.delete_permission = DataStorePermission()
		self.flag = None
		self.period = None
		self.refer_data_id = 0
		self.tags = []
		self.rating_init_param = []
		self.persistence_init_param = DataStorePersistenceInitParam()
		self.extra_data = None
	
	def check_required(self, settings):
		for field in ['size', 'flag', 'period']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings.get("nex.version") >= 30500:
			for field in ['extra_data']:
				if getattr(self, field) is None:
					raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.size = stream.u32()
		self.name = stream.string()
		self.data_type = stream.u16()
		self.meta_binary = stream.qbuffer()
		self.permission = stream.extract(DataStorePermission)
		self.delete_permission = stream.extract(DataStorePermission)
		self.flag = stream.u32()
		self.period = stream.u16()
		self.refer_data_id = stream.u32()
		self.tags = stream.list(stream.string)
		self.rating_init_param = stream.list(DataStoreRatingInitParamWithSlot)
		self.persistence_init_param = stream.extract(DataStorePersistenceInitParam)
		if stream.settings.get("nex.version") >= 30500:
			self.extra_data = stream.list(stream.string)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.size)
		stream.string(self.name)
		stream.u16(self.data_type)
		stream.qbuffer(self.meta_binary)
		stream.add(self.permission)
		stream.add(self.delete_permission)
		stream.u32(self.flag)
		stream.u16(self.period)
		stream.u32(self.refer_data_id)
		stream.list(self.tags, stream.string)
		stream.list(self.rating_init_param, stream.add)
		stream.add(self.persistence_init_param)
		if stream.settings.get("nex.version") >= 30500:
			stream.list(self.extra_data, stream.string)


class DataStoreRatingInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.total_value = None
		self.count = None
		self.initial_value = None
	
	def check_required(self, settings):
		for field in ['total_value', 'count', 'initial_value']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.total_value = stream.s64()
		self.count = stream.u32()
		self.initial_value = stream.s64()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.s64(self.total_value)
		stream.u32(self.count)
		stream.s64(self.initial_value)


class DataStoreRatingInfoWithSlot(common.Structure):
	def __init__(self):
		super().__init__()
		self.slot = None
		self.info = DataStoreRatingInfo()
	
	def check_required(self, settings):
		for field in ['slot']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.slot = stream.u8()
		self.info = stream.extract(DataStoreRatingInfo)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u8(self.slot)
		stream.add(self.info)


class DataStoreRatingInitParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.flag = None
		self.internal_flag = None
		self.lock_type = None
		self.initial_value = None
		self.range_min = None
		self.range_max = None
		self.period_hour = None
		self.period_duration = None
	
	def check_required(self, settings):
		for field in ['flag', 'internal_flag', 'lock_type', 'initial_value', 'range_min', 'range_max', 'period_hour', 'period_duration']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.flag = stream.u8()
		self.internal_flag = stream.u8()
		self.lock_type = stream.u8()
		self.initial_value = stream.s64()
		self.range_min = stream.s32()
		self.range_max = stream.s32()
		self.period_hour = stream.s8()
		self.period_duration = stream.s16()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u8(self.flag)
		stream.u8(self.internal_flag)
		stream.u8(self.lock_type)
		stream.s64(self.initial_value)
		stream.s32(self.range_min)
		stream.s32(self.range_max)
		stream.s8(self.period_hour)
		stream.s16(self.period_duration)


class DataStoreRatingInitParamWithSlot(common.Structure):
	def __init__(self):
		super().__init__()
		self.slot = None
		self.param = DataStoreRatingInitParam()
	
	def check_required(self, settings):
		for field in ['slot']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.slot = stream.s8()
		self.param = stream.extract(DataStoreRatingInitParam)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.s8(self.slot)
		stream.add(self.param)


class DataStoreReqGetInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.url = None
		self.headers = None
		self.size = None
		self.root_ca_cert = None
		self.data_id = None
	
	def check_required(self, settings):
		for field in ['url', 'headers', 'size', 'root_ca_cert']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings.get("nex.version") >= 30500:
			for field in ['data_id']:
				if getattr(self, field) is None:
					raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.url = stream.string()
		self.headers = stream.list(DataStoreKeyValue)
		self.size = stream.u32()
		self.root_ca_cert = stream.buffer()
		if stream.settings.get("nex.version") >= 30500:
			self.data_id = stream.u64()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.url)
		stream.list(self.headers, stream.add)
		stream.u32(self.size)
		stream.buffer(self.root_ca_cert)
		if stream.settings.get("nex.version") >= 30500:
			stream.u64(self.data_id)


class DataStoreReqGetInfoV1(common.Structure):
	def __init__(self):
		super().__init__()
		self.url = None
		self.headers = None
		self.size = None
		self.root_ca_cert = None
	
	def check_required(self, settings):
		for field in ['url', 'headers', 'size', 'root_ca_cert']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.url = stream.string()
		self.headers = stream.list(DataStoreKeyValue)
		self.size = stream.u32()
		self.root_ca_cert = stream.buffer()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.url)
		stream.list(self.headers, stream.add)
		stream.u32(self.size)
		stream.buffer(self.root_ca_cert)


class DataStoreReqPostInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.url = None
		self.headers = None
		self.form = None
		self.root_ca_cert = None
	
	def check_required(self, settings):
		for field in ['data_id', 'url', 'headers', 'form', 'root_ca_cert']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data_id = stream.u64()
		self.url = stream.string()
		self.headers = stream.list(DataStoreKeyValue)
		self.form = stream.list(DataStoreKeyValue)
		self.root_ca_cert = stream.buffer()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)
		stream.string(self.url)
		stream.list(self.headers, stream.add)
		stream.list(self.form, stream.add)
		stream.buffer(self.root_ca_cert)


class EventCourseGhostInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.replay_file = RelationObjectReqGetInfo()
		self.time = None
		self.pid = None
	
	def check_required(self, settings):
		for field in ['time', 'pid']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.replay_file = stream.extract(RelationObjectReqGetInfo)
		self.time = stream.u32()
		self.pid = stream.pid()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.add(self.replay_file)
		stream.u32(self.time)
		stream.pid(self.pid)


class EventCourseHistogram(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.unk1 = None
		self.unk2 = None
		self.unk3 = None
		self.values = None
		self.medals = None
		self.unk4 = None
	
	def check_required(self, settings):
		for field in ['data_id', 'unk1', 'unk2', 'unk3', 'values', 'medals', 'unk4']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data_id = stream.u64()
		self.unk1 = stream.u32()
		self.unk2 = stream.u32()
		self.unk3 = stream.u32()
		self.values = stream.list(stream.u32)
		self.medals = stream.map(stream.u8, stream.u32)
		self.unk4 = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)
		stream.u32(self.unk1)
		stream.u32(self.unk2)
		stream.u32(self.unk3)
		stream.list(self.values, stream.u32)
		stream.map(self.medals, stream.u8, stream.u32)
		stream.u32(self.unk4)


class EventCourseInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.name = None
		self.description = None
		self.game_style = None
		self.course_theme = None
		self.unk1 = None
		self.unk2 = None
		self.upload_time = None
		self.get_info = DataStoreReqGetInfo()
		self.unk3 = None
		self.unk4 = UnknownStruct6()
		self.unk5 = None
		self.one_screen_thumbnail = EventCourseThumbnail()
		self.entire_thumbnail = EventCourseThumbnail()
		self.end_time = None
		self.unk6 = None
		self.unk7 = None
		self.unk8 = None
		self.unk9 = None
		self.best_time = None
		self.unk10 = None
		self.medal_time = None
		self.personal_ghost = RelationObjectReqGetInfo()
	
	def get_version(self, settings):
		version = 0
		version = 1
		return version
	
	def check_required(self, settings):
		for field in ['data_id', 'name', 'description', 'game_style', 'course_theme', 'unk1', 'unk2', 'upload_time', 'unk3', 'unk5', 'end_time', 'unk6', 'unk7', 'unk8', 'unk9', 'best_time', 'unk10', 'medal_time']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data_id = stream.u64()
		self.name = stream.string()
		self.description = stream.string()
		self.game_style = stream.u8()
		self.course_theme = stream.u8()
		self.unk1 = stream.bool()
		self.unk2 = stream.bool()
		self.upload_time = stream.datetime()
		self.get_info = stream.extract(DataStoreReqGetInfo)
		self.unk3 = stream.map(stream.u8, stream.u32)
		self.unk4 = stream.extract(UnknownStruct6)
		self.unk5 = stream.u8()
		self.one_screen_thumbnail = stream.extract(EventCourseThumbnail)
		self.entire_thumbnail = stream.extract(EventCourseThumbnail)
		self.end_time = stream.datetime()
		self.unk6 = stream.u8()
		self.unk7 = stream.u32()
		self.unk8 = stream.u16()
		self.unk9 = stream.u16()
		self.best_time = stream.u32()
		self.unk10 = stream.u32()
		self.medal_time = stream.u32()
		self.personal_ghost = stream.extract(RelationObjectReqGetInfo)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)
		stream.string(self.name)
		stream.string(self.description)
		stream.u8(self.game_style)
		stream.u8(self.course_theme)
		stream.bool(self.unk1)
		stream.bool(self.unk2)
		stream.datetime(self.upload_time)
		stream.add(self.get_info)
		stream.map(self.unk3, stream.u8, stream.u32)
		stream.add(self.unk4)
		stream.u8(self.unk5)
		stream.add(self.one_screen_thumbnail)
		stream.add(self.entire_thumbnail)
		stream.datetime(self.end_time)
		stream.u8(self.unk6)
		stream.u32(self.unk7)
		stream.u16(self.unk8)
		stream.u16(self.unk9)
		stream.u32(self.best_time)
		stream.u32(self.unk10)
		stream.u32(self.medal_time)
		stream.add(self.personal_ghost)


class EventCourseStatusInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
		self.unk3 = None
	
	def check_required(self, settings):
		for field in ['unk1', 'unk2', 'unk3']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk1 = stream.u64()
		self.unk2 = stream.bool()
		self.unk3 = stream.datetime()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.unk1)
		stream.bool(self.unk2)
		stream.datetime(self.unk3)


class EventCourseThumbnail(common.Structure):
	def __init__(self):
		super().__init__()
		self.url = None
		self.headers = None
		self.filesize = None
		self.root_ca_cert = None
		self.filename = None
	
	def check_required(self, settings):
		for field in ['url', 'headers', 'filesize', 'root_ca_cert', 'filename']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.url = stream.string()
		self.headers = stream.list(DataStoreKeyValue)
		self.filesize = stream.u32()
		self.root_ca_cert = stream.buffer()
		self.filename = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.url)
		stream.list(self.headers, stream.add)
		stream.u32(self.filesize)
		stream.buffer(self.root_ca_cert)
		stream.string(self.filename)


class GetCoursesEventParam(common.Structure):
	def __init__(self):
		super().__init__()
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		pass
	
	def save(self, stream):
		self.check_required(stream.settings)


class GetCoursesParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_ids = None
		self.option = 0
	
	def check_required(self, settings):
		for field in ['data_ids']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data_ids = stream.list(stream.u64)
		self.option = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.list(self.data_ids, stream.u64)
		stream.u32(self.option)


class GetEventCourseGhostParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.time = None
		self.count = None
	
	def check_required(self, settings):
		for field in ['data_id', 'time', 'count']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data_id = stream.u64()
		self.time = stream.u32()
		self.count = stream.u8()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)
		stream.u32(self.time)
		stream.u8(self.count)


class GetEventCourseHistogramParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
	
	def check_required(self, settings):
		for field in ['data_id']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.data_id = stream.u64()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.data_id)


class GetUserOrCourseParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.code = None
		self.user_option = 0
		self.course_option = 0
	
	def check_required(self, settings):
		for field in ['code']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.code = stream.string()
		self.user_option = stream.u32()
		self.course_option = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.code)
		stream.u32(self.user_option)
		stream.u32(self.course_option)


class GetUsersParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.pids = None
		self.option = 0
	
	def check_required(self, settings):
		for field in ['pids']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.pids = stream.list(stream.pid)
		self.option = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.list(self.pids, stream.pid)
		stream.u32(self.option)


class RegisterUserParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.name = None
		self.unk1 = UnknownStruct1()
		self.unk2 = None
		self.language = None
		self.country = None
		self.device_id = None
	
	def check_required(self, settings):
		for field in ['name', 'unk2', 'language', 'country', 'device_id']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.name = stream.string()
		self.unk1 = stream.extract(UnknownStruct1)
		self.unk2 = stream.qbuffer()
		self.language = stream.u8()
		self.country = stream.string()
		self.device_id = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.name)
		stream.add(self.unk1)
		stream.qbuffer(self.unk2)
		stream.u8(self.language)
		stream.string(self.country)
		stream.string(self.device_id)


class RelationObjectReqGetInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.url = None
		self.data_type = None
		self.size = None
		self.unk = None
		self.filename = None
	
	def check_required(self, settings):
		for field in ['url', 'data_type', 'size', 'unk', 'filename']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.url = stream.string()
		self.data_type = stream.u8()
		self.size = stream.u32()
		self.unk = stream.buffer()
		self.filename = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.url)
		stream.u8(self.data_type)
		stream.u32(self.size)
		stream.buffer(self.unk)
		stream.string(self.filename)


class ReqGetInfoHeadersInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.headers = None
		self.expiration = None
	
	def check_required(self, settings):
		for field in ['headers', 'expiration']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.headers = stream.list(DataStoreKeyValue)
		self.expiration = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.list(self.headers, stream.add)
		stream.u32(self.expiration)


class SearchCoursesEndlessModeParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.option = 0
		self.count = None
		self.difficulty = None
	
	def check_required(self, settings):
		for field in ['count', 'difficulty']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.option = stream.u32()
		self.count = stream.u32()
		self.difficulty = stream.u8()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.option)
		stream.u32(self.count)
		stream.u8(self.difficulty)


class SearchCoursesEventParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.option = 0
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		self.option = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.option)


class SearchCoursesLatestParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.option = 0
		self.range = common.ResultRange()
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		self.option = stream.u32()
		self.range = stream.extract(common.ResultRange)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.option)
		stream.add(self.range)


class SearchCoursesPointRankingParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.option = 0
		self.range = common.ResultRange()
		self.difficulty = None
		self.reject_regions = []
	
	def check_required(self, settings):
		for field in ['difficulty']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.option = stream.u32()
		self.range = stream.extract(common.ResultRange)
		self.difficulty = stream.u8()
		self.reject_regions = stream.list(stream.u8)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.option)
		stream.add(self.range)
		stream.u8(self.difficulty)
		stream.list(self.reject_regions, stream.u8)


class SearchUsersUserPointParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.option = 0
		self.buffer = None
		self.range = common.ResultRange()
	
	def check_required(self, settings):
		for field in ['buffer']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.option = stream.u32()
		self.buffer = stream.buffer()
		self.range = stream.extract(common.ResultRange)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.option)
		stream.buffer(self.buffer)
		stream.add(self.range)


class SyncUserProfileParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.username = None
		self.unk1 = UnknownStruct1()
		self.unk2 = None
		self.unk3 = None
		self.country = None
		self.unk4 = None
		self.unk5 = None
		self.unk_guid = None
		self.unk6 = None
	
	def check_required(self, settings):
		for field in ['username', 'unk2', 'unk3', 'country', 'unk4', 'unk5', 'unk_guid', 'unk6']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.username = stream.string()
		self.unk1 = stream.extract(UnknownStruct1)
		self.unk2 = stream.qbuffer()
		self.unk3 = stream.u8()
		self.country = stream.string()
		self.unk4 = stream.bool()
		self.unk5 = stream.bool()
		self.unk_guid = stream.string()
		self.unk6 = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.username)
		stream.add(self.unk1)
		stream.qbuffer(self.unk2)
		stream.u8(self.unk3)
		stream.string(self.country)
		stream.bool(self.unk4)
		stream.bool(self.unk5)
		stream.string(self.unk_guid)
		stream.u32(self.unk6)


class SyncUserProfileResult(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.username = None
		self.unk1 = UnknownStruct1()
		self.unk2 = None
		self.unk3 = None
		self.country = None
		self.unk4 = None
		self.unk5 = None
		self.unk6 = None
	
	def check_required(self, settings):
		for field in ['pid', 'username', 'unk2', 'unk3', 'country', 'unk4', 'unk5', 'unk6']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.pid = stream.u64()
		self.username = stream.string()
		self.unk1 = stream.extract(UnknownStruct1)
		self.unk2 = stream.qbuffer()
		self.unk3 = stream.u8()
		self.country = stream.string()
		self.unk4 = stream.u8()
		self.unk5 = stream.bool()
		self.unk6 = stream.bool()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.pid)
		stream.string(self.username)
		stream.add(self.unk1)
		stream.qbuffer(self.unk2)
		stream.u8(self.unk3)
		stream.string(self.country)
		stream.u8(self.unk4)
		stream.bool(self.unk5)
		stream.bool(self.unk6)


class UnknownStruct1(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
		self.unk3 = None
		self.unk4 = None
	
	def check_required(self, settings):
		for field in ['unk1', 'unk2', 'unk3', 'unk4']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk1 = stream.u16()
		self.unk2 = stream.u16()
		self.unk3 = stream.u16()
		self.unk4 = stream.u16()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u16(self.unk1)
		stream.u16(self.unk2)
		stream.u16(self.unk3)
		stream.u16(self.unk4)


class UnknownStruct3(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
	
	def check_required(self, settings):
		for field in ['unk1', 'unk2']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk1 = stream.bool()
		self.unk2 = stream.datetime()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.bool(self.unk1)
		stream.datetime(self.unk2)


class UnknownStruct6(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
	
	def check_required(self, settings):
		for field in ['unk1', 'unk2']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk1 = stream.u64()
		self.unk2 = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.unk1)
		stream.u32(self.unk2)


class UserInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.code = None
		self.name = None
		self.unk1 = UnknownStruct1()
		self.unk2 = None
		self.country = None
		self.region = None
		self.last_active = None
		self.unk3 = None
		self.unk4 = None
		self.unk5 = None
		self.play_stats = None
		self.maker_stats = None
		self.endless_challenge_high_scores = None
		self.multiplayer_stats = None
		self.unk7 = None
		self.badges = None
		self.unk8 = None
		self.unk9 = None
		self.unk10 = None
		self.unk11 = None
		self.unk12 = None
		self.unk13 = UnknownStruct3()
		self.unk14 = None
		self.unk15 = None
		self.unk16 = None
	
	def get_version(self, settings):
		version = 0
		version = 1
		version = 2
		version = 3
		return version
	
	def check_required(self, settings):
		for field in ['pid', 'code', 'name', 'unk2', 'country', 'region', 'last_active', 'unk3', 'unk4', 'unk5', 'play_stats', 'maker_stats', 'endless_challenge_high_scores', 'multiplayer_stats', 'unk7', 'badges', 'unk8', 'unk9', 'unk10', 'unk11', 'unk12', 'unk14', 'unk15', 'unk16']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.pid = stream.pid()
		self.code = stream.string()
		self.name = stream.string()
		self.unk1 = stream.extract(UnknownStruct1)
		self.unk2 = stream.qbuffer()
		self.country = stream.string()
		self.region = stream.u8()
		self.last_active = stream.datetime()
		self.unk3 = stream.bool()
		self.unk4 = stream.bool()
		self.unk5 = stream.bool()
		self.play_stats = stream.map(stream.u8, stream.u32)
		self.maker_stats = stream.map(stream.u8, stream.u32)
		self.endless_challenge_high_scores = stream.map(stream.u8, stream.u32)
		self.multiplayer_stats = stream.map(stream.u8, stream.u32)
		self.unk7 = stream.map(stream.u8, stream.u32)
		self.badges = stream.list(BadgeInfo)
		self.unk8 = stream.map(stream.u8, stream.u32)
		self.unk9 = stream.map(stream.u8, stream.u32)
		self.unk10 = stream.bool()
		self.unk11 = stream.datetime()
		self.unk12 = stream.bool()
		self.unk13 = stream.extract(UnknownStruct3)
		self.unk14 = stream.string()
		self.unk15 = stream.map(stream.u8, stream.u32)
		self.unk16 = stream.bool()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.pid)
		stream.string(self.code)
		stream.string(self.name)
		stream.add(self.unk1)
		stream.qbuffer(self.unk2)
		stream.string(self.country)
		stream.u8(self.region)
		stream.datetime(self.last_active)
		stream.bool(self.unk3)
		stream.bool(self.unk4)
		stream.bool(self.unk5)
		stream.map(self.play_stats, stream.u8, stream.u32)
		stream.map(self.maker_stats, stream.u8, stream.u32)
		stream.map(self.endless_challenge_high_scores, stream.u8, stream.u32)
		stream.map(self.multiplayer_stats, stream.u8, stream.u32)
		stream.map(self.unk7, stream.u8, stream.u32)
		stream.list(self.badges, stream.add)
		stream.map(self.unk8, stream.u8, stream.u32)
		stream.map(self.unk9, stream.u8, stream.u32)
		stream.bool(self.unk10)
		stream.datetime(self.unk11)
		stream.bool(self.unk12)
		stream.add(self.unk13)
		stream.string(self.unk14)
		stream.map(self.unk15, stream.u8, stream.u32)
		stream.bool(self.unk16)


class DataStoreProtocolSMM2:
	METHOD_PREPARE_GET_OBJECT_V1 = 1
	METHOD_PREPARE_POST_OBJECT_V1 = 2
	METHOD_COMPLETE_POST_OBJECT_V1 = 3
	METHOD_DELETE_OBJECT = 4
	METHOD_DELETE_OBJECTS = 5
	METHOD_CHANGE_META_V1 = 6
	METHOD_CHANGE_METAS_V1 = 7
	METHOD_GET_META = 8
	METHOD_GET_METAS = 9
	METHOD_PREPARE_UPDATE_OBJECT = 10
	METHOD_COMPLETE_UPDATE_OBJECT = 11
	METHOD_SEARCH_OBJECT = 12
	METHOD_GET_NOTIFICATION_URL = 13
	METHOD_GET_NEW_ARRIVED_NOTIFICATIONS_V1 = 14
	METHOD_RATE_OBJECT = 15
	METHOD_GET_RATING = 16
	METHOD_GET_RATINGS = 17
	METHOD_RESET_RATING = 18
	METHOD_RESET_RATINGS = 19
	METHOD_GET_SPECIFIC_META_V1 = 20
	METHOD_POST_META_BINARY = 21
	METHOD_TOUCH_OBJECT = 22
	METHOD_GET_RATING_WITH_LOG = 23
	METHOD_PREPARE_POST_OBJECT = 24
	METHOD_PREPARE_GET_OBJECT = 25
	METHOD_COMPLETE_POST_OBJECT = 26
	METHOD_GET_NEW_ARRIVED_NOTIFICATIONS = 27
	METHOD_GET_SPECIFIC_META = 28
	METHOD_GET_PERSISTENCE_INFO = 29
	METHOD_GET_PERSISTENCE_INFOS = 30
	METHOD_PERPETUATE_OBJECT = 31
	METHOD_UNPERPETUATE_OBJECT = 32
	METHOD_PREPARE_GET_OBJECT_OR_META = 33
	METHOD_GET_PASSWORD_INFO = 34
	METHOD_GET_PASSWORD_INFOS = 35
	METHOD_GET_METAS_MULTIPLE_PARAM = 36
	METHOD_COMPLETE_POST_OBJECTS = 37
	METHOD_CHANGE_META = 38
	METHOD_CHANGE_METAS = 39
	METHOD_RATE_OBJECTS = 40
	METHOD_POST_META_BINARY_WITH_DATA_ID = 41
	METHOD_POST_META_BINARIES_WITH_DATA_ID = 42
	METHOD_RATE_OBJECT_WITH_POSTING = 43
	METHOD_RATE_OBJECTS_WITH_POSTING = 44
	METHOD_GET_OBJECT_INFOS = 45
	METHOD_SEARCH_OBJECT_LIGHT = 46
	METHOD_REGISTER_USER = 47
	METHOD_GET_USERS = 48
	METHOD_SYNC_USER_PROFILE = 49
	METHOD_SEARCH_USERS_USER_POINT = 50
	METHOD_UPDATE_LAST_LOGIN_TIME = 59
	METHOD_GET_USERNAME_NG_TYPE = 65
	METHOD_GET_COURSES = 70
	METHOD_SEARCH_COURSES_POINT_RANKING = 71
	METHOD_SEARCH_COURSES_LATEST = 73
	METHOD_SEARCH_COURSES_ENDLESS_MODE = 79
	METHOD_GET_COURSES_EVENT = 85
	METHOD_SEARCH_COURSES_EVENT = 86
	METHOD_GET_COURSE_COMMENTS = 95
	METHOD_GET_USER_OR_COURSE = 131
	METHOD_GET_REQ_GET_INFO_HEADERS_INFO = 134
	METHOD_GET_EVENT_COURSE_STAMP = 153
	METHOD_GET_EVENT_COURSE_STATUS = 154
	METHOD_GET_EVENT_COURSE_HISTOGRAM = 156
	METHOD_GET_EVENT_COURSE_GHOST = 157
	
	PROTOCOL_ID = 0x73


class DataStoreClientSMM2(DataStoreProtocolSMM2):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def prepare_get_object_v1(self, param):
		logger.info("DataStoreClientSMM2.prepare_get_object_v1()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_PREPARE_GET_OBJECT_V1, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqGetInfoV1)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.prepare_get_object_v1 -> done")
		return info
	
	def get_meta(self, param):
		logger.info("DataStoreClientSMM2.get_meta()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_META, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreMetaInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_meta -> done")
		return info
	
	def prepare_post_object(self, param):
		logger.info("DataStoreClientSMM2.prepare_post_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_PREPARE_POST_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqPostInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.prepare_post_object -> done")
		return info
	
	def prepare_get_object(self, param):
		logger.info("DataStoreClientSMM2.prepare_get_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_PREPARE_GET_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqGetInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.prepare_get_object -> done")
		return info
	
	def complete_post_object(self, param):
		logger.info("DataStoreClientSMM2.complete_post_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_COMPLETE_POST_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.complete_post_object -> done")
	
	def get_password_info(self, data_id):
		logger.info("DataStoreClientSMM2.get_password_info()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(data_id)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_PASSWORD_INFO, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		password_info = stream.extract(DataStorePasswordInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_password_info -> done")
		return password_info
	
	def get_metas_multiple_param(self, params):
		logger.info("DataStoreClientSMM2.get_metas_multiple_param()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(params, stream.add)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_METAS_MULTIPLE_PARAM, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.infos = stream.list(DataStoreMetaInfo)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_metas_multiple_param -> done")
		return obj
	
	def register_user(self, param):
		logger.info("DataStoreClientSMM2.register_user()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_REGISTER_USER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.register_user -> done")
	
	def get_users(self, param):
		logger.info("DataStoreClientSMM2.get_users()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_USERS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.users = stream.list(UserInfo)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_users -> done")
		return obj
	
	def sync_user_profile(self, param):
		logger.info("DataStoreClientSMM2.sync_user_profile()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_SYNC_USER_PROFILE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.extract(SyncUserProfileResult)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.sync_user_profile -> done")
		return result
	
	def search_users_user_point(self, param):
		logger.info("DataStoreClientSMM2.search_users_user_point()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_SEARCH_USERS_USER_POINT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.users = stream.list(UserInfo)
		obj.ranks = stream.list(stream.u32)
		obj.result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.search_users_user_point -> done")
		return obj
	
	def update_last_login_time(self):
		logger.info("DataStoreClientSMM2.update_last_login_time()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_UPDATE_LAST_LOGIN_TIME, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.update_last_login_time -> done")
	
	def get_username_ng_type(self):
		logger.info("DataStoreClientSMM2.get_username_ng_type()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_USERNAME_NG_TYPE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		unk = stream.u8()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_username_ng_type -> done")
		return unk
	
	def get_courses(self, param):
		logger.info("DataStoreClientSMM2.get_courses()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_COURSES, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.courses = stream.list(CourseInfo)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_courses -> done")
		return obj
	
	def search_courses_point_ranking(self, param):
		logger.info("DataStoreClientSMM2.search_courses_point_ranking()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_SEARCH_COURSES_POINT_RANKING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.courses = stream.list(CourseInfo)
		obj.ranks = stream.list(stream.u32)
		obj.result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.search_courses_point_ranking -> done")
		return obj
	
	def search_courses_latest(self, param):
		logger.info("DataStoreClientSMM2.search_courses_latest()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_SEARCH_COURSES_LATEST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.courses = stream.list(CourseInfo)
		obj.result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.search_courses_latest -> done")
		return obj
	
	def search_courses_endless_mode(self, param):
		logger.info("DataStoreClientSMM2.search_courses_endless_mode()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_SEARCH_COURSES_ENDLESS_MODE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		courses = stream.list(CourseInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.search_courses_endless_mode -> done")
		return courses
	
	def get_courses_event(self, param, dummy):
		logger.info("DataStoreClientSMM2.get_courses_event()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		stream.add(dummy)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_COURSES_EVENT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.courses = stream.list(EventCourseInfo)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_courses_event -> done")
		return obj
	
	def search_courses_event(self, param):
		logger.info("DataStoreClientSMM2.search_courses_event()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_SEARCH_COURSES_EVENT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		courses = stream.list(EventCourseInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.search_courses_event -> done")
		return courses
	
	def get_course_comments(self, data_id):
		logger.info("DataStoreClientSMM2.get_course_comments()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(data_id)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_COURSE_COMMENTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		comments = stream.list(CommentInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_course_comments -> done")
		return comments
	
	def get_user_or_course(self, param):
		logger.info("DataStoreClientSMM2.get_user_or_course()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_USER_OR_COURSE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.user = stream.extract(UserInfo)
		obj.course = stream.extract(CourseInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_user_or_course -> done")
		return obj
	
	def get_req_get_info_headers_info(self, type):
		logger.info("DataStoreClientSMM2.get_req_get_info_headers_info()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u8(type)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_REQ_GET_INFO_HEADERS_INFO, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.extract(ReqGetInfoHeadersInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_req_get_info_headers_info -> done")
		return result
	
	def get_event_course_stamp(self):
		logger.info("DataStoreClientSMM2.get_event_course_stamp()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_EVENT_COURSE_STAMP, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		stamps = stream.u32()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_event_course_stamp -> done")
		return stamps
	
	def get_event_course_status(self):
		logger.info("DataStoreClientSMM2.get_event_course_status()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_EVENT_COURSE_STATUS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(EventCourseStatusInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_event_course_status -> done")
		return info
	
	def get_event_course_histogram(self, param):
		logger.info("DataStoreClientSMM2.get_event_course_histogram()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_EVENT_COURSE_HISTOGRAM, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		histogram = stream.extract(EventCourseHistogram)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_event_course_histogram -> done")
		return histogram
	
	def get_event_course_ghost(self, param):
		logger.info("DataStoreClientSMM2.get_event_course_ghost()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_EVENT_COURSE_GHOST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		ghosts = stream.list(EventCourseGhostInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM2.get_event_course_ghost -> done")
		return ghosts


class DataStoreServerSMM2(DataStoreProtocolSMM2):
	def __init__(self):
		self.methods = {
			self.METHOD_PREPARE_GET_OBJECT_V1: self.handle_prepare_get_object_v1,
			self.METHOD_PREPARE_POST_OBJECT_V1: self.handle_prepare_post_object_v1,
			self.METHOD_COMPLETE_POST_OBJECT_V1: self.handle_complete_post_object_v1,
			self.METHOD_DELETE_OBJECT: self.handle_delete_object,
			self.METHOD_DELETE_OBJECTS: self.handle_delete_objects,
			self.METHOD_CHANGE_META_V1: self.handle_change_meta_v1,
			self.METHOD_CHANGE_METAS_V1: self.handle_change_metas_v1,
			self.METHOD_GET_META: self.handle_get_meta,
			self.METHOD_GET_METAS: self.handle_get_metas,
			self.METHOD_PREPARE_UPDATE_OBJECT: self.handle_prepare_update_object,
			self.METHOD_COMPLETE_UPDATE_OBJECT: self.handle_complete_update_object,
			self.METHOD_SEARCH_OBJECT: self.handle_search_object,
			self.METHOD_GET_NOTIFICATION_URL: self.handle_get_notification_url,
			self.METHOD_GET_NEW_ARRIVED_NOTIFICATIONS_V1: self.handle_get_new_arrived_notifications_v1,
			self.METHOD_RATE_OBJECT: self.handle_rate_object,
			self.METHOD_GET_RATING: self.handle_get_rating,
			self.METHOD_GET_RATINGS: self.handle_get_ratings,
			self.METHOD_RESET_RATING: self.handle_reset_rating,
			self.METHOD_RESET_RATINGS: self.handle_reset_ratings,
			self.METHOD_GET_SPECIFIC_META_V1: self.handle_get_specific_meta_v1,
			self.METHOD_POST_META_BINARY: self.handle_post_meta_binary,
			self.METHOD_TOUCH_OBJECT: self.handle_touch_object,
			self.METHOD_GET_RATING_WITH_LOG: self.handle_get_rating_with_log,
			self.METHOD_PREPARE_POST_OBJECT: self.handle_prepare_post_object,
			self.METHOD_PREPARE_GET_OBJECT: self.handle_prepare_get_object,
			self.METHOD_COMPLETE_POST_OBJECT: self.handle_complete_post_object,
			self.METHOD_GET_NEW_ARRIVED_NOTIFICATIONS: self.handle_get_new_arrived_notifications,
			self.METHOD_GET_SPECIFIC_META: self.handle_get_specific_meta,
			self.METHOD_GET_PERSISTENCE_INFO: self.handle_get_persistence_info,
			self.METHOD_GET_PERSISTENCE_INFOS: self.handle_get_persistence_infos,
			self.METHOD_PERPETUATE_OBJECT: self.handle_perpetuate_object,
			self.METHOD_UNPERPETUATE_OBJECT: self.handle_unperpetuate_object,
			self.METHOD_PREPARE_GET_OBJECT_OR_META: self.handle_prepare_get_object_or_meta,
			self.METHOD_GET_PASSWORD_INFO: self.handle_get_password_info,
			self.METHOD_GET_PASSWORD_INFOS: self.handle_get_password_infos,
			self.METHOD_GET_METAS_MULTIPLE_PARAM: self.handle_get_metas_multiple_param,
			self.METHOD_COMPLETE_POST_OBJECTS: self.handle_complete_post_objects,
			self.METHOD_CHANGE_META: self.handle_change_meta,
			self.METHOD_CHANGE_METAS: self.handle_change_metas,
			self.METHOD_RATE_OBJECTS: self.handle_rate_objects,
			self.METHOD_POST_META_BINARY_WITH_DATA_ID: self.handle_post_meta_binary_with_data_id,
			self.METHOD_POST_META_BINARIES_WITH_DATA_ID: self.handle_post_meta_binaries_with_data_id,
			self.METHOD_RATE_OBJECT_WITH_POSTING: self.handle_rate_object_with_posting,
			self.METHOD_RATE_OBJECTS_WITH_POSTING: self.handle_rate_objects_with_posting,
			self.METHOD_GET_OBJECT_INFOS: self.handle_get_object_infos,
			self.METHOD_SEARCH_OBJECT_LIGHT: self.handle_search_object_light,
			self.METHOD_REGISTER_USER: self.handle_register_user,
			self.METHOD_GET_USERS: self.handle_get_users,
			self.METHOD_SYNC_USER_PROFILE: self.handle_sync_user_profile,
			self.METHOD_SEARCH_USERS_USER_POINT: self.handle_search_users_user_point,
			self.METHOD_UPDATE_LAST_LOGIN_TIME: self.handle_update_last_login_time,
			self.METHOD_GET_USERNAME_NG_TYPE: self.handle_get_username_ng_type,
			self.METHOD_GET_COURSES: self.handle_get_courses,
			self.METHOD_SEARCH_COURSES_POINT_RANKING: self.handle_search_courses_point_ranking,
			self.METHOD_SEARCH_COURSES_LATEST: self.handle_search_courses_latest,
			self.METHOD_SEARCH_COURSES_ENDLESS_MODE: self.handle_search_courses_endless_mode,
			self.METHOD_GET_COURSES_EVENT: self.handle_get_courses_event,
			self.METHOD_SEARCH_COURSES_EVENT: self.handle_search_courses_event,
			self.METHOD_GET_COURSE_COMMENTS: self.handle_get_course_comments,
			self.METHOD_GET_USER_OR_COURSE: self.handle_get_user_or_course,
			self.METHOD_GET_REQ_GET_INFO_HEADERS_INFO: self.handle_get_req_get_info_headers_info,
			self.METHOD_GET_EVENT_COURSE_STAMP: self.handle_get_event_course_stamp,
			self.METHOD_GET_EVENT_COURSE_STATUS: self.handle_get_event_course_status,
			self.METHOD_GET_EVENT_COURSE_HISTOGRAM: self.handle_get_event_course_histogram,
			self.METHOD_GET_EVENT_COURSE_GHOST: self.handle_get_event_course_ghost,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_prepare_get_object_v1(self, context, input, output):
		logger.info("DataStoreServerSMM2.prepare_get_object_v1()")
		#--- request ---
		param = input.extract(DataStorePrepareGetParamV1)
		response = self.prepare_get_object_v1(context, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqGetInfoV1):
			raise RuntimeError("Expected DataStoreReqGetInfoV1, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_prepare_post_object_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM2.prepare_post_object_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_complete_post_object_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM2.complete_post_object_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_delete_object(self, context, input, output):
		logger.warning("DataStoreServerSMM2.delete_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_delete_objects(self, context, input, output):
		logger.warning("DataStoreServerSMM2.delete_objects is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_change_meta_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM2.change_meta_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_change_metas_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM2.change_metas_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_meta(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_meta()")
		#--- request ---
		param = input.extract(DataStoreGetMetaParam)
		response = self.get_meta(context, param)
		
		#--- response ---
		if not isinstance(response, DataStoreMetaInfo):
			raise RuntimeError("Expected DataStoreMetaInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_metas(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_metas is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_prepare_update_object(self, context, input, output):
		logger.warning("DataStoreServerSMM2.prepare_update_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_complete_update_object(self, context, input, output):
		logger.warning("DataStoreServerSMM2.complete_update_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_search_object(self, context, input, output):
		logger.warning("DataStoreServerSMM2.search_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_notification_url(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_notification_url is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_new_arrived_notifications_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_new_arrived_notifications_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_rate_object(self, context, input, output):
		logger.warning("DataStoreServerSMM2.rate_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_rating(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_rating is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_ratings(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_ratings is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_reset_rating(self, context, input, output):
		logger.warning("DataStoreServerSMM2.reset_rating is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_reset_ratings(self, context, input, output):
		logger.warning("DataStoreServerSMM2.reset_ratings is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_specific_meta_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_specific_meta_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_post_meta_binary(self, context, input, output):
		logger.warning("DataStoreServerSMM2.post_meta_binary is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_touch_object(self, context, input, output):
		logger.warning("DataStoreServerSMM2.touch_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_rating_with_log(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_rating_with_log is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_prepare_post_object(self, context, input, output):
		logger.info("DataStoreServerSMM2.prepare_post_object()")
		#--- request ---
		param = input.extract(DataStorePreparePostParam)
		response = self.prepare_post_object(context, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqPostInfo):
			raise RuntimeError("Expected DataStoreReqPostInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_prepare_get_object(self, context, input, output):
		logger.info("DataStoreServerSMM2.prepare_get_object()")
		#--- request ---
		param = input.extract(DataStorePrepareGetParam)
		response = self.prepare_get_object(context, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqGetInfo):
			raise RuntimeError("Expected DataStoreReqGetInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_complete_post_object(self, context, input, output):
		logger.info("DataStoreServerSMM2.complete_post_object()")
		#--- request ---
		param = input.extract(DataStoreCompletePostParam)
		self.complete_post_object(context, param)
	
	def handle_get_new_arrived_notifications(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_new_arrived_notifications is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_specific_meta(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_specific_meta is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_persistence_info(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_persistence_info is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_persistence_infos(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_persistence_infos is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_perpetuate_object(self, context, input, output):
		logger.warning("DataStoreServerSMM2.perpetuate_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_unperpetuate_object(self, context, input, output):
		logger.warning("DataStoreServerSMM2.unperpetuate_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_prepare_get_object_or_meta(self, context, input, output):
		logger.warning("DataStoreServerSMM2.prepare_get_object_or_meta is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_password_info(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_password_info()")
		#--- request ---
		data_id = input.u64()
		response = self.get_password_info(context, data_id)
		
		#--- response ---
		if not isinstance(response, DataStorePasswordInfo):
			raise RuntimeError("Expected DataStorePasswordInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_password_infos(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_password_infos is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_metas_multiple_param(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_metas_multiple_param()")
		#--- request ---
		params = input.list(DataStoreGetMetaParam)
		response = self.get_metas_multiple_param(context, params)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['infos', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.infos, output.add)
		output.list(response.results, output.result)
	
	def handle_complete_post_objects(self, context, input, output):
		logger.warning("DataStoreServerSMM2.complete_post_objects is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_change_meta(self, context, input, output):
		logger.warning("DataStoreServerSMM2.change_meta is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_change_metas(self, context, input, output):
		logger.warning("DataStoreServerSMM2.change_metas is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_rate_objects(self, context, input, output):
		logger.warning("DataStoreServerSMM2.rate_objects is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_post_meta_binary_with_data_id(self, context, input, output):
		logger.warning("DataStoreServerSMM2.post_meta_binary_with_data_id is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_post_meta_binaries_with_data_id(self, context, input, output):
		logger.warning("DataStoreServerSMM2.post_meta_binaries_with_data_id is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_rate_object_with_posting(self, context, input, output):
		logger.warning("DataStoreServerSMM2.rate_object_with_posting is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_rate_objects_with_posting(self, context, input, output):
		logger.warning("DataStoreServerSMM2.rate_objects_with_posting is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_object_infos(self, context, input, output):
		logger.warning("DataStoreServerSMM2.get_object_infos is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_search_object_light(self, context, input, output):
		logger.warning("DataStoreServerSMM2.search_object_light is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_register_user(self, context, input, output):
		logger.info("DataStoreServerSMM2.register_user()")
		#--- request ---
		param = input.extract(RegisterUserParam)
		self.register_user(context, param)
	
	def handle_get_users(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_users()")
		#--- request ---
		param = input.extract(GetUsersParam)
		response = self.get_users(context, param)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['users', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.users, output.add)
		output.list(response.results, output.result)
	
	def handle_sync_user_profile(self, context, input, output):
		logger.info("DataStoreServerSMM2.sync_user_profile()")
		#--- request ---
		param = input.extract(SyncUserProfileParam)
		response = self.sync_user_profile(context, param)
		
		#--- response ---
		if not isinstance(response, SyncUserProfileResult):
			raise RuntimeError("Expected SyncUserProfileResult, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_search_users_user_point(self, context, input, output):
		logger.info("DataStoreServerSMM2.search_users_user_point()")
		#--- request ---
		param = input.extract(SearchUsersUserPointParam)
		response = self.search_users_user_point(context, param)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['users', 'ranks', 'result']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.users, output.add)
		output.list(response.ranks, output.u32)
		output.bool(response.result)
	
	def handle_update_last_login_time(self, context, input, output):
		logger.info("DataStoreServerSMM2.update_last_login_time()")
		#--- request ---
		self.update_last_login_time(context)
	
	def handle_get_username_ng_type(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_username_ng_type()")
		#--- request ---
		response = self.get_username_ng_type(context)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u8(response)
	
	def handle_get_courses(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_courses()")
		#--- request ---
		param = input.extract(GetCoursesParam)
		response = self.get_courses(context, param)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['courses', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.courses, output.add)
		output.list(response.results, output.result)
	
	def handle_search_courses_point_ranking(self, context, input, output):
		logger.info("DataStoreServerSMM2.search_courses_point_ranking()")
		#--- request ---
		param = input.extract(SearchCoursesPointRankingParam)
		response = self.search_courses_point_ranking(context, param)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['courses', 'ranks', 'result']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.courses, output.add)
		output.list(response.ranks, output.u32)
		output.bool(response.result)
	
	def handle_search_courses_latest(self, context, input, output):
		logger.info("DataStoreServerSMM2.search_courses_latest()")
		#--- request ---
		param = input.extract(SearchCoursesLatestParam)
		response = self.search_courses_latest(context, param)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['courses', 'result']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.courses, output.add)
		output.bool(response.result)
	
	def handle_search_courses_endless_mode(self, context, input, output):
		logger.info("DataStoreServerSMM2.search_courses_endless_mode()")
		#--- request ---
		param = input.extract(SearchCoursesEndlessModeParam)
		response = self.search_courses_endless_mode(context, param)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	def handle_get_courses_event(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_courses_event()")
		#--- request ---
		param = input.extract(GetCoursesParam)
		dummy = input.extract(GetCoursesEventParam)
		response = self.get_courses_event(context, param, dummy)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['courses', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.courses, output.add)
		output.list(response.results, output.result)
	
	def handle_search_courses_event(self, context, input, output):
		logger.info("DataStoreServerSMM2.search_courses_event()")
		#--- request ---
		param = input.extract(SearchCoursesEventParam)
		response = self.search_courses_event(context, param)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	def handle_get_course_comments(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_course_comments()")
		#--- request ---
		data_id = input.u64()
		response = self.get_course_comments(context, data_id)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	def handle_get_user_or_course(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_user_or_course()")
		#--- request ---
		param = input.extract(GetUserOrCourseParam)
		response = self.get_user_or_course(context, param)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['user', 'course']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.add(response.user)
		output.add(response.course)
	
	def handle_get_req_get_info_headers_info(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_req_get_info_headers_info()")
		#--- request ---
		type = input.u8()
		response = self.get_req_get_info_headers_info(context, type)
		
		#--- response ---
		if not isinstance(response, ReqGetInfoHeadersInfo):
			raise RuntimeError("Expected ReqGetInfoHeadersInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_event_course_stamp(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_event_course_stamp()")
		#--- request ---
		response = self.get_event_course_stamp(context)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u32(response)
	
	def handle_get_event_course_status(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_event_course_status()")
		#--- request ---
		response = self.get_event_course_status(context)
		
		#--- response ---
		if not isinstance(response, EventCourseStatusInfo):
			raise RuntimeError("Expected EventCourseStatusInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_event_course_histogram(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_event_course_histogram()")
		#--- request ---
		param = input.extract(GetEventCourseHistogramParam)
		response = self.get_event_course_histogram(context, param)
		
		#--- response ---
		if not isinstance(response, EventCourseHistogram):
			raise RuntimeError("Expected EventCourseHistogram, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_event_course_ghost(self, context, input, output):
		logger.info("DataStoreServerSMM2.get_event_course_ghost()")
		#--- request ---
		param = input.extract(GetEventCourseGhostParam)
		response = self.get_event_course_ghost(context, param)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	def prepare_get_object_v1(self, *args):
		logger.warning("DataStoreServerSMM2.prepare_get_object_v1 not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_meta(self, *args):
		logger.warning("DataStoreServerSMM2.get_meta not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def prepare_post_object(self, *args):
		logger.warning("DataStoreServerSMM2.prepare_post_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def prepare_get_object(self, *args):
		logger.warning("DataStoreServerSMM2.prepare_get_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def complete_post_object(self, *args):
		logger.warning("DataStoreServerSMM2.complete_post_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_password_info(self, *args):
		logger.warning("DataStoreServerSMM2.get_password_info not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_metas_multiple_param(self, *args):
		logger.warning("DataStoreServerSMM2.get_metas_multiple_param not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def register_user(self, *args):
		logger.warning("DataStoreServerSMM2.register_user not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_users(self, *args):
		logger.warning("DataStoreServerSMM2.get_users not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def sync_user_profile(self, *args):
		logger.warning("DataStoreServerSMM2.sync_user_profile not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def search_users_user_point(self, *args):
		logger.warning("DataStoreServerSMM2.search_users_user_point not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def update_last_login_time(self, *args):
		logger.warning("DataStoreServerSMM2.update_last_login_time not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_username_ng_type(self, *args):
		logger.warning("DataStoreServerSMM2.get_username_ng_type not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_courses(self, *args):
		logger.warning("DataStoreServerSMM2.get_courses not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def search_courses_point_ranking(self, *args):
		logger.warning("DataStoreServerSMM2.search_courses_point_ranking not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def search_courses_latest(self, *args):
		logger.warning("DataStoreServerSMM2.search_courses_latest not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def search_courses_endless_mode(self, *args):
		logger.warning("DataStoreServerSMM2.search_courses_endless_mode not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_courses_event(self, *args):
		logger.warning("DataStoreServerSMM2.get_courses_event not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def search_courses_event(self, *args):
		logger.warning("DataStoreServerSMM2.search_courses_event not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_course_comments(self, *args):
		logger.warning("DataStoreServerSMM2.get_course_comments not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_user_or_course(self, *args):
		logger.warning("DataStoreServerSMM2.get_user_or_course not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_req_get_info_headers_info(self, *args):
		logger.warning("DataStoreServerSMM2.get_req_get_info_headers_info not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_event_course_stamp(self, *args):
		logger.warning("DataStoreServerSMM2.get_event_course_stamp not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_event_course_status(self, *args):
		logger.warning("DataStoreServerSMM2.get_event_course_status not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_event_course_histogram(self, *args):
		logger.warning("DataStoreServerSMM2.get_event_course_histogram not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_event_course_ghost(self, *args):
		logger.warning("DataStoreServerSMM2.get_event_course_ghost not implemented")
		raise common.RMCError("Core::NotImplemented")

