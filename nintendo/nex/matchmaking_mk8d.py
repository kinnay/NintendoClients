
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class MatchmakeSystem:
	GLOBAL = 1
	FRIENDS = 2


class SimpleSearchConditionOperator:
	ANY = 0
	EQUAL = 1
	GREATER_THAN = 2
	LESS_THAN = 3
	GREATER_THAN_OR_EQUAL = 4
	LESS_THAN_OR_EQUAL = 5


class Gathering(common.Structure):
	def __init__(self):
		super().__init__()
		self.id = 0
		self.owner = 0
		self.host = 0
		self.min_participants = 0
		self.max_participants = 0
		self.participation_policy = 1
		self.policy_argument = 0
		self.flags = 512
		self.state = 0
		self.description = ""
	
	def check_required(self, settings, version):
		pass
	
	def load(self, stream, version):
		self.id = stream.u32()
		self.owner = stream.pid()
		self.host = stream.pid()
		self.min_participants = stream.u16()
		self.max_participants = stream.u16()
		self.participation_policy = stream.u32()
		self.policy_argument = stream.u32()
		self.flags = stream.u32()
		self.state = stream.u32()
		self.description = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.id)
		stream.pid(self.owner)
		stream.pid(self.host)
		stream.u16(self.min_participants)
		stream.u16(self.max_participants)
		stream.u32(self.participation_policy)
		stream.u32(self.policy_argument)
		stream.u32(self.flags)
		stream.u32(self.state)
		stream.string(self.description)


class GatheringURLs(common.Structure):
	def __init__(self):
		super().__init__()
		self.gid = None
		self.urls = None
	
	def check_required(self, settings, version):
		for field in ['gid', 'urls']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.gid = stream.u32()
		self.urls = stream.list(stream.stationurl)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.gid)
		stream.list(self.urls, stream.stationurl)


class GatheringStats(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.flags = None
		self.values = None
	
	def check_required(self, settings, version):
		for field in ['pid', 'flags', 'values']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.pid = stream.pid()
		self.flags = stream.u32()
		self.values = stream.list(stream.float)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.pid)
		stream.u32(self.flags)
		stream.list(self.values, stream.float)


class Invitation(common.Structure):
	def __init__(self):
		super().__init__()
		self.gid = None
		self.guest = None
		self.message = None
	
	def check_required(self, settings, version):
		for field in ['gid', 'guest', 'message']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.gid = stream.u32()
		self.guest = stream.u32()
		self.message = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.gid)
		stream.u32(self.guest)
		stream.string(self.message)


class ParticipantDetails(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.name = None
		self.message = None
		self.participants = None
	
	def check_required(self, settings, version):
		for field in ['pid', 'name', 'message', 'participants']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.pid = stream.pid()
		self.name = stream.string()
		self.message = stream.string()
		self.participants = stream.u16()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.pid)
		stream.string(self.name)
		stream.string(self.message)
		stream.u16(self.participants)


class DeletionEntry(common.Structure):
	def __init__(self):
		super().__init__()
		self.gid = None
		self.pid = None
		self.reason = None
	
	def check_required(self, settings, version):
		for field in ['gid', 'pid', 'reason']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.gid = stream.u32()
		self.pid = stream.pid()
		self.reason = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.gid)
		stream.pid(self.pid)
		stream.u32(self.reason)


class MatchmakeParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.param = {}
	
	def check_required(self, settings, version):
		pass
	
	def load(self, stream, version):
		self.param = stream.map(stream.string, stream.variant)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.map(self.param, stream.string, stream.variant)


class MatchmakeSessionSearchCriteria(common.Structure):
	def __init__(self):
		super().__init__()
		self.attribs = ["", "", "", "", "", ""]
		self.game_mode = ""
		self.min_participants = ""
		self.max_participants = ""
		self.matchmake_system = ""
		self.vacant_only = True
		self.exclude_locked = True
		self.exclude_non_host_pid = False
		self.selection_method = 0
		self.vacant_participants = 1
		self.param = MatchmakeParam()
		self.exclude_user_password = False
		self.exclude_system_password = False
		self.refer_gid = 0
		self.codeword = ""
		self.range = common.ResultRange()
	
	def check_required(self, settings, version):
		if settings["nex.version"] >= 30500:
			pass
		if settings["nex.version"] >= 40000:
			pass
	
	def load(self, stream, version):
		self.attribs = stream.list(stream.string)
		self.game_mode = stream.string()
		self.min_participants = stream.string()
		self.max_participants = stream.string()
		self.matchmake_system = stream.string()
		self.vacant_only = stream.bool()
		self.exclude_locked = stream.bool()
		self.exclude_non_host_pid = stream.bool()
		self.selection_method = stream.u32()
		if stream.settings["nex.version"] >= 30500:
			self.vacant_participants = stream.u16()
		if stream.settings["nex.version"] >= 40000:
			self.param = stream.extract(MatchmakeParam)
			self.exclude_user_password = stream.bool()
			self.exclude_system_password = stream.bool()
			self.refer_gid = stream.u32()
			self.codeword = stream.string()
			self.range = stream.extract(common.ResultRange)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.list(self.attribs, stream.string)
		stream.string(self.game_mode)
		stream.string(self.min_participants)
		stream.string(self.max_participants)
		stream.string(self.matchmake_system)
		stream.bool(self.vacant_only)
		stream.bool(self.exclude_locked)
		stream.bool(self.exclude_non_host_pid)
		stream.u32(self.selection_method)
		if stream.settings["nex.version"] >= 30500:
			stream.u16(self.vacant_participants)
		if stream.settings["nex.version"] >= 40000:
			stream.add(self.param)
			stream.bool(self.exclude_user_password)
			stream.bool(self.exclude_system_password)
			stream.u32(self.refer_gid)
			stream.string(self.codeword)
			stream.add(self.range)


class MatchmakeSession(Gathering):
	def __init__(self):
		super().__init__()
		self.game_mode = 0
		self.attribs = [0, 0, 0, 0, 0, 0]
		self.open_participation = True
		self.matchmake_system = 0
		self.application_data = b""
		self.num_participants = 0
		self.progress_score = 100
		self.session_key = b""
		self.option = 0
		self.param = MatchmakeParam()
		self.started_time = common.DateTime(0)
		self.user_password = ""
		self.refer_gid = 0
		self.user_password_enabled = False
		self.system_password_enabled = False
		self.codeword = ""
	
	def max_version(self, settings):
		version = 0
		if settings["nex.version"] >= 30600:
			version = 1
		if settings["nex.version"] >= 30700:
			version = 2
		if settings["nex.version"] >= 30800:
			version = 3
		if settings["nex.version"] >= 40000:
			version = 0
		return version
	
	def check_required(self, settings, version):
		if settings["nex.version"] >= 30500:
			pass
		if settings["nex.version"] >= 30000:
			pass
		if settings["nex.version"] >= 30500:
			pass
		if settings["nex.version"] >= 30600:
			if version >= 1:
				pass
		if settings["nex.version"] >= 30700:
			if version >= 2:
				pass
		if settings["nex.version"] >= 30800:
			if version >= 3:
				pass
		if settings["nex.version"] >= 40000:
			if version >= 0:
				pass
	
	def load(self, stream, version):
		self.game_mode = stream.u32()
		self.attribs = stream.list(stream.u32)
		self.open_participation = stream.bool()
		self.matchmake_system = stream.u32()
		self.application_data = stream.buffer()
		self.num_participants = stream.u32()
		if stream.settings["nex.version"] >= 30500:
			self.progress_score = stream.u8()
		if stream.settings["nex.version"] >= 30000:
			self.session_key = stream.buffer()
		if stream.settings["nex.version"] >= 30500:
			self.option = stream.u32()
		if stream.settings["nex.version"] >= 30600:
			if version >= 1:
				self.param = stream.extract(MatchmakeParam)
				self.started_time = stream.datetime()
		if stream.settings["nex.version"] >= 30700:
			if version >= 2:
				self.user_password = stream.string()
		if stream.settings["nex.version"] >= 30800:
			if version >= 3:
				self.refer_gid = stream.u32()
				self.user_password_enabled = stream.bool()
				self.system_password_enabled = stream.bool()
		if stream.settings["nex.version"] >= 40000:
			if version >= 0:
				self.codeword = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.game_mode)
		stream.list(self.attribs, stream.u32)
		stream.bool(self.open_participation)
		stream.u32(self.matchmake_system)
		stream.buffer(self.application_data)
		stream.u32(self.num_participants)
		if stream.settings["nex.version"] >= 30500:
			stream.u8(self.progress_score)
		if stream.settings["nex.version"] >= 30000:
			stream.buffer(self.session_key)
		if stream.settings["nex.version"] >= 30500:
			stream.u32(self.option)
		if stream.settings["nex.version"] >= 30600:
			if version >= 1:
				stream.add(self.param)
				stream.datetime(self.started_time)
		if stream.settings["nex.version"] >= 30700:
			if version >= 2:
				stream.string(self.user_password)
		if stream.settings["nex.version"] >= 30800:
			if version >= 3:
				stream.u32(self.refer_gid)
				stream.bool(self.user_password_enabled)
				stream.bool(self.system_password_enabled)
		if stream.settings["nex.version"] >= 40000:
			if version >= 0:
				stream.string(self.codeword)
common.DataHolder.register(MatchmakeSession, "MatchmakeSession")


class MatchmakeBlockListParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.options = 0
	
	def check_required(self, settings, version):
		pass
	
	def load(self, stream, version):
		self.options = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.options)


class CreateMatchmakeSessionParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.session = MatchmakeSession()
		self.additional_participants = None
		self.gid_for_participation_check = None
		self.options = None
		self.join_message = None
		self.num_participants = None
	
	def check_required(self, settings, version):
		for field in ['additional_participants', 'gid_for_participation_check', 'options', 'join_message', 'num_participants']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.session = stream.extract(MatchmakeSession)
		self.additional_participants = stream.list(stream.pid)
		self.gid_for_participation_check = stream.u32()
		self.options = stream.u32()
		self.join_message = stream.string()
		self.num_participants = stream.u16()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.add(self.session)
		stream.list(self.additional_participants, stream.pid)
		stream.u32(self.gid_for_participation_check)
		stream.u32(self.options)
		stream.string(self.join_message)
		stream.u16(self.num_participants)


class JoinMatchmakeSessionParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.gid = None
		self.participants = None
		self.gid_for_participation_check = None
		self.options = None
		self.behavior = None
		self.user_password = None
		self.system_password = None
		self.join_message = None
		self.num_participants = None
		self.extra_participants = None
		self.block_list = MatchmakeBlockListParam()
	
	def check_required(self, settings, version):
		for field in ['gid', 'participants', 'gid_for_participation_check', 'options', 'behavior', 'user_password', 'system_password', 'join_message', 'num_participants', 'extra_participants']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.gid = stream.u32()
		self.participants = stream.list(stream.pid)
		self.gid_for_participation_check = stream.u32()
		self.options = stream.u32()
		self.behavior = stream.u8()
		self.user_password = stream.string()
		self.system_password = stream.string()
		self.join_message = stream.string()
		self.num_participants = stream.u16()
		self.extra_participants = stream.u16()
		self.block_list = stream.extract(MatchmakeBlockListParam)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.gid)
		stream.list(self.participants, stream.pid)
		stream.u32(self.gid_for_participation_check)
		stream.u32(self.options)
		stream.u8(self.behavior)
		stream.string(self.user_password)
		stream.string(self.system_password)
		stream.string(self.join_message)
		stream.u16(self.num_participants)
		stream.u16(self.extra_participants)
		stream.add(self.block_list)


class UpdateMatchmakeSessionParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.gid = None
		self.modification_flags = None
		self.attributes = None
		self.open_participation = None
		self.application_buffer = None
		self.progress_score = None
		self.param = MatchmakeParam()
		self.started_time = None
		self.user_password = None
		self.game_mode = None
		self.description = None
		self.min_participants = None
		self.max_participants = None
		self.matchmake_system = None
		self.participation_policy = None
		self.policy_argument = None
		self.codeword = None
	
	def check_required(self, settings, version):
		for field in ['gid', 'modification_flags', 'attributes', 'open_participation', 'application_buffer', 'progress_score', 'started_time', 'user_password', 'game_mode', 'description', 'min_participants', 'max_participants', 'matchmake_system', 'participation_policy', 'policy_argument', 'codeword']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.gid = stream.u32()
		self.modification_flags = stream.u32()
		self.attributes = stream.list(stream.u32)
		self.open_participation = stream.bool()
		self.application_buffer = stream.buffer()
		self.progress_score = stream.u8()
		self.param = stream.extract(MatchmakeParam)
		self.started_time = stream.datetime()
		self.user_password = stream.string()
		self.game_mode = stream.u32()
		self.description = stream.string()
		self.min_participants = stream.u16()
		self.max_participants = stream.u16()
		self.matchmake_system = stream.u32()
		self.participation_policy = stream.u32()
		self.policy_argument = stream.u32()
		self.codeword = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.gid)
		stream.u32(self.modification_flags)
		stream.list(self.attributes, stream.u32)
		stream.bool(self.open_participation)
		stream.buffer(self.application_buffer)
		stream.u8(self.progress_score)
		stream.add(self.param)
		stream.datetime(self.started_time)
		stream.string(self.user_password)
		stream.u32(self.game_mode)
		stream.string(self.description)
		stream.u16(self.min_participants)
		stream.u16(self.max_participants)
		stream.u32(self.matchmake_system)
		stream.u32(self.participation_policy)
		stream.u32(self.policy_argument)
		stream.string(self.codeword)


class AutoMatchmakeParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.session = MatchmakeSession()
		self.participants = None
		self.gid_for_participation_check = None
		self.options = None
		self.join_message = None
		self.num_participants = None
		self.search_criteria = None
		self.target_gids = None
		self.block_list = MatchmakeBlockListParam()
	
	def check_required(self, settings, version):
		for field in ['participants', 'gid_for_participation_check', 'options', 'join_message', 'num_participants', 'search_criteria', 'target_gids']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.session = stream.extract(MatchmakeSession)
		self.participants = stream.list(stream.pid)
		self.gid_for_participation_check = stream.u32()
		self.options = stream.u32()
		self.join_message = stream.string()
		self.num_participants = stream.u16()
		self.search_criteria = stream.list(MatchmakeSessionSearchCriteria)
		self.target_gids = stream.list(stream.u32)
		self.block_list = stream.extract(MatchmakeBlockListParam)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.add(self.session)
		stream.list(self.participants, stream.pid)
		stream.u32(self.gid_for_participation_check)
		stream.u32(self.options)
		stream.string(self.join_message)
		stream.u16(self.num_participants)
		stream.list(self.search_criteria, stream.add)
		stream.list(self.target_gids, stream.u32)
		stream.add(self.block_list)


class FindMatchmakeSessionByParticipantParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.pids = None
		self.options = None
		self.block_list = MatchmakeBlockListParam()
	
	def check_required(self, settings, version):
		for field in ['pids', 'options']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.pids = stream.list(stream.pid)
		self.options = stream.u32()
		self.block_list = stream.extract(MatchmakeBlockListParam)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.list(self.pids, stream.pid)
		stream.u32(self.options)
		stream.add(self.block_list)


