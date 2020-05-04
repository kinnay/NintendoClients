
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


class BlacklistedPrincipal(common.Data):
	def __init__(self):
		super().__init__()
		self.principal_info = PrincipalBasicInfo()
		self.game_key = GameKey()
		self.since = None
	
	def check_required(self, settings):
		for field in ['since']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.principal_info = stream.extract(PrincipalBasicInfo)
		self.game_key = stream.extract(GameKey)
		self.since = stream.datetime()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.add(self.principal_info)
		stream.add(self.game_key)
		stream.datetime(self.since)
common.DataHolder.register(BlacklistedPrincipal, "BlacklistedPrincipal")


class Comment(common.Data):
	def __init__(self):
		super().__init__()
		self.unk = None
		self.text = None
		self.changed = None
	
	def check_required(self, settings):
		for field in ['unk', 'text', 'changed']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk = stream.u8()
		self.text = stream.string()
		self.changed = stream.datetime()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u8(self.unk)
		stream.string(self.text)
		stream.datetime(self.changed)
common.DataHolder.register(Comment, "Comment")


class FriendInfo(common.Data):
	def __init__(self):
		super().__init__()
		self.nna_info = NNAInfo()
		self.presence = NintendoPresenceV2()
		self.comment = Comment()
		self.befriended = None
		self.last_online = None
		self.unk = None
	
	def check_required(self, settings):
		for field in ['befriended', 'last_online', 'unk']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.nna_info = stream.extract(NNAInfo)
		self.presence = stream.extract(NintendoPresenceV2)
		self.comment = stream.extract(Comment)
		self.befriended = stream.datetime()
		self.last_online = stream.datetime()
		self.unk = stream.u64()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.add(self.nna_info)
		stream.add(self.presence)
		stream.add(self.comment)
		stream.datetime(self.befriended)
		stream.datetime(self.last_online)
		stream.u64(self.unk)
common.DataHolder.register(FriendInfo, "FriendInfo")


class FriendRequest(common.Data):
	def __init__(self):
		super().__init__()
		self.principal_info = PrincipalBasicInfo()
		self.message = FriendRequestMessage()
		self.sent = None
	
	def check_required(self, settings):
		for field in ['sent']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.principal_info = stream.extract(PrincipalBasicInfo)
		self.message = stream.extract(FriendRequestMessage)
		self.sent = stream.datetime()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.add(self.principal_info)
		stream.add(self.message)
		stream.datetime(self.sent)
common.DataHolder.register(FriendRequest, "FriendRequest")


class FriendRequestMessage(common.Data):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
		self.unk3 = None
		self.message = None
		self.unk4 = None
		self.string = None
		self.game_key = GameKey()
		self.datetime = None
		self.expires = None
	
	def check_required(self, settings):
		for field in ['unk1', 'unk2', 'unk3', 'message', 'unk4', 'string', 'datetime', 'expires']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk1 = stream.u64()
		self.unk2 = stream.u8()
		self.unk3 = stream.u8()
		self.message = stream.string()
		self.unk4 = stream.u8()
		self.string = stream.string()
		self.game_key = stream.extract(GameKey)
		self.datetime = stream.datetime()
		self.expires = stream.datetime()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.unk1)
		stream.u8(self.unk2)
		stream.u8(self.unk3)
		stream.string(self.message)
		stream.u8(self.unk4)
		stream.string(self.string)
		stream.add(self.game_key)
		stream.datetime(self.datetime)
		stream.datetime(self.expires)
common.DataHolder.register(FriendRequestMessage, "FriendRequestMessage")


class GameKey(common.Data):
	def __init__(self):
		super().__init__()
		self.title_id = 0
		self.title_version = 0
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		self.title_id = stream.u64()
		self.title_version = stream.u16()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.title_id)
		stream.u16(self.title_version)
common.DataHolder.register(GameKey, "GameKey")


