
from nintendo.common import scheduler
import random
import struct

import logging
logger = logging.getLogger(__name__)


class ResendingMessage:
	def __init__(self, station, message, ack_id, limit):
		self.station = station
		self.message = message
		self.ack_id = ack_id
		self.limit = limit
		
		self.event = None


class ResendingTransport:
	def __init__(self, transport):
		self.transport = transport
		
		self.ack_id = random.randint(0, 0xFFFFFFFF)
		
		self.packets = {}
		
	def send(self, station, message, interval=.5, limit=10):
		self.ack_id = (self.ack_id + 1) & 0xFFFFFFFF
		if self.ack_id == 0:
			self.ack_id += 1
		
		message.payload += struct.pack(">I", self.ack_id)
		
		resend = ResendingMessage(station, message, self.ack_id, limit)
		resend.event = scheduler.add_timeout(self.handle_timeout, interval, True, resend)
		
		self.packets[self.ack_id] = resend
		
		self.transport.send(station, message)
		
	def acknowledge(self, station, ack_id):
		if ack_id not in self.packets:
			logger.warning("Received ack with unknown ack id")
			return
			
		message = self.packets[ack_id]
		if message.station != station:
			logger.warning("Received ack from wrong station")
			return
			
		scheduler.remove(message.event)
		del self.packets[ack_id]
		
	def handle_timeout(self, message):
		logger.debug("Resending message")
		
		message.limit -= 1
		if message.limit == 0:
			scheduler.remove(message.event)
			del self.packets[message.ack_id]
		else:
			self.transport.send(message.station, message.message)
