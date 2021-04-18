
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class HealthProtocol:
	METHOD_PING_DAEMON = 1
	METHOD_PING_DATABASE = 2
	METHOD_RUN_SANITY_CHECK = 3
	METHOD_FIX_SANITY_ERRORS = 4
	
	PROTOCOL_ID = 0x12


class HealthClient(HealthProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def ping_daemon(self):
		logger.info("HealthClient.ping_daemon()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PING_DAEMON, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("HealthClient.ping_daemon -> done")
		return result
	
	async def ping_database(self):
		logger.info("HealthClient.ping_database()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_PING_DATABASE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("HealthClient.ping_database -> done")
		return result
	
	async def run_sanity_check(self):
		logger.info("HealthClient.run_sanity_check()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_RUN_SANITY_CHECK, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("HealthClient.run_sanity_check -> done")
		return result
	
	async def fix_sanity_errors(self):
		logger.info("HealthClient.fix_sanity_errors()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_FIX_SANITY_ERRORS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("HealthClient.fix_sanity_errors -> done")
		return result


class HealthServer(HealthProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_PING_DAEMON: self.handle_ping_daemon,
			self.METHOD_PING_DATABASE: self.handle_ping_database,
			self.METHOD_RUN_SANITY_CHECK: self.handle_run_sanity_check,
			self.METHOD_FIX_SANITY_ERRORS: self.handle_fix_sanity_errors,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on HealthServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_ping_daemon(self, client, input, output):
		logger.info("HealthServer.ping_daemon()")
		#--- request ---
		response = await self.ping_daemon(client)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_ping_database(self, client, input, output):
		logger.info("HealthServer.ping_database()")
		#--- request ---
		response = await self.ping_database(client)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_run_sanity_check(self, client, input, output):
		logger.info("HealthServer.run_sanity_check()")
		#--- request ---
		response = await self.run_sanity_check(client)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def handle_fix_sanity_errors(self, client, input, output):
		logger.info("HealthServer.fix_sanity_errors()")
		#--- request ---
		response = await self.fix_sanity_errors(client)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	async def ping_daemon(self, *args):
		logger.warning("HealthServer.ping_daemon not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def ping_database(self, *args):
		logger.warning("HealthServer.ping_database not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def run_sanity_check(self, *args):
		logger.warning("HealthServer.run_sanity_check not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def fix_sanity_errors(self, *args):
		logger.warning("HealthServer.fix_sanity_errors not implemented")
		raise common.RMCError("Core::NotImplemented")

