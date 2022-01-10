
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class MyProfile(common.Structure):
	def __init__(self):
		super().__init__()
		self.region = None
		self.country = None
		self.area = None
		self.language = None
		self.platform = None
		self.unk1 = None
		self.unk2 = None
		self.unk3 = None
	
	def check_required(self, settings, version):
		for field in ['region', 'country', 'area', 'language', 'platform', 'unk1', 'unk2', 'unk3']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.region = stream.u8()
		self.country = stream.u8()
		self.area = stream.u8()
		self.language = stream.u8()
		self.platform = stream.u8()
		self.unk1 = stream.u64()
		self.unk2 = stream.string()
		self.unk3 = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u8(self.region)
		stream.u8(self.country)
		stream.u8(self.area)
		stream.u8(self.language)
		stream.u8(self.platform)
		stream.u64(self.unk1)
		stream.string(self.unk2)
		stream.string(self.unk3)


class Mii(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
		self.unk3 = None
		self.mii_data = None
	
	def check_required(self, settings, version):
		for field in ['unk1', 'unk2', 'unk3', 'mii_data']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.unk1 = stream.string()
		self.unk2 = stream.bool()
		self.unk3 = stream.u8()
		self.mii_data = stream.buffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.string(self.unk1)
		stream.bool(self.unk2)
		stream.u8(self.unk3)
		stream.buffer(self.mii_data)


class MiiList(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
		self.unk3 = None
		self.mii_datas = None
	
	def check_required(self, settings, version):
		for field in ['unk1', 'unk2', 'unk3', 'mii_datas']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.unk1 = stream.string()
		self.unk2 = stream.bool()
		self.unk3 = stream.u8()
		self.mii_datas = stream.list(stream.buffer)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.string(self.unk1)
		stream.bool(self.unk2)
		stream.u8(self.unk3)
		stream.list(self.mii_datas, stream.buffer)


class PlayedGame(common.Structure):
	def __init__(self):
		super().__init__()
		self.game_key = GameKey()
		self.datetime = None
	
	def check_required(self, settings, version):
		for field in ['datetime']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.game_key = stream.extract(GameKey)
		self.datetime = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.add(self.game_key)
		stream.datetime(self.datetime)


class GameKey(common.Data):
	def __init__(self):
		super().__init__()
		self.title_id = 0
		self.title_version = 0
	
	def check_required(self, settings, version):
		pass
	
	def load(self, stream, version):
		self.title_id = stream.u64()
		self.title_version = stream.u16()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.title_id)
		stream.u16(self.title_version)
common.DataHolder.register(GameKey, "GameKey")


class FriendMiiRequest(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
	
	def check_required(self, settings, version):
		for field in ['unk1', 'unk2']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.unk1 = stream.u32()
		self.unk2 = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.unk1)
		stream.datetime(self.unk2)


class FriendMii(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.mii = Mii()
		self.unk2 = None
	
	def check_required(self, settings, version):
		for field in ['unk1', 'unk2']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.unk1 = stream.u32()
		self.mii = stream.extract(Mii)
		self.unk2 = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.unk1)
		stream.add(self.mii)
		stream.datetime(self.unk2)


class FriendMiiList(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.mii = MiiList()
		self.unk2 = None
	
	def check_required(self, settings, version):
		for field in ['unk1', 'unk2']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.unk1 = stream.u32()
		self.mii = stream.extract(MiiList)
		self.unk2 = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.unk1)
		stream.add(self.mii)
		stream.datetime(self.unk2)


class FriendRelationship(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk1 = None
		self.unk2 = None
		self.unk3 = None
	
	def check_required(self, settings, version):
		for field in ['unk1', 'unk2', 'unk3']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.unk1 = stream.u32()
		self.unk2 = stream.u64()
		self.unk3 = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.unk1)
		stream.u64(self.unk2)
		stream.u8(self.unk3)


class NintendoPresence(common.Structure):
	def __init__(self):
		super().__init__()
		self.changed_bit_flag = None
		self.game_key = GameKey()
		self.game_mode_description = None
		self.join_availability_flag = None
		self.matchmake_system_type = None
		self.join_game_id = None
		self.join_game_mode = None
		self.owner_pid = None
		self.join_group_id = None
		self.application_data = None
	
	def check_required(self, settings, version):
		for field in ['changed_bit_flag', 'game_mode_description', 'join_availability_flag', 'matchmake_system_type', 'join_game_id', 'join_game_mode', 'owner_pid', 'join_group_id', 'application_data']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.changed_bit_flag = stream.u32()
		self.game_key = stream.extract(GameKey)
		self.game_mode_description = stream.string()
		self.join_availability_flag = stream.u32()
		self.matchmake_system_type = stream.u8()
		self.join_game_id = stream.u32()
		self.join_game_mode = stream.u32()
		self.owner_pid = stream.pid()
		self.join_group_id = stream.u32()
		self.application_data = stream.buffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.changed_bit_flag)
		stream.add(self.game_key)
		stream.string(self.game_mode_description)
		stream.u32(self.join_availability_flag)
		stream.u8(self.matchmake_system_type)
		stream.u32(self.join_game_id)
		stream.u32(self.join_game_mode)
		stream.pid(self.owner_pid)
		stream.u32(self.join_group_id)
		stream.buffer(self.application_data)


