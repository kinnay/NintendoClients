
from nintendo.pia.packet import PIAMessage
import struct

import logging
logger = logging.getLogger(__name__)


class RttProtocol:

	PROTOCOL_ID = 0x600

	def __init__(self, session):
		self.session = session
		self.transport = session.transport
		
	def send(self, station, response, time):
		logger.debug("Sending rtt info packet")
		message = PIAMessage()
		message.flags = 0
		message.protocol_id = self.PROTOCOL_ID
		message.protocol_port = 0
		message.payload = struct.pack(">IxxxxQ", response, time)
		self.transport.send(station, message)
		
	def handle(self, station, message):
		if message.protocol_port == 0:
			response, time = struct.unpack(">IxxxxQ", message.payload)
			if not response:
				logger.info("Received rtt info request")
				self.send(station, True, time)
		else:
			logger.warning("Unknown RttProtocol port: %i", message.protocol_port)
