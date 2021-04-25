
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class ApplicationInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.title_id = None
		self.title_version = None
	
	def check_required(self, settings, version):
		for field in ['title_id', 'title_version']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.title_id = stream.u64()
		self.title_version = stream.u16()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u64(self.title_id)
		stream.u16(self.title_version)


class AAUserProtocol:
	METHOD_REGISTER_APPLICATION = 1
	METHOD_UNREGISTER_APPLICATION = 2
	METHOD_SET_APPLICATION_INFO = 3
	METHOD_GET_APPLICATION_INFO = 4
	
	PROTOCOL_ID = 0x7B


class AAUserClient(AAUserProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def register_application(self, title_id):
		logger.info("AAUserClient.register_application()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(title_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REGISTER_APPLICATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AAUserClient.register_application -> done")
	
	async def unregister_application(self, title_id):
		logger.info("AAUserClient.unregister_application()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u64(title_id)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_UNREGISTER_APPLICATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AAUserClient.unregister_application -> done")
	
	async def set_application_info(self, application_info):
		logger.info("AAUserClient.set_application_info()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(application_info, stream.add)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_SET_APPLICATION_INFO, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AAUserClient.set_application_info -> done")
	
	async def get_application_info(self):
		logger.info("AAUserClient.get_application_info()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_APPLICATION_INFO, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.list(ApplicationInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AAUserClient.get_application_info -> done")
		return info


class AAUserServer(AAUserProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_REGISTER_APPLICATION: self.handle_register_application,
			self.METHOD_UNREGISTER_APPLICATION: self.handle_unregister_application,
			self.METHOD_SET_APPLICATION_INFO: self.handle_set_application_info,
			self.METHOD_GET_APPLICATION_INFO: self.handle_get_application_info,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on AAUserServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_register_application(self, client, input, output):
		logger.info("AAUserServer.register_application()")
		#--- request ---
		title_id = input.u64()
		await self.register_application(client, title_id)
	
	async def handle_unregister_application(self, client, input, output):
		logger.info("AAUserServer.unregister_application()")
		#--- request ---
		title_id = input.u64()
		await self.unregister_application(client, title_id)
	
	async def handle_set_application_info(self, client, input, output):
		logger.info("AAUserServer.set_application_info()")
		#--- request ---
		application_info = input.list(ApplicationInfo)
		await self.set_application_info(client, application_info)
	
	async def handle_get_application_info(self, client, input, output):
		logger.info("AAUserServer.get_application_info()")
		#--- request ---
		response = await self.get_application_info(client)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def register_application(self, *args):
		logger.warning("AAUserServer.register_application not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def unregister_application(self, *args):
		logger.warning("AAUserServer.unregister_application not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def set_application_info(self, *args):
		logger.warning("AAUserServer.set_application_info not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_application_info(self, *args):
		logger.warning("AAUserServer.get_application_info not implemented")
		raise common.RMCError("Core::NotImplemented")

