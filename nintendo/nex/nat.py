
import logging
logger = logging.getLogger(__name__)


class NATTraversalClient:

	METHOD_REQUEST_PROBE_INITIATION = 1
	METHOD_INITIATE_PROBE = 2
	METHOD_REQUEST_PROBE_INITIATION_EXT = 3
	METHOD_REPORT_NAT_TRAVERSAL_RESULT = 4
	METHOD_REPORT_NAT_PROPERTIES = 5
	METHOD_GET_RELAY_SIGNATURE_KEY = 6
	METHOD_REPORT_NAT_TRAVERSAL_RESULT_DETAIL = 7

	PROTOCOL_ID = 3

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
