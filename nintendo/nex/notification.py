
from nintendo.nex import common

import logging
logger = logging.getLogger(__name__)


class NotificationEvent(common.Structure):
	def streamout(self, stream):
		self.pid = stream.u32()
		self.type = stream.u32()
		self.param1 = stream.u32()
		self.param2 = stream.u32()
		self.text = stream.string()
		
		if self.version >= 0:
			self.param3 = stream.u32()

			
class NotificationHandler:
	def process_notification_event(self, event): logger.warning("Notification: unhandled request (ProcessNotificationEvent)")


class NotificationServer:

	METHOD_PROCESS_NOTIFICATION_EVENT = 1

	PROTOCOL_ID = 0xE

	def __init__(self):
		self.methods = {
			self.METHOD_PROCESS_NOTIFICATION_EVENT: self.process_notification_event
		}
		self.handler = NotificationHandler()
	
	def handle_request(self, client, call_id, method_id, stream):
		if method_id in self.methods:
			return self.methods[method_id](client, call_id, method_id, stream)
		logger.warning("NotificationServer received request with unsupported method id: %i", method_id)

	def process_notification_event(self, client, call_id, method_id, stream):
		#--- request ---
		event = stream.extract(NotificationEvent)
		self.handler.process_notification_event(event)
		
		#--- response ---
		return client.init_response(self.PROTOCOL_ID, call_id, method_id)
