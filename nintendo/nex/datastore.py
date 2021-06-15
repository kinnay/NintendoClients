
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class DataStoreChangeMetaCompareParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.comparison_flag = None
		self.name = None
		self.permission = DataStorePermission()
		self.delete_permission = DataStorePermission()
		self.period = None
		self.meta_binary = None
		self.tags = None
		self.referred_count = None
		self.data_type = None
		self.status = None
	
	def check_required(self, settings, version):
		for field in ['comparison_flag', 'name', 'period', 'meta_binary', 'tags', 'referred_count', 'data_type', 'status']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.comparison_flag = stream.u32()
		self.name = stream.string()
		self.permission = stream.extract(DataStorePermission)
		self.delete_permission = stream.extract(DataStorePermission)
		self.period = stream.u16()
		self.meta_binary = stream.qbuffer()
		self.tags = stream.list(stream.string)
		self.referred_count = stream.u32()
		self.data_type = stream.u16()
		self.status = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.comparison_flag)
		stream.string(self.name)
		stream.add(self.permission)
		stream.add(self.delete_permission)
		stream.u16(self.period)
		stream.qbuffer(self.meta_binary)
		stream.list(self.tags, stream.string)
		stream.u32(self.referred_count)
		stream.u16(self.data_type)
		stream.u8(self.status)


class DataStoreChangeMetaParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.modifies_flag = None
		self.name = None
		self.permission = DataStorePermission()
		self.delete_permission = DataStorePermission()
		self.period = None
		self.meta_binary = None
		self.tags = None
		self.update_password = None
		self.referred_count = None
		self.data_type = None
		self.status = None
		self.compare_param = DataStoreChangeMetaCompareParam()
		self.persistence_target = DataStorePersistenceTarget()
	
	def check_required(self, settings, version):
		for field in ['data_id', 'modifies_flag', 'name', 'period', 'meta_binary', 'tags', 'update_password', 'referred_count', 'data_type', 'status']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.modifies_flag = stream.u32()
		self.name = stream.string()
		self.permission = stream.extract(DataStorePermission)
		self.delete_permission = stream.extract(DataStorePermission)
		self.period = stream.u16()
		self.meta_binary = stream.qbuffer()
		self.tags = stream.list(stream.string)
		self.update_password = stream.u64()
		self.referred_count = stream.u32()
		self.data_type = stream.u16()
		self.status = stream.u8()
		self.compare_param = stream.extract(DataStoreChangeMetaCompareParam)
		self.persistence_target = stream.extract(DataStorePersistenceTarget)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.u32(self.modifies_flag)
		stream.string(self.name)
		stream.add(self.permission)
		stream.add(self.delete_permission)
		stream.u16(self.period)
		stream.qbuffer(self.meta_binary)
		stream.list(self.tags, stream.string)
		stream.u64(self.update_password)
		stream.u32(self.referred_count)
		stream.u16(self.data_type)
		stream.u8(self.status)
		stream.add(self.compare_param)
		stream.add(self.persistence_target)


class DataStoreChangeMetaParamV1(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.modifies_flag = None
		self.name = None
		self.permission = DataStorePermission()
		self.delete_permission = DataStorePermission()
		self.period = None
		self.meta_binary = None
		self.tags = None
		self.update_password = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'modifies_flag', 'name', 'period', 'meta_binary', 'tags', 'update_password']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.modifies_flag = stream.u32()
		self.name = stream.string()
		self.permission = stream.extract(DataStorePermission)
		self.delete_permission = stream.extract(DataStorePermission)
		self.period = stream.u16()
		self.meta_binary = stream.qbuffer()
		self.tags = stream.list(stream.string)
		self.update_password = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.u32(self.modifies_flag)
		stream.string(self.name)
		stream.add(self.permission)
		stream.add(self.delete_permission)
		stream.u16(self.period)
		stream.qbuffer(self.meta_binary)
		stream.list(self.tags, stream.string)
		stream.u64(self.update_password)


class DataStoreCompletePostParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.success = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'success']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.success = stream.bool()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.bool(self.success)


class DataStoreCompletePostParamV1(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.success = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'success']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u32()
		self.success = stream.bool()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.data_id)
		stream.bool(self.success)


class DataStoreCompleteUpdateParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.version = None
		self.success = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'version', 'success']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.version = stream.u32()
		self.success = stream.bool()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.u32(self.version)
		stream.bool(self.success)


class DataStoreDeleteParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.update_password = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'update_password']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.update_password = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.u64(self.update_password)


class DataStoreGetMetaParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = 0
		self.persistence_target = DataStorePersistenceTarget()
		self.result_option = 0
		self.access_password = 0
	
	def check_required(self, settings, version):
		pass
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.persistence_target = stream.extract(DataStorePersistenceTarget)
		self.result_option = stream.u8()
		self.access_password = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.add(self.persistence_target)
		stream.u8(self.result_option)
		stream.u64(self.access_password)


class DataStoreGetNewArrivedNotificationsParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.last_notification_id = None
		self.limit = None
	
	def check_required(self, settings, version):
		for field in ['last_notification_id', 'limit']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.last_notification_id = stream.u64()
		self.limit = stream.u16()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.last_notification_id)
		stream.u16(self.limit)


class DataStoreGetNotificationUrlParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.previous_url = None
	
	def check_required(self, settings, version):
		for field in ['previous_url']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.previous_url = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.string(self.previous_url)


class DataStoreGetSpecificMetaParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_ids = None
	
	def check_required(self, settings, version):
		for field in ['data_ids']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_ids = stream.list(stream.u64)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.list(self.data_ids, stream.u64)


class DataStoreGetSpecificMetaParamV1(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_ids = None
	
	def check_required(self, settings, version):
		for field in ['data_ids']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_ids = stream.list(stream.u32)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.list(self.data_ids, stream.u32)


class DataStoreKeyValue(common.Structure):
	def __init__(self):
		super().__init__()
		self.key = None
		self.value = None
	
	def check_required(self, settings, version):
		for field in ['key', 'value']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.key = stream.string()
		self.value = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
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
	
	def check_required(self, settings, version):
		for field in ['data_id', 'owner_id', 'size', 'name', 'data_type', 'meta_binary', 'create_time', 'update_time', 'period', 'status', 'referred_count', 'refer_data_id', 'flag', 'referred_time', 'expire_time', 'tags', 'ratings']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
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
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
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


class DataStoreNotification(common.Structure):
	def __init__(self):
		super().__init__()
		self.notification_id = None
		self.data_id = None
	
	def check_required(self, settings, version):
		for field in ['notification_id', 'data_id']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.notification_id = stream.u64()
		self.data_id = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.notification_id)
		stream.u64(self.data_id)