class FindMatchmakeSessionByParticipantResult(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.session = MatchmakeSession()
	
	def check_required(self, settings, version):
		for field in ['pid']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.pid = stream.pid()
		self.session = stream.extract(MatchmakeSession)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.pid)
		stream.add(self.session)


class PersistentGathering(Gathering):
	def __init__(self):
		super().__init__()
		self.type = None
		self.password = None
		self.attribs = None
		self.application_buffer = None
		self.participation_start = None
		self.participation_end = None
		self.matchmake_session_count = None
		self.num_participants = None
	
	def check_required(self, settings, version):
		for field in ['type', 'password', 'attribs', 'application_buffer', 'participation_start', 'participation_end', 'matchmake_session_count', 'num_participants']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.type = stream.u32()
		self.password = stream.string()
		self.attribs = stream.list(stream.u32)
		self.application_buffer = stream.buffer()
		self.participation_start = stream.datetime()
		self.participation_end = stream.datetime()
		self.matchmake_session_count = stream.u32()
		self.num_participants = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.type)
		stream.string(self.password)
		stream.list(self.attribs, stream.u32)
		stream.buffer(self.application_buffer)
		stream.datetime(self.participation_start)
		stream.datetime(self.participation_end)
		stream.u32(self.matchmake_session_count)
		stream.u32(self.num_participants)
common.DataHolder.register(PersistentGathering, "PersistentGathering")


class SimpleCommunity(common.Structure):
	def __init__(self):
		super().__init__()
		self.gid = None
		self.matchmake_session_count = None
	
	def check_required(self, settings, version):
		for field in ['gid', 'matchmake_session_count']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.gid = stream.u32()
		self.matchmake_session_count = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.gid)
		stream.u32(self.matchmake_session_count)


class PlayingSession(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.gathering = None
	
	def check_required(self, settings, version):
		for field in ['pid', 'gathering']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.pid = stream.pid()
		self.gathering = stream.anydata()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.pid)
		stream.anydata(self.gathering)


class SimplePlayingSession(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.gid = None
		self.game_mode = None
		self.attribute = None
	
	def check_required(self, settings, version):
		for field in ['pid', 'gid', 'game_mode', 'attribute']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.pid = stream.pid()
		self.gid = stream.u32()
		self.game_mode = stream.u32()
		self.attribute = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.pid)
		stream.u32(self.gid)
		stream.u32(self.game_mode)
		stream.u32(self.attribute)


class MatchmakeRefereeRound(common.Structure):
	def __init__(self):
		super().__init__()
		self.id = None
		self.gid = None
		self.state = None
		self.personal_data_category = None
		self.results = None
	
	def check_required(self, settings, version):
		for field in ['id', 'gid', 'state', 'personal_data_category', 'results']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.id = stream.u64()
		self.gid = stream.u32()
		self.state = stream.u32()
		self.personal_data_category = stream.u32()
		self.results = stream.list(MatchmakeRefereePersonalRoundResult)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.id)
		stream.u32(self.gid)
		stream.u32(self.state)
		stream.u32(self.personal_data_category)
		stream.list(self.results, stream.add)


class MatchmakeRefereeStartRoundParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.personal_data_category = None
		self.gid = None
		self.pids = None
	
	def check_required(self, settings, version):
		for field in ['personal_data_category', 'gid', 'pids']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.personal_data_category = stream.u32()
		self.gid = stream.u32()
		self.pids = stream.list(stream.pid)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.personal_data_category)
		stream.u32(self.gid)
		stream.list(self.pids, stream.pid)


class MatchmakeRefereeEndRoundParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.round_id = None
		self.results = None
	
	def check_required(self, settings, version):
		for field in ['round_id', 'results']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.round_id = stream.u64()
		self.results = stream.list(MatchmakeRefereePersonalRoundResult)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.round_id)
		stream.list(self.results, stream.add)


class MatchmakeRefereePersonalRoundResult(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.personal_round_result_flag = None
		self.round_win_loss = None
		self.rating_change = None
		self.buffer = None
	
	def check_required(self, settings, version):
		for field in ['pid', 'personal_round_result_flag', 'round_win_loss', 'rating_change', 'buffer']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.pid = stream.pid()
		self.personal_round_result_flag = stream.u32()
		self.round_win_loss = stream.u32()
		self.rating_change = stream.s32()
		self.buffer = stream.qbuffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.pid)
		stream.u32(self.personal_round_result_flag)
		stream.u32(self.round_win_loss)
		stream.s32(self.rating_change)
		stream.qbuffer(self.buffer)


class MatchmakeRefereeStats(common.Structure):
	def __init__(self):
		super().__init__()
		self.unique_id = None
		self.category = None
		self.pid = None
		self.recent_disconnection = None
		self.recent_violation = None
		self.recent_mismatch = None
		self.recent_win = None
		self.recent_loss = None
		self.recent_draw = None
		self.total_disconnect = None
		self.total_violation = None
		self.total_mismatch = None
		self.total_win = None
		self.total_loss = None
		self.total_draw = None
		self.rating_value = None
	
	def check_required(self, settings, version):
		for field in ['unique_id', 'category', 'pid', 'recent_disconnection', 'recent_violation', 'recent_mismatch', 'recent_win', 'recent_loss', 'recent_draw', 'total_disconnect', 'total_violation', 'total_mismatch', 'total_win', 'total_loss', 'total_draw', 'rating_value']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.unique_id = stream.u64()
		self.category = stream.u32()
		self.pid = stream.pid()
		self.recent_disconnection = stream.u32()
		self.recent_violation = stream.u32()
		self.recent_mismatch = stream.u32()
		self.recent_win = stream.u32()
		self.recent_loss = stream.u32()
		self.recent_draw = stream.u32()
		self.total_disconnect = stream.u32()
		self.total_violation = stream.u32()
		self.total_mismatch = stream.u32()
		self.total_win = stream.u32()
		self.total_loss = stream.u32()
		self.total_draw = stream.u32()
		self.rating_value = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.unique_id)
		stream.u32(self.category)
		stream.pid(self.pid)
		stream.u32(self.recent_disconnection)
		stream.u32(self.recent_violation)
		stream.u32(self.recent_mismatch)
		stream.u32(self.recent_win)
		stream.u32(self.recent_loss)
		stream.u32(self.recent_draw)
		stream.u32(self.total_disconnect)
		stream.u32(self.total_violation)
		stream.u32(self.total_mismatch)
		stream.u32(self.total_win)
		stream.u32(self.total_loss)
		stream.u32(self.total_draw)
		stream.u32(self.rating_value)


class MatchmakeRefereeStatsTarget(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.category = None
	
	def check_required(self, settings, version):
		for field in ['pid', 'category']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.pid = stream.pid()
		self.category = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.pid)
		stream.u32(self.category)


class MatchmakeRefereeStatsInitParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.category = None
		self.initial_rating = None
	
	def check_required(self, settings, version):
		for field in ['category', 'initial_rating']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.category = stream.u32()
		self.initial_rating = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.category)
		stream.u32(self.initial_rating)


class SimpleSearchObject(common.Structure):
	def __init__(self):
		super().__init__()
		self.id = None
		self.owner = None
		self.attributes = None
		self.metadata = None
		self.community_id = None
		self.community_code = None
		self.datetime = SimpleSearchDateTimeAttribute()
		self.unk3 = None
		self.unk4 = None
	
	def max_version(self, settings):
		version = 0
		if settings["nex.version"] >= 40000:
			version = 1
		return version
	
	def check_required(self, settings, version):
		for field in ['id', 'owner', 'attributes', 'metadata', 'community_id', 'community_code']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings["nex.version"] >= 40000:
			if version >= 1:
				for field in ['unk3', 'unk4']:
					if getattr(self, field) is None:
						raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.id = stream.u32()
		self.owner = stream.pid()
		self.attributes = stream.list(stream.u32)
		self.metadata = stream.qbuffer()
		self.community_id = stream.u32()
		self.community_code = stream.string()
		self.datetime = stream.extract(SimpleSearchDateTimeAttribute)
		if stream.settings["nex.version"] >= 40000:
			if version >= 1:
				self.unk3 = stream.u32()
				self.unk4 = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.id)
		stream.pid(self.owner)
		stream.list(self.attributes, stream.u32)
		stream.qbuffer(self.metadata)
		stream.u32(self.community_id)
		stream.string(self.community_code)
		stream.add(self.datetime)
		if stream.settings["nex.version"] >= 40000:
			if version >= 1:
				stream.u32(self.unk3)
				stream.datetime(self.unk4)


class SimpleSearchDateTimeAttribute(common.Structure):
	def __init__(self):
		super().__init__()
		self.start_daytime = None
		self.end_daytime = None
		self.start_time = None
		self.end_time = None
		self.start_datetime = None
		self.end_datetime = None
	
	def check_required(self, settings, version):
		for field in ['start_daytime', 'end_daytime', 'start_time', 'end_time', 'start_datetime', 'end_datetime']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.start_daytime = stream.u32()
		self.end_daytime = stream.u32()
		self.start_time = stream.u32()
		self.end_time = stream.u32()
		self.start_datetime = stream.datetime()
		self.end_datetime = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.start_daytime)
		stream.u32(self.end_daytime)
		stream.u32(self.start_time)
		stream.u32(self.end_time)
		stream.datetime(self.start_datetime)
		stream.datetime(self.end_datetime)


class SimpleSearchParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.id = 0
		self.owner = 0
		self.conditions = []
		self.community_code = ""
		self.range = common.ResultRange()
		self.datetime = common.DateTime(0)
	
	def check_required(self, settings, version):
		pass
	
	def load(self, stream, version):
		self.id = stream.u32()
		self.owner = stream.pid()
		self.conditions = stream.list(SimpleSearchCondition)
		self.community_code = stream.string()
		self.range = stream.extract(common.ResultRange)
		self.datetime = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.id)
		stream.pid(self.owner)
		stream.list(self.conditions, stream.add)
		stream.string(self.community_code)
		stream.add(self.range)
		stream.datetime(self.datetime)


class SimpleSearchCondition(common.Structure):
	def __init__(self):
		super().__init__()
		self.value = None
		self.operator = None
	
	def check_required(self, settings, version):
		for field in ['value', 'operator']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.value = stream.u32()
		self.operator = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.value)
		stream.u32(self.operator)


class MatchMakingProtocol:
	METHOD_REGISTER_GATHERING = 1
	METHOD_UNREGISTER_GATHERING = 2
	METHOD_UNREGISTER_GATHERINGS = 3
	METHOD_UPDATE_GATHERING = 4
	METHOD_INVITE = 5
	METHOD_ACCEPT_INVITATION = 6
	METHOD_DECLINE_INVITATION = 7
	METHOD_CANCEL_INVITATION = 8
	METHOD_GET_INVITATIONS_SENT = 9
	METHOD_GET_INVITATIONS_RECEIVED = 10
	METHOD_PARTICIPATE = 11
	METHOD_CANCEL_PARTICIPATION = 12
	METHOD_GET_PARTICIPANTS = 13
	METHOD_ADD_PARTICIPANTS = 14
	METHOD_GET_DETAILED_PARTICIPANTS = 15
	METHOD_GET_PARTICIPANTS_URLS = 16
	METHOD_FIND_BY_TYPE = 17
	METHOD_FIND_BY_DESCRIPTION = 18
	METHOD_FIND_BY_DESCRIPTION_REGEX = 19
	METHOD_FIND_BY_ID = 20
	METHOD_FIND_BY_SINGLE_ID = 21
	METHOD_FIND_BY_OWNER = 22
	METHOD_FIND_BY_PARTICIPANTS = 23
	METHOD_FIND_INVITATIONS = 24
	METHOD_FIND_BY_SQL_QUERY = 25
	METHOD_LAUNCH_SESSION = 26
	METHOD_UPDATE_SESSION_URL = 27
	METHOD_GET_SESSION_URL = 28
	METHOD_GET_STATE = 29
	METHOD_SET_STATE = 30
	METHOD_REPORT_STATS = 31
	METHOD_GET_STATS = 32
	METHOD_DELETE_GATHERING = 33
	METHOD_GET_PENDING_DELETIONS = 34
	METHOD_DELETE_FROM_DELETIONS = 35
	METHOD_MIGRATE_GATHERING_OWNERSHIP_V1 = 36
	METHOD_FIND_BY_DESCRIPTION_LIKE = 37
	METHOD_REGISTER_LOCAL_URL = 38
	METHOD_REGISTER_LOCAL_URLS = 39
	METHOD_UPDATE_SESSION_HOST_V1 = 40
	METHOD_GET_SESSION_URLS = 41
	METHOD_UPDATE_SESSION_HOST = 42
	METHOD_UPDATE_GATHERING_OWNERSHIP = 43
	METHOD_MIGRATE_GATHERING_OWNERSHIP = 44
	
	PROTOCOL_ID = 0x15


class MatchMakingProtocolExt:
	METHOD_END_PARTICIPATION = 1
	METHOD_GET_PARTICIPANTS = 2
	METHOD_GET_DETAILED_PARTICIPANTS = 3
	METHOD_GET_PARTICIPANTS_URLS = 4
	METHOD_GET_GATHERING_RELATIONS = 5
	METHOD_DELETE_FROM_DELETIONS = 6
	
	PROTOCOL_ID = 0x32


class MatchmakeRefereeProtocol:
	METHOD_START_ROUND = 1
	METHOD_GET_START_ROUND_PARAM = 2
	METHOD_END_ROUND = 3
	METHOD_END_ROUND_WITHOUT_REPORT = 4
	METHOD_GET_ROUND_PARTICIPANTS = 5
	METHOD_GET_NOT_SUMMARIZED_ROUND = 6
	METHOD_GET_ROUND = 7
	METHOD_GET_STATS_PRIMARY = 8
	METHOD_GET_STATS_PRIMARIES = 9
	METHOD_GET_STATS_ALL = 10
	METHOD_CREATE_STATS = 11
	METHOD_GET_OR_CREATE_STATS = 12
	METHOD_RESET_STATS = 13
	
	PROTOCOL_ID = 0x78


