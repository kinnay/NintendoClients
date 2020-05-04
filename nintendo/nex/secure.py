
# This file was generated automatically by generate_protocols.py

from nintendo.nex import common, streams

import logging
logger = logging.getLogger(__name__)


class ConnectionData(common.Structure):
	def __init__(self):
		super().__init__()
		self.station = None
		self.connection_id = None
	
	def check_required(self, settings):
		for field in ['station', 'connection_id']:
			if getattr(self, field) is None:
				raise ValueError("No value assigned to required field: %s" %field)
	
	def load(self, stream):
		self.station = stream.stationurl()
		self.connection_id = stream.u32()
	
	def save(self, stream):
		self.check_required(stream.settings)
		stream.stationurl(self.station)
		stream.u32(self.connection_id)


class SecureConnectionProtocol:
	METHOD_REGISTER = 1
	METHOD_REQUEST_CONNECTION_DATA = 2
	METHOD_REQUEST_URLS = 3
	METHOD_REGISTER_EX = 4
	METHOD_TEST_CONNECTIVITY = 5
	METHOD_REPLACE_URL = 6
	METHOD_SEND_REPORT = 7
	
	PROTOCOL_ID = 0xB


class SecureConnectionClient(SecureConnectionProtocol):
	def __init__(self, client):
		self.settings = client.settings
		self.client = client
	
	def register(self, urls):
		logger.info("SecureConnectionClient.register()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(urls, stream.stationurl)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_REGISTER, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.result = stream.result()
		obj.connection_id = stream.u32()
		obj.public_station = stream.stationurl()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("SecureConnectionClient.register -> done")
		return obj
	
	def request_connection_data(self, cid, pid):
		logger.info("SecureConnectionClient.request_connection_data()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(cid)
		stream.pid(pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_REQUEST_CONNECTION_DATA, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.result = stream.bool()
		obj.connection_data = stream.list(ConnectionData)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("SecureConnectionClient.request_connection_data -> done")
		return obj
	
	def request_urls(self, cid, pid):
		logger.info("SecureConnectionClient.request_urls()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(cid)
		stream.pid(pid)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_REQUEST_URLS, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.result = stream.bool()
		obj.urls = stream.list(stream.stationurl)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("SecureConnectionClient.request_urls -> done")
		return obj
	
	def register_ex(self, urls, login_data):
		logger.info("SecureConnectionClient.register_ex()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.list(urls, stream.stationurl)
		stream.anydata(login_data)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_REGISTER_EX, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		obj = common.RMCResponse()
		obj.result = stream.result()
		obj.connection_id = stream.u32()
		obj.public_station = stream.stationurl()
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("SecureConnectionClient.register_ex -> done")
		return obj
	
	def test_connectivity(self):
		logger.info("SecureConnectionClient.test_connectivity()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_TEST_CONNECTIVITY, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("SecureConnectionClient.test_connectivity -> done")
	
	def replace_url(self, url, new):
		logger.info("SecureConnectionClient.replace_url()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.stationurl(url)
		stream.stationurl(new)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_REPLACE_URL, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("SecureConnectionClient.replace_url -> done")
	
	def send_report(self, report_id, data):
		logger.info("SecureConnectionClient.send_report()")
		#--- request ---
		stream = streams.StreamOut(self.settings)
		stream.u32(report_id)
		stream.qbuffer(data)
		data = self.client.send_request(self.PROTOCOL_ID, self.METHOD_SEND_REPORT, stream.get())
		
		#--- response ---
		stream = streams.StreamIn(data, self.settings)
		if not stream.eof():
			raise ValueError("Response is bigger than expected (got %i bytes, but only %i were read)" %(stream.size(), stream.tell()))
		logger.info("SecureConnectionClient.send_report -> done")


class SecureConnectionServer(SecureConnectionProtocol):
	def __init__(self):
		self.methods = {
			self.METHOD_REGISTER: self.handle_register,
			self.METHOD_REQUEST_CONNECTION_DATA: self.handle_request_connection_data,
			self.METHOD_REQUEST_URLS: self.handle_request_urls,
			self.METHOD_REGISTER_EX: self.handle_register_ex,
			self.METHOD_TEST_CONNECTIVITY: self.handle_test_connectivity,
			self.METHOD_REPLACE_URL: self.handle_replace_url,
			self.METHOD_SEND_REPORT: self.handle_send_report,
		}
	
	def handle(self, context, method_id, input, output):
		if method_id in self.methods:
			self.methods[method_id](context, input, output)
		else:
			logger.warning("Unknown method called on %s: %i", self.__class__.__name__, method_id)
			raise common.RMCError("Core::NotImplemented")
	
	def handle_register(self, context, input, output):
		logger.info("SecureConnectionServer.register()")
		#--- request ---
		urls = input.list(input.stationurl)
		response = self.register(context, urls)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'connection_id', 'public_station']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.u32(response.connection_id)
		output.stationurl(response.public_station)
	
	def handle_request_connection_data(self, context, input, output):
		logger.info("SecureConnectionServer.request_connection_data()")
		#--- request ---
		cid = input.u32()
		pid = input.pid()
		response = self.request_connection_data(context, cid, pid)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'connection_data']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.bool(response.result)
		output.list(response.connection_data, output.add)
	
	def handle_request_urls(self, context, input, output):
		logger.info("SecureConnectionServer.request_urls()")
		#--- request ---
		cid = input.u32()
		pid = input.pid()
		response = self.request_urls(context, cid, pid)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'urls']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.bool(response.result)
		output.list(response.urls, output.stationurl)
	
	def handle_register_ex(self, context, input, output):
		logger.info("SecureConnectionServer.register_ex()")
		#--- request ---
		urls = input.list(input.stationurl)
		login_data = input.anydata()
		response = self.register_ex(context, urls, login_data)
		
		#--- response ---
		if not isinstance(response, common.RMCResponse):
			raise RuntimeError("Expected RMCResponse, got %s" %response.__class__.__name__)
		for field in ['result', 'connection_id', 'public_station']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in RMCResponse: %s" %field)
		output.result(response.result)
		output.u32(response.connection_id)
		output.stationurl(response.public_station)
	
	def handle_test_connectivity(self, context, input, output):
		logger.info("SecureConnectionServer.test_connectivity()")
		#--- request ---
		self.test_connectivity(context)
	
	def handle_replace_url(self, context, input, output):
		logger.info("SecureConnectionServer.replace_url()")
		#--- request ---
		url = input.stationurl()
		new = input.stationurl()
		self.replace_url(context, url, new)
	
	def handle_send_report(self, context, input, output):
		logger.info("SecureConnectionServer.send_report()")
		#--- request ---
		report_id = input.u32()
		data = input.qbuffer()
		self.send_report(context, report_id, data)
	
	def register(self, *args):
		logger.warning("SecureConnectionServer.register not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def request_connection_data(self, *args):
		logger.warning("SecureConnectionServer.request_connection_data not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def request_urls(self, *args):
		logger.warning("SecureConnectionServer.request_urls not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def register_ex(self, *args):
		logger.warning("SecureConnectionServer.register_ex not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def test_connectivity(self, *args):
		logger.warning("SecureConnectionServer.test_connectivity not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def replace_url(self, *args):
		logger.warning("SecureConnectionServer.replace_url not implemented")
		raise common.RMCError("Core::NotImplemented")
	
	def send_report(self, *args):
		logger.warning("SecureConnectionServer.send_report not implemented")
		raise common.RMCError("Core::NotImplemented")

