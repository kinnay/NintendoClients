
# This file was generated automatically by generate_protocols.py

from nintendo.nex import notification, rmc, common, streams

import logging
logger = logging.getLogger(__name__)


class RecipientType:
	PRINCIPAL = 1
	GATHERING = 2


class MessageRecipient(common.Structure):
	def __init__(self):
		super().__init__()
		self.type = None
		self.pid = None
		self.gid = None
	
	def check_required(self, settings, version):
		for field in ['type', 'pid', 'gid']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.type = stream.u32()
		self.pid = stream.pid()
		self.gid = stream.u32()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.type)
		stream.pid(self.pid)
		stream.u32(self.gid)


class UserMessage(common.Data):
	def __init__(self):
		super().__init__()
		self.id = None
		self.parent_id = None
		self.sender = None
		self.reception_time = None
		self.life_time = None
		self.flags = None
		self.subject = None
		self.sender_name = None
		self.recipient = MessageRecipient()
	
	def check_required(self, settings, version):
		for field in ['id', 'parent_id', 'sender', 'reception_time', 'life_time', 'flags', 'subject', 'sender_name']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.id = stream.u32()
		self.parent_id = stream.u32()
		self.sender = stream.pid()
		self.reception_time = stream.datetime()
		self.life_time = stream.u32()
		self.flags = stream.u32()
		self.subject = stream.string()
		self.sender_name = stream.string()
		self.recipient = stream.extract(MessageRecipient)
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.u32(self.id)
		stream.u32(self.parent_id)
		stream.pid(self.sender)
		stream.datetime(self.reception_time)
		stream.u32(self.life_time)
		stream.u32(self.flags)
		stream.string(self.subject)
		stream.string(self.sender_name)
		stream.add(self.recipient)
common.DataHolder.register(UserMessage, "UserMessage")


class TextMessage(UserMessage):
	def __init__(self):
		super().__init__()
		self.body = None
	
	def check_required(self, settings, version):
		for field in ['body']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.body = stream.string()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.string(self.body)
common.DataHolder.register(TextMessage, "TextMessage")


class BinaryMessage(UserMessage):
	def __init__(self):
		super().__init__()
		self.body = None
	
	def check_required(self, settings, version):
		for field in ['body']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream, version):
		self.body = stream.qbuffer()
	
	def save(self, stream, version):
		self.check_required(stream.settings, version)
		stream.qbuffer(self.body)
common.DataHolder.register(BinaryMessage, "BinaryMessage")


class MessagingProtocol:
	METHOD_DELIVER_MESSAGE = 1
	METHOD_GET_NUMBER_OF_MESSAGES = 2
	METHOD_GET_MESSAGE_HEADERS = 3
	METHOD_RETRIEVE_ALL_MESSAGES_WITHIN_RANGE = 4
	METHOD_RETRIEVE_MESSAGES = 5
	METHOD_DELETE_MESSAGES = 6
	METHOD_DELETE_ALL_MESSAGES = 7
	
	PROTOCOL_ID = 0x17


class MessageDeliveryProtocol:
	NORESPONSE = True
	
	METHOD_DELIVER_MESSAGE = 1
	
	PROTOCOL_ID = 0x1B


