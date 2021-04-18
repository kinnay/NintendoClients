
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class MonitoringProtocol:
	METHOD_PING_DAEMON = 1
	METHOD_GET_CLUSTER_MEMBERS = 2
	
	PROTOCOL_ID = 0x13


class MonitoringClient(MonitoringProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def ping_daemon(self):
		logger.info("MonitoringClient.ping_daemon()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PING_DAEMON, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MonitoringClient.ping_daemon -> done")
		return result
	
	async def get_cluster_members(self):
		logger.info("MonitoringClient.get_cluster_members()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_CLUSTER_MEMBERS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		members = stream.list(stream.string)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MonitoringClient.get_cluster_members -> done")
		return members


class MonitoringServer(MonitoringProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_PING_DAEMON: self.handle_ping_daemon,
			self.METHOD_GET_CLUSTER_MEMBERS: self.handle_get_cluster_members,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on MonitoringServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_ping_daemon(self, client, input, output):
		logger.info("MonitoringServer.ping_daemon()")
		#--- request ---
		response = await self.ping_daemon(client)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_get_cluster_members(self, client, input, output):
		logger.info("MonitoringServer.get_cluster_members()")
		#--- request ---
		response = await self.get_cluster_members(client)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.string)
	
	async def ping_daemon(self, *args):
		logger.warning("MonitoringServer.ping_daemon not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_cluster_members(self, *args):
		logger.warning("MonitoringServer.get_cluster_members not implemented")
		raise common.RMCError("Core::NotImplemented")