class DataStoreNotificationV1(common.Structure):
	def __init__(self):
		super().__init__()
		self.notification_id = None
		self.data_id = None
	
	def check_required(self, settings, version):
		for field in ['notification_id', 'data_id']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.notification_id = stream.u64()
		self.data_id = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.notification_id)
		stream.u32(self.data_id)


class DataStorePasswordInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.access_password = None
		self.update_password = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'access_password', 'update_password']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.access_password = stream.u64()
		self.update_password = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.u64(self.access_password)
		stream.u64(self.update_password)


class DataStorePermission(common.Structure):
	def __init__(self):
		super().__init__()
		self.permission = 3
		self.recipients = []
	
	def check_required(self, settings, version):
		pass
	
	def load(self, stream, version):
		self.permission = stream.u8()
		self.recipients = stream.list(stream.pid)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u8(self.permission)
		stream.list(self.recipients, stream.pid)


class DataStorePersistenceInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.owner_id = None
		self.slot_id = None
		self.data_id = None
	
	def check_required(self, settings, version):
		for field in ['owner_id', 'slot_id', 'data_id']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.owner_id = stream.pid()
		self.slot_id = stream.u16()
		self.data_id = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.owner_id)
		stream.u16(self.slot_id)
		stream.u64(self.data_id)


class DataStorePersistenceInitParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.persistence_id = 65535
		self.delete_last_object = True
	
	def check_required(self, settings, version):
		pass
	
	def load(self, stream, version):
		self.persistence_id = stream.u16()
		self.delete_last_object = stream.bool()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u16(self.persistence_id)
		stream.bool(self.delete_last_object)


class DataStorePersistenceTarget(common.Structure):
	def __init__(self):
		super().__init__()
		self.owner_id = 0
		self.persistence_id = 65535
	
	def check_required(self, settings, version):
		pass
	
	def load(self, stream, version):
		self.owner_id = stream.pid()
		self.persistence_id = stream.u16()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
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
	
	def check_required(self, settings, version):
		if settings["nex.version"] >= 30500:
			pass
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.lock_id = stream.u32()
		self.persistence_target = stream.extract(DataStorePersistenceTarget)
		self.access_password = stream.u64()
		if stream.settings["nex.version"] >= 30500:
			self.extra_data = stream.list(stream.string)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.u32(self.lock_id)
		stream.add(self.persistence_target)
		stream.u64(self.access_password)
		if stream.settings["nex.version"] >= 30500:
			stream.list(self.extra_data, stream.string)


class DataStorePrepareGetParamV1(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.lock_id = 0
	
	def check_required(self, settings, version):
		for field in ['data_id']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u32()
		self.lock_id = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.data_id)
		stream.u32(self.lock_id)


class DataStorePreparePostParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.size = None
		self.name = None
		self.data_type = None
		self.meta_binary = None
		self.permission = DataStorePermission()
		self.delete_permission = DataStorePermission()
		self.flag = None
		self.period = None
		self.refer_data_id = 0
		self.tags = []
		self.rating_init_param = []
		self.persistence_init_param = DataStorePersistenceInitParam()
		self.extra_data = None
	
	def check_required(self, settings, version):
		for field in ['size', 'name', 'data_type', 'meta_binary', 'flag', 'period']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings["nex.version"] >= 30500:
			for field in ['extra_data']:
				if getattr(self, field) is None:
					raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
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
		if stream.settings["nex.version"] >= 30500:
			self.extra_data = stream.list(stream.string)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
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
		if stream.settings["nex.version"] >= 30500:
			stream.list(self.extra_data, stream.string)


class DataStorePreparePostParamV1(common.Structure):
	def __init__(self):
		super().__init__()
		self.size = None
		self.name = None
		self.data_type = 0
		self.meta_binary = b""
		self.permission = DataStorePermission()
		self.delete_permission = DataStorePermission()
		self.flag = None
		self.period = None
		self.refer_data_id = 0
		self.tags = None
		self.rating_init_param = None
	
	def check_required(self, settings, version):
		for field in ['size', 'name', 'flag', 'period', 'tags', 'rating_init_param']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
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
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
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


class DataStorePrepareUpdateParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.size = None
		self.update_password = None
		self.extra_data = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'size', 'update_password', 'extra_data']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.size = stream.u32()
		self.update_password = stream.u64()
		self.extra_data = stream.list(stream.string)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.u32(self.size)
		stream.u64(self.update_password)
		stream.list(self.extra_data, stream.string)


class DataStoreRateObjectParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.rating_value = None
		self.access_password = None
	
	def check_required(self, settings, version):
		for field in ['rating_value', 'access_password']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.rating_value = stream.s32()
		self.access_password = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.s32(self.rating_value)
		stream.u64(self.access_password)


class DataStoreRatingInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.total_value = None
		self.count = None
		self.initial_value = None
	
	def check_required(self, settings, version):
		for field in ['total_value', 'count', 'initial_value']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.total_value = stream.s64()
		self.count = stream.u32()
		self.initial_value = stream.s64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.s64(self.total_value)
		stream.u32(self.count)
		stream.s64(self.initial_value)


class DataStoreRatingInfoWithSlot(common.Structure):
	def __init__(self):
		super().__init__()
		self.slot = None
		self.info = DataStoreRatingInfo()
	
	def check_required(self, settings, version):
		for field in ['slot']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.slot = stream.u8()
		self.info = stream.extract(DataStoreRatingInfo)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
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
	
	def check_required(self, settings, version):
		for field in ['flag', 'internal_flag', 'lock_type', 'initial_value', 'range_min', 'range_max', 'period_hour', 'period_duration']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.flag = stream.u8()
		self.internal_flag = stream.u8()
		self.lock_type = stream.u8()
		self.initial_value = stream.s64()
		self.range_min = stream.s32()
		self.range_max = stream.s32()
		self.period_hour = stream.s8()
		self.period_duration = stream.s16()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
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
	
	def check_required(self, settings, version):
		for field in ['slot']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.slot = stream.s8()
		self.param = stream.extract(DataStoreRatingInitParam)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.s8(self.slot)
		stream.add(self.param)


class DataStoreRatingLog(common.Structure):
	def __init__(self):
		super().__init__()
		self.is_rated = None
		self.pid = None
		self.rating_value = None
		self.lock_expiration_time = None
	
	def check_required(self, settings, version):
		for field in ['is_rated', 'pid', 'rating_value', 'lock_expiration_time']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.is_rated = stream.bool()
		self.pid = stream.pid()
		self.rating_value = stream.s32()
		self.lock_expiration_time = stream.datetime()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.bool(self.is_rated)
		stream.pid(self.pid)
		stream.s32(self.rating_value)
		stream.datetime(self.lock_expiration_time)