class FriendPresence(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk = None
		self.presence = NintendoPresence()
	
	def check_required(self, settings, version):
		for field in ['unk']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.unk = stream.u32()
		self.presence = stream.extract(NintendoPresence)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.unk)
		stream.add(self.presence)


class FriendPicture(common.Structure):
	def __init__(self):
		super().__init__()
		self.unk = None
		self.data = None
		self.datetime = None
	
	def check_required(self, settings, version):
		for field in ['unk', 'data', 'datetime']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.unk = stream.u32()
		self.data = stream.buffer()
		self.datetime = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.unk)
		stream.buffer(self.data)
		stream.datetime(self.datetime)


class FriendPersistentInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.region = None
		self.country = None
		self.area = None
		self.language = None
		self.platform = None
		self.game_key = GameKey()
		self.message = None
		self.message_updated = None
		self.friended = None
		self.unk = None
	
	def check_required(self, settings, version):
		for field in ['pid', 'region', 'country', 'area', 'language', 'platform', 'message', 'message_updated', 'friended', 'unk']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.pid = stream.pid()
		self.region = stream.u8()
		self.country = stream.u8()
		self.area = stream.u8()
		self.language = stream.u8()
		self.platform = stream.u8()
		self.game_key = stream.extract(GameKey)
		self.message = stream.string()
		self.message_updated = stream.datetime()
		self.friended = stream.datetime()
		self.unk = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.pid)
		stream.u8(self.region)
		stream.u8(self.country)
		stream.u8(self.area)
		stream.u8(self.language)
		stream.u8(self.platform)
		stream.add(self.game_key)
		stream.string(self.message)
		stream.datetime(self.message_updated)
		stream.datetime(self.friended)
		stream.datetime(self.unk)


class FriendsProtocolV1:
	METHOD_UPDATE_PROFILE = 1
	METHOD_UPDATE_MII = 2
	METHOD_UPDATE_MII_LIST = 3
	METHOD_UPDATE_PLAYED_GAMES = 4
	METHOD_UPDATE_PREFERENCE = 5
	METHOD_GET_FRIEND_MII = 6
	METHOD_GET_FRIEND_MII_LIST = 7
	METHOD_GET_FRIEND_RELATIONSHIPS = 10
	METHOD_ADD_FRIEND_BY_PRINCIPAL_ID = 11
	METHOD_GET_ALL_FRIENDS = 15
	METHOD_SYNC_FRIEND = 17
	METHOD_UPDATE_PRESENCE = 18
	METHOD_UPDATE_FAVORITE_GAME_KEY = 19
	METHOD_UPDATE_COMMENT = 20
	METHOD_GET_FRIEND_PRESENCE = 22
	METHOD_GET_FRIEND_PICTURE = 24
	METHOD_GET_FRIEND_PERSISTENT_INFO = 25
	METHOD_SEND_INVITATION = 26
	
	PROTOCOL_ID = 0x65


