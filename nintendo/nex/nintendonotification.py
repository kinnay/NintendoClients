
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class NintendoNotificationType:
	LOGOUT = 10
	PRESENCE_CHANGE = 24
	UNFRIENDED = 26
	FRIENDED = 30
	STATUS_CHANGE = 33


class u8KeyValue(common.Data):
	def __init__(self):
		super().__init__()
		self.key = None
		self.value = None
	
	def check_required(self, settings, version):
		for field in ['key', 'value']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.key = stream.u8()
		self.value = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u8(self.key)
		stream.u8(self.value)
common.DataHolder.register(u8KeyValue, "u8KeyValue")


class u32KeyValue(common.Data):
	def __init__(self):
		super().__init__()
		self.key = None
		self.value = None
	
	def check_required(self, settings, version):
		for field in ['key', 'value']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.key = stream.u8()
		self.value = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u8(self.key)
		stream.u32(self.value)
common.DataHolder.register(u32KeyValue, "u32KeyValue")


class u64KeyValue(common.Data):
	def __init__(self):
		super().__init__()
		self.key = None
		self.value = None
	
	def check_required(self, settings, version):
		for field in ['key', 'value']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.key = stream.u8()
		self.value = stream.u64()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u8(self.key)
		stream.u64(self.value)
common.DataHolder.register(u64KeyValue, "u64KeyValue")


class StringKeyValue(common.Data):
	def __init__(self):
		super().__init__()
		self.key = None
		self.value = None
	
	def check_required(self, settings, version):
		for field in ['key', 'value']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.key = stream.u8()
		self.value = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u8(self.key)
		stream.string(self.value)
common.DataHolder.register(StringKeyValue, "StringKeyValue")


class NintendoNotificationEvent(common.Structure):
	def __init__(self):
		super().__init__()
		self.type = None
		self.pid = None
		self.data = None
	
	def check_required(self, settings, version):
		for field in ['type', 'pid', 'data']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.type = stream.u32()
		self.pid = stream.pid()
		self.data = stream.anydata()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.type)
		stream.pid(self.pid)
		stream.anydata(self.data)


class NintendoNotificationEventGeneral(common.Data):
	def __init__(self):
		super().__init__()
		self.param1 = None
		self.param2 = None
		self.param3 = None
		self.text = None
	
	def check_required(self, settings, version):
		for field in ['param1', 'param2', 'param3', 'text']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.param1 = stream.u32()
		self.param2 = stream.u64()
		self.param3 = stream.u64()
		self.text = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.param1)
		stream.u64(self.param2)
		stream.u64(self.param3)
		stream.string(self.text)
common.DataHolder.register(NintendoNotificationEventGeneral, "NintendoNotificationEventGeneral")


class NintendoNotificationEventKeyValue(common.Data):
	def __init__(self):
		super().__init__()
		self.u8 = None
		self.u32 = None
		self.u64 = None
		self.string = None
	
	def check_required(self, settings, version):
		for field in ['u8', 'u32', 'u64', 'string']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.u8 = stream.list(u8KeyValue)
		self.u32 = stream.list(u32KeyValue)
		self.u64 = stream.list(u64KeyValue)
		self.string = stream.list(StringKeyValue)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.list(self.u8, stream.add)
		stream.list(self.u32, stream.add)
		stream.list(self.u64, stream.add)
		stream.list(self.string, stream.add)
common.DataHolder.register(NintendoNotificationEventKeyValue, "NintendoNotificationEventKeyValue")


class NintendoNotificationEventProfile(common.Data):
	def __init__(self):
		super().__init__()
		self.region = None
		self.country = None
		self.area = None
		self.language = None
		self.platform = None
	
	def check_required(self, settings, version):
		for field in ['region', 'country', 'area', 'language', 'platform']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.region = stream.u8()
		self.country = stream.u8()
		self.area = stream.u8()
		self.language = stream.u8()
		self.platform = stream.u8()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u8(self.region)
		stream.u8(self.country)
		stream.u8(self.area)
		stream.u8(self.language)
		stream.u8(self.platform)
common.DataHolder.register(NintendoNotificationEventProfile, "NintendoNotificationEventProfile")


class NintendoNotificationProtocol:
	NORESPONSE = True
	
	METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT = 1
	METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT_ALT = 2
	
	PROTOCOL_ID = 0x64


class NintendoNotificationClient(NintendoNotificationProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def process_nintendo_notification_event(self, event):
		logger.info("NintendoNotificationClient.process_nintendo_notification_event()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(event)
		await self.client.request(self.PROTOCOL_ID, self.METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT, stream.get(), True)
	
	async def process_nintendo_notification_event_alt(self, event):
		logger.info("NintendoNotificationClient.process_nintendo_notification_event_alt()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(event)
		await self.client.request(self.PROTOCOL_ID, self.METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT_ALT, stream.get(), True)


class NintendoNotificationServer(NintendoNotificationProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT: self.handle_process_nintendo_notification_event,
			self.METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT_ALT: self.handle_process_nintendo_notification_event_alt,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on NintendoNotificationServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_process_nintendo_notification_event(self, client, input, output):
		logger.info("NintendoNotificationServer.process_nintendo_notification_event()")
		#--- request ---
		event = input.extract(NintendoNotificationEvent)
		await self.process_nintendo_notification_event(client, event)
	
	async def handle_process_nintendo_notification_event_alt(self, client, input, output):
		logger.info("NintendoNotificationServer.process_nintendo_notification_event_alt()")
		#--- request ---
		event = input.extract(NintendoNotificationEvent)
		await self.process_nintendo_notification_event_alt(client, event)
	
	async def process_nintendo_notification_event(self, *args):
		logger.warning("NintendoNotificationServer.process_nintendo_notification_event not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def process_nintendo_notification_event_alt(self, *args):
		logger.warning("NintendoNotificationServer.process_nintendo_notification_event_alt not implemented")
		raise common.RMCError("Core::NotImplemented")

