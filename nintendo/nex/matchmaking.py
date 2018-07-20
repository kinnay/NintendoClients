
from nintendo.nex import common

import logging
logger = logging.getLogger(__name__)


class MatchMakingClient:

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
	METHOD_MIGRATE_GATHERING_OWNERSHIP = 36
	METHOD_FIND_BY_DESCRIPTION_LIKE = 37
	METHOD_REGISTER_LOCAL_URL = 38
	METHOD_REGISTER_LOCAL_URLS = 39
	METHOD_UPDATE_SESSION_HOST = 40
	METHOD_GET_SESSION_URLS = 41
	METHOD_UPDATE_SESSION_HOST = 42

	PROTOCOL_ID = 0x15

	def __init__(self, backend):
		self.client = backend.secure_client
		
	def find_by_sql_query(self, query, result_range):
		logger.info("MatchMaking.find_by_sql_query(%s, [%i, %i])", query, result_range.offset, result_range.size)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_FIND_BY_SQL_QUERY)
		stream.string(query)
		stream.add(result_range)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		gatherings = stream.list(stream.anydata)
		logger.info("MatchMaking.find_by_sql_query -> %i results", len(gatherings))
		return gatherings
		
	def get_session_url(self, gid):
		logger.info("MatchMaking.get_session_url(%08X)", gid)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_SESSION_URL)
		stream.u32(gid)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		result = stream.bool()
		url = stream.string()
		logger.info("MatchMaking.get_session_url -> (%i, %s)", result, url)
		return result, url
		
	def get_session_urls(self, gid):
		logger.info("MatchMaking.get_session_urls(%08X)", gid)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_SESSION_URLS)
		stream.u32(gid)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		urls = stream.list(stream.stationurl)
		logger.info("MatchMaking.get_session_urls -> %s", urls)
		return urls
