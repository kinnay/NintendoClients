
from nintendo.nex import common
import requests

import logging
logger = logging.getLogger(__name__)


class PersistenceTarget(common.Structure):
	def __init__(self, owner_id, persistence_id):
		self.owner_id = owner_id
		self.persistence_id = persistence_id
	
	def streamin(self, stream):
		stream.u32(self.owner_id)
		stream.u16(self.persistence_id)

	
class DataStorePermission(common.Structure):
	def streamout(self, stream):
		self.permission = stream.u8()
		self.recipients = stream.list(stream.u32)
		
	
class DataStoreRatingInfo(common.Structure):
	def streamout(self, stream):
		self.total_value = stream.s64()
		self.count = stream.u32()
		self.initial_value = stream.s64()
	

class DataStoreRatingInfoWithSlot(common.Structure):
	def streamout(self, stream):
		self.slot = stream.u8()
		self.rating_info = stream.extract(DataStoreRatingInfo)
	
	
class DataStoreGetMetaParam(common.Structure):
	def __init__(self, data_id, persistence_target, result_option, access_password):
		self.data_id = data_id
		self.persistence_target = persistence_target
		self.result_option = result_option
		self.access_password = access_password
		
	def streamin(self, stream):
		stream.u64(self.data_id)
		stream.add(self.persistence_target)
		stream.u8(self.result_option)
		stream.u64(self.access_password)
		
		
class DataStoreMetaInfo(common.Structure):
	def streamout(self, stream):
		self.data_id = stream.u64()
		self.owner_id = stream.u32()
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
		self.ratings = stream.list(lambda: stream.extract(DataStoreRatingInfoWithSlot))


class DataStorePrepareGetParam(common.Structure):
	def __init__(self, data_id, lock_id, persistence_target, access_password, extra_data=None):
		self.data_id = data_id
		self.lock_id = lock_id
		self.persistence_target = persistence_target
		self.access_password = access_password
		self.extra_data = extra_data
	
	def streamin(self, stream):
		stream.u64(self.data_id)
		stream.u32(self.lock_id)
		stream.add(self.persistence_target)
		stream.u64(self.access_password)
		
		if self.version >= 0:
			stream.list(self.extra_data, stream.string)

			
class DataStoreKeyValue(common.Structure):
	def streamout(self, stream):
		self.key = stream.string()
		self.value = stream.string()
			
	
class DataStoreReqGetInfo(common.Structure):
	def streamout(self, stream):
		self.url = stream.string()
		self.headers = {item.key: item.value for item in stream.list(lambda: stream.extract(DataStoreKeyValue))}
		self.size = stream.u32()
		self.root_ca_cert = stream.buffer()
		
		if self.version >= 0:
			self.data_id = stream.u64()
	

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
	
	def __init__(self, backend):
		self.client = backend.secure_client
		
	def get_meta(self, param):
		logger.info("DataStore.get_meta(...)")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_META)
		stream.add(param)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		info = stream.extract(DataStoreMetaInfo)
		logger.info("DataStore.get_meta -> done")
		return info
		
	def prepare_get_object(self, param):
		logger.info("DataStore.prepare_get_object(%08X)", param.data_id)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_PREPARE_GET_OBJECT)
		stream.add(param)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		info = stream.extract(DataStoreReqGetInfo)
		logger.info("DataStore.prepare_get_object -> %s", info.url)
		return info
		
	def get_metas_multiple_param(self, param_list):
		logger.info("DataStore.get_metas_multiple_param(...)")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_METAS_MULTIPLE_PARAM)
		stream.list(param_list, stream.add)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		infos = stream.list(lambda: stream.extract(DataStoreMetaInfo))
		results = stream.list(stream.u32) #Error codes
		return infos
	
	
class DataStore:
	def __init__(self, backend):
		self.client = DataStoreClient(backend)
		
	def get_object(self, param):
		get_info = self.client.prepare_get_object(param)
		return requests.get("http://" + get_info.url, headers=get_info.headers).content
