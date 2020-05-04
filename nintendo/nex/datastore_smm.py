
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


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


class DataStoreProtocolSMM:
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
	METHOD_GET_APPLICATION_CONFIG = 61
	METHOD_GET_APPLICATION_CONFIG_STRING = 74
	
	PROTOCOL_ID = 0x73


class DataStoreClientSMM(DataStoreProtocolSMM):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def prepare_get_object_v1(self, param):
		logger.info("DataStoreClientSMM.prepare_get_object_v1()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_PREPARE_GET_OBJECT_V1, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqGetInfoV1)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM.prepare_get_object_v1 -> done")
		return info
	
	def get_meta(self, param):
		logger.info("DataStoreClientSMM.get_meta()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_META, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreMetaInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM.get_meta -> done")
		return info
	
	def prepare_post_object(self, param):
		logger.info("DataStoreClientSMM.prepare_post_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_PREPARE_POST_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqPostInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM.prepare_post_object -> done")
		return info
	
	def prepare_get_object(self, param):
		logger.info("DataStoreClientSMM.prepare_get_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_PREPARE_GET_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqGetInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM.prepare_get_object -> done")
		return info
	
	def complete_post_object(self, param):
		logger.info("DataStoreClientSMM.complete_post_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_COMPLETE_POST_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM.complete_post_object -> done")
	
	def get_password_info(self, data_id):
		logger.info("DataStoreClientSMM.get_password_info()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(data_id)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_PASSWORD_INFO, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		password_info = stream.extract(DataStorePasswordInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM.get_password_info -> done")
		return password_info
	
	def get_metas_multiple_param(self, params):
		logger.info("DataStoreClientSMM.get_metas_multiple_param()")
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
		logger.info("DataStoreClientSMM.get_metas_multiple_param -> done")
		return obj
	
	def get_application_config(self, id):
		logger.info("DataStoreClientSMM.get_application_config()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(id)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_APPLICATION_CONFIG, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		config = stream.list(stream.u32)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM.get_application_config -> done")
		return config
	
	def get_application_config_string(self, id):
		logger.info("DataStoreClientSMM.get_application_config_string()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(id)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_APPLICATION_CONFIG_STRING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		config = stream.list(stream.string)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClientSMM.get_application_config_string -> done")
		return config


