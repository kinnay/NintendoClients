
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class ScreeningProtocol:
	
	PROTOCOL_ID = 0x7C


class ScreeningClient(ScreeningProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	


class ScreeningServer(ScreeningProtocol):
	def __init__(self):
		self.methods = {
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on ScreeningServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")

