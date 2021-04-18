
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class RemoteLogDeviceProtocol:
	METHOD_LOG = 1
	
	PROTOCOL_ID = 0x1


class RemoteLogDeviceClient(RemoteLogDeviceProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def log(self, message):
		logger.info("RemoteLogDeviceClient.log()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_LOG, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("RemoteLogDeviceClient.log -> done")


class RemoteLogDeviceServer(RemoteLogDeviceProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_LOG: self.handle_log,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on RemoteLogDeviceServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_log(self, client, input, output):
		logger.info("RemoteLogDeviceServer.log()")
		#--- request ---
		message = input.string()
		await self.log(client, message)
	
	async def log(self, *args):
		logger.warning("RemoteLogDeviceServer.log not implemented")
		raise common.RMCError("Core::NotImplemented")

