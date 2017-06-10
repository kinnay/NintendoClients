
from nintendo.nex.common import NexEncoder, DataHolder

import logging
logger = logging.getLogger(__name__)


class NintendoNotificationEventGeneral(NexDataEncoder):
	version_map = {
		30504: 0
	}

	def get_name(self):
		return "NintendoNotificationEventGeneral"

	def decode_old(self, stream):
		self.unk1 = stream.u32()
		self.unk2 = stream.u64()
		self.unk3 = stream.u64()
		self.string = stream.string()
		
	decode_v0 = decode_old
DataHolder.register(NintendoNotificationEventGeneral, "NintendoNotificationEventGeneral")


class NintendoNotificationEvent(NexEncoder):
	version_map = {
		30504: 0
	}
	def decode_old(self, stream):
		self.unk1 = stream.u32()
		self.unk2 = stream.u32()
		self.object = DataHolder.from_stream(stream)
		
	decode_v0 = decode_old


class NintendoNotificationServer:

	METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT = 1

	PROTOCOL_ID = 0x64
	
	def __init__(self):
		self.methods = {
			self.METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT: self.process_nintendo_notification_event
		}
		
	def handle_request(self, client, call_id, method_id, stream):
		if method_id in self.methods:
			return self.methods[method_id](client, call_id, method_id, stream)
		logger.warning("NintendoNotificationServer received request with unsupported method id: %i", method_id)

	def process_nintendo_notification_event(self, client, call_id, method_id, stream):
		#--- request ---
		notification = NintendoNotificationEvent.from_stream(stream)
		logger.info(
			"NintendoNotification.process_nintendo_notification_event: (%08X, %08X, %s)",
			notification.unk1, notification.unk2, notification.object.get_name()
		)
		
		#--- response ---
		return client.init_response(self.PROTOCOL_ID, call_id, method_id)