class MessagingClient(MessagingProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def deliver_message(self, message):
		logger.info("MessagingClient.deliver_message()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.anydata(message)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELIVER_MESSAGE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = rmc.RMCResponse()
		obj.modified_message = stream.anydata()
		obj.sandbox_node_ids = stream.list(stream.u32)
		obj.participants = stream.list(stream.pid)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MessagingClient.deliver_message -> done")
		return obj
	
	async def get_number_of_messages(self, recipient):
		logger.info("MessagingClient.get_number_of_messages()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(recipient)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_NUMBER_OF_MESSAGES, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		number = stream.u32()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MessagingClient.get_number_of_messages -> done")
		return number
	
	async def get_message_headers(self, recipient, range):
		logger.info("MessagingClient.get_message_headers()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(recipient)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_GET_MESSAGE_HEADERS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		headers = stream.list(UserMessage)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MessagingClient.get_message_headers -> done")
		return headers
	
	async def retrieve_all_messages_within_range(self, recipient, range):
		logger.info("MessagingClient.retrieve_all_messages_within_range()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(recipient)
		stream.add(range)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_RETRIEVE_ALL_MESSAGES_WITHIN_RANGE, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		messages = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MessagingClient.retrieve_all_messages_within_range -> done")
		return messages
	
	async def retrieve_messages(self, recipient, message_ids, leave_on_server):
		logger.info("MessagingClient.retrieve_messages()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(recipient)
		stream.list(message_ids, stream.u32)
		stream.bool(leave_on_server)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_RETRIEVE_MESSAGES, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		messages = stream.list(stream.anydata)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MessagingClient.retrieve_messages -> done")
		return messages
	
	async def delete_messages(self, recipient, message_ids):
		logger.info("MessagingClient.delete_messages()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(recipient)
		stream.list(message_ids, stream.u32)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_MESSAGES, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MessagingClient.delete_messages -> done")
	
	async def delete_all_messages(self, recipient):
		logger.info("MessagingClient.delete_all_messages()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.add(recipient)
		data = await self.client.request(self.PROTOCOL_ID, self.METHOD_DELETE_ALL_MESSAGES, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		number_deleted = stream.u32()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("MessagingClient.delete_all_messages -> done")
		return number_deleted


class MessageDeliveryClient(MessageDeliveryProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	async def deliver_message(self, message):
		logger.info("MessageDeliveryClient.deliver_message()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.anydata(message)
		await self.client.request(self.PROTOCOL_ID, self.METHOD_DELIVER_MESSAGE, stream.get(), True)


class MessagingServer(MessagingProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_DELIVER_MESSAGE: self.handle_deliver_message,
			self.METHOD_GET_NUMBER_OF_MESSAGES: self.handle_get_number_of_messages,
			self.METHOD_GET_MESSAGE_HEADERS: self.handle_get_message_headers,
			self.METHOD_RETRIEVE_ALL_MESSAGES_WITHIN_RANGE: self.handle_retrieve_all_messages_within_range,
			self.METHOD_RETRIEVE_MESSAGES: self.handle_retrieve_messages,
			self.METHOD_DELETE_MESSAGES: self.handle_delete_messages,
			self.METHOD_DELETE_ALL_MESSAGES: self.handle_delete_all_messages,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on MessagingServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_deliver_message(self, client, input, output):
		logger.info("MessagingServer.deliver_message()")
		#--- request ---
		message = input.anydata()
		response = await self.deliver_message(client, message)
		
		#--- response ---
		if not isinstance(response, rmc.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['modified_message', 'sandbox_node_ids', 'participants']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.anydata(response.modified_message)
		output.list(response.sandbox_node_ids, output.u32)
		output.list(response.participants, output.pid)
	
	async def handle_get_number_of_messages(self, client, input, output):
		logger.info("MessagingServer.get_number_of_messages()")
		#--- request ---
		recipient = input.extract(MessageRecipient)
		response = await self.get_number_of_messages(client, recipient)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u32(response)
	
	async def handle_get_message_headers(self, client, input, output):
		logger.info("MessagingServer.get_message_headers()")
		#--- request ---
		recipient = input.extract(MessageRecipient)
		range = input.extract(common.ResultRange)
		response = await self.get_message_headers(client, recipient, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.add)
	
	async def handle_retrieve_all_messages_within_range(self, client, input, output):
		logger.info("MessagingServer.retrieve_all_messages_within_range()")
		#--- request ---
		recipient = input.extract(MessageRecipient)
		range = input.extract(common.ResultRange)
		response = await self.retrieve_all_messages_within_range(client, recipient, range)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_retrieve_messages(self, client, input, output):
		logger.info("MessagingServer.retrieve_messages()")
		#--- request ---
		recipient = input.extract(MessageRecipient)
		message_ids = input.list(input.u32)
		leave_on_server = input.bool()
		response = await self.retrieve_messages(client, recipient, message_ids, leave_on_server)
		
		#--- response ---
		if not isinstance(response, list):
			raise RuntimeError("Expected list, got %s" %response.__class__.__name__)
		output.list(response, output.anydata)
	
	async def handle_delete_messages(self, client, input, output):
		logger.info("MessagingServer.delete_messages()")
		#--- request ---
		recipient = input.extract(MessageRecipient)
		message_ids = input.list(input.u32)
		await self.delete_messages(client, recipient, message_ids)
	
	async def handle_delete_all_messages(self, client, input, output):
		logger.info("MessagingServer.delete_all_messages()")
		#--- request ---
		recipient = input.extract(MessageRecipient)
		response = await self.delete_all_messages(client, recipient)
		
		#--- response ---
		if not isinstance(response, int):
			raise RuntimeError("Expected int, got %s" %response.__class__.__name__)
		output.u32(response)
	
	async def deliver_message(self, *args):
		logger.warning("MessagingServer.deliver_message not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_number_of_messages(self, *args):
		logger.warning("MessagingServer.get_number_of_messages not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def get_message_headers(self, *args):
		logger.warning("MessagingServer.get_message_headers not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def retrieve_all_messages_within_range(self, *args):
		logger.warning("MessagingServer.retrieve_all_messages_within_range not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def retrieve_messages(self, *args):
		logger.warning("MessagingServer.retrieve_messages not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_messages(self, *args):
		logger.warning("MessagingServer.delete_messages not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	async def delete_all_messages(self, *args):
		logger.warning("MessagingServer.delete_all_messages not implemented")
		raise common.RMCError("Core::NotImplemented")


class MessageDeliveryServer(MessageDeliveryProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_DELIVER_MESSAGE: self.handle_deliver_message,
		}
	
	async def logout(self, client):
		pass
	
	async def handle(self, client, method_id, input, output):
		if method_id in self.methods:
			await self.methods[method_id](client, input, output)
		else:
			logger.warning("Unknown method called on MessageDeliveryServer: %i", method_id)
			raise common.RMCError("Core::NotImplemented")
	
	async def handle_deliver_message(self, client, input, output):
		logger.info("MessageDeliveryServer.deliver_message()")
		#--- request ---
		message = input.anydata()
		await self.deliver_message(client, message)
	
	async def deliver_message(self, *args):
		logger.warning("MessageDeliveryServer.deliver_message not implemented")
		raise common.RMCError("Core::NotImplemented")

