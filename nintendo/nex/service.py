
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
		
		
class RMCMessage:
	REQUEST = 0
	RESPONSE = 1
	
	def __init__(self, settings):
		self.settings = settings
		
		self.mode = RMCMessage.REQUEST
		self.protocol = None
		self.method = None
		self.call_id = 0
		self.error = -1
		self.body = b""
		
	@staticmethod
	def prepare(settings, mode, protocol, method, call_id, body):
		inst = RMCMessage(settings)
		inst.mode = mode
		inst.protocol = protocol
		inst.method = method
		inst.call_id = call_id
		inst.body = body
		return inst
		
	@staticmethod
	def request(settings, protocol, method, call_id, body):
		return RMCMessage.prepare(
			settings, RMCMessage.REQUEST, protocol, method, call_id, body
		)
		
	@staticmethod
	def response(settings, protocol, method, call_id, body):
		return RMCMessage.prepare(
			settings, RMCMessage.RESPONSE, protocol, method, call_id, body
		)
		
	@staticmethod
	def error(settings, protocol, method, call_id, error):
		inst = RMCMessage(settings)
		inst.mode = RMCMessage.RESPONSE
		inst.protocol = protocol
		inst.method = method
		inst.call_id = call_id
		inst.error = error
		return inst
	
	@staticmethod
	def parse(settings, data):
		inst = RMCMessage(settings)
		inst.decode(data)
		return inst
		
	def encode(self):
		stream = streams.StreamOut(self.settings)
		if self.mode == self.REQUEST:
			stream.u8(self.protocol | 0x80)
			stream.u32(self.call_id)
			stream.u32(self.method)
			stream.write(self.body)
		else:
			stream.u8(self.protocol)
			if self.error != -1 and self.error & 0x80000000:
				stream.bool(False)
				stream.u32(self.error)
				stream.u32(self.call_id)
			else:
				stream.bool(True)
				stream.u32(self.call_id)
				stream.u32(self.method | 0x8000)
				stream.write(self.body)
		return struct.pack("I", stream.size()) + stream.get()
	
	def decode(self, data):
		stream = streams.StreamIn(data, self.settings)
		
		length = stream.u32()
		if length != stream.size() - 4:
			raise ValueError("RMC message has unexpected size")
		
		protocol = stream.u8()
		
		self.protocol = protocol & ~0x80
		
		if protocol & 0x80:
			self.mode = self.REQUEST
			self.call_id = stream.u32()
			self.method = stream.u32()
			self.body = stream.readall()
		else:
			self.mode = self.RESPONSE
			if stream.bool():
				self.call_id = stream.u32()
				self.method = stream.u32() & ~0x8000
				self.body = stream.readall()
			else:
				self.error = stream.u32()
				self.call_id = stream.u32()
				if not stream.eof():
					raise ValueError("RMC error message is bigger than expected")
		
		
class RMCClientBase:
	def __init__(self, settings):
		self.settings = settings
		
		self.servers = {}
		
	def register_server(self, server):
		if server.PROTOCOL_ID in self.servers:
			raise ValueError("Server with protocol id 0x%X already exists" %server.PROTOCOL_ID)
		self.servers[server.PROTOCOL_ID] = server
	
	def send_request(self, protocol, method, body):
		raise NotImplementedError("%s.send_request" %self.__class__.__name__)
		
	def handle_request(self, context, request):
		logger.debug(
			"Received RMC request: protocol=%i, call=%i, method=%i",
			request.protocol, request.call_id, request.method
		)
	
		input = streams.StreamIn(request.body, self.settings)
		output = streams.StreamOut(self.settings)
		
		result = common.Result()
		if request.protocol in self.servers:
			try:
				self.servers[request.protocol].handle(context, request.method, input, output)
			except common.RMCError as e:
				result = common.Result(e.code)
			except Exception as e:
				logger.error("Exception occurred while handling method call")
				
				import traceback
				traceback.print_exc()
				
				if isinstance(e, TypeError): result = common.Result.error("PythonCore::TypeError")
				elif isinstance(e, IndexError): result = common.Result.error("PythonCore::IndexError")
				elif isinstance(e, MemoryError): result = common.Result.error("PythonCore::MemoryError")
				elif isinstance(e, KeyError): result = common.Result.error("PythonCore::KeyError")
				else: result = common.Result.error("PythonCore::Exception")
		else:
			logger.warning("Received RMC request with unimplemented protocol id: 0x%X", protocol_id)
			result = common.Result.error("Core::NotImplemented")
			
		if result.is_success():
			response = RMCMessage.response(
				self.settings, request.protocol, request.method,
				request.call_id, output.get()
			)
		else:
			response = RMCMessage.error(
				self.settings, request.protocol, request.method,
				request.call_id, result.code()
			)
		return response
		
		
class RMCClient(RMCClientBase):
	def __init__(self, settings, sock=None):
		super().__init__(settings)
		
		self.sock = sock
		
		if not self.sock:
			self.sock = prudp.RVClient(settings)
			
		if not isinstance(self.sock, prudp.RVClient):
			raise TypeError("RMC protocol must lie on top of RV client")
			
		self.pid = None
		
		self.call_id = 0
		self.responses = {}
		
		self.socket_event = None
		
	def set_access_key(self, key): self.sock.set_access_key(key)
		
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
		
		message = RMCMessage.parse(self.settings, data)
		if message.mode == RMCMessage.REQUEST:
			context = RMCContext(self, self.pid)
			response = self.handle_request(context, message)
			self.sock.send(response.encode())
		else:
			if message.error != -1:
				logger.warning("RMC failed with error code 0x%08X", message.error)
			else:
				logger.debug(
					"Received RMC response: protocol=%i, call=%i, method=%i",
					message.protocol, message.call_id, message.method
				)
			self.responses[message.call_id] = message
			
	def send_request(self, protocol, method, body):
		call_id = self.call_id
		self.call_id += 1
		
		message = RMCMessage.request(self.settings, protocol, method, call_id, body)
		self.sock.send(message.encode())
		
		return self.get_response(call_id)
			
	def get_response(self, call_id, timeout=5):
		start = time.monotonic()
		while call_id not in self.responses:
			if not self.sock.is_connected():
				raise ConnectionError("RMC failed because the PRUDP connection was closed")

			scheduler.update()
			
			now = time.monotonic()
			if now - start >= timeout:
				raise RuntimeError("RMC request timed out")
			
		message = self.responses.pop(call_id)
		if message.error != -1:
			raise common.RMCError(message.error)
		return message.body
		
		
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