class DataStoreRatingTarget(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.slot = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'slot']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.slot = stream.s8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.s8(self.slot)


class DataStoreReqGetAdditionalMeta(common.Structure):
	def __init__(self):
		super().__init__()
		self.owner_id = None
		self.data_type = None
		self.version = None
		self.meta_binary = None
	
	def check_required(self, settings, version):
		for field in ['owner_id', 'data_type', 'version', 'meta_binary']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.owner_id = stream.pid()
		self.data_type = stream.u16()
		self.version = stream.u16()
		self.meta_binary = stream.qbuffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.pid(self.owner_id)
		stream.u16(self.data_type)
		stream.u16(self.version)
		stream.qbuffer(self.meta_binary)


class DataStoreReqGetInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.url = None
		self.headers = None
		self.size = None
		self.root_ca_cert = None
		self.data_id = None
	
	def check_required(self, settings, version):
		for field in ['url', 'headers', 'size', 'root_ca_cert']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings["nex.version"] >= 30500:
			for field in ['data_id']:
				if getattr(self, field) is None:
					raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.url = stream.string()
		self.headers = stream.list(DataStoreKeyValue)
		self.size = stream.u32()
		self.root_ca_cert = stream.buffer()
		if stream.settings["nex.version"] >= 30500:
			self.data_id = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.string(self.url)
		stream.list(self.headers, stream.add)
		stream.u32(self.size)
		stream.buffer(self.root_ca_cert)
		if stream.settings["nex.version"] >= 30500:
			stream.u64(self.data_id)


class DataStoreReqGetInfoV1(common.Structure):
	def __init__(self):
		super().__init__()
		self.url = None
		self.headers = None
		self.size = None
		self.root_ca_cert = None
	
	def check_required(self, settings, version):
		for field in ['url', 'headers', 'size', 'root_ca_cert']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.url = stream.string()
		self.headers = stream.list(DataStoreKeyValue)
		self.size = stream.u32()
		self.root_ca_cert = stream.buffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.string(self.url)
		stream.list(self.headers, stream.add)
		stream.u32(self.size)
		stream.buffer(self.root_ca_cert)


class DataStoreReqGetNotificationUrlInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.url = None
		self.key = None
		self.query = None
		self.root_ca_cert = None
	
	def check_required(self, settings, version):
		for field in ['url', 'key', 'query', 'root_ca_cert']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.url = stream.string()
		self.key = stream.string()
		self.query = stream.string()
		self.root_ca_cert = stream.buffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.string(self.url)
		stream.string(self.key)
		stream.string(self.query)
		stream.buffer(self.root_ca_cert)


class DataStoreReqPostInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.url = None
		self.headers = None
		self.form = None
		self.root_ca_cert = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'url', 'headers', 'form', 'root_ca_cert']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.url = stream.string()
		self.headers = stream.list(DataStoreKeyValue)
		self.form = stream.list(DataStoreKeyValue)
		self.root_ca_cert = stream.buffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.string(self.url)
		stream.list(self.headers, stream.add)
		stream.list(self.form, stream.add)
		stream.buffer(self.root_ca_cert)


class DataStoreReqPostInfoV1(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.url = None
		self.headers = None
		self.form = None
		self.root_ca_cert = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'url', 'headers', 'form', 'root_ca_cert']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u32()
		self.url = stream.string()
		self.headers = stream.list(DataStoreKeyValue)
		self.form = stream.list(DataStoreKeyValue)
		self.root_ca_cert = stream.buffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.data_id)
		stream.string(self.url)
		stream.list(self.headers, stream.add)
		stream.list(self.form, stream.add)
		stream.buffer(self.root_ca_cert)


class DataStoreReqUpdateInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.version = None
		self.url = None
		self.headers = None
		self.form = None
		self.root_ca_cert = None
	
	def check_required(self, settings, version):
		for field in ['version', 'url', 'headers', 'form', 'root_ca_cert']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.version = stream.u32()
		self.url = stream.string()
		self.headers = stream.list(DataStoreKeyValue)
		self.form = stream.list(DataStoreKeyValue)
		self.root_ca_cert = stream.buffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.version)
		stream.string(self.url)
		stream.list(self.headers, stream.add)
		stream.list(self.form, stream.add)
		stream.buffer(self.root_ca_cert)


class DataStoreSearchParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.search_target = 1
		self.owner_ids = []
		self.owner_type = 0
		self.destination_ids = []
		self.data_type = 65535
		self.created_after = common.DateTime(671076024059)
		self.created_before = common.DateTime(671076024059)
		self.updated_after = common.DateTime(671076024059)
		self.updated_before = common.DateTime(671076024059)
		self.refer_data_id = 0
		self.tags = []
		self.result_order_column = 0
		self.result_order = 0
		self.result_range = common.ResultRange()
		self.result_option = 0
		self.minimal_rating_frequency = 0
		self.use_cache = False
		self.total_count_enabled = True
		self.data_types = []
	
	def check_required(self, settings, version):
		pass
	
	def load(self, stream, version):
		self.search_target = stream.u8()
		self.owner_ids = stream.list(stream.pid)
		self.owner_type = stream.u8()
		self.destination_ids = stream.list(stream.u64)
		self.data_type = stream.u16()
		self.created_after = stream.datetime()
		self.created_before = stream.datetime()
		self.updated_after = stream.datetime()
		self.updated_before = stream.datetime()
		self.refer_data_id = stream.u32()
		self.tags = stream.list(stream.string)
		self.result_order_column = stream.u8()
		self.result_order = stream.u8()
		self.result_range = stream.extract(common.ResultRange)
		self.result_option = stream.u8()
		self.minimal_rating_frequency = stream.u32()
		self.use_cache = stream.bool()
		self.total_count_enabled = stream.bool()
		self.data_types = stream.list(stream.u16)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u8(self.search_target)
		stream.list(self.owner_ids, stream.pid)
		stream.u8(self.owner_type)
		stream.list(self.destination_ids, stream.u64)
		stream.u16(self.data_type)
		stream.datetime(self.created_after)
		stream.datetime(self.created_before)
		stream.datetime(self.updated_after)
		stream.datetime(self.updated_before)
		stream.u32(self.refer_data_id)
		stream.list(self.tags, stream.string)
		stream.u8(self.result_order_column)
		stream.u8(self.result_order)
		stream.add(self.result_range)
		stream.u8(self.result_option)
		stream.u32(self.minimal_rating_frequency)
		stream.bool(self.use_cache)
		stream.bool(self.total_count_enabled)
		stream.list(self.data_types, stream.u16)


