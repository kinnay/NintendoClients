
#This might be the 3DS version of the protocol, but until
#I'm sure about that I'm calling it the "friends" protocol,
#since it's only used by IOSU for friend services on Wii U

from nintendo.nex.common import NexEncoder, NexDataEncoder, DateTime
from nintendo.nex.service import ServiceClient
from nintendo.miis import MiiData

import logging
logger = logging.getLogger(__name__)


class FriendsTitle:
	TITLE_ID_EUR = 0x10001C00
	TITLE_ID_USA = 0x10001C00
	TITLE_ID_JAP = 0x10001C00
	LATEST_VERSION = 0
	
	GAME_SERVER_ID = 0x3200
	ACCESS_KEY = "ridfebb9"
	NEX_VERSION = 0

	
class MiiV2(NexDataEncoder):
	def init(self, name, unk1, unk2, data, datetime):
		self.name = name
		self.unk1 = unk1
		self.unk2 = unk2
		self.data = data
		self.datetime = datetime

	def get_name(self):
		return "MiiV2"
		
	def encode_old(self, stream):
		stream.string(self.name)
		stream.u8(self.unk1)
		stream.u8(self.unk2)
		stream.data(self.data.build())
		stream.u64(self.datetime.value)
	
	def decode_old(self, stream):
		self.name = stream.string()
		self.unk1 = stream.u8()
		self.unk2 = stream.u8()
		self.data = MiiData.parse(stream.data())
		self.datetime = DateTime(stream.u64())
		

	
class PrincipalBasicInfo(NexDataEncoder):
	def init(self, pid, nnid, mii, unk):
		self.pid = pid
		self.nnid = nnid
		self.mii = mii
		self.unk = unk

	def get_name(self):
		return "PrincipalBasicInfo"

	def encode_old(self, stream):	
		stream.u32(self.pid)
		stream.string(self.nnid)
		self.mii.encode(stream)
		stream.u8(self.unk)
		
	def decode_old(self, stream):
		self.pid = stream.u32()
		self.nnid = stream.string()
		self.mii = MiiV2.from_stream(stream)
		self.unk = stream.u8()
	
	
class NNAInfo(NexDataEncoder):
	def init(self, principal_info, unk1, unk2):
		self.principal_info = principal_info
		self.unk1 = unk1
		self.unk2 = unk2

	def get_name(self):
		return "NNAInfo"

	def encode_old(self, stream):	
		self.principal_info.encode(stream)
		stream.u8(self.unk1)
		stream.u8(self.unk2)
		
	def decode_old(self, stream):
		self.principal_info = PrincipalBasicInfo.from_stream(stream)
		self.unk1 = stream.u8()
		self.unk2 = stream.u8()
		
		
class GameKey(NexDataEncoder):
	def init(self, title_id, title_version):
		self.title_id = title_id
		self.title_version = title_version
		
	def encode_old(self, stream):
		stream.u64(self.title_id)
		stream.u16(self.title_version)
		
	def decode_old(self, stream):
		self.title_id = stream.u64()
		self.title_version = stream.u16()
		
		
class NintendoPresenceV2(NexDataEncoder):
	def init(self, unk1, is_online, game_key, unk3, string, unk4, unk5, game_server_id, unk7, unk8, unk9, data, unk10, unk11, unk12):
		self.unk1 = unk1
		self.is_online = is_online
		self.game_key = game_key
		self.unk3 = unk3
		self.string = string
		self.unk4 = unk4
		self.unk5 = unk5
		self.game_server_id = game_server_id
		self.unk7 = unk7
		self.unk8 = unk8
		self.unk9 = unk9
		self.data = data
		self.unk10 = unk10
		self.unk11 = unk11
		self.unk12 = unk12
		
	def encode_old(self, stream):
		stream.u32(self.unk1)
		stream.u8(self.is_online)
		self.game_key.encode(stream)
		stream.u8(self.unk3)
		stream.string(self.string)
		stream.u32(self.unk4)
		stream.u8(self.unk5)
		stream.u32(self.game_server_id)
		stream.u32(self.unk7)
		stream.u32(self.unk8)
		stream.u32(self.unk9)
		stream.data(self.data)
		stream.u8(self.unk10)
		stream.u8(self.unk11)
		stream.u8(self.unk12)
		
	def decode_old(self, stream):
		self.unk1 = stream.u32()
		self.is_online = stream.u8()
		self.game_key = GameKey.from_stream(stream)
		self.unk3 = stream.u8()
		self.string = stream.string()
		self.unk4 = stream.u32()
		self.unk5 = stream.u8()
		self.game_server_id = stream.u32()
		self.unk7 = stream.u32()
		self.unk8 = stream.u32()
		self.unk9 = stream.u32()
		self.data = stream.data()
		self.unk10 = stream.u8()
		self.unk11 = stream.u8()
		self.unk12 = stream.u8()
		
		
