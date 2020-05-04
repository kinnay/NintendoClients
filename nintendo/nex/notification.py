
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


class NintendoNotificationType:
	LOGOUT = 10
	PRESENCE_CHANGE = 24
	UNFRIENDED = 26
	FRIENDED = 30
	STATUS_CHANGE = 33


class NotificationEvent(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.type = None
		self.param1 = None
		self.param2 = None
		self.text = None
		self.param3 = None
	
	def check_required(self, settings):
		for field in ['pid', 'type', 'param1', 'param2', 'text']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings.get("nex.version") >= 30500:
			for field in ['param3']:
				if getattr(self, field) is None:
					raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.pid = stream.pid()
		self.type = stream.u32()
		self.param1 = stream.pid()
		self.param2 = stream.pid()
		self.text = stream.string()
		if stream.settings.get("nex.version") >= 30500:
			self.param3 = stream.pid()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.pid)
		stream.u32(self.type)
		stream.pid(self.param1)
		stream.pid(self.param2)
		stream.string(self.text)
		if stream.settings.get("nex.version") >= 30500:
			stream.pid(self.param3)


class NintendoNotificationEvent(common.Structure):
	def __init__(self):
		super().__init__()
		self.type = None
		self.pid = None
		self.data = None
	
	def check_required(self, settings):
		for field in ['type', 'pid', 'data']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.type = stream.u32()
		self.pid = stream.pid()
		self.data = stream.anydata()
	
	def save(self, stream):
		self.check_required(stream.settings)
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
	
	def check_required(self, settings):
		for field in ['param1', 'param2', 'param3', 'text']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.param1 = stream.u32()
		self.param2 = stream.u64()
		self.param3 = stream.u64()
		self.text = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u32(self.param1)
		stream.u64(self.param2)
		stream.u64(self.param3)
		stream.string(self.text)
common.DataHolder.register(NintendoNotificationEventGeneral, "NintendoNotificationEventGeneral")


class NotificationProtocol:
	METHOD_PROCESS_NOTIFICATION_EVENT = 1
	
	PROTOCOL_ID = 0xE


class NintendoNotificationProtocol:
	METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT = 1
	METHOD_PROCESS_PRESENCE_CHANGE_EVENT = 2
	
	PROTOCOL_ID = 0x64


class NotificationClient(NotificationProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def process_notification_event(self, event):
		logger.info("NotificationClient.process_notification_event()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(event)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_PROCESS_NOTIFICATION_EVENT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("NotificationClient.process_notification_event -> done")


class NintendoNotificationClient(NintendoNotificationProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def process_nintendo_notification_event(self, event):
		logger.info("NintendoNotificationClient.process_nintendo_notification_event()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(event)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("NintendoNotificationClient.process_nintendo_notification_event -> done")
	
	def process_presence_change_event(self, event):
		logger.info("NintendoNotificationClient.process_presence_change_event()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(event)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_PROCESS_PRESENCE_CHANGE_EVENT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("NintendoNotificationClient.process_presence_change_event -> done")


class NotificationServer(NotificationProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_PROCESS_NOTIFICATION_EVENT: self.handle_process_notification_event,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_process_notification_event(self, context, input, output):
		logger.info("NotificationServer.process_notification_event()")
		#--- request ---
		event = input.extract(NotificationEvent)
		self.process_notification_event(context, event)
	
	def process_notification_event(self, *args):
		logger.warning("NotificationServer.process_notification_event not implemented")
		raise common.RMCError("Core::NotImplemented")


class NintendoNotificationServer(NintendoNotificationProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT: self.handle_process_nintendo_notification_event,
			self.METHOD_PROCESS_PRESENCE_CHANGE_EVENT: self.handle_process_presence_change_event,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_process_nintendo_notification_event(self, context, input, output):
		logger.info("NintendoNotificationServer.process_nintendo_notification_event()")
		#--- request ---
		event = input.extract(NintendoNotificationEvent)
		self.process_nintendo_notification_event(context, event)
	
	def handle_process_presence_change_event(self, context, input, output):
		logger.info("NintendoNotificationServer.process_presence_change_event()")
		#--- request ---
		event = input.extract(NintendoNotificationEvent)
		self.process_presence_change_event(context, event)
	
	def process_nintendo_notification_event(self, *args):
		logger.warning("NintendoNotificationServer.process_nintendo_notification_event not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def process_presence_change_event(self, *args):
		logger.warning("NintendoNotificationServer.process_presence_change_event not implemented")
		raise common.RMCError("Core::NotImplemented")