class MiiV2(common.Data):
	def __init__(self):
		super().__init__()
		self.name = None
		self.unk1 = 0
		self.unk2 = 0
		self.data = None
		self.datetime = common.DateTime(0)
	
	def check_required(self, settings):
		for field in ['name', 'data']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.name = stream.string()
		self.unk1 = stream.u8()
		self.unk2 = stream.u8()
		self.data = stream.buffer()
		self.datetime = stream.datetime()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.string(self.name)
		stream.u8(self.unk1)
		stream.u8(self.unk2)
		stream.buffer(self.data)
		stream.datetime(self.datetime)
common.DataHolder.register(MiiV2, "MiiV2")


class NNAInfo(common.Data):
	def __init__(self):
		super().__init__()
		self.principal_info = PrincipalBasicInfo()
		self.unk1 = 94
		self.unk2 = 11
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		self.principal_info = stream.extract(PrincipalBasicInfo)
		self.unk1 = stream.u8()
		self.unk2 = stream.u8()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.add(self.principal_info)
		stream.u8(self.unk1)
		stream.u8(self.unk2)
common.DataHolder.register(NNAInfo, "NNAInfo")


class NintendoCreateAccountData(common.Data):
	def __init__(self):
		super().__init__()
		self.info = NNAInfo()
		self.token = None
		self.birthday = None
		self.unk = None
	
	def check_required(self, settings):
		for field in ['token', 'birthday', 'unk']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.info = stream.extract(NNAInfo)
		self.token = stream.string()
		self.birthday = stream.datetime()
		self.unk = stream.u64()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.add(self.info)
		stream.string(self.token)
		stream.datetime(self.birthday)
		stream.u64(self.unk)
common.DataHolder.register(NintendoCreateAccountData, "NintendoCreateAccountData")


class NintendoPresenceV2(common.Data):
	def __init__(self):
		super().__init__()
		self.flags = 0
		self.is_online = False
		self.game_key = GameKey()
		self.unk1 = 0
		self.message = ""
		self.unk2 = 0
		self.unk3 = 0
		self.game_server_id = 0
		self.unk4 = 0
		self.pid = 0
		self.gathering_id = 0
		self.application_data = b""
		self.unk5 = 3
		self.unk6 = 3
		self.unk7 = 3
	
	def check_required(self, settings):
		pass
	
	def load(self, stream):
		self.flags = stream.u32()
		self.is_online = stream.bool()
		self.game_key = stream.extract(GameKey)
		self.unk1 = stream.u8()
		self.message = stream.string()
		self.unk2 = stream.u32()
		self.unk3 = stream.u8()
		self.game_server_id = stream.u32()
		self.unk4 = stream.u32()
		self.pid = stream.u32()
		self.gathering_id = stream.u32()
		self.application_data = stream.buffer()
		self.unk5 = stream.u8()
		self.unk6 = stream.u8()
		self.unk7 = stream.u8()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.flags)
		stream.bool(self.is_online)
		stream.add(self.game_key)
		stream.u8(self.unk1)
		stream.string(self.message)
		stream.u32(self.unk2)
		stream.u8(self.unk3)
		stream.u32(self.game_server_id)
		stream.u32(self.unk4)
		stream.u32(self.pid)
		stream.u32(self.gathering_id)
		stream.buffer(self.application_data)
		stream.u8(self.unk5)
		stream.u8(self.unk6)
		stream.u8(self.unk7)
common.DataHolder.register(NintendoPresenceV2, "NintendoPresenceV2")


class PersistentNotification(common.Data):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
		self.unk3 = None
		self.unk4 = None
		self.string = None
	
	def check_required(self, settings):
		for field in ['unk1', 'unk2', 'unk3', 'unk4', 'string']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unk1 = stream.u64()
		self.unk2 = stream.u32()
		self.unk3 = stream.u32()
		self.unk4 = stream.u32()
		self.string = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.unk1)
		stream.u32(self.unk2)
		stream.u32(self.unk3)
		stream.u32(self.unk4)
		stream.string(self.string)
common.DataHolder.register(PersistentNotification, "PersistentNotification")