class MatchmakeExtensionProtocolMK8D:
	METHOD_CLOSE_PARTICIPATION = 1
	METHOD_OPEN_PARTICIPATION = 2
	METHOD_AUTO_MATCHMAKE_POSTPONE = 3
	METHOD_BROWSE_MATCHMAKE_SESSION = 4
	METHOD_BROWSE_MATCHMAKE_SESSION_WITH_HOST_URLS = 5
	METHOD_CREATE_MATCHMAKE_SESSION = 6
	METHOD_JOIN_MATCHMAKE_SESSION = 7
	METHOD_MODIFY_CURRENT_GAME_ATTRIBUTE = 8
	METHOD_UPDATE_NOTIFICATION_DATA = 9
	METHOD_GET_FRIEND_NOTIFICATION_DATA = 10
	METHOD_UPDATE_APPLICATION_BUFFER = 11
	METHOD_UPDATE_MATCHMAKE_SESSION_ATTRIBUTE = 12
	METHOD_GET_FRIEND_NOTIFICATION_DATA_LIST = 13
	METHOD_UPDATE_MATCHMAKE_SESSION = 14
	METHOD_AUTO_MATCHMAKE_WITH_SEARCH_CRITERIA_POSTPONE = 15
	METHOD_GET_PLAYING_SESSION = 16
	METHOD_CREATE_COMMUNITY = 17
	METHOD_UPDATE_COMMUNITY = 18
	METHOD_JOIN_COMMUNITY = 19
	METHOD_FIND_COMMUNITY_BY_GATHERING_ID = 20
	METHOD_FIND_OFFICIAL_COMMUNITY = 21
	METHOD_FIND_COMMUNITY_BY_PARTICIPANT = 22
	METHOD_UPDATE_PRIVACY_SETTING = 23
	METHOD_GET_MY_BLOCK_LIST = 24
	METHOD_ADD_TO_BLOCK_LIST = 25
	METHOD_REMOVE_FROM_BLOCK_LIST = 26
	METHOD_CLEAR_MY_BLOCK_LIST = 27
	METHOD_REPORT_VIOLATION = 28
	METHOD_IS_VIOLATION_USER = 29
	METHOD_JOIN_MATCHMAKE_SESSION_EX = 30
	METHOD_GET_SIMPLE_PLAYING_SESSION = 31
	METHOD_GET_SIMPLE_COMMUNITY = 32
	METHOD_AUTO_MATCHMAKE_WITH_GATHERING_ID_POSTPONE = 33
	METHOD_UPDATE_PROGRESS_SCORE = 34
	METHOD_DEBUG_NOTIFY_EVENT = 35
	METHOD_GENERATE_MATCHMAKE_SESSION_SYSTEM_PASSWORD = 36
	METHOD_CLEAR_MATCHMAKE_SESSION_SYSTEM_PASSWORD = 37
	METHOD_CREATE_MATCHMAKE_SESSION_WITH_PARAM = 38
	METHOD_JOIN_MATCHMAKE_SESSION_WITH_PARAM = 39
	METHOD_AUTO_MATCHMAKE_WITH_PARAM_POSTPONE = 40
	METHOD_FIND_MATCHMAKE_SESSION_BY_GATHERING_ID_DETAIL = 41
	METHOD_BROWSE_MATCHMAKE_SESSION_NO_HOLDER = 42
	METHOD_BROWSE_MATCHMAKE_SESSION_WITH_HOST_URLS_NO_HOLDER = 43
	METHOD_UPDATE_MATCHMAKE_SESSION_PART = 44
	METHOD_REQUEST_MATCHMAKING = 45
	METHOD_WITHDRAW_MATCHMAKING = 46
	METHOD_WITHDRAW_MATCHMAKING_ALL = 47
	METHOD_FIND_MATCHMAKE_SESSION_BY_GATHERING_ID = 48
	METHOD_FIND_MATCHMAKE_SESSION_BY_SINGLE_GATHERING_ID = 49
	METHOD_FIND_MATCHMAKE_SESSION_BY_OWNER = 50
	METHOD_FIND_MATCHMAKE_SESSION_BY_PARTICIPANT = 51
	METHOD_BROWSE_MATCHMAKE_SESSION_NO_HOLDER_NO_RESULT_RANGE = 52
	METHOD_BROWSE_MATCHMAKE_SESSION_WITH_HOST_URLS_NO_HOLDER_NO_RESULT_RANGE = 53
	METHOD_CREATE_SIMPLE_SEARCH_OBJECT = 54
	METHOD_UPDATE_SIMPLE_SEARCH_OBJECT = 55
	METHOD_DELETE_SIMPLE_SEARCH_OBJECT = 56
	METHOD_SEARCH_SIMPLE_SEARCH_OBJECT = 57
	METHOD_SEARCH_SIMPLE_SEARCH_OBJECT_BY_OBJECT_IDS = 58
	METHOD_JOIN_MATCHMAKE_SESSION_WITH_EXTRA_PARTICIPANTS = 59
	METHOD_CUSTOM_GET_SIMPLE_PLAYING_SESSION = 60
	METHOD_CREATE_COMPETITION = 61
	METHOD_DELETE_COMPETITION = 62
	METHOD_REGISTER_FAVORITE_COMPETITION = 63
	METHOD_UNREGISTER_FAVORITE_COMPETITION = 64
	METHOD_GET_FAVORITE_COMPETITION = 65
	METHOD_GET_TEAM_PARTICIPANTS = 66
	METHOD_FIND_COMMUNITY_BY_OWNER = 67
	
	PROTOCOL_ID = 0x6D


