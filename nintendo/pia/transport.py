
from nintendo.pia.packet import PIAPacket, PIAMessage
from nintendo.pia.socket import P2PSocket
from nintendo.common import scheduler, signal
import itertools
import random
import struct
import time

import logging
logger = logging.getLogger(__name__)


class PacketTransport:
	def __init__(self, session):
		self.session = session
		self.session_key = session.session_key
		self.packets = []
		
	def get_session_time(self):
		return int((time.monotonic() - self.session_start) * 1000)

	def start(self, addr):
		self.socket = P2PSocket()
		self.socket.bind(addr[0], addr[1])
		scheduler.add_socket(self.handle_recv, self.socket)
		
		self.session_start = time.monotonic()
		
	def handle_recv(self, pair):
		data, addr = pair
		
		station = self.session.station_mgr.find_by_address(addr)
		if not station:
			logger.warning("Received packet from unknown station: %s", addr)
			return
		
		packet = PIAPacket()
		if packet.decode(data, self.session_key):
			station.rtt_timer = packet.session_timer
			station.base_timer = self.get_session_time()
			self.packets.append((station, packet))
		
	def recv(self):
		if self.packets:
			return self.packets.pop(0)
			
	def send(self, station, packet):
		session_timer = self.get_session_time()
		packet.session_timer = session_timer & 0xFFFF
		
		packet.rtt_timer = 0
		if station.rtt_timer is not None:
			time_diff = session_timer - station.base_timer
			packet.rtt_timer = (station.rtt_timer + time_diff) & 0xFFFF
			
		if self.session.station.index == 0xFD:
			packet.connection_id = 1
			packet.packet_id = 0
		elif station.index == 0xFD:
			packet.connection_id = 0
			packet.packet_id = 0
		else:
			packet.connection_id = self.session.station.connection_id
			packet.packet_id = station.next_sequence_id()

		data = packet.encode(self.session_key)
		self.socket.send(data, station.address)
		
	def size_limit(self):
		return 1200
		

class MessageTransport:

	packet_received = signal.Signal()

	def __init__(self, session):
		self.session = session
		self.transport = PacketTransport(session)
		
	def start(self, address):
		self.transport.start(address)
		scheduler.add_socket(self.handle_recv, self.transport)
		
	def handle_recv(self, pair):
		station, packet = pair
		for message in packet.messages:
			self.packet_received(station, message)
		
	def send(self, station, message, add_mask=False):	
		message.destination = 0
		if station.index != 0xFD:
			message.destination = 1 << station.index
		message.station_key = self.session.rvcid
		message.station_index = self.session.station.index
		
		packet = PIAPacket([message])
		self.transport.send(station, packet)
		
	def size_limit(self):
		return self.transport.size_limit()
			
		
class ResendMessage:
	def __init__(self, station, message, ack_id, limit):
		self.station = station
		self.message = message
		self.ack_id = ack_id
		self.limit = limit
		self.timeout = None
		self.counter = 0
		
class ResendingTransport:
	def __init__(self, transport):
		self.transport = transport
		
		start = random.randint(0, 0xFFFFFFFF)
		self.ack_id = itertools.count(start)
		
		self.messages = {}
		
	def send(self, station, message, delay=1, limit=0):
		ack_id = next(self.ack_id) & 0xFFFFFFFF
		message.payload += struct.pack(">I", ack_id)
		
		handle = ResendMessage(station, message, ack_id, limit)
		self.messages[ack_id] = handle
		self.transport.send(station, message)
		handle.timeout = scheduler.add_timeout(self.handle_timeout, delay, True, handle)
		
		self.wait_ack(message)
		
	def handle_timeout(self, handle):
		handle.counter += 1
		if handle.counter == handle.limit:
			logger.warning("Removing message from queue because its resend limit was reached")
			self.messages.pop(handle.ack_id)
			scheduler.remove(handle.timeout)
		else:
			logger.debug("Resending message with ack_id=%i" %handle.ack_id)
			self.transport.send(handle.station, handle.message)
		
	def handle_ack(self, payload):
		ack_id = struct.unpack_from(">I", payload, -4)[0]
		if ack_id in self.messages:
			message = self.messages.pop(ack_id)
			scheduler.remove(message.timeout)
		else:
			logger.warning("Received ack with unknown ack id: %i", ack_id)
		
	def wait_ack(self, message):
		ack_id = struct.unpack_from(">I", message.payload, -4)[0]
		while ack_id not in self.messages:
			scheduler.update()
			

