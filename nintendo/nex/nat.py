
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
	def __init__(self, backend):
		self.client = backend.secure_client
		
	def request_probe_initiation_ext(self, target_urls, station_to_probe):
		logger.info("NATTraversal.request_probe_initiation_ext(%s, %s)", target_urls, station_to_probe)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_REQUEST_PROBE_INITIATION_EXT)
		stream.list(target_urls, stream.stationurl)
		stream.stationurl(station_to_probe)
		self.client.send_message(stream)
		
		#--- response ---
		self.client.get_response(call_id)
		logger.info("NATTraversal.request_probe_initiation_ext -> done")
	
	def report_nat_properties(self, nat_mapping, nat_filtering, rtt):
		logger.info("NATTraversal.report_nat_properties(%08X, %08X, %08X)", nat_mapping, nat_filtering, rtt)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_REPORT_NAT_PROPERTIES)
		stream.u32(nat_mapping)
		stream.u32(nat_filtering)
		stream.u32(rtt)
		self.client.send_message(stream)
		
		#--- response ---
		self.client.get_response(call_id)
		logger.info("NATTraversal.report_nat_properties -> done")

		
class NATTraversalHandler:
	def initiate_probe(self, station_to_probe): logger.warning("NATTraversal: unhandled request (InitiateProbe)")
		
		
class NATTraversalServer(NATTraversalProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_INITIATE_PROBE: self.initiate_probe
		}
		self.handler = NATTraversalHandler()

	def handle_request(self, client, call_id, method_id, stream):
		if method_id in self.methods:
			return self.methods[method_id](client, call_id, method_id, stream)
		logger.warning("NATTraversalServer received request with unsupported method id: %i", method_id)
		
	def initiate_probe(self, client, call_id, method_id, stream):
		#--- request ---
		self.handler.initiate_probe(stream.stationurl())
		
		#--- response ---
		return client.init_response(self.PROTOCOL_ID, call_id, method_id)