class MatchMakingClient(MatchMakingProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def register_gathering(self, gathering):
		logger.info("MatchMakingClient.register_gathering()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.anydata(gathering)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REGISTER_GATHERING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gid = stream.u32()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.register_gathering -> done")
		return gid
	
	async def unregister_gathering(self, gid):
		logger.info("MatchMakingClient.unregister_gathering()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UNREGISTER_GATHERING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.unregister_gathering -> done")
		return result
	
	async def unregister_gatherings(self, gids):
		logger.info("MatchMakingClient.unregister_gatherings()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(gids, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UNREGISTER_GATHERINGS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.unregister_gatherings -> done")
		return result
	
	async def update_gathering(self, gathering):
		logger.info("MatchMakingClient.update_gathering()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.anydata(gathering)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_GATHERING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.update_gathering -> done")
		return result
	
	async def invite(self, gid, pids, message):
		logger.info("MatchMakingClient.invite()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.list(pids, stream.pid)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_INVITE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.invite -> done")
		return result
	
	async def accept_invitation(self, gid, message):
		logger.info("MatchMakingClient.accept_invitation()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_ACCEPT_INVITATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.accept_invitation -> done")
		return result
	
	async def decline_invitation(self, gid, message):
		logger.info("MatchMakingClient.decline_invitation()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DECLINE_INVITATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.decline_invitation -> done")
		return result
	
	async def cancel_invitation(self, gid, pids, message):
		logger.info("MatchMakingClient.cancel_invitation()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.list(pids, stream.pid)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CANCEL_INVITATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.cancel_invitation -> done")
		return result
	
	async def get_invitations_sent(self, gid):
		logger.info("MatchMakingClient.get_invitations_sent()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_INVITATIONS_SENT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		invitations = stream.list(Invitation)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.get_invitations_sent -> done")
		return invitations
	
	async def get_invitations_received(self):
		logger.info("MatchMakingClient.get_invitations_received()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_INVITATIONS_RECEIVED, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		invitations = stream.list(Invitation)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.get_invitations_received -> done")
		return invitations
	
	async def participate(self, gid, message):
		logger.info("MatchMakingClient.participate()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PARTICIPATE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.participate -> done")
		return result
	
	async def cancel_participation(self, gid, message):
		logger.info("MatchMakingClient.cancel_participation()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CANCEL_PARTICIPATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.cancel_participation -> done")
		return result
	
	async def get_participants(self, gid):
		logger.info("MatchMakingClient.get_participants()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PARTICIPANTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		participants = stream.list(stream.pid)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.get_participants -> done")
		return participants
	
	async def add_participants(self, gid, pids, message):
		logger.info("MatchMakingClient.add_participants()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.list(pids, stream.pid)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_ADD_PARTICIPANTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.add_participants -> done")
		return result
	
	async def get_detailed_participants(self, gid):
		logger.info("MatchMakingClient.get_detailed_participants()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_DETAILED_PARTICIPANTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		details = stream.list(ParticipantDetails)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.get_detailed_participants -> done")
		return details
	
	async def get_participants_urls(self, gid):
		logger.info("MatchMakingClient.get_participants_urls()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PARTICIPANTS_URLS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		urls = stream.list(stream.stationurl)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.get_participants_urls -> done")
		return urls
	
	async def find_by_type(self, type, range):
		logger.info("MatchMakingClient.find_by_type()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(type)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_BY_TYPE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_by_type -> done")
		return gatherings
	
	async def find_by_description(self, description, range):
		logger.info("MatchMakingClient.find_by_description()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(description)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_BY_DESCRIPTION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_by_description -> done")
		return gatherings
	
	async def find_by_description_regex(self, regex, range):
		logger.info("MatchMakingClient.find_by_description_regex()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(regex)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_BY_DESCRIPTION_REGEX, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_by_description_regex -> done")
		return gatherings
	
	async def find_by_id(self, ids):
		logger.info("MatchMakingClient.find_by_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(ids, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_BY_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_by_id -> done")
		return gatherings
	
	async def find_by_single_id(self, gid):
		logger.info("MatchMakingClient.find_by_single_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_BY_SINGLE_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.bool()
		obj.gathering = stream.anydata()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_by_single_id -> done")
		return obj
	
	async def find_by_owner(self, owner, range):
		logger.info("MatchMakingClient.find_by_owner()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(owner)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_BY_OWNER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_by_owner -> done")
		return gatherings
	
	async def find_by_participants(self, pids):
		logger.info("MatchMakingClient.find_by_participants()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_BY_PARTICIPANTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_by_participants -> done")
		return gatherings
	
	async def find_invitations(self, range):
		logger.info("MatchMakingClient.find_invitations()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_INVITATIONS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_invitations -> done")
		return gatherings
	
	async def find_by_sql_query(self, query, range):
		logger.info("MatchMakingClient.find_by_sql_query()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(query)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_BY_SQL_QUERY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_by_sql_query -> done")
		return gatherings
	
	async def launch_session(self, gid, url):
		logger.info("MatchMakingClient.launch_session()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(url)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_LAUNCH_SESSION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.launch_session -> done")
		return result
	
	async def update_session_url(self, gid, url):
		logger.info("MatchMakingClient.update_session_url()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(url)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_SESSION_URL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.update_session_url -> done")
		return result
	
	async def get_session_url(self, gid):
		logger.info("MatchMakingClient.get_session_url()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_SESSION_URL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.bool()
		obj.url = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.get_session_url -> done")
		return obj
	
	async def get_state(self, gid):
		logger.info("MatchMakingClient.get_state()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_STATE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.bool()
		obj.state = stream.u32()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.get_state -> done")
		return obj
	
	async def set_state(self, gid, state):
		logger.info("MatchMakingClient.set_state()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.u32(state)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_SET_STATE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.set_state -> done")
		return result
	
	async def report_stats(self, gid, stats):
		logger.info("MatchMakingClient.report_stats()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.list(stats, stream.add)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REPORT_STATS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.report_stats -> done")
		return result
	
	async def get_stats(self, gid, pids, columns):
		logger.info("MatchMakingClient.get_stats()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.list(pids, stream.pid)
		stream.list(columns, stream.u8)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_STATS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.bool()
		obj.stats = stream.list(GatheringStats)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.get_stats -> done")
		return obj
	
	async def delete_gathering(self, gid):
		logger.info("MatchMakingClient.delete_gathering()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_GATHERING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.delete_gathering -> done")
		return result
	
	async def get_pending_deletions(self, reason, range):
		logger.info("MatchMakingClient.get_pending_deletions()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(reason)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PENDING_DELETIONS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.bool()
		obj.deletions = stream.list(DeletionEntry)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.get_pending_deletions -> done")
		return obj
	
	async def delete_from_deletions(self, deletions):
		logger.info("MatchMakingClient.delete_from_deletions()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(deletions, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_FROM_DELETIONS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.delete_from_deletions -> done")
		return result
	
	async def migrate_gathering_ownership_v1(self, gid, potential_owners):
		logger.info("MatchMakingClient.migrate_gathering_ownership_v1()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.list(potential_owners, stream.pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_MIGRATE_GATHERING_OWNERSHIP_V1, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.migrate_gathering_ownership_v1 -> done")
		return result
	
	async def find_by_description_like(self, description, range):
		logger.info("MatchMakingClient.find_by_description_like()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(description)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_BY_DESCRIPTION_LIKE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_by_description_like -> done")
		return gatherings
	
	async def register_local_url(self, gid, url):
		logger.info("MatchMakingClient.register_local_url()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.stationurl(url)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REGISTER_LOCAL_URL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.register_local_url -> done")
	
	async def register_local_urls(self, gid, urls):
		logger.info("MatchMakingClient.register_local_urls()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.list(urls, stream.stationurl)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REGISTER_LOCAL_URLS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.register_local_urls -> done")
	
	async def update_session_host_v1(self, gid):
		logger.info("MatchMakingClient.update_session_host_v1()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_SESSION_HOST_V1, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.update_session_host_v1 -> done")
	
	async def get_session_urls(self, gid):
		logger.info("MatchMakingClient.get_session_urls()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_SESSION_URLS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		urls = stream.list(stream.stationurl)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.get_session_urls -> done")
		return urls
	
	async def update_session_host(self, gid, is_migrate_owner):
		logger.info("MatchMakingClient.update_session_host()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.bool(is_migrate_owner)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_SESSION_HOST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.update_session_host -> done")
	
	async def update_gathering_ownership(self, gid, participants_only):
		logger.info("MatchMakingClient.update_gathering_ownership()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.bool(participants_only)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_GATHERING_OWNERSHIP, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.update_gathering_ownership -> done")
		return result
	
	async def migrate_gathering_ownership(self, gid, potential_owners, participants_only):
		logger.info("MatchMakingClient.migrate_gathering_ownership()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.list(potential_owners, stream.pid)
		stream.bool(participants_only)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_MIGRATE_GATHERING_OWNERSHIP, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.migrate_gathering_ownership -> done")


class MatchMakingClientExt(MatchMakingProtocolExt):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def end_participation(self, gid, message):
		logger.info("MatchMakingClientExt.end_participation()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_END_PARTICIPATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClientExt.end_participation -> done")
		return result
	
	async def get_participants(self, gid, only_active):
		logger.info("MatchMakingClientExt.get_participants()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.bool(only_active)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PARTICIPANTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		participants = stream.list(stream.pid)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClientExt.get_participants -> done")
		return participants
	
	async def get_detailed_participants(self, gid, only_active):
		logger.info("MatchMakingClientExt.get_detailed_participants()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.bool(only_active)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_DETAILED_PARTICIPANTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		details = stream.list(ParticipantDetails)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClientExt.get_detailed_participants -> done")
		return details
	
	async def get_participants_urls(self, gids):
		logger.info("MatchMakingClientExt.get_participants_urls()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(gids, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PARTICIPANTS_URLS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		urls = stream.list(GatheringURLs)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClientExt.get_participants_urls -> done")
		return urls
	
	async def get_gathering_relations(self, id, descr):
		logger.info("MatchMakingClientExt.get_gathering_relations()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(id)
		stream.string(descr)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_GATHERING_RELATIONS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClientExt.get_gathering_relations -> done")
		return result
	
	async def delete_from_deletions(self, deletions, pid):
		logger.info("MatchMakingClientExt.delete_from_deletions()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(deletions, stream.u32)
		stream.pid(pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_FROM_DELETIONS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClientExt.delete_from_deletions -> done")


class MatchmakeRefereeClient(MatchmakeRefereeProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def start_round(self, param):
		logger.info("MatchmakeRefereeClient.start_round()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_START_ROUND, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		round_id = stream.u64()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.start_round -> done")
		return round_id
	
	async def get_start_round_param(self, round_id):
		logger.info("MatchmakeRefereeClient.get_start_round_param()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(round_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_START_ROUND_PARAM, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		param = stream.extract(MatchmakeRefereeStartRoundParam)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.get_start_round_param -> done")
		return param
	
	async def end_round(self, param):
		logger.info("MatchmakeRefereeClient.end_round()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_END_ROUND, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.end_round -> done")
	
	async def end_round_without_report(self, round_id):
		logger.info("MatchmakeRefereeClient.end_round_without_report()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(round_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_END_ROUND_WITHOUT_REPORT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.end_round_without_report -> done")
	
	async def get_round_participants(self, round_id):
		logger.info("MatchmakeRefereeClient.get_round_participants()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(round_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_ROUND_PARTICIPANTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		pids = stream.list(stream.pid)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.get_round_participants -> done")
		return pids
	
	async def get_not_summarized_round(self):
		logger.info("MatchmakeRefereeClient.get_not_summarized_round()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_NOT_SUMMARIZED_ROUND, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		rounds = stream.list(MatchmakeRefereeRound)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.get_not_summarized_round -> done")
		return rounds
	
	async def get_round(self, round):
		logger.info("MatchmakeRefereeClient.get_round()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(round)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_ROUND, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		round = stream.extract(MatchmakeRefereeRound)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.get_round -> done")
		return round
	
	async def get_stats_primary(self, target):
		logger.info("MatchmakeRefereeClient.get_stats_primary()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(target)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_STATS_PRIMARY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		stats = stream.extract(MatchmakeRefereeStats)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.get_stats_primary -> done")
		return stats
	
	async def get_stats_primaries(self, targets):
		logger.info("MatchmakeRefereeClient.get_stats_primaries()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(targets, stream.add)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_STATS_PRIMARIES, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.stats = stream.list(MatchmakeRefereeStats)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.get_stats_primaries -> done")
		return obj
	
	async def get_stats_all(self, target):
		logger.info("MatchmakeRefereeClient.get_stats_all()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(target)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_STATS_ALL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		stats = stream.list(MatchmakeRefereeStats)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.get_stats_all -> done")
		return stats
	
	async def create_stats(self, param):
		logger.info("MatchmakeRefereeClient.create_stats()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CREATE_STATS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		stats = stream.extract(MatchmakeRefereeStats)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.create_stats -> done")
		return stats
	
	async def get_or_create_stats(self, param):
		logger.info("MatchmakeRefereeClient.get_or_create_stats()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_OR_CREATE_STATS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		stats = stream.extract(MatchmakeRefereeStats)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.get_or_create_stats -> done")
		return stats
	
	async def reset_stats(self):
		logger.info("MatchmakeRefereeClient.reset_stats()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_RESET_STATS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeRefereeClient.reset_stats -> done")


class MatchmakeExtensionClientMK8D(MatchmakeExtensionProtocolMK8D):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def close_participation(self, gid):
		logger.info("MatchmakeExtensionClientMK8D.close_participation()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CLOSE_PARTICIPATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.close_participation -> done")
	
	async def open_participation(self, gid):
		logger.info("MatchmakeExtensionClientMK8D.open_participation()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_OPEN_PARTICIPATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.open_participation -> done")
	
	async def auto_matchmake_postpone(self, gathering, message):
		logger.info("MatchmakeExtensionClientMK8D.auto_matchmake_postpone()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.anydata(gathering)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_AUTO_MATCHMAKE_POSTPONE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gathering = stream.anydata()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.auto_matchmake_postpone -> done")
		return gathering
	
	async def browse_matchmake_session(self, search_criteria, range):
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(search_criteria)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_BROWSE_MATCHMAKE_SESSION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session -> done")
		return gatherings
	
	async def browse_matchmake_session_with_host_urls(self, search_criteria, range):
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session_with_host_urls()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(search_criteria)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_BROWSE_MATCHMAKE_SESSION_WITH_HOST_URLS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.gatherings = stream.list(stream.anydata)
		obj.urls = stream.list(GatheringURLs)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session_with_host_urls -> done")
		return obj
	
	async def create_matchmake_session(self, gathering, description, num_participants):
		logger.info("MatchmakeExtensionClientMK8D.create_matchmake_session()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.anydata(gathering)
		stream.string(description)
		stream.u16(num_participants)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CREATE_MATCHMAKE_SESSION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.gid = stream.u32()
		obj.session_key = stream.buffer()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.create_matchmake_session -> done")
		return obj
	
	async def join_matchmake_session(self, gid, message):
		logger.info("MatchmakeExtensionClientMK8D.join_matchmake_session()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_JOIN_MATCHMAKE_SESSION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session_key = stream.buffer()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.join_matchmake_session -> done")
		return session_key
	
	async def modify_current_game_attribute(self, gid, attrib, value):
		logger.info("MatchmakeExtensionClientMK8D.modify_current_game_attribute()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.u32(attrib)
		stream.u32(value)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_MODIFY_CURRENT_GAME_ATTRIBUTE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.modify_current_game_attribute -> done")
	
	async def update_notification_data(self, type, param1, param2, param3):
		logger.info("MatchmakeExtensionClientMK8D.update_notification_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(type)
		stream.pid(param1)
		stream.pid(param2)
		stream.string(param3)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_NOTIFICATION_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.update_notification_data -> done")
	
	async def get_friend_notification_data(self, type):
		logger.info("MatchmakeExtensionClientMK8D.get_friend_notification_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.s32(type)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_FRIEND_NOTIFICATION_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		notifications = stream.list(notification.NotificationEvent)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.get_friend_notification_data -> done")
		return notifications
	
	async def update_application_buffer(self, gid, buffer):
		logger.info("MatchmakeExtensionClientMK8D.update_application_buffer()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.buffer(buffer)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_APPLICATION_BUFFER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.update_application_buffer -> done")
	
	async def update_matchmake_session_attribute(self, gid, attribs):
		logger.info("MatchmakeExtensionClientMK8D.update_matchmake_session_attribute()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.list(attribs, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_MATCHMAKE_SESSION_ATTRIBUTE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.update_matchmake_session_attribute -> done")
	
	async def get_friend_notification_data_list(self, types):
		logger.info("MatchmakeExtensionClientMK8D.get_friend_notification_data_list()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(types, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_FRIEND_NOTIFICATION_DATA_LIST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		notifications = stream.list(notification.NotificationEvent)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.get_friend_notification_data_list -> done")
		return notifications
	
	async def update_matchmake_session(self, gathering):
		logger.info("MatchmakeExtensionClientMK8D.update_matchmake_session()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.anydata(gathering)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_MATCHMAKE_SESSION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.update_matchmake_session -> done")
	
	async def auto_matchmake_with_search_criteria_postpone(self, search_criteria, gathering, message):
		logger.info("MatchmakeExtensionClientMK8D.auto_matchmake_with_search_criteria_postpone()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(search_criteria, stream.add)
		stream.anydata(gathering)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_AUTO_MATCHMAKE_WITH_SEARCH_CRITERIA_POSTPONE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gathering = stream.anydata()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.auto_matchmake_with_search_criteria_postpone -> done")
		return gathering
	
	async def get_playing_session(self, pids):
		logger.info("MatchmakeExtensionClientMK8D.get_playing_session()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PLAYING_SESSION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		sessions = stream.list(PlayingSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.get_playing_session -> done")
		return sessions
	
	async def create_community(self, community, message):
		logger.info("MatchmakeExtensionClientMK8D.create_community()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(community)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CREATE_COMMUNITY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gid = stream.u32()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.create_community -> done")
		return gid
	
	async def update_community(self, community):
		logger.info("MatchmakeExtensionClientMK8D.update_community()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(community)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_COMMUNITY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.update_community -> done")
	
	async def join_community(self, gid, message, password):
		logger.info("MatchmakeExtensionClientMK8D.join_community()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(message)
		stream.string(password)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_JOIN_COMMUNITY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.join_community -> done")
	
	async def find_community_by_gathering_id(self, gids):
		logger.info("MatchmakeExtensionClientMK8D.find_community_by_gathering_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(gids, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_COMMUNITY_BY_GATHERING_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		communities = stream.list(PersistentGathering)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.find_community_by_gathering_id -> done")
		return communities
	
	async def find_official_community(self, available_only, range):
		logger.info("MatchmakeExtensionClientMK8D.find_official_community()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.bool(available_only)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_OFFICIAL_COMMUNITY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		communities = stream.list(PersistentGathering)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.find_official_community -> done")
		return communities
	
	async def find_community_by_participant(self, pid, range):
		logger.info("MatchmakeExtensionClientMK8D.find_community_by_participant()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_COMMUNITY_BY_PARTICIPANT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		communities = stream.list(PersistentGathering)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.find_community_by_participant -> done")
		return communities
	
	async def update_privacy_setting(self, online_status, community_participation):
		logger.info("MatchmakeExtensionClientMK8D.update_privacy_setting()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.bool(online_status)
		stream.bool(community_participation)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_PRIVACY_SETTING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.update_privacy_setting -> done")
	
	async def get_my_block_list(self):
		logger.info("MatchmakeExtensionClientMK8D.get_my_block_list()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_MY_BLOCK_LIST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		pids = stream.list(stream.pid)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.get_my_block_list -> done")
		return pids
	
	async def add_to_block_list(self, pids):
		logger.info("MatchmakeExtensionClientMK8D.add_to_block_list()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_ADD_TO_BLOCK_LIST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.add_to_block_list -> done")
	
	async def remove_from_block_list(self, pids):
		logger.info("MatchmakeExtensionClientMK8D.remove_from_block_list()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REMOVE_FROM_BLOCK_LIST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.remove_from_block_list -> done")
	
	async def clear_my_block_list(self):
		logger.info("MatchmakeExtensionClientMK8D.clear_my_block_list()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CLEAR_MY_BLOCK_LIST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.clear_my_block_list -> done")
	
	async def report_violation(self, pid, username, violation_code):
		logger.info("MatchmakeExtensionClientMK8D.report_violation()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		stream.string(username)
		stream.u32(violation_code)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REPORT_VIOLATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.report_violation -> done")
	
	async def is_violation_user(self):
		logger.info("MatchmakeExtensionClientMK8D.is_violation_user()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_IS_VIOLATION_USER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.flag = stream.bool()
		obj.score = stream.u32()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.is_violation_user -> done")
		return obj
	
	async def join_matchmake_session_ex(self, gid, gmessage, ignore_block_list, num_participants):
		logger.info("MatchmakeExtensionClientMK8D.join_matchmake_session_ex()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(gmessage)
		stream.bool(ignore_block_list)
		stream.u16(num_participants)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_JOIN_MATCHMAKE_SESSION_EX, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session_key = stream.buffer()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.join_matchmake_session_ex -> done")
		return session_key
	
	async def get_simple_playing_session(self, pids, include_login_user):
		logger.info("MatchmakeExtensionClientMK8D.get_simple_playing_session()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		stream.bool(include_login_user)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_SIMPLE_PLAYING_SESSION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session = stream.list(SimplePlayingSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.get_simple_playing_session -> done")
		return session
	
	async def get_simple_community(self, gids):
		logger.info("MatchmakeExtensionClientMK8D.get_simple_community()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(gids, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_SIMPLE_COMMUNITY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		communities = stream.list(SimpleCommunity)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.get_simple_community -> done")
		return communities
	
	async def auto_matchmake_with_gathering_id_postpone(self, gids, gathering, message):
		logger.info("MatchmakeExtensionClientMK8D.auto_matchmake_with_gathering_id_postpone()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(gids, stream.u32)
		stream.anydata(gathering)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_AUTO_MATCHMAKE_WITH_GATHERING_ID_POSTPONE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		joined_gathering = stream.anydata()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.auto_matchmake_with_gathering_id_postpone -> done")
		return joined_gathering
	
	async def update_progress_score(self, gid, score):
		logger.info("MatchmakeExtensionClientMK8D.update_progress_score()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.u8(score)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_PROGRESS_SCORE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.update_progress_score -> done")
	
	async def debug_notify_event(self, pid, main_type, sub_type, param1, param2, param3):
		logger.info("MatchmakeExtensionClientMK8D.debug_notify_event()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		stream.u32(main_type)
		stream.u32(sub_type)
		stream.u64(param1)
		stream.u64(param2)
		stream.string(param3)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DEBUG_NOTIFY_EVENT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.debug_notify_event -> done")
	
	async def generate_matchmake_session_system_password(self, gid):
		logger.info("MatchmakeExtensionClientMK8D.generate_matchmake_session_system_password()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GENERATE_MATCHMAKE_SESSION_SYSTEM_PASSWORD, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		password = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.generate_matchmake_session_system_password -> done")
		return password
	
	async def clear_matchmake_session_system_password(self, gid):
		logger.info("MatchmakeExtensionClientMK8D.clear_matchmake_session_system_password()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CLEAR_MATCHMAKE_SESSION_SYSTEM_PASSWORD, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.clear_matchmake_session_system_password -> done")
	
	async def create_matchmake_session_with_param(self, param):
		logger.info("MatchmakeExtensionClientMK8D.create_matchmake_session_with_param()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CREATE_MATCHMAKE_SESSION_WITH_PARAM, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session = stream.extract(MatchmakeSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.create_matchmake_session_with_param -> done")
		return session
	
	async def join_matchmake_session_with_param(self, param):
		logger.info("MatchmakeExtensionClientMK8D.join_matchmake_session_with_param()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_JOIN_MATCHMAKE_SESSION_WITH_PARAM, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session = stream.extract(MatchmakeSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.join_matchmake_session_with_param -> done")
		return session
	
	async def auto_matchmake_with_param_postpone(self, param):
		logger.info("MatchmakeExtensionClientMK8D.auto_matchmake_with_param_postpone()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_AUTO_MATCHMAKE_WITH_PARAM_POSTPONE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session = stream.extract(MatchmakeSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.auto_matchmake_with_param_postpone -> done")
		return session
	
	async def find_matchmake_session_by_gathering_id_detail(self, gid):
		logger.info("MatchmakeExtensionClientMK8D.find_matchmake_session_by_gathering_id_detail()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_MATCHMAKE_SESSION_BY_GATHERING_ID_DETAIL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session = stream.extract(MatchmakeSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.find_matchmake_session_by_gathering_id_detail -> done")
		return session
	
	async def browse_matchmake_session_no_holder(self, search_criteria, range):
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session_no_holder()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(search_criteria)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_BROWSE_MATCHMAKE_SESSION_NO_HOLDER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		sessions = stream.list(MatchmakeSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session_no_holder -> done")
		return sessions
	
	async def browse_matchmake_session_with_host_urls_no_holder(self, search_criteria, range):
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session_with_host_urls_no_holder()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(search_criteria)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_BROWSE_MATCHMAKE_SESSION_WITH_HOST_URLS_NO_HOLDER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.sessions = stream.list(MatchmakeSession)
		obj.urls = stream.list(GatheringURLs)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session_with_host_urls_no_holder -> done")
		return obj
	
	async def update_matchmake_session_part(self, param):
		logger.info("MatchmakeExtensionClientMK8D.update_matchmake_session_part()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_MATCHMAKE_SESSION_PART, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.update_matchmake_session_part -> done")
	
	async def request_matchmaking(self, param):
		logger.info("MatchmakeExtensionClientMK8D.request_matchmaking()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REQUEST_MATCHMAKING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		request_id = stream.u64()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.request_matchmaking -> done")
		return request_id
	
	async def withdraw_matchmaking(self, request_id):
		logger.info("MatchmakeExtensionClientMK8D.withdraw_matchmaking()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(request_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_WITHDRAW_MATCHMAKING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.withdraw_matchmaking -> done")
	
	async def withdraw_matchmaking_all(self):
		logger.info("MatchmakeExtensionClientMK8D.withdraw_matchmaking_all()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_WITHDRAW_MATCHMAKING_ALL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.withdraw_matchmaking_all -> done")
	
	async def find_matchmake_session_by_gathering_id(self, gids):
		logger.info("MatchmakeExtensionClientMK8D.find_matchmake_session_by_gathering_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(gids, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_MATCHMAKE_SESSION_BY_GATHERING_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		sessions = stream.list(MatchmakeSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.find_matchmake_session_by_gathering_id -> done")
		return sessions
	
	async def find_matchmake_session_by_single_gathering_id(self, gid):
		logger.info("MatchmakeExtensionClientMK8D.find_matchmake_session_by_single_gathering_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_MATCHMAKE_SESSION_BY_SINGLE_GATHERING_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session = stream.extract(MatchmakeSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.find_matchmake_session_by_single_gathering_id -> done")
		return session
	
	async def find_matchmake_session_by_owner(self, pid, range):
		logger.info("MatchmakeExtensionClientMK8D.find_matchmake_session_by_owner()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_MATCHMAKE_SESSION_BY_OWNER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		sessions = stream.list(MatchmakeSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.find_matchmake_session_by_owner -> done")
		return sessions
	
	async def find_matchmake_session_by_participant(self, param):
		logger.info("MatchmakeExtensionClientMK8D.find_matchmake_session_by_participant()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIND_MATCHMAKE_SESSION_BY_PARTICIPANT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.list(FindMatchmakeSessionByParticipantResult)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.find_matchmake_session_by_participant -> done")
		return result
	
	async def browse_matchmake_session_no_holder_no_result_range(self, search_criteria):
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session_no_holder_no_result_range()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(search_criteria)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_BROWSE_MATCHMAKE_SESSION_NO_HOLDER_NO_RESULT_RANGE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		sessions = stream.list(MatchmakeSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session_no_holder_no_result_range -> done")
		return sessions
	
	async def browse_matchmake_session_with_host_urls_no_holder_no_result_range(self, search_criteria):
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session_with_host_urls_no_holder_no_result_range()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(search_criteria)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_BROWSE_MATCHMAKE_SESSION_WITH_HOST_URLS_NO_HOLDER_NO_RESULT_RANGE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.sessions = stream.list(MatchmakeSession)
		obj.urls = stream.list(GatheringURLs)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.browse_matchmake_session_with_host_urls_no_holder_no_result_range -> done")
		return obj
	
	async def create_simple_search_object(self, object):
		logger.info("MatchmakeExtensionClientMK8D.create_simple_search_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(object)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CREATE_SIMPLE_SEARCH_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		id = stream.u32()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.create_simple_search_object -> done")
		return id
	
	async def update_simple_search_object(self, id, object):
		logger.info("MatchmakeExtensionClientMK8D.update_simple_search_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(id)
		stream.add(object)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_SIMPLE_SEARCH_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.update_simple_search_object -> done")
	
	async def delete_simple_search_object(self, id):
		logger.info("MatchmakeExtensionClientMK8D.delete_simple_search_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_SIMPLE_SEARCH_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.delete_simple_search_object -> done")
	
	async def search_simple_search_object(self, param):
		logger.info("MatchmakeExtensionClientMK8D.search_simple_search_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_SEARCH_SIMPLE_SEARCH_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		objects = stream.list(SimpleSearchObject)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.search_simple_search_object -> done")
		return objects
	
	async def search_simple_search_object_by_object_ids(self, ids):
		logger.info("MatchmakeExtensionClientMK8D.search_simple_search_object_by_object_ids()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(ids, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_SEARCH_SIMPLE_SEARCH_OBJECT_BY_OBJECT_IDS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		objects = stream.list(SimpleSearchObject)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.search_simple_search_object_by_object_ids -> done")
		return objects
	
	async def join_matchmake_session_with_extra_participants(self, gid, join_message, ignore_blacklist, participation_count, extra_participants):
		logger.info("MatchmakeExtensionClientMK8D.join_matchmake_session_with_extra_participants()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(join_message)
		stream.bool(ignore_blacklist)
		stream.u16(participation_count)
		stream.u32(extra_participants)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_JOIN_MATCHMAKE_SESSION_WITH_EXTRA_PARTICIPANTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session_key = stream.buffer()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.join_matchmake_session_with_extra_participants -> done")
		return session_key
	
	async def create_competition(self, competition):
		logger.info("MatchmakeExtensionClientMK8D.create_competition()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(competition)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CREATE_COMPETITION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		competition = stream.extract(SimpleSearchObject)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.create_competition -> done")
		return competition
	
	async def delete_competition(self, id):
		logger.info("MatchmakeExtensionClientMK8D.delete_competition()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_COMPETITION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.delete_competition -> done")
	
	async def register_favorite_competition(self, id):
		logger.info("MatchmakeExtensionClientMK8D.register_favorite_competition()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REGISTER_FAVORITE_COMPETITION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.register_favorite_competition -> done")
	
	async def unregister_favorite_competition(self, id):
		logger.info("MatchmakeExtensionClientMK8D.unregister_favorite_competition()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UNREGISTER_FAVORITE_COMPETITION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.unregister_favorite_competition -> done")
	
	async def get_favorite_competition(self):
		logger.info("MatchmakeExtensionClientMK8D.get_favorite_competition()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_FAVORITE_COMPETITION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		competitions = stream.list(SimpleSearchObject)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClientMK8D.get_favorite_competition -> done")
		return competitions


class MatchMakingServer(MatchMakingProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_REGISTER_GATHERING: self.handle_register_gathering,
			self.METHOD_UNREGISTER_GATHERING: self.handle_unregister_gathering,
			self.METHOD_UNREGISTER_GATHERINGS: self.handle_unregister_gatherings,
			self.METHOD_UPDATE_GATHERING: self.handle_update_gathering,
			self.METHOD_INVITE: self.handle_invite,
			self.METHOD_ACCEPT_INVITATION: self.handle_accept_invitation,
			self.METHOD_DECLINE_INVITATION: self.handle_decline_invitation,
			self.METHOD_CANCEL_INVITATION: self.handle_cancel_invitation,
			self.METHOD_GET_INVITATIONS_SENT: self.handle_get_invitations_sent,
			self.METHOD_GET_INVITATIONS_RECEIVED: self.handle_get_invitations_received,
			self.METHOD_PARTICIPATE: self.handle_participate,
			self.METHOD_CANCEL_PARTICIPATION: self.handle_cancel_participation,
			self.METHOD_GET_PARTICIPANTS: self.handle_get_participants,
			self.METHOD_ADD_PARTICIPANTS: self.handle_add_participants,
			self.METHOD_GET_DETAILED_PARTICIPANTS: self.handle_get_detailed_participants,
			self.METHOD_GET_PARTICIPANTS_URLS: self.handle_get_participants_urls,
			self.METHOD_FIND_BY_TYPE: self.handle_find_by_type,
			self.METHOD_FIND_BY_DESCRIPTION: self.handle_find_by_description,
			self.METHOD_FIND_BY_DESCRIPTION_REGEX: self.handle_find_by_description_regex,
			self.METHOD_FIND_BY_ID: self.handle_find_by_id,
			self.METHOD_FIND_BY_SINGLE_ID: self.handle_find_by_single_id,
			self.METHOD_FIND_BY_OWNER: self.handle_find_by_owner,
			self.METHOD_FIND_BY_PARTICIPANTS: self.handle_find_by_participants,
			self.METHOD_FIND_INVITATIONS: self.handle_find_invitations,
			self.METHOD_FIND_BY_SQL_QUERY: self.handle_find_by_sql_query,
			self.METHOD_LAUNCH_SESSION: self.handle_launch_session,
			self.METHOD_UPDATE_SESSION_URL: self.handle_update_session_url,
			self.METHOD_GET_SESSION_URL: self.handle_get_session_url,
			self.METHOD_GET_STATE: self.handle_get_state,
			self.METHOD_SET_STATE: self.handle_set_state,
			self.METHOD_REPORT_STATS: self.handle_report_stats,
			self.METHOD_GET_STATS: self.handle_get_stats,
			self.METHOD_DELETE_GATHERING: self.handle_delete_gathering,
			self.METHOD_GET_PENDING_DELETIONS: self.handle_get_pending_deletions,
			self.METHOD_DELETE_FROM_DELETIONS: self.handle_delete_from_deletions,
			self.METHOD_MIGRATE_GATHERING_OWNERSHIP_V1: self.handle_migrate_gathering_ownership_v1,
			self.METHOD_FIND_BY_DESCRIPTION_LIKE: self.handle_find_by_description_like,
			self.METHOD_REGISTER_LOCAL_URL: self.handle_register_local_url,
			self.METHOD_REGISTER_LOCAL_URLS: self.handle_register_local_urls,
			self.METHOD_UPDATE_SESSION_HOST_V1: self.handle_update_session_host_v1,
			self.METHOD_GET_SESSION_URLS: self.handle_get_session_urls,
			self.METHOD_UPDATE_SESSION_HOST: self.handle_update_session_host,
			self.METHOD_UPDATE_GATHERING_OWNERSHIP: self.handle_update_gathering_ownership,
			self.METHOD_MIGRATE_GATHERING_OWNERSHIP: self.handle_migrate_gathering_ownership,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on MatchMakingServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_register_gathering(self, client, input, output):
		logger.info("MatchMakingServer.register_gathering()")
		#--- request ---
		gathering = input.anydata()
		response = await self.register_gathering(client, gathering)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u32(response)
	
	async def handle_unregister_gathering(self, client, input, output):
		logger.info("MatchMakingServer.unregister_gathering()")
		#--- request ---
		gid = input.u32()
		response = await self.unregister_gathering(client, gid)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_unregister_gatherings(self, client, input, output):
		logger.info("MatchMakingServer.unregister_gatherings()")
		#--- request ---
		gids = input.list(input.u32)
		response = await self.unregister_gatherings(client, gids)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_update_gathering(self, client, input, output):
		logger.info("MatchMakingServer.update_gathering()")
		#--- request ---
		gathering = input.anydata()
		response = await self.update_gathering(client, gathering)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_invite(self, client, input, output):
		logger.info("MatchMakingServer.invite()")
		#--- request ---
		gid = input.u32()
		pids = input.list(input.pid)
		message = input.string()
		response = await self.invite(client, gid, pids, message)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_accept_invitation(self, client, input, output):
		logger.info("MatchMakingServer.accept_invitation()")
		#--- request ---
		gid = input.u32()
		message = input.string()
		response = await self.accept_invitation(client, gid, message)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_decline_invitation(self, client, input, output):
		logger.info("MatchMakingServer.decline_invitation()")
		#--- request ---
		gid = input.u32()
		message = input.string()
		response = await self.decline_invitation(client, gid, message)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_cancel_invitation(self, client, input, output):
		logger.info("MatchMakingServer.cancel_invitation()")
		#--- request ---
		gid = input.u32()
		pids = input.list(input.pid)
		message = input.string()
		response = await self.cancel_invitation(client, gid, pids, message)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_get_invitations_sent(self, client, input, output):
		logger.info("MatchMakingServer.get_invitations_sent()")
		#--- request ---
		gid = input.u32()
		response = await self.get_invitations_sent(client, gid)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_invitations_received(self, client, input, output):
		logger.info("MatchMakingServer.get_invitations_received()")
		#--- request ---
		response = await self.get_invitations_received(client)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_participate(self, client, input, output):
		logger.info("MatchMakingServer.participate()")
		#--- request ---
		gid = input.u32()
		message = input.string()
		response = await self.participate(client, gid, message)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_cancel_participation(self, client, input, output):
		logger.info("MatchMakingServer.cancel_participation()")
		#--- request ---
		gid = input.u32()
		message = input.string()
		response = await self.cancel_participation(client, gid, message)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_get_participants(self, client, input, output):
		logger.info("MatchMakingServer.get_participants()")
		#--- request ---
		gid = input.u32()
		response = await self.get_participants(client, gid)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.pid)
	
	async def handle_add_participants(self, client, input, output):
		logger.info("MatchMakingServer.add_participants()")
		#--- request ---
		gid = input.u32()
		pids = input.list(input.pid)
		message = input.string()
		response = await self.add_participants(client, gid, pids, message)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_get_detailed_participants(self, client, input, output):
		logger.info("MatchMakingServer.get_detailed_participants()")
		#--- request ---
		gid = input.u32()
		response = await self.get_detailed_participants(client, gid)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_participants_urls(self, client, input, output):
		logger.info("MatchMakingServer.get_participants_urls()")
		#--- request ---
		gid = input.u32()
		response = await self.get_participants_urls(client, gid)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.stationurl)
	
	async def handle_find_by_type(self, client, input, output):
		logger.info("MatchMakingServer.find_by_type()")
		#--- request ---
		type = input.string()
		range = input.extract(common.ResultRange)
		response = await self.find_by_type(client, type, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_find_by_description(self, client, input, output):
		logger.info("MatchMakingServer.find_by_description()")
		#--- request ---
		description = input.string()
		range = input.extract(common.ResultRange)
		response = await self.find_by_description(client, description, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_find_by_description_regex(self, client, input, output):
		logger.info("MatchMakingServer.find_by_description_regex()")
		#--- request ---
		regex = input.string()
		range = input.extract(common.ResultRange)
		response = await self.find_by_description_regex(client, regex, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_find_by_id(self, client, input, output):
		logger.info("MatchMakingServer.find_by_id()")
		#--- request ---
		ids = input.list(input.u32)
		response = await self.find_by_id(client, ids)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_find_by_single_id(self, client, input, output):
		logger.info("MatchMakingServer.find_by_single_id()")
		#--- request ---
		gid = input.u32()
		response = await self.find_by_single_id(client, gid)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'gathering']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.bool(response.result)
		output.anydata(response.gathering)
	
	async def handle_find_by_owner(self, client, input, output):
		logger.info("MatchMakingServer.find_by_owner()")
		#--- request ---
		owner = input.pid()
		range = input.extract(common.ResultRange)
		response = await self.find_by_owner(client, owner, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_find_by_participants(self, client, input, output):
		logger.info("MatchMakingServer.find_by_participants()")
		#--- request ---
		pids = input.list(input.pid)
		response = await self.find_by_participants(client, pids)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_find_invitations(self, client, input, output):
		logger.info("MatchMakingServer.find_invitations()")
		#--- request ---
		range = input.extract(common.ResultRange)
		response = await self.find_invitations(client, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_find_by_sql_query(self, client, input, output):
		logger.info("MatchMakingServer.find_by_sql_query()")
		#--- request ---
		query = input.string()
		range = input.extract(common.ResultRange)
		response = await self.find_by_sql_query(client, query, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_launch_session(self, client, input, output):
		logger.info("MatchMakingServer.launch_session()")
		#--- request ---
		gid = input.u32()
		url = input.string()
		response = await self.launch_session(client, gid, url)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_update_session_url(self, client, input, output):
		logger.info("MatchMakingServer.update_session_url()")
		#--- request ---
		gid = input.u32()
		url = input.string()
		response = await self.update_session_url(client, gid, url)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_get_session_url(self, client, input, output):
		logger.info("MatchMakingServer.get_session_url()")
		#--- request ---
		gid = input.u32()
		response = await self.get_session_url(client, gid)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'url']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.bool(response.result)
		output.string(response.url)
	
	async def handle_get_state(self, client, input, output):
		logger.info("MatchMakingServer.get_state()")
		#--- request ---
		gid = input.u32()
		response = await self.get_state(client, gid)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'state']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.bool(response.result)
		output.u32(response.state)
	
	async def handle_set_state(self, client, input, output):
		logger.info("MatchMakingServer.set_state()")
		#--- request ---
		gid = input.u32()
		state = input.u32()
		response = await self.set_state(client, gid, state)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_report_stats(self, client, input, output):
		logger.info("MatchMakingServer.report_stats()")
		#--- request ---
		gid = input.u32()
		stats = input.list(GatheringStats)
		response = await self.report_stats(client, gid, stats)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_get_stats(self, client, input, output):
		logger.info("MatchMakingServer.get_stats()")
		#--- request ---
		gid = input.u32()
		pids = input.list(input.pid)
		columns = input.list(input.u8)
		response = await self.get_stats(client, gid, pids, columns)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'stats']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.bool(response.result)
		output.list(response.stats, output.add)
	
	async def handle_delete_gathering(self, client, input, output):
		logger.info("MatchMakingServer.delete_gathering()")
		#--- request ---
		gid = input.u32()
		response = await self.delete_gathering(client, gid)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_get_pending_deletions(self, client, input, output):
		logger.info("MatchMakingServer.get_pending_deletions()")
		#--- request ---
		reason = input.u32()
		range = input.extract(common.ResultRange)
		response = await self.get_pending_deletions(client, reason, range)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'deletions']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.bool(response.result)
		output.list(response.deletions, output.add)
	
	async def handle_delete_from_deletions(self, client, input, output):
		logger.info("MatchMakingServer.delete_from_deletions()")
		#--- request ---
		deletions = input.list(input.u32)
		response = await self.delete_from_deletions(client, deletions)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_migrate_gathering_ownership_v1(self, client, input, output):
		logger.info("MatchMakingServer.migrate_gathering_ownership_v1()")
		#--- request ---
		gid = input.u32()
		potential_owners = input.list(input.pid)
		response = await self.migrate_gathering_ownership_v1(client, gid, potential_owners)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_find_by_description_like(self, client, input, output):
		logger.info("MatchMakingServer.find_by_description_like()")
		#--- request ---
		description = input.string()
		range = input.extract(common.ResultRange)
		response = await self.find_by_description_like(client, description, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_register_local_url(self, client, input, output):
		logger.info("MatchMakingServer.register_local_url()")
		#--- request ---
		gid = input.u32()
		url = input.stationurl()
		await self.register_local_url(client, gid, url)
	
	async def handle_register_local_urls(self, client, input, output):
		logger.info("MatchMakingServer.register_local_urls()")
		#--- request ---
		gid = input.u32()
		urls = input.list(input.stationurl)
		await self.register_local_urls(client, gid, urls)
	
	async def handle_update_session_host_v1(self, client, input, output):
		logger.info("MatchMakingServer.update_session_host_v1()")
		#--- request ---
		gid = input.u32()
		await self.update_session_host_v1(client, gid)
	
	async def handle_get_session_urls(self, client, input, output):
		logger.info("MatchMakingServer.get_session_urls()")
		#--- request ---
		gid = input.u32()
		response = await self.get_session_urls(client, gid)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.stationurl)
	
	async def handle_update_session_host(self, client, input, output):
		logger.info("MatchMakingServer.update_session_host()")
		#--- request ---
		gid = input.u32()
		is_migrate_owner = input.bool()
		await self.update_session_host(client, gid, is_migrate_owner)
	
	async def handle_update_gathering_ownership(self, client, input, output):
		logger.info("MatchMakingServer.update_gathering_ownership()")
		#--- request ---
		gid = input.u32()
		participants_only = input.bool()
		response = await self.update_gathering_ownership(client, gid, participants_only)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_migrate_gathering_ownership(self, client, input, output):
		logger.info("MatchMakingServer.migrate_gathering_ownership()")
		#--- request ---
		gid = input.u32()
		potential_owners = input.list(input.pid)
		participants_only = input.bool()
		await self.migrate_gathering_ownership(client, gid, potential_owners, participants_only)
	
	async def register_gathering(self, *args):
		logger.warning("MatchMakingServer.register_gathering not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def unregister_gathering(self, *args):
		logger.warning("MatchMakingServer.unregister_gathering not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def unregister_gatherings(self, *args):
		logger.warning("MatchMakingServer.unregister_gatherings not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_gathering(self, *args):
		logger.warning("MatchMakingServer.update_gathering not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def invite(self, *args):
		logger.warning("MatchMakingServer.invite not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def accept_invitation(self, *args):
		logger.warning("MatchMakingServer.accept_invitation not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def decline_invitation(self, *args):
		logger.warning("MatchMakingServer.decline_invitation not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def cancel_invitation(self, *args):
		logger.warning("MatchMakingServer.cancel_invitation not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_invitations_sent(self, *args):
		logger.warning("MatchMakingServer.get_invitations_sent not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_invitations_received(self, *args):
		logger.warning("MatchMakingServer.get_invitations_received not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def participate(self, *args):
		logger.warning("MatchMakingServer.participate not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def cancel_participation(self, *args):
		logger.warning("MatchMakingServer.cancel_participation not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_participants(self, *args):
		logger.warning("MatchMakingServer.get_participants not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def add_participants(self, *args):
		logger.warning("MatchMakingServer.add_participants not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_detailed_participants(self, *args):
		logger.warning("MatchMakingServer.get_detailed_participants not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_participants_urls(self, *args):
		logger.warning("MatchMakingServer.get_participants_urls not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_by_type(self, *args):
		logger.warning("MatchMakingServer.find_by_type not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_by_description(self, *args):
		logger.warning("MatchMakingServer.find_by_description not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_by_description_regex(self, *args):
		logger.warning("MatchMakingServer.find_by_description_regex not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_by_id(self, *args):
		logger.warning("MatchMakingServer.find_by_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_by_single_id(self, *args):
		logger.warning("MatchMakingServer.find_by_single_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_by_owner(self, *args):
		logger.warning("MatchMakingServer.find_by_owner not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_by_participants(self, *args):
		logger.warning("MatchMakingServer.find_by_participants not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_invitations(self, *args):
		logger.warning("MatchMakingServer.find_invitations not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_by_sql_query(self, *args):
		logger.warning("MatchMakingServer.find_by_sql_query not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def launch_session(self, *args):
		logger.warning("MatchMakingServer.launch_session not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_session_url(self, *args):
		logger.warning("MatchMakingServer.update_session_url not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_session_url(self, *args):
		logger.warning("MatchMakingServer.get_session_url not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_state(self, *args):
		logger.warning("MatchMakingServer.get_state not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def set_state(self, *args):
		logger.warning("MatchMakingServer.set_state not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def report_stats(self, *args):
		logger.warning("MatchMakingServer.report_stats not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_stats(self, *args):
		logger.warning("MatchMakingServer.get_stats not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_gathering(self, *args):
		logger.warning("MatchMakingServer.delete_gathering not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_pending_deletions(self, *args):
		logger.warning("MatchMakingServer.get_pending_deletions not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_from_deletions(self, *args):
		logger.warning("MatchMakingServer.delete_from_deletions not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def migrate_gathering_ownership_v1(self, *args):
		logger.warning("MatchMakingServer.migrate_gathering_ownership_v1 not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_by_description_like(self, *args):
		logger.warning("MatchMakingServer.find_by_description_like not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def register_local_url(self, *args):
		logger.warning("MatchMakingServer.register_local_url not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def register_local_urls(self, *args):
		logger.warning("MatchMakingServer.register_local_urls not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_session_host_v1(self, *args):
		logger.warning("MatchMakingServer.update_session_host_v1 not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_session_urls(self, *args):
		logger.warning("MatchMakingServer.get_session_urls not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_session_host(self, *args):
		logger.warning("MatchMakingServer.update_session_host not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_gathering_ownership(self, *args):
		logger.warning("MatchMakingServer.update_gathering_ownership not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def migrate_gathering_ownership(self, *args):
		logger.warning("MatchMakingServer.migrate_gathering_ownership not implemented")
		raise common.RMCError("Core::NotImplemented")


class MatchMakingServerExt(MatchMakingProtocolExt):
	def __init__(self):
		self.methods = {
			self.METHOD_END_PARTICIPATION: self.handle_end_participation,
			self.METHOD_GET_PARTICIPANTS: self.handle_get_participants,
			self.METHOD_GET_DETAILED_PARTICIPANTS: self.handle_get_detailed_participants,
			self.METHOD_GET_PARTICIPANTS_URLS: self.handle_get_participants_urls,
			self.METHOD_GET_GATHERING_RELATIONS: self.handle_get_gathering_relations,
			self.METHOD_DELETE_FROM_DELETIONS: self.handle_delete_from_deletions,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on MatchMakingServerExt: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_end_participation(self, client, input, output):
		logger.info("MatchMakingServerExt.end_participation()")
		#--- request ---
		gid = input.u32()
		message = input.string()
		response = await self.end_participation(client, gid, message)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_get_participants(self, client, input, output):
		logger.info("MatchMakingServerExt.get_participants()")
		#--- request ---
		gid = input.u32()
		only_active = input.bool()
		response = await self.get_participants(client, gid, only_active)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.pid)
	
	async def handle_get_detailed_participants(self, client, input, output):
		logger.info("MatchMakingServerExt.get_detailed_participants()")
		#--- request ---
		gid = input.u32()
		only_active = input.bool()
		response = await self.get_detailed_participants(client, gid, only_active)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_participants_urls(self, client, input, output):
		logger.info("MatchMakingServerExt.get_participants_urls()")
		#--- request ---
		gids = input.list(input.u32)
		response = await self.get_participants_urls(client, gids)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_gathering_relations(self, client, input, output):
		logger.info("MatchMakingServerExt.get_gathering_relations()")
		#--- request ---
		id = input.u32()
		descr = input.string()
		response = await self.get_gathering_relations(client, id, descr)
		
		#--- response ---
		if not isinstance(response, str):
			raise RuntimeError("Expected str, got %s" %response.__class__.__name__)
		output.string(response)
	
	async def handle_delete_from_deletions(self, client, input, output):
		logger.info("MatchMakingServerExt.delete_from_deletions()")
		#--- request ---
		deletions = input.list(input.u32)
		pid = input.pid()
		await self.delete_from_deletions(client, deletions, pid)
	
	async def end_participation(self, *args):
		logger.warning("MatchMakingServerExt.end_participation not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_participants(self, *args):
		logger.warning("MatchMakingServerExt.get_participants not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_detailed_participants(self, *args):
		logger.warning("MatchMakingServerExt.get_detailed_participants not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_participants_urls(self, *args):
		logger.warning("MatchMakingServerExt.get_participants_urls not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_gathering_relations(self, *args):
		logger.warning("MatchMakingServerExt.get_gathering_relations not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_from_deletions(self, *args):
		logger.warning("MatchMakingServerExt.delete_from_deletions not implemented")
		raise common.RMCError("Core::NotImplemented")


class MatchmakeRefereeServer(MatchmakeRefereeProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_START_ROUND: self.handle_start_round,
			self.METHOD_GET_START_ROUND_PARAM: self.handle_get_start_round_param,
			self.METHOD_END_ROUND: self.handle_end_round,
			self.METHOD_END_ROUND_WITHOUT_REPORT: self.handle_end_round_without_report,
			self.METHOD_GET_ROUND_PARTICIPANTS: self.handle_get_round_participants,
			self.METHOD_GET_NOT_SUMMARIZED_ROUND: self.handle_get_not_summarized_round,
			self.METHOD_GET_ROUND: self.handle_get_round,
			self.METHOD_GET_STATS_PRIMARY: self.handle_get_stats_primary,
			self.METHOD_GET_STATS_PRIMARIES: self.handle_get_stats_primaries,
			self.METHOD_GET_STATS_ALL: self.handle_get_stats_all,
			self.METHOD_CREATE_STATS: self.handle_create_stats,
			self.METHOD_GET_OR_CREATE_STATS: self.handle_get_or_create_stats,
			self.METHOD_RESET_STATS: self.handle_reset_stats,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on MatchmakeRefereeServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_start_round(self, client, input, output):
		logger.info("MatchmakeRefereeServer.start_round()")
		#--- request ---
		param = input.extract(MatchmakeRefereeStartRoundParam)
		response = await self.start_round(client, param)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u64(response)
	
	async def handle_get_start_round_param(self, client, input, output):
		logger.info("MatchmakeRefereeServer.get_start_round_param()")
		#--- request ---
		round_id = input.u64()
		response = await self.get_start_round_param(client, round_id)
		
		#--- response ---
		if not isinstance(response, MatchmakeRefereeStartRoundParam):
			raise RuntimeError("Expected MatchmakeRefereeStartRoundParam, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_end_round(self, client, input, output):
		logger.info("MatchmakeRefereeServer.end_round()")
		#--- request ---
		param = input.extract(MatchmakeRefereeEndRoundParam)
		await self.end_round(client, param)
	
	async def handle_end_round_without_report(self, client, input, output):
		logger.info("MatchmakeRefereeServer.end_round_without_report()")
		#--- request ---
		round_id = input.u64()
		await self.end_round_without_report(client, round_id)
	
	async def handle_get_round_participants(self, client, input, output):
		logger.info("MatchmakeRefereeServer.get_round_participants()")
		#--- request ---
		round_id = input.u64()
		response = await self.get_round_participants(client, round_id)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.pid)
	
	async def handle_get_not_summarized_round(self, client, input, output):
		logger.info("MatchmakeRefereeServer.get_not_summarized_round()")
		#--- request ---
		response = await self.get_not_summarized_round(client)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_round(self, client, input, output):
		logger.info("MatchmakeRefereeServer.get_round()")
		#--- request ---
		round = input.u64()
		response = await self.get_round(client, round)
		
		#--- response ---
		if not isinstance(response, MatchmakeRefereeRound):
			raise RuntimeError("Expected MatchmakeRefereeRound, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_stats_primary(self, client, input, output):
		logger.info("MatchmakeRefereeServer.get_stats_primary()")
		#--- request ---
		target = input.extract(MatchmakeRefereeStatsTarget)
		response = await self.get_stats_primary(client, target)
		
		#--- response ---
		if not isinstance(response, MatchmakeRefereeStats):
			raise RuntimeError("Expected MatchmakeRefereeStats, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_stats_primaries(self, client, input, output):
		logger.info("MatchmakeRefereeServer.get_stats_primaries()")
		#--- request ---
		targets = input.list(MatchmakeRefereeStatsTarget)
		response = await self.get_stats_primaries(client, targets)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['stats', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.stats, output.add)
		output.list(response.results, output.result)
	
	async def handle_get_stats_all(self, client, input, output):
		logger.info("MatchmakeRefereeServer.get_stats_all()")
		#--- request ---
		target = input.extract(MatchmakeRefereeStatsTarget)
		response = await self.get_stats_all(client, target)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_create_stats(self, client, input, output):
		logger.info("MatchmakeRefereeServer.create_stats()")
		#--- request ---
		param = input.extract(MatchmakeRefereeStatsInitParam)
		response = await self.create_stats(client, param)
		
		#--- response ---
		if not isinstance(response, MatchmakeRefereeStats):
			raise RuntimeError("Expected MatchmakeRefereeStats, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_or_create_stats(self, client, input, output):
		logger.info("MatchmakeRefereeServer.get_or_create_stats()")
		#--- request ---
		param = input.extract(MatchmakeRefereeStatsInitParam)
		response = await self.get_or_create_stats(client, param)
		
		#--- response ---
		if not isinstance(response, MatchmakeRefereeStats):
			raise RuntimeError("Expected MatchmakeRefereeStats, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_reset_stats(self, client, input, output):
		logger.info("MatchmakeRefereeServer.reset_stats()")
		#--- request ---
		await self.reset_stats(client)
	
	async def start_round(self, *args):
		logger.warning("MatchmakeRefereeServer.start_round not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_start_round_param(self, *args):
		logger.warning("MatchmakeRefereeServer.get_start_round_param not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def end_round(self, *args):
		logger.warning("MatchmakeRefereeServer.end_round not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def end_round_without_report(self, *args):
		logger.warning("MatchmakeRefereeServer.end_round_without_report not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_round_participants(self, *args):
		logger.warning("MatchmakeRefereeServer.get_round_participants not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_not_summarized_round(self, *args):
		logger.warning("MatchmakeRefereeServer.get_not_summarized_round not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_round(self, *args):
		logger.warning("MatchmakeRefereeServer.get_round not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_stats_primary(self, *args):
		logger.warning("MatchmakeRefereeServer.get_stats_primary not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_stats_primaries(self, *args):
		logger.warning("MatchmakeRefereeServer.get_stats_primaries not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_stats_all(self, *args):
		logger.warning("MatchmakeRefereeServer.get_stats_all not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def create_stats(self, *args):
		logger.warning("MatchmakeRefereeServer.create_stats not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_or_create_stats(self, *args):
		logger.warning("MatchmakeRefereeServer.get_or_create_stats not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def reset_stats(self, *args):
		logger.warning("MatchmakeRefereeServer.reset_stats not implemented")
		raise common.RMCError("Core::NotImplemented")


class MatchmakeExtensionServerMK8D(MatchmakeExtensionProtocolMK8D):
	def __init__(self):
		self.methods = {
			self.METHOD_CLOSE_PARTICIPATION: self.handle_close_participation,
			self.METHOD_OPEN_PARTICIPATION: self.handle_open_participation,
			self.METHOD_AUTO_MATCHMAKE_POSTPONE: self.handle_auto_matchmake_postpone,
			self.METHOD_BROWSE_MATCHMAKE_SESSION: self.handle_browse_matchmake_session,
			self.METHOD_BROWSE_MATCHMAKE_SESSION_WITH_HOST_URLS: self.handle_browse_matchmake_session_with_host_urls,
			self.METHOD_CREATE_MATCHMAKE_SESSION: self.handle_create_matchmake_session,
			self.METHOD_JOIN_MATCHMAKE_SESSION: self.handle_join_matchmake_session,
			self.METHOD_MODIFY_CURRENT_GAME_ATTRIBUTE: self.handle_modify_current_game_attribute,
			self.METHOD_UPDATE_NOTIFICATION_DATA: self.handle_update_notification_data,
			self.METHOD_GET_FRIEND_NOTIFICATION_DATA: self.handle_get_friend_notification_data,
			self.METHOD_UPDATE_APPLICATION_BUFFER: self.handle_update_application_buffer,
			self.METHOD_UPDATE_MATCHMAKE_SESSION_ATTRIBUTE: self.handle_update_matchmake_session_attribute,
			self.METHOD_GET_FRIEND_NOTIFICATION_DATA_LIST: self.handle_get_friend_notification_data_list,
			self.METHOD_UPDATE_MATCHMAKE_SESSION: self.handle_update_matchmake_session,
			self.METHOD_AUTO_MATCHMAKE_WITH_SEARCH_CRITERIA_POSTPONE: self.handle_auto_matchmake_with_search_criteria_postpone,
			self.METHOD_GET_PLAYING_SESSION: self.handle_get_playing_session,
			self.METHOD_CREATE_COMMUNITY: self.handle_create_community,
			self.METHOD_UPDATE_COMMUNITY: self.handle_update_community,
			self.METHOD_JOIN_COMMUNITY: self.handle_join_community,
			self.METHOD_FIND_COMMUNITY_BY_GATHERING_ID: self.handle_find_community_by_gathering_id,
			self.METHOD_FIND_OFFICIAL_COMMUNITY: self.handle_find_official_community,
			self.METHOD_FIND_COMMUNITY_BY_PARTICIPANT: self.handle_find_community_by_participant,
			self.METHOD_UPDATE_PRIVACY_SETTING: self.handle_update_privacy_setting,
			self.METHOD_GET_MY_BLOCK_LIST: self.handle_get_my_block_list,
			self.METHOD_ADD_TO_BLOCK_LIST: self.handle_add_to_block_list,
			self.METHOD_REMOVE_FROM_BLOCK_LIST: self.handle_remove_from_block_list,
			self.METHOD_CLEAR_MY_BLOCK_LIST: self.handle_clear_my_block_list,
			self.METHOD_REPORT_VIOLATION: self.handle_report_violation,
			self.METHOD_IS_VIOLATION_USER: self.handle_is_violation_user,
			self.METHOD_JOIN_MATCHMAKE_SESSION_EX: self.handle_join_matchmake_session_ex,
			self.METHOD_GET_SIMPLE_PLAYING_SESSION: self.handle_get_simple_playing_session,
			self.METHOD_GET_SIMPLE_COMMUNITY: self.handle_get_simple_community,
			self.METHOD_AUTO_MATCHMAKE_WITH_GATHERING_ID_POSTPONE: self.handle_auto_matchmake_with_gathering_id_postpone,
			self.METHOD_UPDATE_PROGRESS_SCORE: self.handle_update_progress_score,
			self.METHOD_DEBUG_NOTIFY_EVENT: self.handle_debug_notify_event,
			self.METHOD_GENERATE_MATCHMAKE_SESSION_SYSTEM_PASSWORD: self.handle_generate_matchmake_session_system_password,
			self.METHOD_CLEAR_MATCHMAKE_SESSION_SYSTEM_PASSWORD: self.handle_clear_matchmake_session_system_password,
			self.METHOD_CREATE_MATCHMAKE_SESSION_WITH_PARAM: self.handle_create_matchmake_session_with_param,
			self.METHOD_JOIN_MATCHMAKE_SESSION_WITH_PARAM: self.handle_join_matchmake_session_with_param,
			self.METHOD_AUTO_MATCHMAKE_WITH_PARAM_POSTPONE: self.handle_auto_matchmake_with_param_postpone,
			self.METHOD_FIND_MATCHMAKE_SESSION_BY_GATHERING_ID_DETAIL: self.handle_find_matchmake_session_by_gathering_id_detail,
			self.METHOD_BROWSE_MATCHMAKE_SESSION_NO_HOLDER: self.handle_browse_matchmake_session_no_holder,
			self.METHOD_BROWSE_MATCHMAKE_SESSION_WITH_HOST_URLS_NO_HOLDER: self.handle_browse_matchmake_session_with_host_urls_no_holder,
			self.METHOD_UPDATE_MATCHMAKE_SESSION_PART: self.handle_update_matchmake_session_part,
			self.METHOD_REQUEST_MATCHMAKING: self.handle_request_matchmaking,
			self.METHOD_WITHDRAW_MATCHMAKING: self.handle_withdraw_matchmaking,
			self.METHOD_WITHDRAW_MATCHMAKING_ALL: self.handle_withdraw_matchmaking_all,
			self.METHOD_FIND_MATCHMAKE_SESSION_BY_GATHERING_ID: self.handle_find_matchmake_session_by_gathering_id,
			self.METHOD_FIND_MATCHMAKE_SESSION_BY_SINGLE_GATHERING_ID: self.handle_find_matchmake_session_by_single_gathering_id,
			self.METHOD_FIND_MATCHMAKE_SESSION_BY_OWNER: self.handle_find_matchmake_session_by_owner,
			self.METHOD_FIND_MATCHMAKE_SESSION_BY_PARTICIPANT: self.handle_find_matchmake_session_by_participant,
			self.METHOD_BROWSE_MATCHMAKE_SESSION_NO_HOLDER_NO_RESULT_RANGE: self.handle_browse_matchmake_session_no_holder_no_result_range,
			self.METHOD_BROWSE_MATCHMAKE_SESSION_WITH_HOST_URLS_NO_HOLDER_NO_RESULT_RANGE: self.handle_browse_matchmake_session_with_host_urls_no_holder_no_result_range,
			self.METHOD_CREATE_SIMPLE_SEARCH_OBJECT: self.handle_create_simple_search_object,
			self.METHOD_UPDATE_SIMPLE_SEARCH_OBJECT: self.handle_update_simple_search_object,
			self.METHOD_DELETE_SIMPLE_SEARCH_OBJECT: self.handle_delete_simple_search_object,
			self.METHOD_SEARCH_SIMPLE_SEARCH_OBJECT: self.handle_search_simple_search_object,
			self.METHOD_SEARCH_SIMPLE_SEARCH_OBJECT_BY_OBJECT_IDS: self.handle_search_simple_search_object_by_object_ids,
			self.METHOD_JOIN_MATCHMAKE_SESSION_WITH_EXTRA_PARTICIPANTS: self.handle_join_matchmake_session_with_extra_participants,
			self.METHOD_CUSTOM_GET_SIMPLE_PLAYING_SESSION: self.handle_custom_get_simple_playing_session,
			self.METHOD_CREATE_COMPETITION: self.handle_create_competition,
			self.METHOD_DELETE_COMPETITION: self.handle_delete_competition,
			self.METHOD_REGISTER_FAVORITE_COMPETITION: self.handle_register_favorite_competition,
			self.METHOD_UNREGISTER_FAVORITE_COMPETITION: self.handle_unregister_favorite_competition,
			self.METHOD_GET_FAVORITE_COMPETITION: self.handle_get_favorite_competition,
			self.METHOD_GET_TEAM_PARTICIPANTS: self.handle_get_team_participants,
			self.METHOD_FIND_COMMUNITY_BY_OWNER: self.handle_find_community_by_owner,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on MatchmakeExtensionServerMK8D: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_close_participation(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.close_participation()")
		#--- request ---
		gid = input.u32()
		await self.close_participation(client, gid)
	
	async def handle_open_participation(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.open_participation()")
		#--- request ---
		gid = input.u32()
		await self.open_participation(client, gid)
	
	async def handle_auto_matchmake_postpone(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.auto_matchmake_postpone()")
		#--- request ---
		gathering = input.anydata()
		message = input.string()
		response = await self.auto_matchmake_postpone(client, gathering, message)
		
		#--- response ---
		if not isinstance(response, common.Data):
			raise RuntimeError("Expected common.Data, got %s" %response.__class__.__name__)
		output.anydata(response)
	
	async def handle_browse_matchmake_session(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.browse_matchmake_session()")
		#--- request ---
		search_criteria = input.extract(MatchmakeSessionSearchCriteria)
		range = input.extract(common.ResultRange)
		response = await self.browse_matchmake_session(client, search_criteria, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_browse_matchmake_session_with_host_urls(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.browse_matchmake_session_with_host_urls()")
		#--- request ---
		search_criteria = input.extract(MatchmakeSessionSearchCriteria)
		range = input.extract(common.ResultRange)
		response = await self.browse_matchmake_session_with_host_urls(client, search_criteria, range)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['gatherings', 'urls']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.gatherings, output.anydata)
		output.list(response.urls, output.add)
	
	async def handle_create_matchmake_session(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.create_matchmake_session()")
		#--- request ---
		gathering = input.anydata()
		description = input.string()
		num_participants = input.u16()
		response = await self.create_matchmake_session(client, gathering, description, num_participants)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['gid', 'session_key']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.u32(response.gid)
		output.buffer(response.session_key)
	
	async def handle_join_matchmake_session(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.join_matchmake_session()")
		#--- request ---
		gid = input.u32()
		message = input.string()
		response = await self.join_matchmake_session(client, gid, message)
		
		#--- response ---
		if not isinstance(response, bytes):
			raise RuntimeError("Expected bytes, got %s" %response.__class__.__name__)
		output.buffer(response)
	
	async def handle_modify_current_game_attribute(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.modify_current_game_attribute()")
		#--- request ---
		gid = input.u32()
		attrib = input.u32()
		value = input.u32()
		await self.modify_current_game_attribute(client, gid, attrib, value)
	
	async def handle_update_notification_data(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.update_notification_data()")
		#--- request ---
		type = input.u32()
		param1 = input.pid()
		param2 = input.pid()
		param3 = input.string()
		await self.update_notification_data(client, type, param1, param2, param3)
	
	async def handle_get_friend_notification_data(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.get_friend_notification_data()")
		#--- request ---
		type = input.s32()
		response = await self.get_friend_notification_data(client, type)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_update_application_buffer(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.update_application_buffer()")
		#--- request ---
		gid = input.u32()
		buffer = input.buffer()
		await self.update_application_buffer(client, gid, buffer)
	
	async def handle_update_matchmake_session_attribute(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.update_matchmake_session_attribute()")
		#--- request ---
		gid = input.u32()
		attribs = input.list(input.u32)
		await self.update_matchmake_session_attribute(client, gid, attribs)
	
	async def handle_get_friend_notification_data_list(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.get_friend_notification_data_list()")
		#--- request ---
		types = input.list(input.u32)
		response = await self.get_friend_notification_data_list(client, types)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_update_matchmake_session(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.update_matchmake_session()")
		#--- request ---
		gathering = input.anydata()
		await self.update_matchmake_session(client, gathering)
	
	async def handle_auto_matchmake_with_search_criteria_postpone(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.auto_matchmake_with_search_criteria_postpone()")
		#--- request ---
		search_criteria = input.list(MatchmakeSessionSearchCriteria)
		gathering = input.anydata()
		message = input.string()
		response = await self.auto_matchmake_with_search_criteria_postpone(client, search_criteria, gathering, message)
		
		#--- response ---
		if not isinstance(response, common.Data):
			raise RuntimeError("Expected common.Data, got %s" %response.__class__.__name__)
		output.anydata(response)
	
	async def handle_get_playing_session(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.get_playing_session()")
		#--- request ---
		pids = input.list(input.pid)
		response = await self.get_playing_session(client, pids)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_create_community(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.create_community()")
		#--- request ---
		community = input.extract(PersistentGathering)
		message = input.string()
		response = await self.create_community(client, community, message)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u32(response)
	
	async def handle_update_community(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.update_community()")
		#--- request ---
		community = input.extract(PersistentGathering)
		await self.update_community(client, community)
	
	async def handle_join_community(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.join_community()")
		#--- request ---
		gid = input.u32()
		message = input.string()
		password = input.string()
		await self.join_community(client, gid, message, password)
	
	async def handle_find_community_by_gathering_id(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.find_community_by_gathering_id()")
		#--- request ---
		gids = input.list(input.u32)
		response = await self.find_community_by_gathering_id(client, gids)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_find_official_community(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.find_official_community()")
		#--- request ---
		available_only = input.bool()
		range = input.extract(common.ResultRange)
		response = await self.find_official_community(client, available_only, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_find_community_by_participant(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.find_community_by_participant()")
		#--- request ---
		pid = input.pid()
		range = input.extract(common.ResultRange)
		response = await self.find_community_by_participant(client, pid, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_update_privacy_setting(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.update_privacy_setting()")
		#--- request ---
		online_status = input.bool()
		community_participation = input.bool()
		await self.update_privacy_setting(client, online_status, community_participation)
	
	async def handle_get_my_block_list(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.get_my_block_list()")
		#--- request ---
		response = await self.get_my_block_list(client)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.pid)
	
	async def handle_add_to_block_list(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.add_to_block_list()")
		#--- request ---
		pids = input.list(input.pid)
		await self.add_to_block_list(client, pids)
	
	async def handle_remove_from_block_list(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.remove_from_block_list()")
		#--- request ---
		pids = input.list(input.pid)
		await self.remove_from_block_list(client, pids)
	
	async def handle_clear_my_block_list(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.clear_my_block_list()")
		#--- request ---
		await self.clear_my_block_list(client)
	
	async def handle_report_violation(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.report_violation()")
		#--- request ---
		pid = input.pid()
		username = input.string()
		violation_code = input.u32()
		await self.report_violation(client, pid, username, violation_code)
	
	async def handle_is_violation_user(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.is_violation_user()")
		#--- request ---
		response = await self.is_violation_user(client)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['flag', 'score']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.bool(response.flag)
		output.u32(response.score)
	
	async def handle_join_matchmake_session_ex(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.join_matchmake_session_ex()")
		#--- request ---
		gid = input.u32()
		gmessage = input.string()
		ignore_block_list = input.bool()
		num_participants = input.u16()
		response = await self.join_matchmake_session_ex(client, gid, gmessage, ignore_block_list, num_participants)
		
		#--- response ---
		if not isinstance(response, bytes):
			raise RuntimeError("Expected bytes, got %s" %response.__class__.__name__)
		output.buffer(response)
	
	async def handle_get_simple_playing_session(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.get_simple_playing_session()")
		#--- request ---
		pids = input.list(input.pid)
		include_login_user = input.bool()
		response = await self.get_simple_playing_session(client, pids, include_login_user)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_simple_community(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.get_simple_community()")
		#--- request ---
		gids = input.list(input.u32)
		response = await self.get_simple_community(client, gids)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_auto_matchmake_with_gathering_id_postpone(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.auto_matchmake_with_gathering_id_postpone()")
		#--- request ---
		gids = input.list(input.u32)
		gathering = input.anydata()
		message = input.string()
		response = await self.auto_matchmake_with_gathering_id_postpone(client, gids, gathering, message)
		
		#--- response ---
		if not isinstance(response, common.Data):
			raise RuntimeError("Expected common.Data, got %s" %response.__class__.__name__)
		output.anydata(response)
	
	async def handle_update_progress_score(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.update_progress_score()")
		#--- request ---
		gid = input.u32()
		score = input.u8()
		await self.update_progress_score(client, gid, score)
	
	async def handle_debug_notify_event(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.debug_notify_event()")
		#--- request ---
		pid = input.pid()
		main_type = input.u32()
		sub_type = input.u32()
		param1 = input.u64()
		param2 = input.u64()
		param3 = input.string()
		await self.debug_notify_event(client, pid, main_type, sub_type, param1, param2, param3)
	
	async def handle_generate_matchmake_session_system_password(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.generate_matchmake_session_system_password()")
		#--- request ---
		gid = input.u32()
		response = await self.generate_matchmake_session_system_password(client, gid)
		
		#--- response ---
		if not isinstance(response, str):
			raise RuntimeError("Expected str, got %s" %response.__class__.__name__)
		output.string(response)
	
	async def handle_clear_matchmake_session_system_password(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.clear_matchmake_session_system_password()")
		#--- request ---
		gid = input.u32()
		await self.clear_matchmake_session_system_password(client, gid)
	
	async def handle_create_matchmake_session_with_param(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.create_matchmake_session_with_param()")
		#--- request ---
		param = input.extract(CreateMatchmakeSessionParam)
		response = await self.create_matchmake_session_with_param(client, param)
		
		#--- response ---
		if not isinstance(response, MatchmakeSession):
			raise RuntimeError("Expected MatchmakeSession, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_join_matchmake_session_with_param(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.join_matchmake_session_with_param()")
		#--- request ---
		param = input.extract(JoinMatchmakeSessionParam)
		response = await self.join_matchmake_session_with_param(client, param)
		
		#--- response ---
		if not isinstance(response, MatchmakeSession):
			raise RuntimeError("Expected MatchmakeSession, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_auto_matchmake_with_param_postpone(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.auto_matchmake_with_param_postpone()")
		#--- request ---
		param = input.extract(AutoMatchmakeParam)
		response = await self.auto_matchmake_with_param_postpone(client, param)
		
		#--- response ---
		if not isinstance(response, MatchmakeSession):
			raise RuntimeError("Expected MatchmakeSession, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_find_matchmake_session_by_gathering_id_detail(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.find_matchmake_session_by_gathering_id_detail()")
		#--- request ---
		gid = input.u32()
		response = await self.find_matchmake_session_by_gathering_id_detail(client, gid)
		
		#--- response ---
		if not isinstance(response, MatchmakeSession):
			raise RuntimeError("Expected MatchmakeSession, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_browse_matchmake_session_no_holder(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.browse_matchmake_session_no_holder()")
		#--- request ---
		search_criteria = input.extract(MatchmakeSessionSearchCriteria)
		range = input.extract(common.ResultRange)
		response = await self.browse_matchmake_session_no_holder(client, search_criteria, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_browse_matchmake_session_with_host_urls_no_holder(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.browse_matchmake_session_with_host_urls_no_holder()")
		#--- request ---
		search_criteria = input.extract(MatchmakeSessionSearchCriteria)
		range = input.extract(common.ResultRange)
		response = await self.browse_matchmake_session_with_host_urls_no_holder(client, search_criteria, range)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['sessions', 'urls']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.sessions, output.add)
		output.list(response.urls, output.add)
	
	async def handle_update_matchmake_session_part(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.update_matchmake_session_part()")
		#--- request ---
		param = input.extract(UpdateMatchmakeSessionParam)
		await self.update_matchmake_session_part(client, param)
	
	async def handle_request_matchmaking(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.request_matchmaking()")
		#--- request ---
		param = input.extract(AutoMatchmakeParam)
		response = await self.request_matchmaking(client, param)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u64(response)
	
	async def handle_withdraw_matchmaking(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.withdraw_matchmaking()")
		#--- request ---
		request_id = input.u64()
		await self.withdraw_matchmaking(client, request_id)
	
	async def handle_withdraw_matchmaking_all(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.withdraw_matchmaking_all()")
		#--- request ---
		await self.withdraw_matchmaking_all(client)
	
	async def handle_find_matchmake_session_by_gathering_id(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.find_matchmake_session_by_gathering_id()")
		#--- request ---
		gids = input.list(input.u32)
		response = await self.find_matchmake_session_by_gathering_id(client, gids)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_find_matchmake_session_by_single_gathering_id(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.find_matchmake_session_by_single_gathering_id()")
		#--- request ---
		gid = input.u32()
		response = await self.find_matchmake_session_by_single_gathering_id(client, gid)
		
		#--- response ---
		if not isinstance(response, MatchmakeSession):
			raise RuntimeError("Expected MatchmakeSession, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_find_matchmake_session_by_owner(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.find_matchmake_session_by_owner()")
		#--- request ---
		pid = input.pid()
		range = input.extract(common.ResultRange)
		response = await self.find_matchmake_session_by_owner(client, pid, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_find_matchmake_session_by_participant(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.find_matchmake_session_by_participant()")
		#--- request ---
		param = input.extract(FindMatchmakeSessionByParticipantParam)
		response = await self.find_matchmake_session_by_participant(client, param)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_browse_matchmake_session_no_holder_no_result_range(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.browse_matchmake_session_no_holder_no_result_range()")
		#--- request ---
		search_criteria = input.extract(MatchmakeSessionSearchCriteria)
		response = await self.browse_matchmake_session_no_holder_no_result_range(client, search_criteria)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_browse_matchmake_session_with_host_urls_no_holder_no_result_range(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.browse_matchmake_session_with_host_urls_no_holder_no_result_range()")
		#--- request ---
		search_criteria = input.extract(MatchmakeSessionSearchCriteria)
		response = await self.browse_matchmake_session_with_host_urls_no_holder_no_result_range(client, search_criteria)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['sessions', 'urls']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.sessions, output.add)
		output.list(response.urls, output.add)
	
	async def handle_create_simple_search_object(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.create_simple_search_object()")
		#--- request ---
		object = input.extract(SimpleSearchObject)
		response = await self.create_simple_search_object(client, object)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u32(response)
	
	async def handle_update_simple_search_object(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.update_simple_search_object()")
		#--- request ---
		id = input.u32()
		object = input.extract(SimpleSearchObject)
		await self.update_simple_search_object(client, id, object)
	
	async def handle_delete_simple_search_object(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.delete_simple_search_object()")
		#--- request ---
		id = input.u32()
		await self.delete_simple_search_object(client, id)
	
	async def handle_search_simple_search_object(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.search_simple_search_object()")
		#--- request ---
		param = input.extract(SimpleSearchParam)
		response = await self.search_simple_search_object(client, param)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_search_simple_search_object_by_object_ids(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.search_simple_search_object_by_object_ids()")
		#--- request ---
		ids = input.list(input.u32)
		response = await self.search_simple_search_object_by_object_ids(client, ids)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_join_matchmake_session_with_extra_participants(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.join_matchmake_session_with_extra_participants()")
		#--- request ---
		gid = input.u32()
		join_message = input.string()
		ignore_blacklist = input.bool()
		participation_count = input.u16()
		extra_participants = input.u32()
		response = await self.join_matchmake_session_with_extra_participants(client, gid, join_message, ignore_blacklist, participation_count, extra_participants)
		
		#--- response ---
		if not isinstance(response, bytes):
			raise RuntimeError("Expected bytes, got %s" %response.__class__.__name__)
		output.buffer(response)
	
	async def handle_custom_get_simple_playing_session(self, client, input, output):
		logger.warning("MatchmakeExtensionServerMK8D.custom_get_simple_playing_session is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_create_competition(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.create_competition()")
		#--- request ---
		competition = input.extract(SimpleSearchObject)
		response = await self.create_competition(client, competition)
		
		#--- response ---
		if not isinstance(response, SimpleSearchObject):
			raise RuntimeError("Expected SimpleSearchObject, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_delete_competition(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.delete_competition()")
		#--- request ---
		id = input.u32()
		await self.delete_competition(client, id)
	
	async def handle_register_favorite_competition(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.register_favorite_competition()")
		#--- request ---
		id = input.u32()
		await self.register_favorite_competition(client, id)
	
	async def handle_unregister_favorite_competition(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.unregister_favorite_competition()")
		#--- request ---
		id = input.u32()
		await self.unregister_favorite_competition(client, id)
	
	async def handle_get_favorite_competition(self, client, input, output):
		logger.info("MatchmakeExtensionServerMK8D.get_favorite_competition()")
		#--- request ---
		response = await self.get_favorite_competition(client)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_team_participants(self, client, input, output):
		logger.warning("MatchmakeExtensionServerMK8D.get_team_participants is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_find_community_by_owner(self, client, input, output):
		logger.warning("MatchmakeExtensionServerMK8D.find_community_by_owner is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def close_participation(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.close_participation not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def open_participation(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.open_participation not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def auto_matchmake_postpone(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.auto_matchmake_postpone not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def browse_matchmake_session(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.browse_matchmake_session not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def browse_matchmake_session_with_host_urls(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.browse_matchmake_session_with_host_urls not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def create_matchmake_session(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.create_matchmake_session not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def join_matchmake_session(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.join_matchmake_session not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def modify_current_game_attribute(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.modify_current_game_attribute not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_notification_data(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.update_notification_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_friend_notification_data(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.get_friend_notification_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_application_buffer(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.update_application_buffer not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_matchmake_session_attribute(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.update_matchmake_session_attribute not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_friend_notification_data_list(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.get_friend_notification_data_list not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_matchmake_session(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.update_matchmake_session not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def auto_matchmake_with_search_criteria_postpone(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.auto_matchmake_with_search_criteria_postpone not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_playing_session(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.get_playing_session not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def create_community(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.create_community not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_community(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.update_community not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def join_community(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.join_community not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_community_by_gathering_id(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.find_community_by_gathering_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_official_community(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.find_official_community not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_community_by_participant(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.find_community_by_participant not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_privacy_setting(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.update_privacy_setting not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_my_block_list(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.get_my_block_list not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def add_to_block_list(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.add_to_block_list not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def remove_from_block_list(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.remove_from_block_list not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def clear_my_block_list(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.clear_my_block_list not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def report_violation(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.report_violation not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def is_violation_user(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.is_violation_user not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def join_matchmake_session_ex(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.join_matchmake_session_ex not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_simple_playing_session(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.get_simple_playing_session not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_simple_community(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.get_simple_community not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def auto_matchmake_with_gathering_id_postpone(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.auto_matchmake_with_gathering_id_postpone not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_progress_score(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.update_progress_score not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def debug_notify_event(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.debug_notify_event not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def generate_matchmake_session_system_password(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.generate_matchmake_session_system_password not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def clear_matchmake_session_system_password(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.clear_matchmake_session_system_password not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def create_matchmake_session_with_param(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.create_matchmake_session_with_param not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def join_matchmake_session_with_param(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.join_matchmake_session_with_param not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def auto_matchmake_with_param_postpone(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.auto_matchmake_with_param_postpone not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_matchmake_session_by_gathering_id_detail(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.find_matchmake_session_by_gathering_id_detail not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def browse_matchmake_session_no_holder(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.browse_matchmake_session_no_holder not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def browse_matchmake_session_with_host_urls_no_holder(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.browse_matchmake_session_with_host_urls_no_holder not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_matchmake_session_part(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.update_matchmake_session_part not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def request_matchmaking(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.request_matchmaking not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def withdraw_matchmaking(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.withdraw_matchmaking not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def withdraw_matchmaking_all(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.withdraw_matchmaking_all not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_matchmake_session_by_gathering_id(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.find_matchmake_session_by_gathering_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_matchmake_session_by_single_gathering_id(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.find_matchmake_session_by_single_gathering_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_matchmake_session_by_owner(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.find_matchmake_session_by_owner not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def find_matchmake_session_by_participant(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.find_matchmake_session_by_participant not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def browse_matchmake_session_no_holder_no_result_range(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.browse_matchmake_session_no_holder_no_result_range not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def browse_matchmake_session_with_host_urls_no_holder_no_result_range(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.browse_matchmake_session_with_host_urls_no_holder_no_result_range not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def create_simple_search_object(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.create_simple_search_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_simple_search_object(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.update_simple_search_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_simple_search_object(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.delete_simple_search_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def search_simple_search_object(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.search_simple_search_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def search_simple_search_object_by_object_ids(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.search_simple_search_object_by_object_ids not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def join_matchmake_session_with_extra_participants(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.join_matchmake_session_with_extra_participants not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def create_competition(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.create_competition not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_competition(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.delete_competition not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def register_favorite_competition(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.register_favorite_competition not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def unregister_favorite_competition(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.unregister_favorite_competition not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_favorite_competition(self, *args):
		logger.warning("MatchmakeExtensionServerMK8D.get_favorite_competition not implemented")
		raise common.RMCError("Core::NotImplemented")

