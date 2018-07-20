
from nintendo.nex import common

import logging
logger = logging.getLogger(__name__)


class NotificationType:
	LOGOUT = 10
	PRESENCE_CHANGE = 24
	UNFRIENDED = 26
	STATUS_CHANGE = 33


class NintendoNotificationEventGeneral(common.Data):
	def get_name(self):
		return "NintendoNotificationEventGeneral"

	def streamout(self, stream):
		self.param1 = stream.u32()
		self.param2 = stream.u64()
		self.param3 = stream.u64()
		self.text = stream.string()
common.DataHolder.register(NintendoNotificationEventGeneral, "NintendoNotificationEventGeneral")


class NintendoNotificationEvent(common.Structure):
	def streamout(self, stream):
		self.type = stream.u32()
		self.pid = stream.u32()
		self.data = stream.anydata()


class NintendoNotificationHandler:
	def process_notification_event(self, event):
		logger.warning("NintendoNotification: unhandled request (ProcessNotificationEvent)")

		
class NintendoNotificationServer:

	METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT = 1
	METHOD_PROCESS_PRESENCE_CHANGE_EVENT = 2 #Only used by iosu

	PROTOCOL_ID = 0x64
	
	def __init__(self):
		self.methods = {
			self.METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT: self.process_notification_event,
			self.METHOD_PROCESS_PRESENCE_CHANGE_EVENT: self.process_notification_event
		}
		self.handler = NintendoNotificationHandler()
		
	def handle_request(self, client, call_id, method_id, stream):
		if method_id in self.methods:
			return self.methods[method_id](client, call_id, method_id, stream)
		logger.warning("NintendoNotificationServer received request with unsupported method id: %i", method_id)

	def process_notification_event(self, client, call_id, method_id, stream):
		#--- request ---
		event = stream.extract(NintendoNotificationEvent)
		self.handler.process_notification_event(event)
		
		#--- response ---
		return client.init_response(self.PROTOCOL_ID, call_id, method_id)
