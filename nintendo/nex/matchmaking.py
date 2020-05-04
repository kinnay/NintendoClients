
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


class MatchmakeSystem:
	GLOBAL = 1
	FRIENDS = 2


class Gathering(common.Structure):
	def __init__(self):
		super().__init__()
		self.id = 0
		self.owner_pid = 0
		self.host_pid = 0
		self.min_participants = 0
		self.max_participants = 0
		self.participation_policy = 1
		self.policy_argument = 0
		self.flags = 512
		self.state = 0
		self.description = ""
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		self.id = stream.u32()
		self.owner_pid = stream.pid()
		self.host_pid = stream.pid()
		self.min_participants = stream.u16()
		self.max_participants = stream.u16()
		self.participation_policy = stream.u32()
		self.policy_argument = stream.u32()
		self.flags = stream.u32()
		self.state = stream.u32()
		self.description = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.id)
		stream.pid(self.owner_pid)
		stream.pid(self.host_pid)
		stream.u16(self.min_participants)
		stream.u16(self.max_participants)
		stream.u32(self.participation_policy)
		stream.u32(self.policy_argument)
		stream.u32(self.flags)
		stream.u32(self.state)
		stream.string(self.description)


class MatchmakeParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.param = {}
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		self.param = stream.map(stream.string, stream.variant)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.map(self.param, stream.string, stream.variant)


class MatchmakeSession(Gathering):
	def __init__(self):
		super().__init__()
		self.game_mode = 0
		self.attribs = [0, 0, 0, 0, 0, 0]
		self.open_participation = True
		self.matchmake_system = 0
		self.application_data = b""
		self.player_count = 0
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
	
	def check_required(self, settings):
		if settings.get("nex.version") >= 30500:
			pass
		if settings.get("nex.version") >= 30000:
			pass
		if settings.get("nex.version") >= 30500:
			pass
		if settings.get("nex.version") >= 40000:
			pass
	
	def load(self, stream):
		self.game_mode = stream.u32()
		self.attribs = stream.list(stream.u32)
		self.open_participation = stream.bool()
		self.matchmake_system = stream.u32()
		self.application_data = stream.buffer()
		self.player_count = stream.u32()
		if stream.settings.get("nex.version") >= 30500:
			self.progress_score = stream.u8()
		if stream.settings.get("nex.version") >= 30000:
			self.session_key = stream.buffer()
		if stream.settings.get("nex.version") >= 30500:
			self.option = stream.u32()
		if stream.settings.get("nex.version") >= 40000:
			self.param = stream.extract(MatchmakeParam)
			self.started_time = stream.datetime()
			self.user_password = stream.string()
			self.refer_gid = stream.u32()
			self.user_password_enabled = stream.bool()
			self.system_password_enabled = stream.bool()
			self.codeword = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.game_mode)
		stream.list(self.attribs, stream.u32)
		stream.bool(self.open_participation)
		stream.u32(self.matchmake_system)
		stream.buffer(self.application_data)
		stream.u32(self.player_count)
		if stream.settings.get("nex.version") >= 30500:
			stream.u8(self.progress_score)
		if stream.settings.get("nex.version") >= 30000:
			stream.buffer(self.session_key)
		if stream.settings.get("nex.version") >= 30500:
			stream.u32(self.option)
		if stream.settings.get("nex.version") >= 40000:
			stream.add(self.param)
			stream.datetime(self.started_time)
			stream.string(self.user_password)
			stream.u32(self.refer_gid)
			stream.bool(self.user_password_enabled)
			stream.bool(self.system_password_enabled)
			stream.string(self.codeword)
common.DataHolder.register(MatchmakeSession, "MatchmakeSession")


