
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


class UniqueIdInfo(common.Structure):
	def __init__(self):
		super().__init__()
		self.unique_id = None
		self.password = None
	
	def check_required(self, settings):
		for field in ['unique_id', 'password']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.unique_id = stream.u64()
		self.password = stream.u64()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.u64(self.unique_id)
		stream.u64(self.password)


class UtilityProtocol:
	METHOD_ACQUIRE_NEX_UNIQUE_ID = 1
	METHOD_ACQUIRE_NEX_UNIQUE_ID_WITH_PASSWORD = 2
	METHOD_ASSOCIATE_NEX_UNIQUE_ID_WITH_MY_PRINCIPAL_ID = 3
	METHOD_ASSOCIATE_NEX_UNIQUE_IDS_WITH_MY_PRINCIPAL_ID = 4
	METHOD_GET_ASSOCIATED_NEX_UNIQUE_ID_WITH_MY_PRINCIPAL_ID = 5
	METHOD_GET_ASSOCIATED_NEX_UNIQUE_IDS_WITH_MY_PRINCIPAL_ID = 6
	METHOD_GET_INTEGER_SETTINGS = 7
	METHOD_GET_STRING_SETTINGS = 8
	
	PROTOCOL_ID = 0x6E


class UtilityClient(UtilityProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def acquire_nex_unique_id(self):
		logger.info("UtilityClient.acquire_nex_unique_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_ACQUIRE_NEX_UNIQUE_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		unique_id = stream.u64()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("UtilityClient.acquire_nex_unique_id -> done")
		return unique_id
	
	def acquire_nex_unique_id_with_password(self):
		logger.info("UtilityClient.acquire_nex_unique_id_with_password()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_ACQUIRE_NEX_UNIQUE_ID_WITH_PASSWORD, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(UniqueIdInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("UtilityClient.acquire_nex_unique_id_with_password -> done")
		return info
	
	def associate_nex_unique_id_with_my_principal_id(self, info):
		logger.info("UtilityClient.associate_nex_unique_id_with_my_principal_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(info)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_ASSOCIATE_NEX_UNIQUE_ID_WITH_MY_PRINCIPAL_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("UtilityClient.associate_nex_unique_id_with_my_principal_id -> done")
	
	def associate_nex_unique_ids_with_my_principal_id(self, infos):
		logger.info("UtilityClient.associate_nex_unique_ids_with_my_principal_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(infos, stream.add)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_ASSOCIATE_NEX_UNIQUE_IDS_WITH_MY_PRINCIPAL_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("UtilityClient.associate_nex_unique_ids_with_my_principal_id -> done")
	
	def get_associated_nex_unique_id_with_my_principal_id(self):
		logger.info("UtilityClient.get_associated_nex_unique_id_with_my_principal_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_ASSOCIATED_NEX_UNIQUE_ID_WITH_MY_PRINCIPAL_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		info = stream.extract(UniqueIdInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("UtilityClient.get_associated_nex_unique_id_with_my_principal_id -> done")
		return info
	
	def get_associated_nex_unique_ids_with_my_principal_id(self):
		logger.info("UtilityClient.get_associated_nex_unique_ids_with_my_principal_id()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_ASSOCIATED_NEX_UNIQUE_IDS_WITH_MY_PRINCIPAL_ID, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		infos = stream.list(UniqueIdInfo)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("UtilityClient.get_associated_nex_unique_ids_with_my_principal_id -> done")
		return infos
	
	def get_integer_settings(self, index):
		logger.info("UtilityClient.get_integer_settings()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(index)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_INTEGER_SETTINGS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		settings = stream.map(stream.u16, stream.s32)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("UtilityClient.get_integer_settings -> done")
		return settings
	
	def get_string_settings(self, index):
		logger.info("UtilityClient.get_string_settings()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(index)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_GET_STRING_SETTINGS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		settings = stream.map(stream.u16, stream.string)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("UtilityClient.get_string_settings -> done")
		return settings


class UtilityServer(UtilityProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_ACQUIRE_NEX_UNIQUE_ID: self.handle_acquire_nex_unique_id,
			self.METHOD_ACQUIRE_NEX_UNIQUE_ID_WITH_PASSWORD: self.handle_acquire_nex_unique_id_with_password,
			self.METHOD_ASSOCIATE_NEX_UNIQUE_ID_WITH_MY_PRINCIPAL_ID: self.handle_associate_nex_unique_id_with_my_principal_id,
			self.METHOD_ASSOCIATE_NEX_UNIQUE_IDS_WITH_MY_PRINCIPAL_ID: self.handle_associate_nex_unique_ids_with_my_principal_id,
			self.METHOD_GET_ASSOCIATED_NEX_UNIQUE_ID_WITH_MY_PRINCIPAL_ID: self.handle_get_associated_nex_unique_id_with_my_principal_id,
			self.METHOD_GET_ASSOCIATED_NEX_UNIQUE_IDS_WITH_MY_PRINCIPAL_ID: self.handle_get_associated_nex_unique_ids_with_my_principal_id,
			self.METHOD_GET_INTEGER_SETTINGS: self.handle_get_integer_settings,
			self.METHOD_GET_STRING_SETTINGS: self.handle_get_string_settings,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_acquire_nex_unique_id(self, context, input, output):
		logger.info("UtilityServer.acquire_nex_unique_id()")
		#--- request ---
		response = self.acquire_nex_unique_id(context)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u64(response)
	
	def handle_acquire_nex_unique_id_with_password(self, context, input, output):
		logger.info("UtilityServer.acquire_nex_unique_id_with_password()")
		#--- request ---
		response = self.acquire_nex_unique_id_with_password(context)
		
		#--- response ---
		if not isinstance(response, UniqueIdInfo):
			raise RuntimeError("Expected UniqueIdInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_associate_nex_unique_id_with_my_principal_id(self, context, input, output):
		logger.info("UtilityServer.associate_nex_unique_id_with_my_principal_id()")
		#--- request ---
		info = input.extract(UniqueIdInfo)
		self.associate_nex_unique_id_with_my_principal_id(context, info)
	
	def handle_associate_nex_unique_ids_with_my_principal_id(self, context, input, output):
		logger.info("UtilityServer.associate_nex_unique_ids_with_my_principal_id()")
		#--- request ---
		infos = input.list(UniqueIdInfo)
		self.associate_nex_unique_ids_with_my_principal_id(context, infos)
	
	def handle_get_associated_nex_unique_id_with_my_principal_id(self, context, input, output):
		logger.info("UtilityServer.get_associated_nex_unique_id_with_my_principal_id()")
		#--- request ---
		response = self.get_associated_nex_unique_id_with_my_principal_id(context)
		
		#--- response ---
		if not isinstance(response, UniqueIdInfo):
			raise RuntimeError("Expected UniqueIdInfo, got %s" %response.__class__.__name__)
		output.add(response)
	
	def handle_get_associated_nex_unique_ids_with_my_principal_id(self, context, input, output):
		logger.info("UtilityServer.get_associated_nex_unique_ids_with_my_principal_id()")
		#--- request ---
		response = self.get_associated_nex_unique_ids_with_my_principal_id(context)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	def handle_get_integer_settings(self, context, input, output):
		logger.info("UtilityServer.get_integer_settings()")
		#--- request ---
		index = input.u32()
		response = self.get_integer_settings(context, index)
		
		#--- response ---
		if not isinstance(response, dict):
			raise RuntimeError("Expected dict, got %s" %response.__class__.__name__)
		output.map(response, output.u16, output.s32)
	
	def handle_get_string_settings(self, context, input, output):
		logger.info("UtilityServer.get_string_settings()")
		#--- request ---
		index = input.u32()
		response = self.get_string_settings(context, index)
		
		#--- response ---
		if not isinstance(response, dict):
			raise RuntimeError("Expected dict, got %s" %response.__class__.__name__)
		output.map(response, output.u16, output.string)
	
	def acquire_nex_unique_id(self, *args):
		logger.warning("UtilityServer.acquire_nex_unique_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def acquire_nex_unique_id_with_password(self, *args):
		logger.warning("UtilityServer.acquire_nex_unique_id_with_password not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def associate_nex_unique_id_with_my_principal_id(self, *args):
		logger.warning("UtilityServer.associate_nex_unique_id_with_my_principal_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def associate_nex_unique_ids_with_my_principal_id(self, *args):
		logger.warning("UtilityServer.associate_nex_unique_ids_with_my_principal_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_associated_nex_unique_id_with_my_principal_id(self, *args):
		logger.warning("UtilityServer.get_associated_nex_unique_id_with_my_principal_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_associated_nex_unique_ids_with_my_principal_id(self, *args):
		logger.warning("UtilityServer.get_associated_nex_unique_ids_with_my_principal_id not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_integer_settings(self, *args):
		logger.warning("UtilityServer.get_integer_settings not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def get_string_settings(self, *args):
		logger.warning("UtilityServer.get_string_settings not implemented")
		raise common.RMCError("Core::NotImplemented")

