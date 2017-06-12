
from nintendo.nex.common import StationUrl

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
	
	def report_nat_properties(self, arg1, arg2, arg3):
		logger.info("NATTraversal.report_nat_properties(%08X, %08X, %08X)", arg1, arg2, arg3)
		#--- request ---
		stream, call_id = self.client.init_message(self.PROTOCOL_ID, self.METHOD_REPORT_NAT_PROPERTIES)
		stream.u32(arg1)
		stream.u32(arg2)
		stream.u32(arg3)
		self.client.send_message(stream)
		
		#--- response ---
		self.client.get_response(call_id)
		logger.info("NATTraversal.report_nat_properties -> done")

		
class NATTraversalServer(NATTraversalProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_INITIATE_PROBE: self.initiate_probe
		}

	def handle_request(self, client, call_id, method_id, stream):
		if method_id in self.methods:
			return self.methods[method_id](client, call_id, method_id, stream)
		logger.warning("NATTraversalServer received request with unsupported method id: %i", method_id)
		
	def initiate_probe(self, client, call_id, method_id, stream):
		#--- request ---
		url = StationUrl(stream.string())
		logger.info("NATTraversal.initiate_probe: %s", url)
		
		#--- response ---
		return client.init_response(self.PROTOCOL_ID, call_id, method_id)