class MatchmakeSessionSearchCriteria(common.Structure):
	def __init__(self):
		super().__init__()
		self.attribs = None
		self.game_mode = None
		self.min_players = None
		self.max_players = None
		self.matchmake_system = None
		self.vacant_only = None
		self.exclude_locked = None
		self.exclude_non_host_pid = None
		self.selection_method = None
		self.vacant_participants = None
		self.param = MatchmakeParam()
		self.exclude_user_password = None
		self.exclude_system_password = None
		self.refer_gid = None
		self.codeword = None
		self.range = common.ResultRange()
	
	def check_required(self, settings):
		for field in ['attribs', 'game_mode', 'min_players', 'max_players', 'matchmake_system', 'vacant_only', 'exclude_locked', 'exclude_non_host_pid', 'selection_method']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings.get("nex.version") >= 30500:
			for field in ['vacant_participants']:
				if getattr(self, field) is None:
					raise ValueError("No value assigned to required field: %s" %field)
		if settings.get("nex.version") >= 40000:
			for field in ['exclude_user_password', 'exclude_system_password', 'refer_gid', 'codeword']:
				if getattr(self, field) is None:
					raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.attribs = stream.list(stream.string)
		self.game_mode = stream.string()
		self.min_players = stream.string()
		self.max_players = stream.string()
		self.matchmake_system = stream.string()
		self.vacant_only = stream.bool()
		self.exclude_locked = stream.bool()
		self.exclude_non_host_pid = stream.bool()
		self.selection_method = stream.u32()
		if stream.settings.get("nex.version") >= 30500:
			self.vacant_participants = stream.u16()
		if stream.settings.get("nex.version") >= 40000:
			self.param = stream.extract(MatchmakeParam)
			self.exclude_user_password = stream.bool()
			self.exclude_system_password = stream.bool()
			self.refer_gid = stream.u32()
			self.codeword = stream.string()
			self.range = stream.extract(common.ResultRange)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.list(self.attribs, stream.string)
		stream.string(self.game_mode)
		stream.string(self.min_players)
		stream.string(self.max_players)
		stream.string(self.matchmake_system)
		stream.bool(self.vacant_only)
		stream.bool(self.exclude_locked)
		stream.bool(self.exclude_non_host_pid)
		stream.u32(self.selection_method)
		if stream.settings.get("nex.version") >= 30500:
			stream.u16(self.vacant_participants)
		if stream.settings.get("nex.version") >= 40000:
			stream.add(self.param)
			stream.bool(self.exclude_user_password)
			stream.bool(self.exclude_system_password)
			stream.u32(self.refer_gid)
			stream.string(self.codeword)
			stream.add(self.range)


class PlayingSession(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.gathering = None
	
	def check_required(self, settings):
		for field in ['pid', 'gathering']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.pid = stream.pid()
		self.gathering = stream.anydata()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.pid)
		stream.anydata(self.gathering)


class SimplePlayingSession(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.gid = None
		self.game_mode = None
		self.attribute = None
	
	def check_required(self, settings):
		for field in ['pid', 'gid', 'game_mode', 'attribute']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.pid = stream.pid()
		self.gid = stream.u32()
		self.game_mode = stream.u32()
		self.attribute = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.pid)
		stream.u32(self.gid)
		stream.u32(self.game_mode)
		stream.u32(self.attribute)


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
	METHOD_ADD_PARTITIPANTS = 14
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
	METHOD_MIGRATE_GATHERING_OWNERSHIP = 36
	METHOD_FIND_BY_DESCRIPTION_LIKE = 37
	METHOD_REGISTER_LOCAL_URL = 38
	METHOD_REGISTER_LOCAL_URLS = 39
	METHOD_UPDATE_SESSION_HOST_V1 = 40
	METHOD_GET_SESSION_URLS = 41
	METHOD_UPDATE_SESSION_HOST = 42
	
	PROTOCOL_ID = 0x15


class MatchmakeExtensionProtocol:
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
	METHOD_GETLST_FRIEND_NOTIFICATION_DATA = 13
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
	METHOD_GET_MY_BLACK_LIST = 24
	METHOD_ADD_TO_BLACK_LIST = 25
	METHOD_REMOVE_FROM_BLACK_LIST = 26
	METHOD_CLEAR_MY_BLACK_LIST = 27
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
	
	PROTOCOL_ID = 0x6D