class FriendsClientV1(FriendsProtocolV1):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def update_profile(self, profile_data):
		logger.info("FriendsClientV1.update_profile()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(profile_data)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_PROFILE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.update_profile -> done")
	
	async def update_mii(self, mii):
		logger.info("FriendsClientV1.update_mii()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(mii)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_MII, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.update_mii -> done")
	
	async def update_mii_list(self, mii_list):
		logger.info("FriendsClientV1.update_mii_list()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(mii_list)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_MII_LIST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.update_mii_list -> done")
	
	async def update_played_games(self, played_games):
		logger.info("FriendsClientV1.update_played_games()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(played_games, stream.add)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_PLAYED_GAMES, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.update_played_games -> done")
	
	async def update_preference(self, unk1, unk2, unk3):
		logger.info("FriendsClientV1.update_preference()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.bool(unk1)
		stream.bool(unk2)
		stream.bool(unk3)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_PREFERENCE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.update_preference -> done")
	
	async def get_friend_mii(self, friends):
		logger.info("FriendsClientV1.get_friend_mii()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(friends, stream.add)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_FRIEND_MII, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		miis = stream.list(FriendMii)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.get_friend_mii -> done")
		return miis
	
	async def get_friend_mii_list(self, friends):
		logger.info("FriendsClientV1.get_friend_mii_list()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(friends, stream.add)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_FRIEND_MII_LIST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		mii_lists = stream.list(FriendMiiList)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.get_friend_mii_list -> done")
		return mii_lists
	
	async def get_friend_relationships(self, unk):
		logger.info("FriendsClientV1.get_friend_relationships()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(unk, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_FRIEND_RELATIONSHIPS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		friend_relationships = stream.list(FriendRelationship)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.get_friend_relationships -> done")
		return friend_relationships
	
	async def add_friend_by_principal_id(self, unk, pid):
		logger.info("FriendsClientV1.add_friend_by_principal_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(unk)
		stream.u32(pid)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_ADD_FRIEND_BY_PRINCIPAL_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		friend_relationship = stream.extract(FriendRelationship)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.add_friend_by_principal_id -> done")
		return friend_relationship
	
	async def get_all_friends(self):
		logger.info("FriendsClientV1.get_all_friends()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_ALL_FRIENDS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		friend_relationships = stream.list(FriendRelationship)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.get_all_friends -> done")
		return friend_relationships
	
	async def sync_friend(self, unk1, unk2, unk3):
		logger.info("FriendsClientV1.sync_friend()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(unk1)
		stream.list(unk2, stream.u32)
		stream.list(unk3, stream.u64)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_SYNC_FRIEND, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		friend_list = stream.list(FriendRelationship)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.sync_friend -> done")
		return friend_list
	
	async def update_presence(self, presence_info, unk):
		logger.info("FriendsClientV1.update_presence()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(presence_info)
		stream.bool(unk)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_PRESENCE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.update_presence -> done")
	
	async def update_favorite_game_key(self, game_key):
		logger.info("FriendsClientV1.update_favorite_game_key()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(game_key)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_FAVORITE_GAME_KEY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.update_favorite_game_key -> done")
	
	async def update_comment(self, comment):
		logger.info("FriendsClientV1.update_comment()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(comment)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UPDATE_COMMENT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.update_comment -> done")
	
	async def get_friend_presence(self, unk):
		logger.info("FriendsClientV1.get_friend_presence()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(unk, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_FRIEND_PRESENCE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		friend_presence_list = stream.list(FriendPresence)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.get_friend_presence -> done")
		return friend_presence_list
	
	async def get_friend_picture(self, unk):
		logger.info("FriendsClientV1.get_friend_picture()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(unk, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_FRIEND_PICTURE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		friend_pictures = stream.list(FriendPicture)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.get_friend_picture -> done")
		return friend_pictures
	
	async def get_friend_persistent_info(self, unk):
		logger.info("FriendsClientV1.get_friend_persistent_info()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(unk, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_FRIEND_PERSISTENT_INFO, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		persistent_infos = stream.list(FriendPersistentInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.get_friend_persistent_info -> done")
		return persistent_infos
	
	async def send_invitation(self, unk):
		logger.info("FriendsClientV1.send_invitation()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(unk, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_SEND_INVITATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("FriendsClientV1.send_invitation -> done")


class FriendsServerV1(FriendsProtocolV1):
	def __init__(self):
		self.methods = {
			self.METHOD_UPDATE_PROFILE: self.handle_update_profile,
			self.METHOD_UPDATE_MII: self.handle_update_mii,
			self.METHOD_UPDATE_MII_LIST: self.handle_update_mii_list,
			self.METHOD_UPDATE_PLAYED_GAMES: self.handle_update_played_games,
			self.METHOD_UPDATE_PREFERENCE: self.handle_update_preference,
			self.METHOD_GET_FRIEND_MII: self.handle_get_friend_mii,
			self.METHOD_GET_FRIEND_MII_LIST: self.handle_get_friend_mii_list,
			self.METHOD_GET_FRIEND_RELATIONSHIPS: self.handle_get_friend_relationships,
			self.METHOD_ADD_FRIEND_BY_PRINCIPAL_ID: self.handle_add_friend_by_principal_id,
			self.METHOD_GET_ALL_FRIENDS: self.handle_get_all_friends,
			self.METHOD_SYNC_FRIEND: self.handle_sync_friend,
			self.METHOD_UPDATE_PRESENCE: self.handle_update_presence,
			self.METHOD_UPDATE_FAVORITE_GAME_KEY: self.handle_update_favorite_game_key,
			self.METHOD_UPDATE_COMMENT: self.handle_update_comment,
			self.METHOD_GET_FRIEND_PRESENCE: self.handle_get_friend_presence,
			self.METHOD_GET_FRIEND_PICTURE: self.handle_get_friend_picture,
			self.METHOD_GET_FRIEND_PERSISTENT_INFO: self.handle_get_friend_persistent_info,
			self.METHOD_SEND_INVITATION: self.handle_send_invitation,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on FriendsServerV1: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_update_profile(self, client, input, output):
		logger.info("FriendsServerV1.update_profile()")
		#--- request ---
		profile_data = input.extract(MyProfile)
		await self.update_profile(client, profile_data)
	
	async def handle_update_mii(self, client, input, output):
		logger.info("FriendsServerV1.update_mii()")
		#--- request ---
		mii = input.extract(Mii)
		await self.update_mii(client, mii)
	
	async def handle_update_mii_list(self, client, input, output):
		logger.info("FriendsServerV1.update_mii_list()")
		#--- request ---
		mii_list = input.extract(MiiList)
		await self.update_mii_list(client, mii_list)
	
	async def handle_update_played_games(self, client, input, output):
		logger.info("FriendsServerV1.update_played_games()")
		#--- request ---
		played_games = input.list(PlayedGame)
		await self.update_played_games(client, played_games)
	
	async def handle_update_preference(self, client, input, output):
		logger.info("FriendsServerV1.update_preference()")
		#--- request ---
		unk1 = input.bool()
		unk2 = input.bool()
		unk3 = input.bool()
		await self.update_preference(client, unk1, unk2, unk3)
	
	async def handle_get_friend_mii(self, client, input, output):
		logger.info("FriendsServerV1.get_friend_mii()")
		#--- request ---
		friends = input.list(FriendMiiRequest)
		response = await self.get_friend_mii(client, friends)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_friend_mii_list(self, client, input, output):
		logger.info("FriendsServerV1.get_friend_mii_list()")
		#--- request ---
		friends = input.list(FriendMiiRequest)
		response = await self.get_friend_mii_list(client, friends)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_friend_relationships(self, client, input, output):
		logger.info("FriendsServerV1.get_friend_relationships()")
		#--- request ---
		unk = input.list(input.u32)
		response = await self.get_friend_relationships(client, unk)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_add_friend_by_principal_id(self, client, input, output):
		logger.info("FriendsServerV1.add_friend_by_principal_id()")
		#--- request ---
		unk = input.u64()
		pid = input.u32()
		response = await self.add_friend_by_principal_id(client, unk, pid)
		
		#--- response ---
		if not isinstance(response, FriendRelationship):
			raise RuntimeError("Expected FriendRelationship, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_all_friends(self, client, input, output):
		logger.info("FriendsServerV1.get_all_friends()")
		#--- request ---
		response = await self.get_all_friends(client)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_sync_friend(self, client, input, output):
		logger.info("FriendsServerV1.sync_friend()")
		#--- request ---
		unk1 = input.u64()
		unk2 = input.list(input.u32)
		unk3 = input.list(input.u64)
		response = await self.sync_friend(client, unk1, unk2, unk3)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_update_presence(self, client, input, output):
		logger.info("FriendsServerV1.update_presence()")
		#--- request ---
		presence_info = input.extract(NintendoPresence)
		unk = input.bool()
		await self.update_presence(client, presence_info, unk)
	
	async def handle_update_favorite_game_key(self, client, input, output):
		logger.info("FriendsServerV1.update_favorite_game_key()")
		#--- request ---
		game_key = input.extract(GameKey)
		await self.update_favorite_game_key(client, game_key)
	
	async def handle_update_comment(self, client, input, output):
		logger.info("FriendsServerV1.update_comment()")
		#--- request ---
		comment = input.string()
		await self.update_comment(client, comment)
	
	async def handle_get_friend_presence(self, client, input, output):
		logger.info("FriendsServerV1.get_friend_presence()")
		#--- request ---
		unk = input.list(input.u32)
		response = await self.get_friend_presence(client, unk)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_friend_picture(self, client, input, output):
		logger.info("FriendsServerV1.get_friend_picture()")
		#--- request ---
		unk = input.list(input.u32)
		response = await self.get_friend_picture(client, unk)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_friend_persistent_info(self, client, input, output):
		logger.info("FriendsServerV1.get_friend_persistent_info()")
		#--- request ---
		unk = input.list(input.u32)
		response = await self.get_friend_persistent_info(client, unk)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_send_invitation(self, client, input, output):
		logger.info("FriendsServerV1.send_invitation()")
		#--- request ---
		unk = input.list(input.u32)
		await self.send_invitation(client, unk)
	
	async def update_profile(self, *args):
		logger.warning("FriendsServerV1.update_profile not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_mii(self, *args):
		logger.warning("FriendsServerV1.update_mii not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_mii_list(self, *args):
		logger.warning("FriendsServerV1.update_mii_list not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_played_games(self, *args):
		logger.warning("FriendsServerV1.update_played_games not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_preference(self, *args):
		logger.warning("FriendsServerV1.update_preference not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_friend_mii(self, *args):
		logger.warning("FriendsServerV1.get_friend_mii not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_friend_mii_list(self, *args):
		logger.warning("FriendsServerV1.get_friend_mii_list not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_friend_relationships(self, *args):
		logger.warning("FriendsServerV1.get_friend_relationships not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def add_friend_by_principal_id(self, *args):
		logger.warning("FriendsServerV1.add_friend_by_principal_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_all_friends(self, *args):
		logger.warning("FriendsServerV1.get_all_friends not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def sync_friend(self, *args):
		logger.warning("FriendsServerV1.sync_friend not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_presence(self, *args):
		logger.warning("FriendsServerV1.update_presence not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_favorite_game_key(self, *args):
		logger.warning("FriendsServerV1.update_favorite_game_key not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def update_comment(self, *args):
		logger.warning("FriendsServerV1.update_comment not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_friend_presence(self, *args):
		logger.warning("FriendsServerV1.get_friend_presence not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_friend_picture(self, *args):
		logger.warning("FriendsServerV1.get_friend_picture not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_friend_persistent_info(self, *args):
		logger.warning("FriendsServerV1.get_friend_persistent_info not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def send_invitation(self, *args):
		logger.warning("FriendsServerV1.send_invitation not implemented")
		raise common.RMCError("Core::NotImplemented")

