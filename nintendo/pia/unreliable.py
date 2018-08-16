
from nintendo.pia.packet import PIAMessage

import logging
logger = logging.getLogger(__name__)


class UnreliableProtocol:

	PROTOCOL_ID = 0x2000

	def __init__(self, session):
		self.session = session
		self.transport = session.transport
		
		self.packets = []
		
	def send(self, station, data):
		logger.debug("Sending %i bytes of unreliable data", len(data))
		message = PIAMessage()
		message.flags = 0
		message.protocol_id = self.PROTOCOL_ID
		message.protocol_port = 1
		message.payload = data
		self.transport.send(station, message)
		
	def recv(self):
		if self.packets:
			return self.packets.pop(0)
		
	def handle(self, station, message):
		if message.protocol_port == 1:
			logger.debug("Received %i bytes of unreliable data", len(message.payload))
			self.packets.append((station, message.payload))
		else:
			logger.warning("Unknown UnreliableProtocol port: %i", message.protocol_port)