class MatchMakingClient(MatchMakingProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def find_by_participants(self, pids):
		logger.info("MatchMakingClient.find_by_participants()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_FIND_BY_PARTICIPANTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_by_participants -> done")
		return gatherings
	
	def find_by_sql_query(self, query, range):
		logger.info("MatchMakingClient.find_by_sql_query()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(query)
		stream.add(range)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_FIND_BY_SQL_QUERY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gatherings = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.find_by_sql_query -> done")
		return gatherings
	
	def get_session_urls(self, gid):
		logger.info("MatchMakingClient.get_session_urls()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_SESSION_URLS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		urls = stream.list(stream.stationurl)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchMakingClient.get_session_urls -> done")
		return urls


class MatchmakeExtensionClient(MatchmakeExtensionProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def auto_matchmake_postpone(self, gathering, message):
		logger.info("MatchmakeExtensionClient.auto_matchmake_postpone()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.anydata(gathering)
		stream.string(message)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_AUTO_MATCHMAKE_POSTPONE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gathering = stream.anydata()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClient.auto_matchmake_postpone -> done")
		return gathering
	
	def create_matchmake_session(self, gathering, description, participation_count):
		logger.info("MatchmakeExtensionClient.create_matchmake_session()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.anydata(gathering)
		stream.string(description)
		stream.u16(participation_count)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_CREATE_MATCHMAKE_SESSION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.gid = stream.u32()
		obj.session_key = stream.buffer()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClient.create_matchmake_session -> done")
		return obj
	
	def join_matchmake_session(self, gid, message):
		logger.info("MatchmakeExtensionClient.join_matchmake_session()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		stream.string(message)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_JOIN_MATCHMAKE_SESSION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session_key = stream.buffer()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClient.join_matchmake_session -> done")
		return session_key
	
	def auto_matchmake_with_search_criteria_postpone(self, search_criteria, gathering, message):
		logger.info("MatchmakeExtensionClient.auto_matchmake_with_search_criteria_postpone()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(search_criteria, stream.add)
		stream.anydata(gathering)
		stream.string(message)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_AUTO_MATCHMAKE_WITH_SEARCH_CRITERIA_POSTPONE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		gathering = stream.anydata()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClient.auto_matchmake_with_search_criteria_postpone -> done")
		return gathering
	
	def get_playing_session(self, pids):
		logger.info("MatchmakeExtensionClient.get_playing_session()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_PLAYING_SESSION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		sessions = stream.list(PlayingSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClient.get_playing_session -> done")
		return sessions
	
	def get_simple_playing_session(self, pids, include_login_user):
		logger.info("MatchmakeExtensionClient.get_simple_playing_session()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		stream.bool(include_login_user)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_SIMPLE_PLAYING_SESSION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session = stream.list(SimplePlayingSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClient.get_simple_playing_session -> done")
		return session
	
	def find_matchmake_session_by_gathering_id_detail(self, gid):
		logger.info("MatchmakeExtensionClient.find_matchmake_session_by_gathering_id_detail()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(gid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_FIND_MATCHMAKE_SESSION_BY_GATHERING_ID_DETAIL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		session = stream.extract(MatchmakeSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClient.find_matchmake_session_by_gathering_id_detail -> done")
		return session
	
	def withdraw_matchmaking(self, request_id):
		logger.info("MatchmakeExtensionClient.withdraw_matchmaking()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(request_id)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_WITHDRAW_MATCHMAKING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClient.withdraw_matchmaking -> done")
	
	def withdraw_matchmaking_all(self):
		logger.info("MatchmakeExtensionClient.withdraw_matchmaking_all()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_WITHDRAW_MATCHMAKING_ALL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClient.withdraw_matchmaking_all -> done")
	
	def browse_matchmake_session_no_holder_no_result_range(self, search_criteria):
		logger.info("MatchmakeExtensionClient.browse_matchmake_session_no_holder_no_result_range()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(search_criteria)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_BROWSE_MATCHMAKE_SESSION_NO_HOLDER_NO_RESULT_RANGE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		sessions = stream.list(MatchmakeSession)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MatchmakeExtensionClient.browse_matchmake_session_no_holder_no_result_range -> done")
		return sessions


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
			self.METHOD_ADD_PARTITIPANTS: self.handle_add_partitipants,
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
			self.METHOD_MIGRATE_GATHERING_OWNERSHIP: self.handle_migrate_gathering_ownership,
			self.METHOD_FIND_BY_DESCRIPTION_LIKE: self.handle_find_by_description_like,
			self.METHOD_REGISTER_LOCAL_URL: self.handle_register_local_url,
			self.METHOD_REGISTER_LOCAL_URLS: self.handle_register_local_urls,
			self.METHOD_UPDATE_SESSION_HOST_V1: self.handle_update_session_host_v1,
			self.METHOD_GET_SESSION_URLS: self.handle_get_session_urls,
			self.METHOD_UPDATE_SESSION_HOST: self.handle_update_session_host,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_register_gathering(self, context, input, output):
		logger.warning("MatchMakingServer.register_gathering is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_unregister_gathering(self, context, input, output):
		logger.warning("MatchMakingServer.unregister_gathering is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_unregister_gatherings(self, context, input, output):
		logger.warning("MatchMakingServer.unregister_gatherings is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_gathering(self, context, input, output):
		logger.warning("MatchMakingServer.update_gathering is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_invite(self, context, input, output):
		logger.warning("MatchMakingServer.invite is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_accept_invitation(self, context, input, output):
		logger.warning("MatchMakingServer.accept_invitation is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_decline_invitation(self, context, input, output):
		logger.warning("MatchMakingServer.decline_invitation is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_cancel_invitation(self, context, input, output):
		logger.warning("MatchMakingServer.cancel_invitation is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_invitations_sent(self, context, input, output):
		logger.warning("MatchMakingServer.get_invitations_sent is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_invitations_received(self, context, input, output):
		logger.warning("MatchMakingServer.get_invitations_received is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_participate(self, context, input, output):
		logger.warning("MatchMakingServer.participate is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_cancel_participation(self, context, input, output):
		logger.warning("MatchMakingServer.cancel_participation is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_participants(self, context, input, output):
		logger.warning("MatchMakingServer.get_participants is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_add_partitipants(self, context, input, output):
		logger.warning("MatchMakingServer.add_partitipants is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_detailed_participants(self, context, input, output):
		logger.warning("MatchMakingServer.get_detailed_participants is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_participants_urls(self, context, input, output):
		logger.warning("MatchMakingServer.get_participants_urls is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_by_type(self, context, input, output):
		logger.warning("MatchMakingServer.find_by_type is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_by_description(self, context, input, output):
		logger.warning("MatchMakingServer.find_by_description is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_by_description_regex(self, context, input, output):
		logger.warning("MatchMakingServer.find_by_description_regex is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_by_id(self, context, input, output):
		logger.warning("MatchMakingServer.find_by_id is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_by_single_id(self, context, input, output):
		logger.warning("MatchMakingServer.find_by_single_id is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_by_owner(self, context, input, output):
		logger.warning("MatchMakingServer.find_by_owner is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_by_participants(self, context, input, output):
		logger.info("MatchMakingServer.find_by_participants()")
		#--- request ---
		pids = input.list(input.pid)
		response = self.find_by_participants(context, pids)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	def handle_find_invitations(self, context, input, output):
		logger.warning("MatchMakingServer.find_invitations is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_by_sql_query(self, context, input, output):
		logger.info("MatchMakingServer.find_by_sql_query()")
		#--- request ---
		query = input.string()
		range = input.extract(common.ResultRange)
		response = self.find_by_sql_query(context, query, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	def handle_launch_session(self, context, input, output):
		logger.warning("MatchMakingServer.launch_session is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_session_url(self, context, input, output):
		logger.warning("MatchMakingServer.update_session_url is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_session_url(self, context, input, output):
		logger.warning("MatchMakingServer.get_session_url is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_state(self, context, input, output):
		logger.warning("MatchMakingServer.get_state is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_set_state(self, context, input, output):
		logger.warning("MatchMakingServer.set_state is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_report_stats(self, context, input, output):
		logger.warning("MatchMakingServer.report_stats is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_stats(self, context, input, output):
		logger.warning("MatchMakingServer.get_stats is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_delete_gathering(self, context, input, output):
		logger.warning("MatchMakingServer.delete_gathering is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_pending_deletions(self, context, input, output):
		logger.warning("MatchMakingServer.get_pending_deletions is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_delete_from_deletions(self, context, input, output):
		logger.warning("MatchMakingServer.delete_from_deletions is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_migrate_gathering_ownership(self, context, input, output):
		logger.warning("MatchMakingServer.migrate_gathering_ownership is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_by_description_like(self, context, input, output):
		logger.warning("MatchMakingServer.find_by_description_like is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_register_local_url(self, context, input, output):
		logger.warning("MatchMakingServer.register_local_url is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_register_local_urls(self, context, input, output):
		logger.warning("MatchMakingServer.register_local_urls is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_session_host_v1(self, context, input, output):
		logger.warning("MatchMakingServer.update_session_host_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_session_urls(self, context, input, output):
		logger.info("MatchMakingServer.get_session_urls()")
		#--- request ---
		gid = input.u32()
		response = self.get_session_urls(context, gid)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.stationurl)
	
	def handle_update_session_host(self, context, input, output):
		logger.warning("MatchMakingServer.update_session_host is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def find_by_participants(self, *args):
		logger.warning("MatchMakingServer.find_by_participants not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def find_by_sql_query(self, *args):
		logger.warning("MatchMakingServer.find_by_sql_query not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_session_urls(self, *args):
		logger.warning("MatchMakingServer.get_session_urls not implemented")
		raise common.RMCError("Core::NotImplemented")


class MatchmakeExtensionServer(MatchmakeExtensionProtocol):
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
			self.METHOD_GETLST_FRIEND_NOTIFICATION_DATA: self.handle_getlst_friend_notification_data,
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
			self.METHOD_GET_MY_BLACK_LIST: self.handle_get_my_black_list,
			self.METHOD_ADD_TO_BLACK_LIST: self.handle_add_to_black_list,
			self.METHOD_REMOVE_FROM_BLACK_LIST: self.handle_remove_from_black_list,
			self.METHOD_CLEAR_MY_BLACK_LIST: self.handle_clear_my_black_list,
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
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_close_participation(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.close_participation is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_open_participation(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.open_participation is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_auto_matchmake_postpone(self, context, input, output):
		logger.info("MatchmakeExtensionServer.auto_matchmake_postpone()")
		#--- request ---
		gathering = input.anydata()
		message = input.string()
		response = self.auto_matchmake_postpone(context, gathering, message)
		
		#--- response ---
		if not isinstance(response, common.Data):
			raise RuntimeError("Expected common.Data, got %s" %response.__class__.__name__)
		output.anydata(response)
	
	def handle_browse_matchmake_session(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.browse_matchmake_session is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_browse_matchmake_session_with_host_urls(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.browse_matchmake_session_with_host_urls is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_create_matchmake_session(self, context, input, output):
		logger.info("MatchmakeExtensionServer.create_matchmake_session()")
		#--- request ---
		gathering = input.anydata()
		description = input.string()
		participation_count = input.u16()
		response = self.create_matchmake_session(context, gathering, description, participation_count)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['gid', 'session_key']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.u32(response.gid)
		output.buffer(response.session_key)
	
	def handle_join_matchmake_session(self, context, input, output):
		logger.info("MatchmakeExtensionServer.join_matchmake_session()")
		#--- request ---
		gid = input.u32()
		message = input.string()
		response = self.join_matchmake_session(context, gid, message)
		
		#--- response ---
		if not isinstance(response, bytes):
			raise RuntimeError("Expected bytes, got %s" %response.__class__.__name__)
		output.buffer(response)
	
	def handle_modify_current_game_attribute(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.modify_current_game_attribute is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_notification_data(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.update_notification_data is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_friend_notification_data(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.get_friend_notification_data is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_application_buffer(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.update_application_buffer is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_matchmake_session_attribute(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.update_matchmake_session_attribute is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_getlst_friend_notification_data(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.getlst_friend_notification_data is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_matchmake_session(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.update_matchmake_session is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_auto_matchmake_with_search_criteria_postpone(self, context, input, output):
		logger.info("MatchmakeExtensionServer.auto_matchmake_with_search_criteria_postpone()")
		#--- request ---
		search_criteria = input.list(MatchmakeSessionSearchCriteria)
		gathering = input.anydata()
		message = input.string()
		response = self.auto_matchmake_with_search_criteria_postpone(context, search_criteria, gathering, message)
		
		#--- response ---
		if not isinstance(response, common.Data):
			raise RuntimeError("Expected common.Data, got %s" %response.__class__.__name__)
		output.anydata(response)
	
	def handle_get_playing_session(self, context, input, output):
		logger.info("MatchmakeExtensionServer.get_playing_session()")
		#--- request ---
		pids = input.list(input.pid)
		response = self.get_playing_session(context, pids)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	def handle_create_community(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.create_community is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_community(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.update_community is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_join_community(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.join_community is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_community_by_gathering_id(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.find_community_by_gathering_id is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_official_community(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.find_official_community is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_community_by_participant(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.find_community_by_participant is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_privacy_setting(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.update_privacy_setting is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_my_black_list(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.get_my_black_list is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_add_to_black_list(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.add_to_black_list is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_remove_from_black_list(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.remove_from_black_list is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_clear_my_black_list(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.clear_my_black_list is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_report_violation(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.report_violation is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_is_violation_user(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.is_violation_user is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_join_matchmake_session_ex(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.join_matchmake_session_ex is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_simple_playing_session(self, context, input, output):
		logger.info("MatchmakeExtensionServer.get_simple_playing_session()")
		#--- request ---
		pids = input.list(input.pid)
		include_login_user = input.bool()
		response = self.get_simple_playing_session(context, pids, include_login_user)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	def handle_get_simple_community(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.get_simple_community is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_auto_matchmake_with_gathering_id_postpone(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.auto_matchmake_with_gathering_id_postpone is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_progress_score(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.update_progress_score is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_debug_notify_event(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.debug_notify_event is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_generate_matchmake_session_system_password(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.generate_matchmake_session_system_password is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_clear_matchmake_session_system_password(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.clear_matchmake_session_system_password is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_create_matchmake_session_with_param(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.create_matchmake_session_with_param is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_join_matchmake_session_with_param(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.join_matchmake_session_with_param is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_auto_matchmake_with_param_postpone(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.auto_matchmake_with_param_postpone is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_matchmake_session_by_gathering_id_detail(self, context, input, output):
		logger.info("MatchmakeExtensionServer.find_matchmake_session_by_gathering_id_detail()")
		#--- request ---
		gid = input.u32()
		response = self.find_matchmake_session_by_gathering_id_detail(context, gid)
		
		#--- response ---
		if not isinstance(response, MatchmakeSession):
			raise RuntimeError("Expected MatchmakeSession, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_browse_matchmake_session_no_holder(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.browse_matchmake_session_no_holder is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_browse_matchmake_session_with_host_urls_no_holder(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.browse_matchmake_session_with_host_urls_no_holder is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_matchmake_session_part(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.update_matchmake_session_part is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_request_matchmaking(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.request_matchmaking is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_withdraw_matchmaking(self, context, input, output):
		logger.info("MatchmakeExtensionServer.withdraw_matchmaking()")
		#--- request ---
		request_id = input.u64()
		self.withdraw_matchmaking(context, request_id)
	
	def handle_withdraw_matchmaking_all(self, context, input, output):
		logger.info("MatchmakeExtensionServer.withdraw_matchmaking_all()")
		#--- request ---
		self.withdraw_matchmaking_all(context)
	
	def handle_find_matchmake_session_by_gathering_id(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.find_matchmake_session_by_gathering_id is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_matchmake_session_by_single_gathering_id(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.find_matchmake_session_by_single_gathering_id is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_matchmake_session_by_owner(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.find_matchmake_session_by_owner is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_find_matchmake_session_by_participant(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.find_matchmake_session_by_participant is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_browse_matchmake_session_no_holder_no_result_range(self, context, input, output):
		logger.info("MatchmakeExtensionServer.browse_matchmake_session_no_holder_no_result_range()")
		#--- request ---
		search_criteria = input.extract(MatchmakeSessionSearchCriteria)
		response = self.browse_matchmake_session_no_holder_no_result_range(context, search_criteria)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	def handle_browse_matchmake_session_with_host_urls_no_holder_no_result_range(self, context, input, output):
		logger.warning("MatchmakeExtensionServer.browse_matchmake_session_with_host_urls_no_holder_no_result_range is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def auto_matchmake_postpone(self, *args):
		logger.warning("MatchmakeExtensionServer.auto_matchmake_postpone not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def create_matchmake_session(self, *args):
		logger.warning("MatchmakeExtensionServer.create_matchmake_session not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def join_matchmake_session(self, *args):
		logger.warning("MatchmakeExtensionServer.join_matchmake_session not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def auto_matchmake_with_search_criteria_postpone(self, *args):
		logger.warning("MatchmakeExtensionServer.auto_matchmake_with_search_criteria_postpone not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_playing_session(self, *args):
		logger.warning("MatchmakeExtensionServer.get_playing_session not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_simple_playing_session(self, *args):
		logger.warning("MatchmakeExtensionServer.get_simple_playing_session not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def find_matchmake_session_by_gathering_id_detail(self, *args):
		logger.warning("MatchmakeExtensionServer.find_matchmake_session_by_gathering_id_detail not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def withdraw_matchmaking(self, *args):
		logger.warning("MatchmakeExtensionServer.withdraw_matchmaking not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def withdraw_matchmaking_all(self, *args):
		logger.warning("MatchmakeExtensionServer.withdraw_matchmaking_all not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def browse_matchmake_session_no_holder_no_result_range(self, *args):
		logger.warning("MatchmakeExtensionServer.browse_matchmake_session_no_holder_no_result_range not implemented")
		raise common.RMCError("Core::NotImplemented")