class DataStoreServerSMM(DataStoreProtocolSMM):
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
			self.METHOD_GET_APPLICATION_CONFIG: self.handle_get_application_config,
			self.METHOD_GET_APPLICATION_CONFIG_STRING: self.handle_get_application_config_string,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_prepare_get_object_v1(self, context, input, output):
		logger.info("DataStoreServerSMM.prepare_get_object_v1()")
		#--- request ---
		param = input.extract(DataStorePrepareGetParamV1)
		response = self.prepare_get_object_v1(context, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqGetInfoV1):
			raise RuntimeError("Expected DataStoreReqGetInfoV1, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_prepare_post_object_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM.prepare_post_object_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_complete_post_object_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM.complete_post_object_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_delete_object(self, context, input, output):
		logger.warning("DataStoreServerSMM.delete_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_delete_objects(self, context, input, output):
		logger.warning("DataStoreServerSMM.delete_objects is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_change_meta_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM.change_meta_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_change_metas_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM.change_metas_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_meta(self, context, input, output):
		logger.info("DataStoreServerSMM.get_meta()")
		#--- request ---
		param = input.extract(DataStoreGetMetaParam)
		response = self.get_meta(context, param)
		
		#--- response ---
		if not isinstance(response, DataStoreMetaInfo):
			raise RuntimeError("Expected DataStoreMetaInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_metas(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_metas is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_prepare_update_object(self, context, input, output):
		logger.warning("DataStoreServerSMM.prepare_update_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_complete_update_object(self, context, input, output):
		logger.warning("DataStoreServerSMM.complete_update_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_search_object(self, context, input, output):
		logger.warning("DataStoreServerSMM.search_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_notification_url(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_notification_url is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_new_arrived_notifications_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_new_arrived_notifications_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_rate_object(self, context, input, output):
		logger.warning("DataStoreServerSMM.rate_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_rating(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_rating is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_ratings(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_ratings is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_reset_rating(self, context, input, output):
		logger.warning("DataStoreServerSMM.reset_rating is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_reset_ratings(self, context, input, output):
		logger.warning("DataStoreServerSMM.reset_ratings is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_specific_meta_v1(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_specific_meta_v1 is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_post_meta_binary(self, context, input, output):
		logger.warning("DataStoreServerSMM.post_meta_binary is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_touch_object(self, context, input, output):
		logger.warning("DataStoreServerSMM.touch_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_rating_with_log(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_rating_with_log is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_prepare_post_object(self, context, input, output):
		logger.info("DataStoreServerSMM.prepare_post_object()")
		#--- request ---
		param = input.extract(DataStorePreparePostParam)
		response = self.prepare_post_object(context, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqPostInfo):
			raise RuntimeError("Expected DataStoreReqPostInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_prepare_get_object(self, context, input, output):
		logger.info("DataStoreServerSMM.prepare_get_object()")
		#--- request ---
		param = input.extract(DataStorePrepareGetParam)
		response = self.prepare_get_object(context, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqGetInfo):
			raise RuntimeError("Expected DataStoreReqGetInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_complete_post_object(self, context, input, output):
		logger.info("DataStoreServerSMM.complete_post_object()")
		#--- request ---
		param = input.extract(DataStoreCompletePostParam)
		self.complete_post_object(context, param)
	
	def handle_get_new_arrived_notifications(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_new_arrived_notifications is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_specific_meta(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_specific_meta is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_persistence_info(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_persistence_info is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_persistence_infos(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_persistence_infos is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_perpetuate_object(self, context, input, output):
		logger.warning("DataStoreServerSMM.perpetuate_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_unperpetuate_object(self, context, input, output):
		logger.warning("DataStoreServerSMM.unperpetuate_object is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_prepare_get_object_or_meta(self, context, input, output):
		logger.warning("DataStoreServerSMM.prepare_get_object_or_meta is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_password_info(self, context, input, output):
		logger.info("DataStoreServerSMM.get_password_info()")
		#--- request ---
		data_id = input.u64()
		response = self.get_password_info(context, data_id)
		
		#--- response ---
		if not isinstance(response, DataStorePasswordInfo):
			raise RuntimeError("Expected DataStorePasswordInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_password_infos(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_password_infos is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_metas_multiple_param(self, context, input, output):
		logger.info("DataStoreServerSMM.get_metas_multiple_param()")
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
		logger.warning("DataStoreServerSMM.complete_post_objects is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_change_meta(self, context, input, output):
		logger.warning("DataStoreServerSMM.change_meta is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_change_metas(self, context, input, output):
		logger.warning("DataStoreServerSMM.change_metas is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_rate_objects(self, context, input, output):
		logger.warning("DataStoreServerSMM.rate_objects is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_post_meta_binary_with_data_id(self, context, input, output):
		logger.warning("DataStoreServerSMM.post_meta_binary_with_data_id is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_post_meta_binaries_with_data_id(self, context, input, output):
		logger.warning("DataStoreServerSMM.post_meta_binaries_with_data_id is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_rate_object_with_posting(self, context, input, output):
		logger.warning("DataStoreServerSMM.rate_object_with_posting is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_rate_objects_with_posting(self, context, input, output):
		logger.warning("DataStoreServerSMM.rate_objects_with_posting is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_object_infos(self, context, input, output):
		logger.warning("DataStoreServerSMM.get_object_infos is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_search_object_light(self, context, input, output):
		logger.warning("DataStoreServerSMM.search_object_light is unsupported")
		raise common.RMCError("Core::NotImplemented")
	
	def handle_get_application_config(self, context, input, output):
		logger.info("DataStoreServerSMM.get_application_config()")
		#--- request ---
		id = input.u32()
		response = self.get_application_config(context, id)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.u32)
	
	def handle_get_application_config_string(self, context, input, output):
		logger.info("DataStoreServerSMM.get_application_config_string()")
		#--- request ---
		id = input.u32()
		response = self.get_application_config_string(context, id)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.string)
	
	def prepare_get_object_v1(self, *args):
		logger.warning("DataStoreServerSMM.prepare_get_object_v1 not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_meta(self, *args):
		logger.warning("DataStoreServerSMM.get_meta not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def prepare_post_object(self, *args):
		logger.warning("DataStoreServerSMM.prepare_post_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def prepare_get_object(self, *args):
		logger.warning("DataStoreServerSMM.prepare_get_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def complete_post_object(self, *args):
		logger.warning("DataStoreServerSMM.complete_post_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_password_info(self, *args):
		logger.warning("DataStoreServerSMM.get_password_info not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_metas_multiple_param(self, *args):
		logger.warning("DataStoreServerSMM.get_metas_multiple_param not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_application_config(self, *args):
		logger.warning("DataStoreServerSMM.get_application_config not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_application_config_string(self, *args):
		logger.warning("DataStoreServerSMM.get_application_config_string not implemented")
		raise common.RMCError("Core::NotImplemented")