class DataStoreSearchResult(common.Structure):
	def __init__(self):
		super().__init__()
		self.total_count = None
		self.result = None
		self.total_count_type = None
	
	def check_required(self, settings, version):
		for field in ['total_count', 'result', 'total_count_type']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.total_count = stream.u32()
		self.result = stream.list(DataStoreMetaInfo)
		self.total_count_type = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.total_count)
		stream.list(self.result, stream.add)
		stream.u8(self.total_count_type)


class DataStoreSpecificMetaInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.owner_id = None
		self.size = None
		self.data_type = None
		self.version = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'owner_id', 'size', 'data_type', 'version']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.owner_id = stream.pid()
		self.size = stream.u32()
		self.data_type = stream.u16()
		self.version = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.pid(self.owner_id)
		stream.u32(self.size)
		stream.u16(self.data_type)
		stream.u32(self.version)


class DataStoreSpecificMetaInfoV1(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.owner_id = None
		self.size = None
		self.data_type = None
		self.version = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'owner_id', 'size', 'data_type', 'version']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u32()
		self.owner_id = stream.pid()
		self.size = stream.u32()
		self.data_type = stream.u16()
		self.version = stream.u16()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.data_id)
		stream.pid(self.owner_id)
		stream.u32(self.size)
		stream.u16(self.data_type)
		stream.u16(self.version)


class DataStoreTouchObjectParam(common.Structure):
	def __init__(self):
		super().__init__()
		self.data_id = None
		self.lock_id = None
		self.access_password = None
	
	def check_required(self, settings, version):
		for field in ['data_id', 'lock_id', 'access_password']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.data_id = stream.u64()
		self.lock_id = stream.u32()
		self.access_password = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.data_id)
		stream.u32(self.lock_id)
		stream.u64(self.access_password)


class DataStoreProtocol:
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
	METHOD_PREPARE_GET_OBJECT_OR_META_BINARY = 33
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


