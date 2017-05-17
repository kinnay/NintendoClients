
from proto.common.stream import StreamOut

import logging
logger = logging.getLogger(__name__)


class AccountManagementClient:
	
	METHOD_CREATE_ACCOUNT = 1
	METHOD_DELETE_ACCOUNT = 2
	METHOD_DISABLE_ACCOUNT = 3
	METHOD_CHANGE_PASSWORD = 4
	METHOD_TEST_CAPABILITY = 5
	METHOD_GET_NAME = 6
	
	PROTOCOL_ID = 0xE
	
	def __init__(self, back_end):
		self.client = back_end.secure_client
		
	def get_name(self, arg):
		logger.info("AccountManager.get_name(%08X)", arg)
		#--- request ---
		stream = StreamOut()
		call_id = self.client.init_message(stream, self.PROTOCOL_ID, self.METHOD_GET_NAME)
		stream.u32(arg)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		return stream.string(stream.u16)