class PrincipalPreference(NexDataEncoder):
	def decode_old(self, stream):
		self.unk1 = stream.bool()
		self.unk2 = stream.bool()
		self.unk3 = stream.bool()
		
		
class Comment(NexDataEncoder):
	"""This is the status message shown in the friend list"""
	def decode_old(self, stream):
		self.unk = stream.u8()
		self.text = stream.string()
		self.changed = DateTime(stream.u64())
		
		
class FriendInfo(NexDataEncoder):
	def decode_old(self, stream):
		self.nna_info = NNAInfo.from_stream(stream)
		self.presence = NintendoPresenceV2.from_stream(stream)
		self.comment = Comment.from_stream(stream)
		self.befriended = DateTime(stream.u64())
		self.last_online = DateTime(stream.u64())
		self.unk = stream.u64()
		
		
class FriendRequestMessage(NexDataEncoder):
	def decode_old(self, stream):
		self.unk1 = stream.u64()
		self.unk2 = stream.u8()
		self.unk3 = stream.u8()
		self.message = stream.string()
		self.unk4 = stream.u8()
		self.string = stream.string()
		self.game_key = GameKey.from_stream(stream)
		self.datetime = DateTime(stream.u64())
		self.expires = DateTime(stream.u64())
		
		
class FriendRequest(NexDataEncoder):
	def decode_old(self, stream):
		self.principal_info = PrincipalBasicInfo.from_stream(stream)
		self.message = FriendRequestMessage.from_stream(stream)
		self.sent = DateTime(stream.u64())

		
class BlacklistedPrincipal(NexDataEncoder):
	def decode_old(self, stream):
		self.principal_info = PrincipalBasicInfo.from_stream(stream)
		self.game_key = GameKey.from_stream(stream)
		self.datetime = DateTime(stream.u64())
		
		
class PersistentNotification(NexDataEncoder):
	def decode_old(self, stream):
		self.unk1 = stream.u64()
		self.unk2 = stream.u32()
		self.unk3 = stream.u32()
		self.unk4 = stream.u32()
		self.string = stream.string()
		
	
class FriendsClient:
	#I couldn't find any apps/games with debug symbols for
	#this protocol, the method names are merely guesses
	METHOD_GET_ALL_INFORMATION = 1
	#The friends client got at least 13 methods
	
	PROTOCOL_ID = 0x66
	
	def __init__(self, back_end):
		self.client = back_end.secure_client
	
	def get_all_information(self, nna_info, presence, birthday):
		logger.info("Friends.get_all_information(...)")
		#--- request ---
		stream, call_id = self.client.init_message(self.PROTOCOL_ID, self.METHOD_GET_ALL_INFORMATION)
		nna_info.encode(stream)
		presence.encode(stream)
		stream.u64(birthday.value)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		principal_preference = PrincipalPreference.from_stream(stream)
		comment = Comment.from_stream(stream)
		friends = stream.list(lambda: FriendInfo.from_stream(stream))
		sent_requests = stream.list(lambda: FriendRequest.from_stream(stream))
		received_requests = stream.list(lambda: FriendRequest.from_stream(stream))
		blacklist = stream.list(lambda: BlacklistedPrincipal.from_stream(stream))
		unk1 = stream.bool()
		notifications = stream.list(lambda: PersistentNotification.from_stream(stream))
		unk2 = stream.u8()
		logger.info("Friends.get_all_information -> ...")
		return principal_preference, comment, friends, sent_requests, received_requests, blacklist, unk1, notifications, unk2
