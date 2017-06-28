
from nintendo.nex.common import StationUrl
from nintendo.nex.server import ProtocolServer

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

	PROTOCOL_ID = 3


class NATTraversalClient(NATTraversalProtocol):
	def __init__(self, back_end):
		self.client = back_end.secure_client
		
	def request_probe_initiation_ext(self, urllist, url):
		logger.info("NATTraversal.request_probe_initiation_ext(%s, %s)", urllist, url)
		#--- request ---
		stream, call_id = self.client.init_message(self.PROTOCOL_ID, self.METHOD_REQUEST_PROBE_INITIATION_EXT)
		stream.list(urllist, lambda x: stream.string(str(x)))
		stream.string(str(url))
		self.client.send_message(stream)
		
		#--- response ---
		self.client.get_response(call_id)
		logger.info("NATTraversal.request_probe_initiation_ext -> done")
	
	def report_nat_properties(self, nat_mapping, nat_filtering, lag):
		logger.info("NATTraversal.report_nat_properties(%08X, %08X, %08X)", nat_mapping, nat_filtering, lag)
		#--- request ---
		stream, call_id = self.client.init_message(self.PROTOCOL_ID, self.METHOD_REPORT_NAT_PROPERTIES)
		stream.u32(nat_mapping)
		stream.u32(nat_filtering)
		stream.u32(lag)
		self.client.send_message(stream)
		
		#--- response ---
		self.client.get_response(call_id)
		logger.info("NATTraversal.report_nat_properties -> done")

		
class NATTraversalServer(NATTraversalProtocol, ProtocolServer):
	def __init__(self):
		self.methods = {
			self.METHOD_INITIATE_PROBE: self.initiate_probe
		}
		self.init_callbacks(*self.methods)

	def handle_request(self, client, call_id, method_id, stream):
		if method_id in self.methods:
			return self.methods[method_id](client, call_id, method_id, stream)
		logger.warning("NATTraversalServer received request with unsupported method id: %i", method_id)
		
	def initiate_probe(self, client, call_id, method_id, stream):
		#--- request ---
		url = StationUrl.parse(stream.string())
		logger.info("NATTraversal.initiate_probe: %s", url)
		
		self.callback(method_id, url)
		
		#--- response ---
		return client.init_response(self.PROTOCOL_ID, call_id, method_id)
