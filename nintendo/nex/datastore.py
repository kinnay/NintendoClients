
from nintendo.nex.common import NexEncoder, DateTime
import requests

import logging
logger = logging.getLogger(__name__)


class PersistenceTarget(NexEncoder):
	version_map = {
		30400: -1,
		30504: 0,
		30810: 0
	}
	
	def init(self, owner_id, persistence_id):
		self.owner_id = owner_id
		self.persistence_id = persistence_id
	
	def encode_old(self, stream):
		stream.u32(self.owner_id)
		stream.u16(self.persistence_id)
		
	encode_v0 = encode_old
	
	
class DataStorePermission(NexEncoder):
	version_map = {
		30400: -1,
		30810: 0
	}
	
	def decode_old(self, stream):
		self.permission = stream.u8()
		self.unk = stream.list(stream.u32)
		
	decode_v0 = decode_old
		
	
class DataStoreRatingInfo(NexEncoder):
	version_map = {
		30400: -1,
		30810: 0
	}
	
	def decode_old(self, stream):
		self.unk1 = stream.s64()
		self.unk2 = stream.u32()
		self.unk3 = stream.s64()
		
	decode_v0 = decode_old
	

class DataStoreRatingInfoWithSlot(NexEncoder):
	version_map = {
		30400: -1,
		30810: 0
	}
	
	def decode_old(self, stream):
		self.slot = stream.u8()
		self.rating_info = DataStoreRatingInfo.from_stream(stream)
		
	decode_v0 = decode_old
	
	
class DataStoreGetMetaParam(NexEncoder):
	version_map = {
		30400: -1,
		30810: 0
	}
	
	def init(self, unk1, persistence_target, unk2, unk3):
		self.unk1 = unk1
		self.persistence_target = persistence_target
		self.unk2 = unk2
		self.unk3 = unk3
		
	def encode_old(self, stream):
		stream.u64(self.unk1)
		self.persistence_target.encode(stream)
		stream.u8(self.unk2)
		stream.u64(self.unk3)
		
	encode_v0 = encode_old
		
		
class DataStoreMetaInfo(NexEncoder):
	version_map = {
		30400: -1,
		30810: 0
	}
	
	def decode_old(self, stream):
		self.unk1 = stream.u64()
		self.unk2 = stream.u32()
		self.unk3 = stream.u32()
		self.owner_name = stream.string()
		self.unk4 = stream.u16()
		self.data = stream.read(stream.u16())
		self.perm1 = DataStorePermission.from_stream(stream)
		self.perm2 = DataStorePermission.from_stream(stream)
		self.date1 = DateTime(stream.u64())
		self.date2 = DateTime(stream.u64())
		self.unk5 = stream.u16()
		self.unk6 = stream.u8()
		self.unk7 = stream.u32()
		self.unk8 = stream.u32()
		self.unk9 = stream.u32()
		self.date3 = DateTime(stream.u64())
		self.date4 = DateTime(stream.u64())
		self.strings = stream.list(stream.string)
		self.rating_infos = stream.list(lambda: DataStoreRatingInfoWithSlot.from_stream(stream))
		
	decode_v0 = decode_old


class DataStoreGetParam(NexEncoder):
	version_map = {
		30400: -1,
		30504: 0,
		30810: 0
	}
	
	def init(self, object_id, unk, persistence_target, unk2):
		self.object_id = object_id
		self.unk = unk
		self.persistence_target = persistence_target
		self.unk2 = unk2
	
	def encode_old(self, stream):
		stream.u64(self.object_id)
		stream.u32(self.unk)
		self.persistence_target.encode(stream)
		stream.u64(self.unk2)

	encode_v0 = encode_old

	
class DataStoreGetInfo(NexEncoder):
	version_map = {
		30400: -1,
		30504: 0,
		30810: 0
	}
	
	def decode_old(self, stream):
		self.url = stream.string()
		self.params = dict(stream.list(lambda: (stream.string(), stream.string())))
		self.file_size = stream.u32()
		self.unk = stream.list(stream.u8)
		
	def decode_v0(self, stream):
		self.decode_old(stream)
		self.unk2 = stream.u64()
	

class DataStoreClient:

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
	
	PROTOCOL_ID = 0x73
	
	def __init__(self, back_end):
		self.client = back_end.secure_client
		
	def get_meta(self, param):
		logger.info("DataStore.get_meta(...)")
		#--- request ---
		stream, call_id = self.client.init_message(self.PROTOCOL_ID, self.METHOD_GET_META)
		param.encode(stream)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		info = DataStoreMetaInfo.from_stream(stream)
		logger.info("DataStore.get_meta -> done")
		return info
		
	def prepare_get_object(self, param):
		logger.info("DataStore.prepare_get_object(%08X)", param.object_id)
		#--- request ---
		stream, call_id = self.client.init_message(self.PROTOCOL_ID, self.METHOD_PREPARE_GET_OBJECT)
		param.encode(stream)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		info = DataStoreGetInfo.from_stream(stream)
		logger.info("DataStore.prepare_get_object -> %s", info.url)
		return info
	
	
class DataStore:
	def __init__(self, back_end):
		self.client = DataStoreClient(back_end)
		
	def get_object(self, param):
		get_info = self.client.prepare_get_object(param)
		return requests.get("http://" + get_info.url, headers=get_info.params).content