class DataStoreClient(DataStoreProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def prepare_get_object_v1(self, param):
		logger.info("DataStoreClient.prepare_get_object_v1()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PREPARE_GET_OBJECT_V1, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqGetInfoV1)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.prepare_get_object_v1 -> done")
		return info
	
	async def prepare_post_object_v1(self, param):
		logger.info("DataStoreClient.prepare_post_object_v1()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PREPARE_POST_OBJECT_V1, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqPostInfoV1)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.prepare_post_object_v1 -> done")
		return info
	
	async def complete_post_object_v1(self, param):
		logger.info("DataStoreClient.complete_post_object_v1()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_COMPLETE_POST_OBJECT_V1, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.complete_post_object_v1 -> done")
	
	async def delete_object(self, param):
		logger.info("DataStoreClient.delete_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.delete_object -> done")
	
	async def delete_objects(self, param, transactional):
		logger.info("DataStoreClient.delete_objects()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(param, stream.add)
		stream.bool(transactional)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_OBJECTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.delete_objects -> done")
		return results
	
	async def change_meta_v1(self, param):
		logger.info("DataStoreClient.change_meta_v1()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CHANGE_META_V1, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.change_meta_v1 -> done")
	
	async def change_metas_v1(self, data_ids, param, transactional):
		logger.info("DataStoreClient.change_metas_v1()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(data_ids, stream.u64)
		stream.list(param, stream.add)
		stream.bool(transactional)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CHANGE_METAS_V1, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.change_metas_v1 -> done")
		return results
	
	async def get_meta(self, param):
		logger.info("DataStoreClient.get_meta()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_META, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreMetaInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_meta -> done")
		return info
	
	async def get_metas(self, data_ids, param):
		logger.info("DataStoreClient.get_metas()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(data_ids, stream.u64)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_METAS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.info = stream.list(DataStoreMetaInfo)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_metas -> done")
		return obj
	
	async def prepare_update_object(self, param):
		logger.info("DataStoreClient.prepare_update_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PREPARE_UPDATE_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqUpdateInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.prepare_update_object -> done")
		return info
	
	async def complete_update_object(self, param):
		logger.info("DataStoreClient.complete_update_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_COMPLETE_UPDATE_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.complete_update_object -> done")
	
	async def search_object(self, param):
		logger.info("DataStoreClient.search_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_SEARCH_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.extract(DataStoreSearchResult)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.search_object -> done")
		return result
	
	async def get_notification_url(self, param):
		logger.info("DataStoreClient.get_notification_url()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_NOTIFICATION_URL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqGetNotificationUrlInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_notification_url -> done")
		return info
	
	async def get_new_arrived_notifications_v1(self, param):
		logger.info("DataStoreClient.get_new_arrived_notifications_v1()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_NEW_ARRIVED_NOTIFICATIONS_V1, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.list(DataStoreNotificationV1)
		obj.has_next = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_new_arrived_notifications_v1 -> done")
		return obj
	
	async def rate_object(self, target, param, fetch_ratings):
		logger.info("DataStoreClient.rate_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(target)
		stream.add(param)
		stream.bool(fetch_ratings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_RATE_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreRatingInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.rate_object -> done")
		return info
	
	async def get_rating(self, target, access_password):
		logger.info("DataStoreClient.get_rating()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(target)
		stream.u64(access_password)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_RATING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		rating = stream.extract(DataStoreRatingInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_rating -> done")
		return rating
	
	async def get_ratings(self, data_ids, access_password):
		logger.info("DataStoreClient.get_ratings()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(data_ids, stream.u64)
		stream.u64(access_password)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_RATINGS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.ratings = stream.list(lambda: stream.list(DataStoreRatingInfoWithSlot))
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_ratings -> done")
		return obj
	
	async def reset_rating(self, target, update_password):
		logger.info("DataStoreClient.reset_rating()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(target)
		stream.u64(update_password)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_RESET_RATING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.reset_rating -> done")
	
	async def reset_ratings(self, data_ids, transactional):
		logger.info("DataStoreClient.reset_ratings()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(data_ids, stream.u64)
		stream.bool(transactional)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_RESET_RATINGS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.reset_ratings -> done")
		return results
	
	async def get_specific_meta_v1(self, param):
		logger.info("DataStoreClient.get_specific_meta_v1()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_SPECIFIC_META_V1, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		infos = stream.list(DataStoreSpecificMetaInfoV1)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_specific_meta_v1 -> done")
		return infos
	
	async def post_meta_binary(self, param):
		logger.info("DataStoreClient.post_meta_binary()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_POST_META_BINARY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		data_id = stream.u64()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.post_meta_binary -> done")
		return data_id
	
	async def touch_object(self, param):
		logger.info("DataStoreClient.touch_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_TOUCH_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.touch_object -> done")
	
	async def get_rating_with_log(self, target, access_password):
		logger.info("DataStoreClient.get_rating_with_log()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(target)
		stream.u64(access_password)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_RATING_WITH_LOG, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.rating = stream.extract(DataStoreRatingInfo)
		obj.log = stream.extract(DataStoreRatingLog)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_rating_with_log -> done")
		return obj
	
	async def prepare_post_object(self, param):
		logger.info("DataStoreClient.prepare_post_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PREPARE_POST_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqPostInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.prepare_post_object -> done")
		return info
	
	async def prepare_get_object(self, param):
		logger.info("DataStoreClient.prepare_get_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PREPARE_GET_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreReqGetInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.prepare_get_object -> done")
		return info
	
	async def complete_post_object(self, param):
		logger.info("DataStoreClient.complete_post_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_COMPLETE_POST_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.complete_post_object -> done")
	
	async def get_new_arrived_notifications(self, param):
		logger.info("DataStoreClient.get_new_arrived_notifications()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_NEW_ARRIVED_NOTIFICATIONS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.result = stream.list(DataStoreNotification)
		obj.has_next = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_new_arrived_notifications -> done")
		return obj
	
	async def get_specific_meta(self, param):
		logger.info("DataStoreClient.get_specific_meta()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_SPECIFIC_META, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		infos = stream.list(DataStoreSpecificMetaInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_specific_meta -> done")
		return infos
	
	async def get_persistence_info(self, owner_id, slot_id):
		logger.info("DataStoreClient.get_persistence_info()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(owner_id)
		stream.u16(slot_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PERSISTENCE_INFO, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStorePersistenceInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_persistence_info -> done")
		return info
	
	async def get_persistence_infos(self, owner_id, slot_ids):
		logger.info("DataStoreClient.get_persistence_infos()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(owner_id)
		stream.list(slot_ids, stream.u16)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PERSISTENCE_INFOS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.infos = stream.list(DataStorePersistenceInfo)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_persistence_infos -> done")
		return obj
	
	async def perpetuate_object(self, persistence_slot_id, data_id, delete_last_object):
		logger.info("DataStoreClient.perpetuate_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u16(persistence_slot_id)
		stream.u64(data_id)
		stream.bool(delete_last_object)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PERPETUATE_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.perpetuate_object -> done")
	
	async def unperpetuate_object(self, persistence_slot_id, delete_last_object):
		logger.info("DataStoreClient.unperpetuate_object()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u16(persistence_slot_id)
		stream.bool(delete_last_object)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UNPERPETUATE_OBJECT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.unperpetuate_object -> done")
	
	async def prepare_get_object_or_meta_binary(self, param):
		logger.info("DataStoreClient.prepare_get_object_or_meta_binary()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PREPARE_GET_OBJECT_OR_META_BINARY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.get_info = stream.extract(DataStoreReqGetInfo)
		obj.additional_meta = stream.extract(DataStoreReqGetAdditionalMeta)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.prepare_get_object_or_meta_binary -> done")
		return obj
	
	async def get_password_info(self, data_id):
		logger.info("DataStoreClient.get_password_info()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(data_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PASSWORD_INFO, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStorePasswordInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_password_info -> done")
		return info
	
	async def get_password_infos(self, data_ids):
		logger.info("DataStoreClient.get_password_infos()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(data_ids, stream.u64)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_PASSWORD_INFOS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.infos = stream.list(DataStorePasswordInfo)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_password_infos -> done")
		return obj
	
	async def get_metas_multiple_param(self, params):
		logger.info("DataStoreClient.get_metas_multiple_param()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(params, stream.add)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_METAS_MULTIPLE_PARAM, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.infos = stream.list(DataStoreMetaInfo)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_metas_multiple_param -> done")
		return obj
	
	async def complete_post_objects(self, data_ids):
		logger.info("DataStoreClient.complete_post_objects()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(data_ids, stream.u64)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_COMPLETE_POST_OBJECTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.complete_post_objects -> done")
	
	async def change_meta(self, param):
		logger.info("DataStoreClient.change_meta()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CHANGE_META, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.change_meta -> done")
	
	async def change_metas(self, data_ids, param, transactional):
		logger.info("DataStoreClient.change_metas()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(data_ids, stream.u64)
		stream.list(param, stream.add)
		stream.bool(transactional)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_CHANGE_METAS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.change_metas -> done")
		return results
	
	async def rate_objects(self, targets, param, transactional, fetch_ratings):
		logger.info("DataStoreClient.rate_objects()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(targets, stream.add)
		stream.list(param, stream.add)
		stream.bool(transactional)
		stream.bool(fetch_ratings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_RATE_OBJECTS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.infos = stream.list(DataStoreRatingInfo)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.rate_objects -> done")
		return obj
	
	async def post_meta_binary_with_data_id(self, data_id, param):
		logger.info("DataStoreClient.post_meta_binary_with_data_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(data_id)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_POST_META_BINARY_WITH_DATA_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.post_meta_binary_with_data_id -> done")
	
	async def post_meta_binaries_with_data_id(self, data_ids, param, transactional):
		logger.info("DataStoreClient.post_meta_binaries_with_data_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(data_ids, stream.u64)
		stream.list(param, stream.add)
		stream.bool(transactional)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_POST_META_BINARIES_WITH_DATA_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.post_meta_binaries_with_data_id -> done")
		return results
	
	async def rate_object_with_posting(self, target, rate_param, post_param, fetch_ratings):
		logger.info("DataStoreClient.rate_object_with_posting()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(target)
		stream.add(rate_param)
		stream.add(post_param)
		stream.bool(fetch_ratings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_RATE_OBJECT_WITH_POSTING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(DataStoreRatingInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.rate_object_with_posting -> done")
		return info
	
	async def rate_objects_with_posting(self, targets, rate_param, post_param, transactional, fetch_ratings):
		logger.info("DataStoreClient.rate_objects_with_posting()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(targets, stream.add)
		stream.list(rate_param, stream.add)
		stream.list(post_param, stream.add)
		stream.bool(transactional)
		stream.bool(fetch_ratings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_RATE_OBJECTS_WITH_POSTING, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.ratings = stream.list(DataStoreRatingInfo)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.rate_objects_with_posting -> done")
		return obj
	
	async def get_object_infos(self, data_ids):
		logger.info("DataStoreClient.get_object_infos()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(data_ids, stream.u64)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_OBJECT_INFOS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.infos = stream.list(DataStoreReqGetInfo)
		obj.results = stream.list(stream.result)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.get_object_infos -> done")
		return obj
	
	async def search_object_light(self, param):
		logger.info("DataStoreClient.search_object_light()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(param)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_SEARCH_OBJECT_LIGHT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.extract(DataStoreSearchResult)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("DataStoreClient.search_object_light -> done")
		return result


class DataStoreServer(DataStoreProtocol):
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
			self.METHOD_PREPARE_GET_OBJECT_OR_META_BINARY: self.handle_prepare_get_object_or_meta_binary,
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
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on DataStoreServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_prepare_get_object_v1(self, client, input, output):
		logger.info("DataStoreServer.prepare_get_object_v1()")
		#--- request ---
		param = input.extract(DataStorePrepareGetParamV1)
		response = await self.prepare_get_object_v1(client, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqGetInfoV1):
			raise RuntimeError("Expected DataStoreReqGetInfoV1, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_prepare_post_object_v1(self, client, input, output):
		logger.info("DataStoreServer.prepare_post_object_v1()")
		#--- request ---
		param = input.extract(DataStorePreparePostParamV1)
		response = await self.prepare_post_object_v1(client, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqPostInfoV1):
			raise RuntimeError("Expected DataStoreReqPostInfoV1, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_complete_post_object_v1(self, client, input, output):
		logger.info("DataStoreServer.complete_post_object_v1()")
		#--- request ---
		param = input.extract(DataStoreCompletePostParamV1)
		await self.complete_post_object_v1(client, param)
	
	async def handle_delete_object(self, client, input, output):
		logger.info("DataStoreServer.delete_object()")
		#--- request ---
		param = input.extract(DataStoreDeleteParam)
		await self.delete_object(client, param)
	
	async def handle_delete_objects(self, client, input, output):
		logger.info("DataStoreServer.delete_objects()")
		#--- request ---
		param = input.list(DataStoreDeleteParam)
		transactional = input.bool()
		response = await self.delete_objects(client, param, transactional)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.result)
	
	async def handle_change_meta_v1(self, client, input, output):
		logger.info("DataStoreServer.change_meta_v1()")
		#--- request ---
		param = input.extract(DataStoreChangeMetaParamV1)
		await self.change_meta_v1(client, param)
	
	async def handle_change_metas_v1(self, client, input, output):
		logger.info("DataStoreServer.change_metas_v1()")
		#--- request ---
		data_ids = input.list(input.u64)
		param = input.list(DataStoreChangeMetaParamV1)
		transactional = input.bool()
		response = await self.change_metas_v1(client, data_ids, param, transactional)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.result)
	
	async def handle_get_meta(self, client, input, output):
		logger.info("DataStoreServer.get_meta()")
		#--- request ---
		param = input.extract(DataStoreGetMetaParam)
		response = await self.get_meta(client, param)
		
		#--- response ---
		if not isinstance(response, DataStoreMetaInfo):
			raise RuntimeError("Expected DataStoreMetaInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_metas(self, client, input, output):
		logger.info("DataStoreServer.get_metas()")
		#--- request ---
		data_ids = input.list(input.u64)
		param = input.extract(DataStoreGetMetaParam)
		response = await self.get_metas(client, data_ids, param)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['info', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.info, output.add)
		output.list(response.results, output.result)
	
	async def handle_prepare_update_object(self, client, input, output):
		logger.info("DataStoreServer.prepare_update_object()")
		#--- request ---
		param = input.extract(DataStorePrepareUpdateParam)
		response = await self.prepare_update_object(client, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqUpdateInfo):
			raise RuntimeError("Expected DataStoreReqUpdateInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_complete_update_object(self, client, input, output):
		logger.info("DataStoreServer.complete_update_object()")
		#--- request ---
		param = input.extract(DataStoreCompleteUpdateParam)
		await self.complete_update_object(client, param)
	
	async def handle_search_object(self, client, input, output):
		logger.info("DataStoreServer.search_object()")
		#--- request ---
		param = input.extract(DataStoreSearchParam)
		response = await self.search_object(client, param)
		
		#--- response ---
		if not isinstance(response, DataStoreSearchResult):
			raise RuntimeError("Expected DataStoreSearchResult, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_notification_url(self, client, input, output):
		logger.info("DataStoreServer.get_notification_url()")
		#--- request ---
		param = input.extract(DataStoreGetNotificationUrlParam)
		response = await self.get_notification_url(client, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqGetNotificationUrlInfo):
			raise RuntimeError("Expected DataStoreReqGetNotificationUrlInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_new_arrived_notifications_v1(self, client, input, output):
		logger.info("DataStoreServer.get_new_arrived_notifications_v1()")
		#--- request ---
		param = input.extract(DataStoreGetNewArrivedNotificationsParam)
		response = await self.get_new_arrived_notifications_v1(client, param)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'has_next']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.result, output.add)
		output.bool(response.has_next)
	
	async def handle_rate_object(self, client, input, output):
		logger.info("DataStoreServer.rate_object()")
		#--- request ---
		target = input.extract(DataStoreRatingTarget)
		param = input.extract(DataStoreRateObjectParam)
		fetch_ratings = input.bool()
		response = await self.rate_object(client, target, param, fetch_ratings)
		
		#--- response ---
		if not isinstance(response, DataStoreRatingInfo):
			raise RuntimeError("Expected DataStoreRatingInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_rating(self, client, input, output):
		logger.info("DataStoreServer.get_rating()")
		#--- request ---
		target = input.extract(DataStoreRatingTarget)
		access_password = input.u64()
		response = await self.get_rating(client, target, access_password)
		
		#--- response ---
		if not isinstance(response, DataStoreRatingInfo):
			raise RuntimeError("Expected DataStoreRatingInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_ratings(self, client, input, output):
		logger.info("DataStoreServer.get_ratings()")
		#--- request ---
		data_ids = input.list(input.u64)
		access_password = input.u64()
		response = await self.get_ratings(client, data_ids, access_password)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['ratings', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.ratings, lambda x: output.list(x, output.add))
		output.list(response.results, output.result)
	
	async def handle_reset_rating(self, client, input, output):
		logger.info("DataStoreServer.reset_rating()")
		#--- request ---
		target = input.extract(DataStoreRatingTarget)
		update_password = input.u64()
		await self.reset_rating(client, target, update_password)
	
	async def handle_reset_ratings(self, client, input, output):
		logger.info("DataStoreServer.reset_ratings()")
		#--- request ---
		data_ids = input.list(input.u64)
		transactional = input.bool()
		response = await self.reset_ratings(client, data_ids, transactional)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.result)
	
	async def handle_get_specific_meta_v1(self, client, input, output):
		logger.info("DataStoreServer.get_specific_meta_v1()")
		#--- request ---
		param = input.extract(DataStoreGetSpecificMetaParamV1)
		response = await self.get_specific_meta_v1(client, param)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_post_meta_binary(self, client, input, output):
		logger.info("DataStoreServer.post_meta_binary()")
		#--- request ---
		param = input.extract(DataStorePreparePostParam)
		response = await self.post_meta_binary(client, param)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u64(response)
	
	async def handle_touch_object(self, client, input, output):
		logger.info("DataStoreServer.touch_object()")
		#--- request ---
		param = input.extract(DataStoreTouchObjectParam)
		await self.touch_object(client, param)
	
	async def handle_get_rating_with_log(self, client, input, output):
		logger.info("DataStoreServer.get_rating_with_log()")
		#--- request ---
		target = input.extract(DataStoreRatingTarget)
		access_password = input.u64()
		response = await self.get_rating_with_log(client, target, access_password)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['rating', 'log']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.add(response.rating)
		output.add(response.log)
	
	async def handle_prepare_post_object(self, client, input, output):
		logger.info("DataStoreServer.prepare_post_object()")
		#--- request ---
		param = input.extract(DataStorePreparePostParam)
		response = await self.prepare_post_object(client, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqPostInfo):
			raise RuntimeError("Expected DataStoreReqPostInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_prepare_get_object(self, client, input, output):
		logger.info("DataStoreServer.prepare_get_object()")
		#--- request ---
		param = input.extract(DataStorePrepareGetParam)
		response = await self.prepare_get_object(client, param)
		
		#--- response ---
		if not isinstance(response, DataStoreReqGetInfo):
			raise RuntimeError("Expected DataStoreReqGetInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_complete_post_object(self, client, input, output):
		logger.info("DataStoreServer.complete_post_object()")
		#--- request ---
		param = input.extract(DataStoreCompletePostParam)
		await self.complete_post_object(client, param)
	
	async def handle_get_new_arrived_notifications(self, client, input, output):
		logger.info("DataStoreServer.get_new_arrived_notifications()")
		#--- request ---
		param = input.extract(DataStoreGetNewArrivedNotificationsParam)
		response = await self.get_new_arrived_notifications(client, param)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'has_next']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.result, output.add)
		output.bool(response.has_next)
	
	async def handle_get_specific_meta(self, client, input, output):
		logger.info("DataStoreServer.get_specific_meta()")
		#--- request ---
		param = input.extract(DataStoreGetSpecificMetaParam)
		response = await self.get_specific_meta(client, param)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_get_persistence_info(self, client, input, output):
		logger.info("DataStoreServer.get_persistence_info()")
		#--- request ---
		owner_id = input.pid()
		slot_id = input.u16()
		response = await self.get_persistence_info(client, owner_id, slot_id)
		
		#--- response ---
		if not isinstance(response, DataStorePersistenceInfo):
			raise RuntimeError("Expected DataStorePersistenceInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_persistence_infos(self, client, input, output):
		logger.info("DataStoreServer.get_persistence_infos()")
		#--- request ---
		owner_id = input.pid()
		slot_ids = input.list(input.u16)
		response = await self.get_persistence_infos(client, owner_id, slot_ids)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['infos', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.infos, output.add)
		output.list(response.results, output.result)
	
	async def handle_perpetuate_object(self, client, input, output):
		logger.info("DataStoreServer.perpetuate_object()")
		#--- request ---
		persistence_slot_id = input.u16()
		data_id = input.u64()
		delete_last_object = input.bool()
		await self.perpetuate_object(client, persistence_slot_id, data_id, delete_last_object)
	
	async def handle_unperpetuate_object(self, client, input, output):
		logger.info("DataStoreServer.unperpetuate_object()")
		#--- request ---
		persistence_slot_id = input.u16()
		delete_last_object = input.bool()
		await self.unperpetuate_object(client, persistence_slot_id, delete_last_object)
	
	async def handle_prepare_get_object_or_meta_binary(self, client, input, output):
		logger.info("DataStoreServer.prepare_get_object_or_meta_binary()")
		#--- request ---
		param = input.extract(DataStorePrepareGetParam)
		response = await self.prepare_get_object_or_meta_binary(client, param)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['get_info', 'additional_meta']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.add(response.get_info)
		output.add(response.additional_meta)
	
	async def handle_get_password_info(self, client, input, output):
		logger.info("DataStoreServer.get_password_info()")
		#--- request ---
		data_id = input.u64()
		response = await self.get_password_info(client, data_id)
		
		#--- response ---
		if not isinstance(response, DataStorePasswordInfo):
			raise RuntimeError("Expected DataStorePasswordInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_get_password_infos(self, client, input, output):
		logger.info("DataStoreServer.get_password_infos()")
		#--- request ---
		data_ids = input.list(input.u64)
		response = await self.get_password_infos(client, data_ids)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['infos', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.infos, output.add)
		output.list(response.results, output.result)
	
	async def handle_get_metas_multiple_param(self, client, input, output):
		logger.info("DataStoreServer.get_metas_multiple_param()")
		#--- request ---
		params = input.list(DataStoreGetMetaParam)
		response = await self.get_metas_multiple_param(client, params)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['infos', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.infos, output.add)
		output.list(response.results, output.result)
	
	async def handle_complete_post_objects(self, client, input, output):
		logger.info("DataStoreServer.complete_post_objects()")
		#--- request ---
		data_ids = input.list(input.u64)
		await self.complete_post_objects(client, data_ids)
	
	async def handle_change_meta(self, client, input, output):
		logger.info("DataStoreServer.change_meta()")
		#--- request ---
		param = input.extract(DataStoreChangeMetaParam)
		await self.change_meta(client, param)
	
	async def handle_change_metas(self, client, input, output):
		logger.info("DataStoreServer.change_metas()")
		#--- request ---
		data_ids = input.list(input.u64)
		param = input.list(DataStoreChangeMetaParam)
		transactional = input.bool()
		response = await self.change_metas(client, data_ids, param, transactional)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.result)
	
	async def handle_rate_objects(self, client, input, output):
		logger.info("DataStoreServer.rate_objects()")
		#--- request ---
		targets = input.list(DataStoreRatingTarget)
		param = input.list(DataStoreRateObjectParam)
		transactional = input.bool()
		fetch_ratings = input.bool()
		response = await self.rate_objects(client, targets, param, transactional, fetch_ratings)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['infos', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.infos, output.add)
		output.list(response.results, output.result)
	
	async def handle_post_meta_binary_with_data_id(self, client, input, output):
		logger.info("DataStoreServer.post_meta_binary_with_data_id()")
		#--- request ---
		data_id = input.u64()
		param = input.extract(DataStorePreparePostParam)
		await self.post_meta_binary_with_data_id(client, data_id, param)
	
	async def handle_post_meta_binaries_with_data_id(self, client, input, output):
		logger.info("DataStoreServer.post_meta_binaries_with_data_id()")
		#--- request ---
		data_ids = input.list(input.u64)
		param = input.list(DataStorePreparePostParam)
		transactional = input.bool()
		response = await self.post_meta_binaries_with_data_id(client, data_ids, param, transactional)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.result)
	
	async def handle_rate_object_with_posting(self, client, input, output):
		logger.info("DataStoreServer.rate_object_with_posting()")
		#--- request ---
		target = input.extract(DataStoreRatingTarget)
		rate_param = input.extract(DataStoreRateObjectParam)
		post_param = input.extract(DataStorePreparePostParam)
		fetch_ratings = input.bool()
		response = await self.rate_object_with_posting(client, target, rate_param, post_param, fetch_ratings)
		
		#--- response ---
		if not isinstance(response, DataStoreRatingInfo):
			raise RuntimeError("Expected DataStoreRatingInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def handle_rate_objects_with_posting(self, client, input, output):
		logger.info("DataStoreServer.rate_objects_with_posting()")
		#--- request ---
		targets = input.list(DataStoreRatingTarget)
		rate_param = input.list(DataStoreRateObjectParam)
		post_param = input.list(DataStorePreparePostParam)
		transactional = input.bool()
		fetch_ratings = input.bool()
		response = await self.rate_objects_with_posting(client, targets, rate_param, post_param, transactional, fetch_ratings)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['ratings', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.ratings, output.add)
		output.list(response.results, output.result)
	
	async def handle_get_object_infos(self, client, input, output):
		logger.info("DataStoreServer.get_object_infos()")
		#--- request ---
		data_ids = input.list(input.u64)
		response = await self.get_object_infos(client, data_ids)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['infos', 'results']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.list(response.infos, output.add)
		output.list(response.results, output.result)
	
	async def handle_search_object_light(self, client, input, output):
		logger.info("DataStoreServer.search_object_light()")
		#--- request ---
		param = input.extract(DataStoreSearchParam)
		response = await self.search_object_light(client, param)
		
		#--- response ---
		if not isinstance(response, DataStoreSearchResult):
			raise RuntimeError("Expected DataStoreSearchResult, got %s" %response.__class__.__name__)
		output.add(response)
	
	async def prepare_get_object_v1(self, *args):
		logger.warning("DataStoreServer.prepare_get_object_v1 not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def prepare_post_object_v1(self, *args):
		logger.warning("DataStoreServer.prepare_post_object_v1 not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def complete_post_object_v1(self, *args):
		logger.warning("DataStoreServer.complete_post_object_v1 not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_object(self, *args):
		logger.warning("DataStoreServer.delete_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_objects(self, *args):
		logger.warning("DataStoreServer.delete_objects not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def change_meta_v1(self, *args):
		logger.warning("DataStoreServer.change_meta_v1 not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def change_metas_v1(self, *args):
		logger.warning("DataStoreServer.change_metas_v1 not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_meta(self, *args):
		logger.warning("DataStoreServer.get_meta not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_metas(self, *args):
		logger.warning("DataStoreServer.get_metas not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def prepare_update_object(self, *args):
		logger.warning("DataStoreServer.prepare_update_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def complete_update_object(self, *args):
		logger.warning("DataStoreServer.complete_update_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def search_object(self, *args):
		logger.warning("DataStoreServer.search_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_notification_url(self, *args):
		logger.warning("DataStoreServer.get_notification_url not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_new_arrived_notifications_v1(self, *args):
		logger.warning("DataStoreServer.get_new_arrived_notifications_v1 not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def rate_object(self, *args):
		logger.warning("DataStoreServer.rate_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_rating(self, *args):
		logger.warning("DataStoreServer.get_rating not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_ratings(self, *args):
		logger.warning("DataStoreServer.get_ratings not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def reset_rating(self, *args):
		logger.warning("DataStoreServer.reset_rating not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def reset_ratings(self, *args):
		logger.warning("DataStoreServer.reset_ratings not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_specific_meta_v1(self, *args):
		logger.warning("DataStoreServer.get_specific_meta_v1 not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def post_meta_binary(self, *args):
		logger.warning("DataStoreServer.post_meta_binary not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def touch_object(self, *args):
		logger.warning("DataStoreServer.touch_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_rating_with_log(self, *args):
		logger.warning("DataStoreServer.get_rating_with_log not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def prepare_post_object(self, *args):
		logger.warning("DataStoreServer.prepare_post_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def prepare_get_object(self, *args):
		logger.warning("DataStoreServer.prepare_get_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def complete_post_object(self, *args):
		logger.warning("DataStoreServer.complete_post_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_new_arrived_notifications(self, *args):
		logger.warning("DataStoreServer.get_new_arrived_notifications not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_specific_meta(self, *args):
		logger.warning("DataStoreServer.get_specific_meta not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_persistence_info(self, *args):
		logger.warning("DataStoreServer.get_persistence_info not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_persistence_infos(self, *args):
		logger.warning("DataStoreServer.get_persistence_infos not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def perpetuate_object(self, *args):
		logger.warning("DataStoreServer.perpetuate_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def unperpetuate_object(self, *args):
		logger.warning("DataStoreServer.unperpetuate_object not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def prepare_get_object_or_meta_binary(self, *args):
		logger.warning("DataStoreServer.prepare_get_object_or_meta_binary not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_password_info(self, *args):
		logger.warning("DataStoreServer.get_password_info not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_password_infos(self, *args):
		logger.warning("DataStoreServer.get_password_infos not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_metas_multiple_param(self, *args):
		logger.warning("DataStoreServer.get_metas_multiple_param not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def complete_post_objects(self, *args):
		logger.warning("DataStoreServer.complete_post_objects not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def change_meta(self, *args):
		logger.warning("DataStoreServer.change_meta not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def change_metas(self, *args):
		logger.warning("DataStoreServer.change_metas not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def rate_objects(self, *args):
		logger.warning("DataStoreServer.rate_objects not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def post_meta_binary_with_data_id(self, *args):
		logger.warning("DataStoreServer.post_meta_binary_with_data_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def post_meta_binaries_with_data_id(self, *args):
		logger.warning("DataStoreServer.post_meta_binaries_with_data_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def rate_object_with_posting(self, *args):
		logger.warning("DataStoreServer.rate_object_with_posting not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def rate_objects_with_posting(self, *args):
		logger.warning("DataStoreServer.rate_objects_with_posting not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_object_infos(self, *args):
		logger.warning("DataStoreServer.get_object_infos not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def search_object_light(self, *args):
		logger.warning("DataStoreServer.search_object_light not implemented")
		raise common.RMCError("Core::NotImplemented")

