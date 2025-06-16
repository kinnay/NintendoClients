
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class ScreeningProtocol:
	METHOD_REPORT_DATA_STORE_CONTENT = 1
	METHOD_REPORT_USER = 2
	
	PROTOCOL_ID = 0x7C


class ScreeningClient(ScreeningProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	


class ScreeningServer(ScreeningProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_REPORT_DATA_STORE_CONTENT: self.handle_report_data_store_content,
			self.METHOD_REPORT_USER: self.handle_report_user,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on ScreeningServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_report_data_store_content(self, client, input, output):
		logger.warning("ScreeningServer.report_data_store_content is not supported")
		raise common.RMCError("Core::NotImplemented")
	
	async def handle_report_user(self, client, input, output):
		logger.warning("ScreeningServer.report_user is not supported")
		raise common.RMCError("Core::NotImplemented")

