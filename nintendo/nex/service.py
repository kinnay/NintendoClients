
from nintendo.common import scheduler
from nintendo.nex import prudp, streams, kerberos, common
import random
import struct
import time

import logging
logger = logging.getLogger(__name__)


class RMCContext:
	def __init__(self, client, pid):
		self.client = client
		self.pid = pid


class RMCClient:
	def __init__(self, settings, sock=None):
		self.settings = settings
		self.sock = sock
		
		if not self.sock:
			self.sock = prudp.RVClient(settings)
			
		if not isinstance(self.sock, prudp.RVClient):
			raise TypeError("RMC protocol must lie on top of RV client")
		
		self.servers = {}
		self.pid = None
		
		self.call_id = 0
		self.responses = {}
		
		self.socket_event = None
		
	def set_access_key(self, key): self.sock.set_access_key(key)
		
	def register_server(self, server):
		if server.PROTOCOL_ID in self.servers:
			raise ValueError("Server with protocol id 0x%X already exists" %server.PROTOCOL_ID)
		self.servers[server.PROTOCOL_ID] = server
		
	def connect(self, host, port, stream_id, ticket=None):
		if not self.sock.connect(host, port, stream_id, ticket):
			return False
		self.socket_event = scheduler.add_socket(self.handle_recv, self.sock)
		return True
		
	def accept(self):
		self.pid = self.sock.pid
		self.socket_event = scheduler.add_socket(self.handle_recv, self.sock)
		return True
		
	def close(self):
		if self.socket_event:
			scheduler.remove(self.socket_event)
		self.sock.close()
		
	def stream_id(self): return self.sock.local_port
		
	def is_connected(self): return self.sock.is_connected()
	def local_address(self): return self.sock.local_address()
	def remote_address(self): return self.sock.remote_address()
		
	def handle_recv(self, data):
		if not data:
			logger.debug("Connection was closed")
			scheduler.remove(self.socket_event)
			return

		stream = streams.StreamIn(data, self.settings)
		length = stream.u32()
		protocol_id = stream.u8()

		if protocol_id & 0x80:
			self.handle_request(protocol_id & 0x7F, stream)
		else:
			self.handle_response(protocol_id, stream)

	def init_request(self, protocol_id, method_id):
		self.call_id += 1
		stream = streams.StreamOut(self.settings)
		stream.u8(protocol_id | 0x80)
		stream.u32(self.call_id)
		stream.u32(method_id)
		return stream, self.call_id
		
	def init_response(self, protocol_id, call_id, method_id, error=None):
		stream = streams.StreamOut(self.settings)
		stream.u8(protocol_id)
		if error:
			stream.u8(0)
			stream.result(error)
			stream.u32(call_id)
		else:
			stream.u8(1)
			stream.u32(call_id)
			stream.u32(method_id | 0x8000)
		return stream
		
	def send_message(self, stream):
		if self.sock.is_connected():
			self.sock.send(struct.pack("I", len(stream.get())) + stream.get())
		else:
			raise RuntimeError("Can't send message on disconnected service client")
			
	def handle_request(self, protocol_id, stream):
		call_id = stream.u32()
		method_id = stream.u32()
		logger.debug("Received RMC request: protocol=%i, call=%i, method=%i", protocol_id, call_id, method_id)
		
		result = common.Result(0x10001)
		if protocol_id in self.servers:
			context = RMCContext(self, self.pid)
			response = self.init_response(protocol_id, call_id, method_id)
			try:
				self.servers[protocol_id].handle(context, method_id, stream, response)
			except common.RMCError as e:
				result = common.Result(e.error_code)
			except Exception as e:
				logger.error("Exception occurred while handling method call")
				
				import traceback
				traceback.print_exc()
				
				if isinstance(e, TypeError): result = common.Result("PythonCore::TypeError")
				elif isinstance(e, IndexError): result = common.Result("PythonCore::IndexError")
				elif isinstance(e, MemoryError): result = common.Result("PythonCore::MemoryError")
				elif isinstance(e, KeyError): result = common.Result("PythonCore::KeyError")
				else: result = common.Result("PythonCore::Exception")
		else:
			logger.warning("Received RMC request with unimplemented protocol id: 0x%X", protocol_id)
			result = common.Result("Core::NotImplemented")
		
		if result.is_error():
			logger.info("RMC failed with error 0x%08X (%s)" %(result.code(), result.name()))
			response = self.init_response(protocol_id, call_id, method_id, result)
			
		self.send_message(response)
			
	def handle_response(self, protocol_id, stream):
		success = stream.u8()
		if not success:
			result = stream.result()
			call_id = stream.u32()

			logger.warning("RMC failed with error code 0x%08X", result.code())
			self.responses[call_id] = (result, None)

		else:
			call_id = stream.u32()
			method_id = stream.u32() & 0x7FFF
			logger.debug("Received RMC response: protocol=%i, call=%i, method=%i", protocol_id, call_id, method_id)

			self.responses[call_id] = (None, stream)
			
	def get_response(self, call_id, timeout=5):
		start = time.monotonic()
		while call_id not in self.responses:
			if not self.sock.is_connected():
				raise ConnectionError("RMC failed because the PRUDP connection was closed")

			scheduler.update()
			
			now = time.monotonic()
			if now - start >= timeout:
				raise RuntimeError("RMC request timed out")
			
		result, stream = self.responses.pop(call_id)
		if result:
			result.raise_if_error()
		return stream
		
		
class RMCServer:
	def __init__(self, settings, server=None):
		self.settings = settings
		self.server = server
		
		if not self.server:
			self.server = prudp.RVServer(settings)
			
		if not isinstance(self.server, prudp.RVServer):
			raise TypeError("RMC server must lie on top of RV server")
			
		self.protocols = {}
		
	def register_protocol(self, protocol):
		if protocol.PROTOCOL_ID in self.protocols:
			raise ValueError("Server protocol with id 0x%X already exists" %protocol.PROTOCOL_ID)
		self.protocols[protocol.PROTOCOL_ID] = protocol
		
	def start(self, host, port, stream_id=1, key=None):
		self.server.start(host, port, stream_id, key)
		scheduler.add_server(self.handle, self.server)
		
	def handle(self, socket):
		client = RMCClient(self.settings, socket)
		if client.accept():
			for protocol in self.protocols.values():
				client.register_server(protocol)
