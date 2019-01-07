
# This file was generated automatically from secure.proto

from nintendo.nex import common

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
		self.client = client

	def register(self, urls):
		logger.info("SecureConnectionClient.register()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_REGISTER)
		stream.list(urls, stream.stationurl)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		obj = common.ResponseObject()
		obj.result = stream.result()
		obj.connection_id = stream.u32()
		obj.public_station = stream.stationurl()
		logger.info("SecureConnectionClient.register -> done")
		return obj

	def request_connection_data(self, cid, pid):
		logger.info("SecureConnectionClient.request_connection_data()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_REQUEST_CONNECTION_DATA)
		stream.u32(cid)
		stream.pid(pid)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		obj = common.ResponseObject()
		obj.result = stream.bool()
		obj.connection_data = stream.list(ConnectionData)
		logger.info("SecureConnectionClient.request_connection_data -> done")
		return obj

	def request_urls(self, cid, pid):
		logger.info("SecureConnectionClient.request_urls()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_REQUEST_URLS)
		stream.u32(cid)
		stream.pid(pid)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		obj = common.ResponseObject()
		obj.result = stream.bool()
		obj.urls = stream.list(stream.stationurl)
		logger.info("SecureConnectionClient.request_urls -> done")
		return obj

	def register_ex(self, urls, login_data):
		logger.info("SecureConnectionClient.register_ex()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_REGISTER_EX)
		stream.list(urls, stream.stationurl)
		stream.anydata(login_data)
		self.client.send_message(stream)

		#--- response ---
		stream = self.client.get_response(call_id)
		obj = common.ResponseObject()
		obj.result = stream.result()
		obj.connection_id = stream.u32()
		obj.public_station = stream.stationurl()
		logger.info("SecureConnectionClient.register_ex -> done")
		return obj

	def test_connectivity(self):
		logger.info("SecureConnectionClient.test_connectivity()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_TEST_CONNECTIVITY)
		self.client.send_message(stream)

		#--- response ---
		self.client.get_response(call_id)
		logger.info("SecureConnectionClient.test_connectivity -> done")

	def replace_url(self, url, new):
		logger.info("SecureConnectionClient.replace_url()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_REPLACE_URL)
		stream.stationurl(url)
		stream.stationurl(new)
		self.client.send_message(stream)

		#--- response ---
		self.client.get_response(call_id)
		logger.info("SecureConnectionClient.replace_url -> done")

	def send_report(self, report_id, data):
		logger.info("SecureConnectionClient.send_report()")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_SEND_REPORT)
		stream.u32(report_id)
		stream.qbuffer(data)
		self.client.send_message(stream)

		#--- response ---
		self.client.get_response(call_id)
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

	def handle(self, caller_id, method_id, input, output):
		if method_id in self.methods:
			return self.methods[method_id](caller_id, input, output)
		logger.warning("Unknown method called on SecureConnectionServer: %i", method_id)
		return common.Result("Core::NotImplemented")

	def handle_register(self, caller_id, input, output):
		logger.info("SecureConnectionServer.register()")
		#--- request ---
		urls = input.list(input.stationurl)
		response = common.ResponseObject()
		self.register(caller_id, response, urls)

		#--- response ---
		for field in ['result', 'connection_id', 'public_station']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in response object: %s" %field)
		output.result(response.result)
		output.u32(response.connection_id)
		output.stationurl(response.public_station)

	def handle_request_connection_data(self, caller_id, input, output):
		logger.info("SecureConnectionServer.request_connection_data()")
		#--- request ---
		cid = input.u32()
		pid = input.pid()
		response = common.ResponseObject()
		self.request_connection_data(caller_id, response, cid, pid)

		#--- response ---
		for field in ['result', 'connection_data']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in response object: %s" %field)
		output.bool(response.result)
		output.list(response.connection_data, output.add)

	def handle_request_urls(self, caller_id, input, output):
		logger.info("SecureConnectionServer.request_urls()")
		#--- request ---
		cid = input.u32()
		pid = input.pid()
		response = common.ResponseObject()
		self.request_urls(caller_id, response, cid, pid)

		#--- response ---
		for field in ['result', 'urls']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in response object: %s" %field)
		output.bool(response.result)
		output.list(response.urls, output.stationurl)

	def handle_register_ex(self, caller_id, input, output):
		logger.info("SecureConnectionServer.register_ex()")
		#--- request ---
		urls = input.list(input.stationurl)
		login_data = input.anydata()
		response = common.ResponseObject()
		self.register_ex(caller_id, response, urls, login_data)

		#--- response ---
		for field in ['result', 'connection_id', 'public_station']:
			if not hasattr(response, field):
				raise RuntimeError("Missing field in response object: %s" %field)
		output.result(response.result)
		output.u32(response.connection_id)
		output.stationurl(response.public_station)

	def handle_test_connectivity(self, caller_id, input, output):
		logger.info("SecureConnectionServer.test_connectivity()")
		#--- request ---
		self.test_connectivity()

	def handle_replace_url(self, caller_id, input, output):
		logger.info("SecureConnectionServer.replace_url()")
		#--- request ---
		url = input.stationurl()
		new = input.stationurl()
		self.replace_url(url, new)

	def handle_send_report(self, caller_id, input, output):
		logger.info("SecureConnectionServer.send_report()")
		#--- request ---
		report_id = input.u32()
		data = input.qbuffer()
		self.send_report(report_id, data)

	def register(self, *args):
		logger.warning("SecureConnectionServer.register not implemented")
		return common.Result("Core::NotImplemented")

	def request_connection_data(self, *args):
		logger.warning("SecureConnectionServer.request_connection_data not implemented")
		return common.Result("Core::NotImplemented")

	def request_urls(self, *args):
		logger.warning("SecureConnectionServer.request_urls not implemented")
		return common.Result("Core::NotImplemented")

	def register_ex(self, *args):
		logger.warning("SecureConnectionServer.register_ex not implemented")
		return common.Result("Core::NotImplemented")

	def test_connectivity(self, *args):
		logger.warning("SecureConnectionServer.test_connectivity not implemented")
		return common.Result("Core::NotImplemented")

	def replace_url(self, *args):
		logger.warning("SecureConnectionServer.replace_url not implemented")
		return common.Result("Core::NotImplemented")

	def send_report(self, *args):
		logger.warning("SecureConnectionServer.send_report not implemented")
		return common.Result("Core::NotImplemented")
