
from nintendo.nex.common import NexEncoder

import logging
logger = logging.getLogger(__name__)


class NotificationEvent(NexEncoder):
	version_map = {
		30504: 0
	}
	
	def decode_old(self, stream):
		self.unk1 = stream.u32()
		self.unk2 = stream.u32()
		self.unk3 = stream.u32()
		self.unk4 = stream.u32()
		self.string = stream.string()
		
	def decode_v0(self, stream):
		self.decode_old(stream)
		self.unk5 = stream.u32()


class NotificationServer:

	METHOD_PROCESS_NOTIFICATION_EVENT = 1

	PROTOCOL_ID = 0xE

	def __init__(self):
		self.methods = {
			self.METHOD_PROCESS_NOTIFICATION_EVENT: self.process_notification_event
		}
	
	def handle_request(self, client, call_id, method_id, stream):
		if method_id in self.methods:
			return self.methods[method_id](client, call_id, method_id, stream)
		logger.warning("NotificationServer received request with unsupported method id: %i", method_id)
			
	def process_notification_event(self, client, call_id, method_id, stream):
		#--- request ---
		notification = NotificationEvent.from_stream(stream)
		logger.info(
			"Notification.process_notification_event: (%08X, %08X, %08X, %08X, %s)",
			notification.unk1, notification.unk2, notification.unk3, notification.unk4, notification.string
		)
		
		#--- response ---
		return client.init_response(self.PROTOCOL_ID, call_id, method_id)