
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


class AccountData(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.name = None
		self.groups = None
		self.email = None
		self.creation_date = None
		self.effective_date = None
		self.not_effective_message = None
		self.expiry_date = None
		self.expired_message = None
	
	def check_required(self, settings):
		for field in ['pid', 'name', 'groups', 'email', 'creation_date', 'effective_date', 'not_effective_message', 'expiry_date', 'expired_message']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
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
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.pid)
		stream.string(self.name)
		stream.u32(self.groups)
		stream.string(self.email)
		stream.datetime(self.creation_date)
		stream.datetime(self.effective_date)
		stream.string(self.not_effective_message)
		stream.datetime(self.expiry_date)
		stream.string(self.expired_message)


class BasicAccountInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.pid = None
		self.name = None
	
	def check_required(self, settings):
		for field in ['pid', 'name']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.pid = stream.pid()
		self.name = stream.string()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.pid(self.pid)
		stream.string(self.name)


class AccountProtocol:
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


class AccountClient(AccountProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def create_account(self, name, key, groups, email):
		logger.info("AccountClient.create_account()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(name)
		stream.string(key)
		stream.u32(groups)
		stream.string(email)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_CREATE_ACCOUNT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.result()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.create_account -> done")
		return result
	
	def delete_account(self, pid):
		logger.info("AccountClient.delete_account()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_DELETE_ACCOUNT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.delete_account -> done")
	
	def disable_account(self, pid, until, message):
		logger.info("AccountClient.disable_account()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		stream.datetime(until)
		stream.string(message)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_DISABLE_ACCOUNT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.result()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.disable_account -> done")
		return result
	
	def change_password(self, new_key):
		logger.info("AccountClient.change_password()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(new_key)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_CHANGE_PASSWORD, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.change_password -> done")
		return result
	
	def test_capability(self, capability):
		logger.info("AccountClient.test_capability()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(capability)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_TEST_CAPABILITY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.test_capability -> done")
		return result
	
	def get_name(self, pid):
		logger.info("AccountClient.get_name()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_NAME, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		name = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.get_name -> done")
		return name
	
	def get_account_data(self):
		logger.info("AccountClient.get_account_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_ACCOUNT_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.result = stream.result()
		obj.data = stream.extract(AccountData)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.get_account_data -> done")
		return obj
	
	def get_private_data(self):
		logger.info("AccountClient.get_private_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_PRIVATE_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.result = stream.bool()
		obj.data = stream.anydata()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.get_private_data -> done")
		return obj
	
	def get_public_data(self, pid):
		logger.info("AccountClient.get_public_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_PUBLIC_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.result = stream.bool()
		obj.data = stream.anydata()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.get_public_data -> done")
		return obj
	
	def get_multiple_public_data(self, pids):
		logger.info("AccountClient.get_multiple_public_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(pids, stream.pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_MULTIPLE_PUBLIC_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.result = stream.bool()
		obj.data = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.get_multiple_public_data -> done")
		return obj
	
	def update_account_name(self, name):
		logger.info("AccountClient.update_account_name()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(name)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_UPDATE_ACCOUNT_NAME, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.result()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.update_account_name -> done")
		return result
	
	def update_account_email(self, email):
		logger.info("AccountClient.update_account_email()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(email)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_UPDATE_ACCOUNT_EMAIL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.result()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.update_account_email -> done")
		return result
	
	def update_custom_data(self, public_data, private_data):
		logger.info("AccountClient.update_custom_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.anydata(public_data)
		stream.anydata(private_data)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_UPDATE_CUSTOM_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.result()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.update_custom_data -> done")
		return result
	
	def find_by_name_regex(self, groups, regex, range):
		logger.info("AccountClient.find_by_name_regex()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(groups)
		stream.string(regex)
		stream.add(range)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_FIND_BY_NAME_REGEX, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		accounts = stream.list(BasicAccountInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.find_by_name_regex -> done")
		return accounts
	
	def update_account_expiry_date(self, pid, expiry, message):
		logger.info("AccountClient.update_account_expiry_date()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		stream.datetime(expiry)
		stream.string(message)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_UPDATE_ACCOUNT_EXPIRY_DATE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.update_account_expiry_date -> done")
	
	def update_account_effective_date(self, pid, effective_from, message):
		logger.info("AccountClient.update_account_effective_date()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		stream.datetime(effective_from)
		stream.string(message)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_UPDATE_ACCOUNT_EFFECTIVE_DATE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.update_account_effective_date -> done")
	
	def update_status(self, status):
		logger.info("AccountClient.update_status()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(status)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_UPDATE_STATUS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.update_status -> done")
	
	def get_status(self, pid):
		logger.info("AccountClient.get_status()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_STATUS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		status = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.get_status -> done")
		return status
	
	def get_last_connection_stats(self, pid):
		logger.info("AccountClient.get_last_connection_stats()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_LAST_CONNECTION_STATS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.last_session_login = stream.datetime()
		obj.last_session_logout = stream.datetime()
		obj.current_session_login = stream.datetime()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.get_last_connection_stats -> done")
		return obj
	
	def reset_password(self):
		logger.info("AccountClient.reset_password()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_RESET_PASSWORD, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.reset_password -> done")
		return result
	
	def create_account_with_custom_data(self, name, key, groups, email, public_data, private_data):
		logger.info("AccountClient.create_account_with_custom_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(name)
		stream.string(key)
		stream.u32(groups)
		stream.string(email)
		stream.anydata(public_data)
		stream.anydata(private_data)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_CREATE_ACCOUNT_WITH_CUSTOM_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.create_account_with_custom_data -> done")
	
	def retrieve_account(self):
		logger.info("AccountClient.retrieve_account()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_RETRIEVE_ACCOUNT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.account_data = stream.extract(AccountData)
		obj.public_data = stream.anydata()
		obj.private_data = stream.anydata()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.retrieve_account -> done")
		return obj
	
	def update_account(self, key, email, public_data, private_data):
		logger.info("AccountClient.update_account()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(key)
		stream.string(email)
		stream.anydata(public_data)
		stream.anydata(private_data)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_UPDATE_ACCOUNT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.update_account -> done")
	
	def change_password_by_guest(self, name, email, key):
		logger.info("AccountClient.change_password_by_guest()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(name)
		stream.string(email)
		stream.string(key)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_CHANGE_PASSWORD_BY_GUEST, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.change_password_by_guest -> done")
	
	def find_by_name_like(self, groups, like, range):
		logger.info("AccountClient.find_by_name_like()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(groups)
		stream.string(like)
		stream.add(range)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_FIND_BY_NAME_LIKE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		accounts = stream.list(BasicAccountInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.find_by_name_like -> done")
		return accounts
	
	def custom_create_account(self, name, key, groups, email, auth_data):
		logger.info("AccountClient.custom_create_account()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(name)
		stream.string(key)
		stream.u32(groups)
		stream.string(email)
		stream.anydata(auth_data)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_CUSTOM_CREATE_ACCOUNT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		pid = stream.pid()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.custom_create_account -> done")
		return pid
	
	def nintendo_create_account(self, name, key, groups, email, auth_data):
		logger.info("AccountClient.nintendo_create_account()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(name)
		stream.string(key)
		stream.u32(groups)
		stream.string(email)
		stream.anydata(auth_data)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_NINTENDO_CREATE_ACCOUNT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.pid = stream.pid()
		obj.pid_hmac = stream.string()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.nintendo_create_account -> done")
		return obj
	
	def lookup_or_create_account(self, name, key, groups, email, auth_data):
		logger.info("AccountClient.lookup_or_create_account()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.string(name)
		stream.string(key)
		stream.u32(groups)
		stream.string(email)
		stream.anydata(auth_data)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_LOOKUP_OR_CREATE_ACCOUNT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		pid = stream.pid()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.lookup_or_create_account -> done")
		return pid
	
	def disconnect_principal(self, pid):
		logger.info("AccountClient.disconnect_principal()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.pid(pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_DISCONNECT_PRINCIPAL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.disconnect_principal -> done")
		return result
	
	def disconnect_all_principals(self):
		logger.info("AccountClient.disconnect_all_principals()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_DISCONNECT_ALL_PRINCIPALS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		result = stream.bool()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("AccountClient.disconnect_all_principals -> done")
		return result


class AccountServer(AccountProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_CREATE_ACCOUNT: self.handle_create_account,
			self.METHOD_DELETE_ACCOUNT: self.handle_delete_account,
			self.METHOD_DISABLE_ACCOUNT: self.handle_disable_account,
			self.METHOD_CHANGE_PASSWORD: self.handle_change_password,
			self.METHOD_TEST_CAPABILITY: self.handle_test_capability,
			self.METHOD_GET_NAME: self.handle_get_name,
			self.METHOD_GET_ACCOUNT_DATA: self.handle_get_account_data,
			self.METHOD_GET_PRIVATE_DATA: self.handle_get_private_data,
			self.METHOD_GET_PUBLIC_DATA: self.handle_get_public_data,
			self.METHOD_GET_MULTIPLE_PUBLIC_DATA: self.handle_get_multiple_public_data,
			self.METHOD_UPDATE_ACCOUNT_NAME: self.handle_update_account_name,
			self.METHOD_UPDATE_ACCOUNT_EMAIL: self.handle_update_account_email,
			self.METHOD_UPDATE_CUSTOM_DATA: self.handle_update_custom_data,
			self.METHOD_FIND_BY_NAME_REGEX: self.handle_find_by_name_regex,
			self.METHOD_UPDATE_ACCOUNT_EXPIRY_DATE: self.handle_update_account_expiry_date,
			self.METHOD_UPDATE_ACCOUNT_EFFECTIVE_DATE: self.handle_update_account_effective_date,
			self.METHOD_UPDATE_STATUS: self.handle_update_status,
			self.METHOD_GET_STATUS: self.handle_get_status,
			self.METHOD_GET_LAST_CONNECTION_STATS: self.handle_get_last_connection_stats,
			self.METHOD_RESET_PASSWORD: self.handle_reset_password,
			self.METHOD_CREATE_ACCOUNT_WITH_CUSTOM_DATA: self.handle_create_account_with_custom_data,
			self.METHOD_RETRIEVE_ACCOUNT: self.handle_retrieve_account,
			self.METHOD_UPDATE_ACCOUNT: self.handle_update_account,
			self.METHOD_CHANGE_PASSWORD_BY_GUEST: self.handle_change_password_by_guest,
			self.METHOD_FIND_BY_NAME_LIKE: self.handle_find_by_name_like,
			self.METHOD_CUSTOM_CREATE_ACCOUNT: self.handle_custom_create_account,
			self.METHOD_NINTENDO_CREATE_ACCOUNT: self.handle_nintendo_create_account,
			self.METHOD_LOOKUP_OR_CREATE_ACCOUNT: self.handle_lookup_or_create_account,
			self.METHOD_DISCONNECT_PRINCIPAL: self.handle_disconnect_principal,
			self.METHOD_DISCONNECT_ALL_PRINCIPALS: self.handle_disconnect_all_principals,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_create_account(self, context, input, output):
		logger.info("AccountServer.create_account()")
		#--- request ---
		name = input.string()
		key = input.string()
		groups = input.u32()
		email = input.string()
		response = self.create_account(context, name, key, groups, email)
		
		#--- response ---
		if not isinstance(response, comon.Result):
			raise RuntimeError("Expected comon.Result, got %s" %response.__class__.__name__)
		output.result(response)
	
	def handle_delete_account(self, context, input, output):
		logger.info("AccountServer.delete_account()")
		#--- request ---
		pid = input.pid()
		self.delete_account(context, pid)
	
	def handle_disable_account(self, context, input, output):
		logger.info("AccountServer.disable_account()")
		#--- request ---
		pid = input.pid()
		until = input.datetime()
		message = input.string()
		response = self.disable_account(context, pid, until, message)
		
		#--- response ---
		if not isinstance(response, comon.Result):
			raise RuntimeError("Expected comon.Result, got %s" %response.__class__.__name__)
		output.result(response)
	
	def handle_change_password(self, context, input, output):
		logger.info("AccountServer.change_password()")
		#--- request ---
		new_key = input.string()
		response = self.change_password(context, new_key)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	def handle_test_capability(self, context, input, output):
		logger.info("AccountServer.test_capability()")
		#--- request ---
		capability = input.u32()
		response = self.test_capability(context, capability)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	def handle_get_name(self, context, input, output):
		logger.info("AccountServer.get_name()")
		#--- request ---
		pid = input.pid()
		response = self.get_name(context, pid)
		
		#--- response ---
		if not isinstance(response, str):
			raise RuntimeError("Expected str, got %s" %response.__class__.__name__)
		output.string(response)
	
	def handle_get_account_data(self, context, input, output):
		logger.info("AccountServer.get_account_data()")
		#--- request ---
		response = self.get_account_data(context)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'data']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.add(response.data)
	
	def handle_get_private_data(self, context, input, output):
		logger.info("AccountServer.get_private_data()")
		#--- request ---
		response = self.get_private_data(context)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'data']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.bool(response.result)
		output.anydata(response.data)
	
	def handle_get_public_data(self, context, input, output):
		logger.info("AccountServer.get_public_data()")
		#--- request ---
		pid = input.pid()
		response = self.get_public_data(context, pid)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'data']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.bool(response.result)
		output.anydata(response.data)
	
	def handle_get_multiple_public_data(self, context, input, output):
		logger.info("AccountServer.get_multiple_public_data()")
		#--- request ---
		pids = input.list(input.pid)
		response = self.get_multiple_public_data(context, pids)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'data']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.bool(response.result)
		output.list(response.data, output.anydata)
	
	def handle_update_account_name(self, context, input, output):
		logger.info("AccountServer.update_account_name()")
		#--- request ---
		name = input.string()
		response = self.update_account_name(context, name)
		
		#--- response ---
		if not isinstance(response, comon.Result):
			raise RuntimeError("Expected comon.Result, got %s" %response.__class__.__name__)
		output.result(response)
	
	def handle_update_account_email(self, context, input, output):
		logger.info("AccountServer.update_account_email()")
		#--- request ---
		email = input.string()
		response = self.update_account_email(context, email)
		
		#--- response ---
		if not isinstance(response, comon.Result):
			raise RuntimeError("Expected comon.Result, got %s" %response.__class__.__name__)
		output.result(response)
	
	def handle_update_custom_data(self, context, input, output):
		logger.info("AccountServer.update_custom_data()")
		#--- request ---
		public_data = input.anydata()
		private_data = input.anydata()
		response = self.update_custom_data(context, public_data, private_data)
		
		#--- response ---
		if not isinstance(response, comon.Result):
			raise RuntimeError("Expected comon.Result, got %s" %response.__class__.__name__)
		output.result(response)
	
	def handle_find_by_name_regex(self, context, input, output):
		logger.info("AccountServer.find_by_name_regex()")
		#--- request ---
		groups = input.u32()
		regex = input.string()
		range = input.extract(common.ResultRange)
		response = self.find_by_name_regex(context, groups, regex, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	def handle_update_account_expiry_date(self, context, input, output):
		logger.info("AccountServer.update_account_expiry_date()")
		#--- request ---
		pid = input.pid()
		expiry = input.datetime()
		message = input.string()
		self.update_account_expiry_date(context, pid, expiry, message)
	
	def handle_update_account_effective_date(self, context, input, output):
		logger.info("AccountServer.update_account_effective_date()")
		#--- request ---
		pid = input.pid()
		effective_from = input.datetime()
		message = input.string()
		self.update_account_effective_date(context, pid, effective_from, message)
	
	def handle_update_status(self, context, input, output):
		logger.info("AccountServer.update_status()")
		#--- request ---
		status = input.string()
		self.update_status(context, status)
	
	def handle_get_status(self, context, input, output):
		logger.info("AccountServer.get_status()")
		#--- request ---
		pid = input.pid()
		response = self.get_status(context, pid)
		
		#--- response ---
		if not isinstance(response, str):
			raise RuntimeError("Expected str, got %s" %response.__class__.__name__)
		output.string(response)
	
	def handle_get_last_connection_stats(self, context, input, output):
		logger.info("AccountServer.get_last_connection_stats()")
		#--- request ---
		pid = input.pid()
		response = self.get_last_connection_stats(context, pid)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['last_session_login', 'last_session_logout', 'current_session_login']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.datetime(response.last_session_login)
		output.datetime(response.last_session_logout)
		output.datetime(response.current_session_login)
	
	def handle_reset_password(self, context, input, output):
		logger.info("AccountServer.reset_password()")
		#--- request ---
		response = self.reset_password(context)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	def handle_create_account_with_custom_data(self, context, input, output):
		logger.info("AccountServer.create_account_with_custom_data()")
		#--- request ---
		name = input.string()
		key = input.string()
		groups = input.u32()
		email = input.string()
		public_data = input.anydata()
		private_data = input.anydata()
		self.create_account_with_custom_data(context, name, key, groups, email, public_data, private_data)
	
	def handle_retrieve_account(self, context, input, output):
		logger.info("AccountServer.retrieve_account()")
		#--- request ---
		response = self.retrieve_account(context)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['account_data', 'public_data', 'private_data']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.add(response.account_data)
		output.anydata(response.public_data)
		output.anydata(response.private_data)
	
	def handle_update_account(self, context, input, output):
		logger.info("AccountServer.update_account()")
		#--- request ---
		key = input.string()
		email = input.string()
		public_data = input.anydata()
		private_data = input.anydata()
		self.update_account(context, key, email, public_data, private_data)
	
	def handle_change_password_by_guest(self, context, input, output):
		logger.info("AccountServer.change_password_by_guest()")
		#--- request ---
		name = input.string()
		email = input.string()
		key = input.string()
		self.change_password_by_guest(context, name, email, key)
	
	def handle_find_by_name_like(self, context, input, output):
		logger.info("AccountServer.find_by_name_like()")
		#--- request ---
		groups = input.u32()
		like = input.string()
		range = input.extract(common.ResultRange)
		response = self.find_by_name_like(context, groups, like, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	def handle_custom_create_account(self, context, input, output):
		logger.info("AccountServer.custom_create_account()")
		#--- request ---
		name = input.string()
		key = input.string()
		groups = input.u32()
		email = input.string()
		auth_data = input.anydata()
		response = self.custom_create_account(context, name, key, groups, email, auth_data)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.pid(response)
	
	def handle_nintendo_create_account(self, context, input, output):
		logger.info("AccountServer.nintendo_create_account()")
		#--- request ---
		name = input.string()
		key = input.string()
		groups = input.u32()
		email = input.string()
		auth_data = input.anydata()
		response = self.nintendo_create_account(context, name, key, groups, email, auth_data)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['pid', 'pid_hmac']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.pid(response.pid)
		output.string(response.pid_hmac)
	
	def handle_lookup_or_create_account(self, context, input, output):
		logger.info("AccountServer.lookup_or_create_account()")
		#--- request ---
		name = input.string()
		key = input.string()
		groups = input.u32()
		email = input.string()
		auth_data = input.anydata()
		response = self.lookup_or_create_account(context, name, key, groups, email, auth_data)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.pid(response)
	
	def handle_disconnect_principal(self, context, input, output):
		logger.info("AccountServer.disconnect_principal()")
		#--- request ---
		pid = input.pid()
		response = self.disconnect_principal(context, pid)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	def handle_disconnect_all_principals(self, context, input, output):
		logger.info("AccountServer.disconnect_all_principals()")
		#--- request ---
		response = self.disconnect_all_principals(context)
		
		#--- response ---
		if not isinstance(response, bool):
			raise RuntimeError("Expected bool, got %s" %response.__class__.__name__)
		output.bool(response)
	
	def create_account(self, *args):
		logger.warning("AccountServer.create_account not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def delete_account(self, *args):
		logger.warning("AccountServer.delete_account not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def disable_account(self, *args):
		logger.warning("AccountServer.disable_account not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def change_password(self, *args):
		logger.warning("AccountServer.change_password not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def test_capability(self, *args):
		logger.warning("AccountServer.test_capability not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_name(self, *args):
		logger.warning("AccountServer.get_name not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_account_data(self, *args):
		logger.warning("AccountServer.get_account_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_private_data(self, *args):
		logger.warning("AccountServer.get_private_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_public_data(self, *args):
		logger.warning("AccountServer.get_public_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_multiple_public_data(self, *args):
		logger.warning("AccountServer.get_multiple_public_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def update_account_name(self, *args):
		logger.warning("AccountServer.update_account_name not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def update_account_email(self, *args):
		logger.warning("AccountServer.update_account_email not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def update_custom_data(self, *args):
		logger.warning("AccountServer.update_custom_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def find_by_name_regex(self, *args):
		logger.warning("AccountServer.find_by_name_regex not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def update_account_expiry_date(self, *args):
		logger.warning("AccountServer.update_account_expiry_date not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def update_account_effective_date(self, *args):
		logger.warning("AccountServer.update_account_effective_date not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def update_status(self, *args):
		logger.warning("AccountServer.update_status not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_status(self, *args):
		logger.warning("AccountServer.get_status not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_last_connection_stats(self, *args):
		logger.warning("AccountServer.get_last_connection_stats not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def reset_password(self, *args):
		logger.warning("AccountServer.reset_password not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def create_account_with_custom_data(self, *args):
		logger.warning("AccountServer.create_account_with_custom_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def retrieve_account(self, *args):
		logger.warning("AccountServer.retrieve_account not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def update_account(self, *args):
		logger.warning("AccountServer.update_account not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def change_password_by_guest(self, *args):
		logger.warning("AccountServer.change_password_by_guest not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def find_by_name_like(self, *args):
		logger.warning("AccountServer.find_by_name_like not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def custom_create_account(self, *args):
		logger.warning("AccountServer.custom_create_account not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def nintendo_create_account(self, *args):
		logger.warning("AccountServer.nintendo_create_account not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def lookup_or_create_account(self, *args):
		logger.warning("AccountServer.lookup_or_create_account not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def disconnect_principal(self, *args):
		logger.warning("AccountServer.disconnect_principal not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def disconnect_all_principals(self, *args):
		logger.warning("AccountServer.disconnect_all_principals not implemented")
		raise common.RMCError("Core::NotImplemented")

