
from nintendo.pia.message import PIAMessage
from nintendo.pia.streams import StreamOut, StreamIn
from nintendo.pia.types import StationConnectionInfo, StationLocation
import random

import logging
logger = logging.getLogger(__name__)


class LanProtocol:
	
	MESSAGE_HOST_REQUEST = 3
	MESSAGE_HOST_REPLY = 4
	MESSAGE_SESSION_REQUEST = 5
	MESSAGE_SESSION_REPLY = 6
	MESSAGE_KEEP_ALIVE = 7

	def __init__(self, session):
		self.session = session
		self.settings = session.settings
		self.transport = session.transport
		
		self.handlers = {
			self.MESSAGE_HOST_REQUEST: self.handle_host_request,
			self.MESSAGE_HOST_REPLY: self.handle_host_reply,
			self.MESSAGE_SESSION_REQUEST: self.handle_session_request,
			self.MESSAGE_SESSION_REPLY: self.handle_session_reply,
			self.MESSAGE_KEEP_ALIVE: self.handle_keep_alive
		}
		
		self.session_reply_id = 0
		
		self.host_requests = {}
		self.session_requests = {}
		
	def get_protocol_type(self):
		if self.settings.get("pia.protocol_type_revision") == 0:
			return 0x4400
		return 0x44
		
	def handle(self, station, message):
		if message.protocol_port == 0:
			message_type = message.payload[0]
			if message_type in self.handlers:
				self.handlers[message_type](station, message.payload)
			else:
				logger.warning("Unknown LAN protocol message: %i" %message_type)
		else:
			logger.error("Unknown LAN protocol port: %i", message.protocol_port)
			
	def handle_host_request(self, station, data):
		logger.debug("Received host request")
		
		if len(data) != 0x10:
			logger.error("Session request has unexpected size")
			return
			
		stream = StreamIn(data, self.settings)
		stream.skip(12)
		
		session_id = stream.u32()
		
		session_info = self.session.get_session_info()
		if session_info.session_id != session_id:
			logger.warning("Received session request with different session id")
			return
			
		if not self.session.is_host():
			logger.info("Ignoring host request because we aren't host")
			return
			
		self.send_host_reply(station, session_info)
		
	def handle_host_reply(self, station, data):
		logger.debug("Received host reply")
		
		stream = StreamIn(data, self.settings)
		stream.skip(12)
		
		session_id = stream.u32()
		
		if self.settings.get("pia.version") < 51000:
			host = stream.extract(StationConnectionInfo).public
		else:
			host = stream.extract(StationLocation)
			
		if session_id not in self.host_requests:
			logger.warning("Received unexpected host reply")
			return
			
		self.host_requests[session_id] = host
	
	def handle_session_request(self, station, data):
		logger.debug("Received session request")
		
		if len(data) != 0x10:
			logger.error("Session request has unexpected size")
			return
		
		stream = StreamIn(data, self.settings)
		stream.skip(12)
		
		session_id = stream.u32()
		
		session_info = self.session.get_session_info()
		if session_info.session_id != session_id:
			logger.warning("Received session request with different session id")
			return
			
		if not self.session.is_host():
			logger.info("Ignoring session request because we aren't host")
			return
		
		self.send_session_reply(station, session_info)
		
	def handle_session_reply(self, station, data):
		logger.debug("Received session reply")
		
		stream = StreamIn(data, self.settings)
		stream.skip(12)
		
		session_id = stream.u32()
			
		if session_id not in self.host_requests:
			logger.warning("Received unexpected session reply")
			return
			
		self.session_requests[session_id].update(stream)
			
	def handle_keep_alive(self, station, data):
		logger.debug("Received keep-alive message")
		
	def send_host_request(self, session_id):
		logger.debug("Sending host request")
		
		stream = StreamOut(self.settings)
		stream.u8(self.MESSAGE_HOST_REQUEST)
		stream.pad(11)
		stream.u32(session_id)
		
		message = PIAMessage()
		message.protocol_id = self.get_protocol_type()
		message.payload = stream.get()
		
		for port in range(0xC000, 0xC004):
			self.transport.broadcast(port, message)
			
	def send_host_reply(self, station, session_info):
		logger.debug("Sending host reply")
		
		stream = StreamOut(self.settings)
		stream.u8(self.MESSAGE_HOST_REPLY)
		stream.pad(11)
		stream.u32(session_info.session_id)
		
		host = self.session.host_station()
		if self.settings.get("pia.version") < 51000:
			stream.add(host.connection_info)
		else:
			stream.add(host.connection_info.local)
		
		message = PIAMessage()
		message.protocol_id = self.get_protocol_type()
		message.payload = stream.get()
		
		for i in range(3):
			self.transport.send(station, message)
		
	def send_session_request(self, session_id):
		logger.debug("Sending host request")
		
		stream = StreamOut(self.settings)
		stream.u8(self.MESSAGE_SESSION_REQUEST)
		stream.pad(11)
		stream.u32(session_id)
		
		message = PIAMessage()
		message.protocol_id = self.get_protocol_type()
		message.payload = stream.get()
		
		for port in range(0xC000, 0xC004):
			self.transport.broadcast(port, message)
		
	def send_session_reply(self, station, session_info):
		logger.debug("Sending session reply")
		
		stream = StreamOut(self.settings)
		stream.add(session_info)
		data = stream.get()
		
		rand_value = random.randint(0, 0xFFFFFFFF)
		
		fragments = (len(data) - 1) // 800 + 1
		for i in range(fragments):
			stream = StreamOut(self.settings)
			stream.u8(self.MESSAGE_SESSION_REPLY)
			stream.pad(11)
			stream.u32(rand_value)
			stream.u16(self.session_reply_id)
			stream.u8(i)
			stream.u8(fragments)
			
			body = data[i * 800 : (i + 1) * 800]
			stream.u32(len(body))
			stream.write(body)
			
			message = PIAMessage()
			message.protocol_id = self.get_protocol_type()
			message.payload = stream.get()
			self.transport.send(station, message)
			
		self.session_reply_id += 1
