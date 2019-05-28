
from nintendo.common.streams import StreamIn, StreamOut
import hmac

import logging
logger = logging.getLogger(__name__)


class PIAMessage:
	def __init__(self):
		self.flags = None
		self.station_index = None
		self.destination = None
		self.station_key = None
		self.protocol_id = None
		self.protocol_port = None
		self.payload = None
		
	def decode(self, stream):
		self.flags = stream.u8()
		self.station_index = stream.u8() #Source
		payload_size = stream.u16()
		self.destination = stream.u32()
		self.station_key = stream.u32()
		self.protocol_id = stream.u16()
		self.protocol_port = stream.u16()
		
		if stream.u32() != 0:
			logger.error("Reserved field should be cleared")
			return False

		self.payload = stream.read(payload_size)
		stream.align(4)
		return True
		
	def encode(self, stream):
		stream.u8(self.flags)
		stream.u8(self.station_index)
		stream.u16(len(self.payload))
		stream.u32(self.destination)
		stream.u32(self.station_key)
		stream.u16(self.protocol_id)
		stream.u16(self.protocol_port)
		stream.u32(0) #Reserved, always 0
		
		stream.write(self.payload)
		stream.align(4)


class PIAPacket:
	def __init__(self, messages=None):
		self.connection_id = None
		self.packet_id = None
		self.session_timer = None
		self.rtt_timer = None
		
		self.messages = messages
		if self.messages is None:
			self.messages = []

	def decode(self, data, session_key):
		if len(data) < 0x30:
			logger.error("Packet is too small")
			return False
	
		stream = StreamIn(data, ">")
		if stream.u32() != 0x32AB9864:
			logger.error("Invalid packet signature")
			return False
			
		encryption = stream.u8()
		if encryption not in [1, 2]:
			logger.error("Invalid encryption method")
			return False
			
		if encryption == 2:
			logger.error("Encryption is not supported yet")
			return False
			
		self.connection_id = stream.u8()
		self.packet_id = stream.u16()
		self.session_timer = stream.u16()
		self.rtt_timer = stream.u16()
		
		while stream.available() > 0x10:
			message = PIAMessage()
			if not message.decode(stream):
				return False
			self.messages.append(message)
		
		signature = stream.read(0x10)
		if hmac.new(session_key, data[:-0x10]).digest() != signature:
			logger.error("Incorrect packet signature")
			return False
		return True

	def encode(self, session_key):
		stream = StreamOut(">")
		stream.u32(0x32AB9864) #Magic number
		stream.u8(1) #No encryption
		stream.u8(self.connection_id)
		stream.u16(self.packet_id)
		stream.u16(self.session_timer)
		stream.u16(self.rtt_timer)
		
		for message in self.messages:
			message.encode(stream)
		
		#Checksum
		stream.write(hmac.new(session_key, stream.get()).digest())
		return stream.get()
