
# This file was generated automatically from nattraversal.proto

from nintendo.nex import common

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
		self.client = client

	def request_probe_initiation(self, target_urls):
		logger.info("NATTraversalClient.request_probe_initiation()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_REQUEST_PROBE_INITIATION)
		stream.list(target_urls, stream.stationurl)
		self.client.send_message(stream)

		#--- response ---
		self.client.get_response(call_id)
		logger.info("NATTraversalClient.request_probe_initiation -> done")

	def initiate_probe(self, station_to_probe):
		logger.info("NATTraversalClient.initiate_probe()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_INITIATE_PROBE)
		stream.stationurl(station_to_probe)
		self.client.send_message(stream)

		#--- response ---
		self.client.get_response(call_id)
		logger.info("NATTraversalClient.initiate_probe -> done")

	def request_probe_initiation_ext(self, target_urls, station_to_probe):
		logger.info("NATTraversalClient.request_probe_initiation_ext()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_REQUEST_PROBE_INITIATION_EXT)
		stream.list(target_urls, stream.stationurl)
		stream.stationurl(station_to_probe)
		self.client.send_message(stream)

		#--- response ---
		self.client.get_response(call_id)
		logger.info("NATTraversalClient.request_probe_initiation_ext -> done")

	def report_nat_properties(self, natm, natf, rtt):
		logger.info("NATTraversalClient.report_nat_properties()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_REPORT_NAT_PROPERTIES)
		stream.u32(natm)
		stream.u32(natf)
		stream.u32(rtt)
		self.client.send_message(stream)

		#--- response ---
		self.client.get_response(call_id)
		logger.info("NATTraversalClient.report_nat_properties -> done")


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

	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			return self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on NATTraversalServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")

	def handle_request_probe_initiation(self, context, input, output):
		logger.info("NATTraversalServer.request_probe_initiation()")
		#--- request ---
		target_urls = input.list(input.stationurl)
		self.request_probe_initiation(context, target_urls)

	def handle_initiate_probe(self, context, input, output):
		logger.info("NATTraversalServer.initiate_probe()")
		#--- request ---
		station_to_probe = input.stationurl()
		self.initiate_probe(context, station_to_probe)

	def handle_request_probe_initiation_ext(self, context, input, output):
		logger.info("NATTraversalServer.request_probe_initiation_ext()")
		#--- request ---
		target_urls = input.list(input.stationurl)
		station_to_probe = input.stationurl()
		self.request_probe_initiation_ext(context, target_urls, station_to_probe)

	def handle_report_nat_traversal_result(self, context, input, output):
		logger.warning("NATTraversalSever.report_nat_traversal_result is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_report_nat_properties(self, context, input, output):
		logger.info("NATTraversalServer.report_nat_properties()")
		#--- request ---
		natm = input.u32()
		natf = input.u32()
		rtt = input.u32()
		self.report_nat_properties(context, natm, natf, rtt)

	def handle_get_relay_signature_key(self, context, input, output):
		logger.warning("NATTraversalSever.get_relay_signature_key is unsupported")
		return common.Result("Core::NotImplemented")

	def handle_report_nat_traversal_result_detail(self, context, input, output):
		logger.warning("NATTraversalSever.report_nat_traversal_result_detail is unsupported")
		return common.Result("Core::NotImplemented")

	def request_probe_initiation(self, *args):
		logger.warning("NATTraversalServer.request_probe_initiation not implemented")
		raise common.RMCError("Core::NotImplemented")

	def initiate_probe(self, *args):
		logger.warning("NATTraversalServer.initiate_probe not implemented")
		raise common.RMCError("Core::NotImplemented")

	def request_probe_initiation_ext(self, *args):
		logger.warning("NATTraversalServer.request_probe_initiation_ext not implemented")
		raise common.RMCError("Core::NotImplemented")

	def report_nat_properties(self, *args):
		logger.warning("NATTraversalServer.report_nat_properties not implemented")
		raise common.RMCError("Core::NotImplemented")
