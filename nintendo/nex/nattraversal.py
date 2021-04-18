
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class NATTraversalProtocol:
	METHOD_REQUEST_PROBE_INITIATION = 1
	METHOD_INITIATE_PROBE = 2
	METHOD_REQUEST_PROBE_INITIATION_EXT = 3
	METHOD_REPORT_NAT_TRAVERSAL_RESULT = 4
	METHOD_REPORT_NAT_PROPERTIES = 5
	METHOD_GET_RELAY_SIGNATURE_KEY = 6
	METHOD_REPORT_NAT_TRAVERSAL_RESULT_DETAIL = 7
	
	PROTOCOL_ID = 0x3


class NATTraversalClient(NATTraversalProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def request_probe_initiation(self, target_urls):
		logger.info("NATTraversalClient.request_probe_initiation()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(target_urls, stream.stationurl)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REQUEST_PROBE_INITIATION, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("NATTraversalClient.request_probe_initiation -> done")
	
	async def initiate_probe(self, station_to_probe):
		logger.info("NATTraversalClient.initiate_probe()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.stationurl(station_to_probe)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_INITIATE_PROBE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("NATTraversalClient.initiate_probe -> done")
	
	async def request_probe_initiation_ext(self, target_urls, station_to_probe):
		logger.info("NATTraversalClient.request_probe_initiation_ext()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(target_urls, stream.stationurl)
		stream.stationurl(station_to_probe)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REQUEST_PROBE_INITIATION_EXT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("NATTraversalClient.request_probe_initiation_ext -> done")
	
	async def report_nat_traversal_result(self, cid, result):
		logger.info("NATTraversalClient.report_nat_traversal_result()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(cid)
		stream.bool(result)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REPORT_NAT_TRAVERSAL_RESULT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("NATTraversalClient.report_nat_traversal_result -> done")
	
	async def report_nat_properties(self, natm, natf, rtt):
		logger.info("NATTraversalClient.report_nat_properties()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(natm)
		stream.u32(natf)
		stream.u32(rtt)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REPORT_NAT_PROPERTIES, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("NATTraversalClient.report_nat_properties -> done")
	
	async def get_relay_signature_key(self):
		logger.info("NATTraversalClient.get_relay_signature_key()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_RELAY_SIGNATURE_KEY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.mode = stream.s32()
		obj.time = stream.datetime()
		obj.address = stream.string()
		obj.port = stream.u16()
		obj.address_type = stream.s32()
		obj.game_server_id = stream.u32()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("NATTraversalClient.get_relay_signature_key -> done")
		return obj
	
	async def report_nat_traversal_result_detail(self, cid, result, detail, rtt):
		logger.info("NATTraversalClient.report_nat_traversal_result_detail()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(cid)
		stream.bool(result)
		stream.s32(detail)
		stream.u32(rtt)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_REPORT_NAT_TRAVERSAL_RESULT_DETAIL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("NATTraversalClient.report_nat_traversal_result_detail -> done")


class NATTraversalServer(NATTraversalProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_REQUEST_PROBE_INITIATION: self.handle_request_probe_initiation,
			self.METHOD_INITIATE_PROBE: self.handle_initiate_probe,
			self.METHOD_REQUEST_PROBE_INITIATION_EXT: self.handle_request_probe_initiation_ext,
			self.METHOD_REPORT_NAT_TRAVERSAL_RESULT: self.handle_report_nat_traversal_result,
			self.METHOD_REPORT_NAT_PROPERTIES: self.handle_report_nat_properties,
			self.METHOD_GET_RELAY_SIGNATURE_KEY: self.handle_get_relay_signature_key,
			self.METHOD_REPORT_NAT_TRAVERSAL_RESULT_DETAIL: self.handle_report_nat_traversal_result_detail,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on NATTraversalServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_request_probe_initiation(self, client, input, output):
		logger.info("NATTraversalServer.request_probe_initiation()")
		#--- request ---
		target_urls = input.list(input.stationurl)
		await self.request_probe_initiation(client, target_urls)
	
	async def handle_initiate_probe(self, client, input, output):
		logger.info("NATTraversalServer.initiate_probe()")
		#--- request ---
		station_to_probe = input.stationurl()
		await self.initiate_probe(client, station_to_probe)
	
	async def handle_request_probe_initiation_ext(self, client, input, output):
		logger.info("NATTraversalServer.request_probe_initiation_ext()")
		#--- request ---
		target_urls = input.list(input.stationurl)
		station_to_probe = input.stationurl()
		await self.request_probe_initiation_ext(client, target_urls, station_to_probe)
	
	async def handle_report_nat_traversal_result(self, client, input, output):
		logger.info("NATTraversalServer.report_nat_traversal_result()")
		#--- request ---
		cid = input.u32()
		result = input.bool()
		await self.report_nat_traversal_result(client, cid, result)
	
	async def handle_report_nat_properties(self, client, input, output):
		logger.info("NATTraversalServer.report_nat_properties()")
		#--- request ---
		natm = input.u32()
		natf = input.u32()
		rtt = input.u32()
		await self.report_nat_properties(client, natm, natf, rtt)
	
	async def handle_get_relay_signature_key(self, client, input, output):
		logger.info("NATTraversalServer.get_relay_signature_key()")
		#--- request ---
		response = await self.get_relay_signature_key(client)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['mode', 'time', 'address', 'port', 'address_type', 'game_server_id']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.s32(response.mode)
		output.datetime(response.time)
		output.string(response.address)
		output.u16(response.port)
		output.s32(response.address_type)
		output.u32(response.game_server_id)
	
	async def handle_report_nat_traversal_result_detail(self, client, input, output):
		logger.info("NATTraversalServer.report_nat_traversal_result_detail()")
		#--- request ---
		cid = input.u32()
		result = input.bool()
		detail = input.s32()
		rtt = input.u32()
		await self.report_nat_traversal_result_detail(client, cid, result, detail, rtt)
	
	async def request_probe_initiation(self, *args):
		logger.warning("NATTraversalServer.request_probe_initiation not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def initiate_probe(self, *args):
		logger.warning("NATTraversalServer.initiate_probe not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def request_probe_initiation_ext(self, *args):
		logger.warning("NATTraversalServer.request_probe_initiation_ext not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def report_nat_traversal_result(self, *args):
		logger.warning("NATTraversalServer.report_nat_traversal_result not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def report_nat_properties(self, *args):
		logger.warning("NATTraversalServer.report_nat_properties not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_relay_signature_key(self, *args):
		logger.warning("NATTraversalServer.get_relay_signature_key not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def report_nat_traversal_result_detail(self, *args):
		logger.warning("NATTraversalServer.report_nat_traversal_result_detail not implemented")
		raise common.RMCError("Core::NotImplemented")

