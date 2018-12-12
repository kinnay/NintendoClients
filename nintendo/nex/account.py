
from nintendo.nex import common

import logging
logger = logging.getLogger(__name__)


class AccountData(common.Structure):
	def load(self, stream):
		self.pid = stream.pid()
		self.name = stream.string()
		self.groups = stream.u32()
		self.email = stream.string()
		self.creation_date = stream.datetime()
		self.effective_date = stream.datetime()
		self.not_effective_message = stream.string()
		self.expiry_date = stream.datetime()
		self.expired_message = stream.string()


class AccountManagementClient:

	METHOD_CREATE_ACCOUNT = 1
	METHOD_DELETE_ACCOUNT = 2
	METHOD_DISABLE_ACCOUNT = 3
	METHOD_CHANGE_PASSWORD = 4
	METHOD_TEST_CAPABILITY = 5
	METHOD_GET_NAME = 6
	METHOD_GET_ACCOUNT_DATA = 7
	METHOD_GET_PRIVATE_DATA = 8
	METHOD_GET_PUBLIC_DATA = 9
	METHOD_GET_MULTIPLE_PUBLIC_DATA = 10
	METHOD_UPDATE_ACCOUNT_NAME = 11
	METHOD_UPDATE_ACCOUNT_EMAIL = 12
	METHOD_UPDATE_CUSTOM_DATA = 13
	METHOD_FIND_BY_NAME_REGEX = 14
	METHOD_UPDATE_ACCOUNT_EXPIRY_DATE = 15
	METHOD_UPDATE_ACCOUNT_EFFECTIVE_DATE = 16
	METHOD_UPDATE_STATUS = 17
	METHOD_GET_STATUS = 18
	METHOD_GET_LAST_CONNECTION_STATS = 19
	METHOD_RESET_PASSWORD = 20
	METHOD_CREATE_ACCOUNT_WITH_CUSTOM_DATA = 21
	METHOD_RETRIEVE_ACCOUNT = 22
	METHOD_UPDATE_ACCOUNT = 23
	METHOD_CHANGE_PASSWORD_BY_GUEST = 24
	METHOD_FIND_BY_NAME_LIKE = 25
	METHOD_CUSTOM_CREATE_ACCOUNT = 26
	METHOD_NINTENDO_CREATE_ACCOUNT = 27
	METHOD_LOOKUP_OR_CREATE_ACCOUNT = 28
	METHOD_DISCONNECT_PRINCIPAL = 29
	METHOD_DISCONNECT_ALL_PRINCIPALS = 30

	PROTOCOL_ID = 0x19

	def __init__(self, backend):
		self.client = backend.secure_client
		
	def test_capability(self, capability):
		logger.info("AccountManagement.test_capability(%i)", capability)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_TEST_CAPABILITY)
		stream.u32(capability)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		result = stream.bool()
		logger.info("AccountManagement.test_capability -> %s", result)
		return result
		
	def get_name(self, pid):
		logger.info("AccountManagement.get_name(%i)", pid)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_NAME)
		stream.pid(pid)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		name = stream.string()
		logger.info("AccountManagement.get_name -> %s", name)
		return name

	def get_account_data(self):
		logger.info("AccountManagement.get_account_data()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_ACCOUNT_DATA)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		result = stream.u32()
		if result & 0x80000000:
			raise RuntimeError("Request failed (%s)" %errors.error_names.get(result, "unknown error"))

		data = stream.extract(AccountData)
		logger.info("AccountManagement.get_account_data -> Done")
		return data