class PrincipalBasicInfo(common.Data):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.nnid = None
		self.mii = MiiV2()
		self.unk = 2
	
	def check_required(self, settings):
		for field in ['pid', 'nnid']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.pid = stream.pid()
		self.nnid = stream.string()
		self.mii = stream.extract(MiiV2)
		self.unk = stream.u8()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.pid)
		stream.string(self.nnid)
		stream.add(self.mii)
		stream.u8(self.unk)
common.DataHolder.register(PrincipalBasicInfo, "PrincipalBasicInfo")


class PrincipalPreference(common.Data):
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
		self.unk1 = stream.bool()
		self.unk2 = stream.bool()
		self.unk3 = stream.bool()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.bool(self.unk1)
		stream.bool(self.unk2)
		stream.bool(self.unk3)
common.DataHolder.register(PrincipalPreference, "PrincipalPreference")


class FriendsProtocol:
	METHOD_GET_ALL_INFORMATION = 1
	METHOD_ADD_FRIEND = 2
	METHOD_ADD_FRIEND_BY_NAME = 3
	METHOD_REMOVE_FRIEND = 4
	METHOD_ADD_FRIEND_REQUEST = 5
	METHOD_CANCEL_FRIEND_REQUEST = 6
	METHOD_ACCEPT_FRIEND_REQUEST = 7
	METHOD_DELETE_FRIEND_REQUEST = 8
	METHOD_DENY_FRIEND_REQUEST = 9
	METHOD_MARK_FRIEND_REQUESTS_AS_RECEIVED = 10
	METHOD_ADD_BLACK_LIST = 11
	METHOD_REMOVE_BLACK_LIST = 12
	METHOD_UPDATE_PRESENCE = 13
	METHOD_UPDATE_MII = 14
	METHOD_UPDATE_COMMENT = 15
	METHOD_UPDATE_PREFERENCE = 16
	METHOD_GET_BASIC_INFO = 17
	METHOD_DELETE_FRIEND_FLAGS = 18
	METHOD_CHECK_SETTING_STATUS = 19
	METHOD_GET_REQUEST_BLOCK_SETTINGS = 20
	
	PROTOCOL_ID = 0x66