class ReliableMessage:
	def __init__(self, data, packet_id):
		self.data = data
		self.packet_id = packet_id
		self.timeout = None

class ReliableTransport:
	def __init__(self, transport, station, protocol_id, protocol_port, callback):
		self.transport = transport
		self.station = station
		self.protocol_id = protocol_id
		self.protocol_port = protocol_port
		self.callback = callback

		self.packet_id_in = 0xFFFFF82F
		self.packet_id_out = 0xFFFFF82F
		self.early_packets = 0
		
		self.last_received_ack = 0xFFFFF82F
		
		self.messages = {}
		self.incoming = {}
		self.packets = []
		self.fragments = b""
		
	def send(self, data, delay=0.5):
		limit = (self.transport.size_limit() & ~7) - 0x18
		fragments = (len(data) - 1) // limit
		
		for i in range(fragments):
			flags = 1
			if i == fragments - 1: #Last fragment
				flags |= 2
			chunk = data[i * limit : (i + 1) * limit]
			
			payload = struct.pack(
				">HHIIIQ", flags, len(chunk), 0, self.packet_id_out,
				self.packet_id_in, self.early_packets
			) + chunk
			
			message = ReliableMessage(payload, self.packet_id_out, delay)
			message.timeout = scheduler.add_timeout(
				self.handle_timeout, delay, True, message
			)
			self.messages[self.packet_id_out] = message

			self.send_raw(payload)

			self.packet_id_out += 1
		
	def handle_timeout(self, message):
		logger.debug("Resending reliable message (%X)" %message.packet_id)
		self.send_raw(message.data)
			
	def send_raw(self, data):
		message = PIAMessage()
		message.flags = 0
		message.protocol_id = self.protocol_id
		message.protocol_port = self.protocol_port
		message.payload = data
		self.transport.send(self.station, message)
		
	def send_ack(self):
		data = struct.pack(">HHIIIQ", 0, 0, 0, 0, self.packet_id_in, self.early_packets)
		self.send_raw(data)
		
	def handle(self, message):
		flags, length, packet_id, ack_id, early_packets = \
			struct.unpack_from(">HHxxxxIIQ", message.payload)
		payload = message.payload[0x18:]
		
		if len(payload) != length:
			logger.warning("Payload size doesn't match length field in reliable message")
			return

		if flags & 1:
			if packet_id == self.packet_id_in:
				self.incoming[packet_id] = message
				
				while self.packet_id_in in self.incoming:
					self.process_packet(self.incoming.pop(self.packet_id_in))
					self.packet_id_in += 1
					
					self.early_packets >>= 1
					if self.packet_id_in + 64 in self.incoming:
						self.early_packets |= 1 << 63
					
				self.send_ack()

			elif packet_id > self.packet_id_in:
				self.incoming[packet_id] = message
				diff = packet_id - self.packet_id_in - 1
				if diff < 64:
					self.early_packets |= 1 << diff
				self.send_ack()
					
		for packet_id in range(self.last_received_ack, ack_id):
			self.handle_ack(packet_id)
		self.last_received_ack = ack_id
		
		for i in range(self.packet_id_out - self.last_received_ack - 1):
			if early_packets & (1 << i):
				packet_id = self.packet_id_out + i + 1
				self.handle_ack(packet_id)
				
	def handle_ack(self, packet_id):
		if packet_id in self.messages:
			message = self.messages.pop(packet_id)
			scheduler.remove(message.timeout)
					
	def process_packet(self, message):
		flags = struct.unpack_from(">H", message.payload)[0]
		payload = message.payload[0x18:]
		
		self.fragments += payload
		if flags & 2:
			self.callback(self.station, self.fragments)
			self.fragments = b""
