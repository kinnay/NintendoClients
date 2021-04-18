
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class NotificationEvent(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.type = None
		self.param1 = 0
		self.param2 = 0
		self.text = ""
		self.param3 = 0
		self.map = {}
	
	def get_version(self, settings):
		version = 0
		if settings["nex.version"] >= 40000:
			version = 1
		return version
	
	def check_required(self, settings):
		for field in ['pid', 'type']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
		if settings["nex.version"] >= 30500:
			pass
		if settings["nex.version"] >= 40000:
			pass
	
	def load(self, stream):
		self.pid = stream.pid()
		self.type = stream.u32()
		self.param1 = stream.pid()
		self.param2 = stream.pid()
		self.text = stream.string()
		if stream.settings["nex.version"] >= 30500:
			self.param3 = stream.pid()
		if stream.settings["nex.version"] >= 40000:
			self.map = stream.map(stream.string, stream.variant)
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.pid)
		stream.u32(self.type)
		stream.pid(self.param1)
		stream.pid(self.param2)
		stream.string(self.text)
		if stream.settings["nex.version"] >= 30500:
			stream.pid(self.param3)
		if stream.settings["nex.version"] >= 40000:
			stream.map(self.map, stream.string, stream.variant)


class NotificationProtocol:
	METHOD_PROCESS_NOTIFICATION_EVENT = 1
	
	PROTOCOL_ID = 0xE


class NotificationClient(NotificationProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def process_notification_event(self, event):
		logger.info("NotificationClient.process_notification_event()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(event)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PROCESS_NOTIFICATION_EVENT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("NotificationClient.process_notification_event -> done")


class NotificationServer(NotificationProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_PROCESS_NOTIFICATION_EVENT: self.handle_process_notification_event,
		}
	
	async def process_event(self, type, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on NotificationServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_process_notification_event(self, client, input, output):
		logger.info("NotificationServer.process_notification_event()")
		#--- request ---
		event = input.extract(NotificationEvent)
		await self.process_notification_event(client, event)
	
	async def process_notification_event(self, *args):
		logger.warning("NotificationServer.process_notification_event not implemented")
		raise common.RMCError("Core::NotImplemented")