class FriendsClient(FriendsProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def get_all_information(self, nna_info, presence, birthday):
		logger.info("FriendsClient.get_all_information()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(nna_info)
		stream.add(presence)
		stream.datetime(birthday)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_ALL_INFORMATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.principal_preference = stream.extract(PrincipalPreference)
		obj.comment = stream.extract(Comment)
		obj.friends = stream.list(FriendInfo)
		obj.sent_requests = stream.list(FriendRequest)
		obj.received_requests = stream.list(FriendRequest)
		obj.blacklist = stream.list(BlacklistedPrincipal)
		obj.unk1 = stream.bool()
		obj.notifications = stream.list(PersistentNotification)
		obj.unk2 = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClient.get_all_information -> done")
		return obj
	
	def update_presence(self, presence):
		logger.info("FriendsClient.update_presence()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(presence)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_UPDATE_PRESENCE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClient.update_presence -> done")


class FriendsServer(FriendsProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_GET_ALL_INFORMATION: self.handle_get_all_information,
			self.METHOD_ADD_FRIEND: self.handle_add_friend,
			self.METHOD_ADD_FRIEND_BY_NAME: self.handle_add_friend_by_name,
			self.METHOD_REMOVE_FRIEND: self.handle_remove_friend,
			self.METHOD_ADD_FRIEND_REQUEST: self.handle_add_friend_request,
			self.METHOD_CANCEL_FRIEND_REQUEST: self.handle_cancel_friend_request,
			self.METHOD_ACCEPT_FRIEND_REQUEST: self.handle_accept_friend_request,
			self.METHOD_DELETE_FRIEND_REQUEST: self.handle_delete_friend_request,
			self.METHOD_DENY_FRIEND_REQUEST: self.handle_deny_friend_request,
			self.METHOD_MARK_FRIEND_REQUESTS_AS_RECEIVED: self.handle_mark_friend_requests_as_received,
			self.METHOD_ADD_BLACK_LIST: self.handle_add_black_list,
			self.METHOD_REMOVE_BLACK_LIST: self.handle_remove_black_list,
			self.METHOD_UPDATE_PRESENCE: self.handle_update_presence,
			self.METHOD_UPDATE_MII: self.handle_update_mii,
			self.METHOD_UPDATE_COMMENT: self.handle_update_comment,
			self.METHOD_UPDATE_PREFERENCE: self.handle_update_preference,
			self.METHOD_GET_BASIC_INFO: self.handle_get_basic_info,
			self.METHOD_DELETE_FRIEND_FLAGS: self.handle_delete_friend_flags,
			self.METHOD_CHECK_SETTING_STATUS: self.handle_check_setting_status,
			self.METHOD_GET_REQUEST_BLOCK_SETTINGS: self.handle_get_request_block_settings,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_get_all_information(self, context, input, output):
		logger.info("FriendsServer.get_all_information()")
		#--- request ---
		nna_info = input.extract(NNAInfo)
		presence = input.extract(NintendoPresenceV2)
		birthday = input.datetime()
		response = self.get_all_information(context, nna_info, presence, birthday)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['principal_preference', 'comment', 'friends', 'sent_requests', 'received_requests', 'blacklist', 'unk1', 'notifications', 'unk2']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.add(response.principal_preference)
		output.add(response.comment)
		output.list(response.friends, output.add)
		output.list(response.sent_requests, output.add)
		output.list(response.received_requests, output.add)
		output.list(response.blacklist, output.add)
		output.bool(response.unk1)
		output.list(response.notifications, output.add)
		output.bool(response.unk2)
	
	def handle_add_friend(self, context, input, output):
		logger.warning("FriendsServer.add_friend is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_add_friend_by_name(self, context, input, output):
		logger.warning("FriendsServer.add_friend_by_name is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_remove_friend(self, context, input, output):
		logger.warning("FriendsServer.remove_friend is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_add_friend_request(self, context, input, output):
		logger.warning("FriendsServer.add_friend_request is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_cancel_friend_request(self, context, input, output):
		logger.warning("FriendsServer.cancel_friend_request is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_accept_friend_request(self, context, input, output):
		logger.warning("FriendsServer.accept_friend_request is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_delete_friend_request(self, context, input, output):
		logger.warning("FriendsServer.delete_friend_request is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_deny_friend_request(self, context, input, output):
		logger.warning("FriendsServer.deny_friend_request is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_mark_friend_requests_as_received(self, context, input, output):
		logger.warning("FriendsServer.mark_friend_requests_as_received is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_add_black_list(self, context, input, output):
		logger.warning("FriendsServer.add_black_list is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_remove_black_list(self, context, input, output):
		logger.warning("FriendsServer.remove_black_list is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_presence(self, context, input, output):
		logger.info("FriendsServer.update_presence()")
		#--- request ---
		presence = input.extract(NintendoPresenceV2)
		self.update_presence(context, presence)
	
	def handle_update_mii(self, context, input, output):
		logger.warning("FriendsServer.update_mii is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_comment(self, context, input, output):
		logger.warning("FriendsServer.update_comment is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_update_preference(self, context, input, output):
		logger.warning("FriendsServer.update_preference is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_basic_info(self, context, input, output):
		logger.warning("FriendsServer.get_basic_info is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_delete_friend_flags(self, context, input, output):
		logger.warning("FriendsServer.delete_friend_flags is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_check_setting_status(self, context, input, output):
		logger.warning("FriendsServer.check_setting_status is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_request_block_settings(self, context, input, output):
		logger.warning("FriendsServer.get_request_block_settings is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def get_all_information(self, *args):
		logger.warning("FriendsServer.get_all_information not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def update_presence(self, *args):
		logger.warning("FriendsServer.update_presence not implemented")
		raise common.RMCError("Core::NotImplemented")

