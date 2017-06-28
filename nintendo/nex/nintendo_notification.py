
from nintendo.nex.common import NexEncoder, NexDataEncoder, DataHolder
from nintendo.nex.server import ProtocolServer

import logging
logger = logging.getLogger(__name__)


class NotificationType:
	LOGOUT = 10
	PRESENCE_CHANGE = 24
	UNFRIENDED = 26
	STATUS_CHANGE = 33


class NintendoNotificationEventGeneral(NexDataEncoder):
	version_map = {
		30504: 0
	}

	def get_name(self):
		return "NintendoNotificationEventGeneral"

	def decode_old(self, stream):
		self.unk1 = stream.u32()
		self.unk2 = stream.u64()
		self.notification_id = stream.u64()
		self.text = stream.string()
		
	decode_v0 = decode_old
DataHolder.register(NintendoNotificationEventGeneral, "NintendoNotificationEventGeneral")


class NintendoNotificationEvent(NexEncoder):
	version_map = {
		30504: 0
	}
	def decode_old(self, stream):
		self.type = stream.u32()
		self.pid = stream.u32()
		self.object = DataHolder.from_stream(stream).data
		
	decode_v0 = decode_old


class NintendoNotificationServer(ProtocolServer):

	METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT = 1
	METHOD_PROCESS_PRESENCE_CHANGE_EVENT = 2 #Only used by iosu

	PROTOCOL_ID = 0x64
	
	def __init__(self):
		self.methods = {
			self.METHOD_PROCESS_NINTENDO_NOTIFICATION_EVENT: self.process_notification_event,
			self.METHOD_PROCESS_PRESENCE_CHANGE_EVENT: self.process_notification_event
		}
		self.init_callbacks(*self.methods)
		
	def handle_request(self, client, call_id, method_id, stream):
		if method_id in self.methods:
			return self.methods[method_id](client, call_id, method_id, stream)
		logger.warning("NintendoNotificationServer received request with unsupported method id: %i", method_id)

	def process_notification_event(self, client, call_id, method_id, stream):
		#--- request ---
		notification = NintendoNotificationEvent.from_stream(stream)
		logger.info(
			"NintendoNotification.process_nintendo_notification_event: (%i, %08X, %s)",
			notification.type, notification.pid, notification.object.get_name()
		)
		
		self.callback(method_id, notification)
		
		#--- response ---
		return client.init_response(self.PROTOCOL_ID, call_id, method_id)
