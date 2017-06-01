
from nintendo.common.transport import Socket
from nintendo.common.scheduler import Scheduler
from nintendo.common.crypto import RC4
from nintendo.common import util

import hashlib
import hmac
import struct
import random
import time

import logging
logger = logging.getLogger(__name__)

#These values are actually a bit more complicated,
#but since 0xA1 and 0xAF always work, there's no
#point in doing it differently.
PORT_SERVER = 0xA1
PORT_CLIENT = 0xAF

PACKET_SYN = 0
PACKET_CONNECT = 1
PACKET_DATA = 2
PACKET_DISCONNECT = 3
PACKET_PING = 4

FLAG_ACK = 0x10
FLAG_RELIABLE = 0x20
FLAG_NEED_ACK = 0x40
FLAG_80 = 0x80
FLAG_ACK2 = 0x2000

#Supported functions, unknown purpose
SUPPORT_2 = 2
SUPPORT_4 = 4
SUPPORT_100 = 0x100

#I ran into issues when I was missing a support
#flag, so I'm just setting all bits to 1 here
SUPPORT_ALL = 0xFFFFFFFF


class PRUDPError(ConnectionError): pass


class PRUDPPacketV1:
	def __init__(self, client, type=None, flags=None, packet_id=None, data=b""):
		self.client = client
		self.type = type
		self.flags = flags
		self.packet_id = packet_id
		self.data = data

	def encode(self):
		self.flags |= FLAG_80
		option = self.encode_option()
		header = self.encode_header(len(option))
		checksum = self.checksum(header, option)
		return b"\xEA\xD0" + header + checksum + option + self.data
		
	def decode(self, data):
		if len(data) >= 2 + 12 + 16: #Magic, header, checksum
			if data[:2] != b"\xEA\xD0": logger.error("Received packet (V1) with invalid magic number")

			header = data[2 : 14]
			option_len, data_len = self.decode_header(header)
			total_size = 2 + 12 + option_len + 16 + data_len
			if len(data) >= total_size:
				option = data[30 : 30 + option_len]
				self.decode_option(option)
				self.data = data[30 + option_len : 30 + option_len + data_len]
				return total_size
		return 0
		
	def encode_option(self):
		if self.type in [PACKET_SYN, PACKET_CONNECT]:
			data = b"\x00\x04"
			data += struct.pack("I", SUPPORT_ALL)
			data += b"\x01\x10"
			if self.type == PACKET_CONNECT:
				data += self.client.server_signature
				data += b"\x03\x02"
				data += struct.pack("H", random.randint(0, 0xFFFF))
			else:
				data += b"\x00" * 0x10
			data += b"\x04\x01\x00"
			return data
		elif self.type == PACKET_DATA:
			return bytes([self.type, 1, 0])
		return b""
			
	def decode_option(self, data):
		if self.type == PACKET_SYN:
			self.client.connection_signature = data[8 : 24]
			
	def encode_header(self, option_len):
		data = b"\x01" #PRUDP version
		data += struct.pack("B", option_len)
		data += struct.pack("H", len(self.data))
		data += struct.pack("BB", PORT_CLIENT, PORT_SERVER)
		data += struct.pack("H", self.type | self.flags)
		data += struct.pack("B", self.client.session_id)
		data += struct.pack("B", 0) #Chunk id
		data += struct.pack("H", self.packet_id)
		return data
		
	def decode_header(self, data):
		if data[0] != 1: #PRUDP Version
			logger.error("Received packet (V1) with invalid version number")

		option_len = data[1]
		data_len = struct.unpack_from("H", data, 2)[0]
		
		if data[4] != PORT_SERVER: logger.error("Received packet (V1) with invalid source port")
		if data[5] != PORT_CLIENT: logger.error("Received packet (V1) with invalid dest port")
		
		type_flags = struct.unpack_from("H", data, 6)[0]
		self.type = type_flags & 0xF
		self.flags = type_flags & 0xFFF0
		self.packet_id = struct.unpack_from("H", data, 10)[0]
		return option_len, data_len
		
	def checksum(self, header, option):
		mac = hmac.HMAC(self.client.signature_key)
		mac.update(header[4:])
		mac.update(self.client.secure_key)
		mac.update(struct.pack("I", self.client.signature_sum))
		mac.update(self.client.connection_signature)
		mac.update(option)
		mac.update(self.data)
		return mac.digest()


class PRUDP:

	DISCONNECTED = 0
	CONNECTING = 1
	CONNECTED = 2
	DISCONNECTING = 3
	
	connection_id = random.randint(0, 0xFF)

	def __init__(self, key, secure_key=b"", resend_timeout=2, ping_timeout=5, silence_timeout=8):
		logger.debug("New client - key=%s", key)
		self.s = Socket(Socket.UDP)
		self.encrypt = RC4(b"CD&ML", False)
		self.decrypt = RC4(b"CD&ML", False)
		
		self.signature_key = hashlib.md5(key).digest()
		self.signature_sum = sum(key)
		self.secure_key = secure_key
		self.resend_timeout = resend_timeout
		self.ping_timeout = ping_timeout
		self.silence_timeout = silence_timeout
		
		self.reset_connection()
		
	def set_secure_key(self, key):
		self.encrypt.set_key(key)
		self.decrypt.set_key(key)
		self.secure_key = key
		
	def reset_connection(self):
		self.state = PRUDP.DISCONNECTED
		self.ack_timers = {}
		self.packet_id = 0
		self.connection_signature = b"\x00" * 0x10
		self.buffer = b""
		self.session_id = 0
		self.fragment_buffer = b""
		
		self.ping_timer = 0
		self.ping_sent = False
		
		self.server_signature = None
		self.connection_data = None
		
		self.encrypt.reset()
		self.decrypt.reset()
		
	def calc_server_signature(self, host, port):
		data = struct.pack("IH", util.ip_to_hex(host), port)
		return hmac.HMAC(self.signature_key, data).digest()
		
	def connect(self, host, port, data=b"", blocking=True):
		self.s.connect(host, port)
		self.server_signature = self.calc_server_signature(host, port)
		self.connection_data = data
		self.state = self.CONNECTING
		
		Scheduler.instance.add(self.update)
		
		logger.debug("Connecting to %s:%i", host, port)
		
		self.send_syn()
		
		if blocking:
			while self.state == self.CONNECTING:
				time.sleep(0.05)
			if self.state != self.CONNECTED:
				raise PRUDPError("PRUDP couldn't connect to %s:%i" %(host, port))
		
	def send(self, data):
		self.send_data(data)
		
	def close(self, blocking=True):
		self.state = self.DISCONNECTING
		self.send_disconnect()
		
		if blocking:
			while self.state == self.DISCONNECTING:
				time.sleep(0.05)
		
	def send_syn(self):
		logger.debug("Sending SYN [%i:%i]", self.session_id, self.packet_id)
		packet = PRUDPPacketV1(
			self,
			PACKET_SYN,
			FLAG_NEED_ACK,
			self.packet_id
		)
		self.packet_id += 1
		self.send_packet(packet)
		
	def send_connect(self):
		self.session_id = PRUDP.connection_id
		PRUDP.connection_id = (PRUDP.connection_id + 1) % 256

		logger.debug("Sending CONNECT [%i:%i]", self.session_id, self.packet_id)
		packet = PRUDPPacketV1(
			self,
			PACKET_CONNECT,
			FLAG_RELIABLE | FLAG_NEED_ACK,
			self.packet_id,
			self.connection_data
		)
		self.packet_id += 1
		self.send_packet(packet)
		
	def send_data(self, data):
		logger.debug("Sending data packet with %i bytes of data [%i:%i]", len(data), self.session_id, self.packet_id)
		packet = PRUDPPacketV1(
			self,
			PACKET_DATA,
			FLAG_RELIABLE | FLAG_NEED_ACK,
			self.packet_id,
			self.encrypt.crypt(data)
		)
		self.packet_id += 1
		self.send_packet(packet)
		
	def send_disconnect(self):
		logger.debug("Sending DISCONNECT [%i:%i]", self.session_id, self.packet_id)
		packet = PRUDPPacketV1(
			self,
			PACKET_DISCONNECT,
			FLAG_RELIABLE | FLAG_NEED_ACK,
			self.packet_id
		)
		self.send_packet(packet)
		
	def send_ping(self):
		logger.debug("Sending PING [%i:%i]", self.session_id, self.packet_id)
		packet = PRUDPPacketV1(
			self,
			PACKET_PING,
			FLAG_RELIABLE | FLAG_NEED_ACK,
			self.packet_id
		)
		self.packet_id += 1
		self.send_packet(packet)
		
	def send_ack(self, packet):
		logger.debug("Sending ACK")
		packet = PRUDPPacketV1(
			self,
			packet.type,
			FLAG_ACK,
			packet.packet_id,
			packet.data
		)
		self.send_packet(packet)
		
	def send_ack2(self, packet):
		logger.debug("Sending data ACK")
		packet = PRUDPPacketV1(
			self,
			PACKET_DATA,
			FLAG_ACK2,
			self.packet_id,
			b"\x00\x00" + struct.pack("H", packet.packet_id)
		)
		self.packet_id += 1
		self.send_packet(packet)
		
	def send_packet(self, packet):
		self.s.send(packet.encode())
		if packet.flags & FLAG_NEED_ACK:
			self.ack_timers[packet.packet_id] = [packet, 0]
			
	def handle(self, packet):
		if packet.flags & FLAG_ACK:
			logger.debug("Packet acknowledged: [%i:%i]", self.session_id, packet.packet_id)
			self.ack_timers.pop(packet.packet_id)
		if packet.flags & FLAG_NEED_ACK:
			if packet.type == PACKET_DATA:
				#self.send_ack2(packet)
				self.send_ack(packet)
			else:
				self.send_ack(packet)
		
		if packet.flags & FLAG_ACK2:
			packet_id = struct.unpack_from("H", packet.data, 2 + packet.data[1] * 2)[0]
			logger.debug("Data acknowledged: [%i:%i]", self.session_id, packet_id)
			self.ack_timers.pop(packet_id)

		elif packet.type == PACKET_SYN:
			logger.debug("Received SYN packet")
			self.send_connect()
		elif packet.type == PACKET_CONNECT:
			logger.debug("Received CONNECT packet")
			self.state = self.CONNECTED
			self.on_connect(packet.data)
		elif packet.type == PACKET_DISCONNECT:
			logger.debug("Received DISCONNECT packet")
			Scheduler.instance.remove(self.update)
			self.reset_connection()
			self.on_disconnect()
		elif packet.type == PACKET_PING:
			logger.debug("Received PING packet")
		elif packet.type == PACKET_DATA:
			logger.debug("Received DATA packet with %i bytes", len(packet.data))
			self.fragment_buffer += self.decrypt.crypt(packet.data)
			if len(packet.data) != 1300:
				self.on_data(self.fragment_buffer)
				self.fragment_buffer = b""
		
	def update(self, tick):
		for timer in self.ack_timers.values():
			timer[1] += tick
			if timer[1] >= self.resend_timeout:
				logger.info("Packet timed out [%i:%i]", self.session_id, timer[0].packet_id)
				self.send_packet(timer[0])
				
		self.ping_timer += tick
		if self.ping_timer >= self.ping_timeout and not self.ping_sent:
			self.send_ping()
			self.ping_sent = True
		if self.ping_timer >= self.silence_timeout:
			self.reset_connection()
			self.on_disconnect()
			return
				
		data = self.s.recv()
		if data:
			self.buffer += data
		
		while self.buffer:
			packet = PRUDPPacketV1(self)
			size = packet.decode(self.buffer)
			if size:
				self.buffer = self.buffer[size:]
				self.ping_timer = 0
				self.ping_sent = False
				self.handle(packet)
			else:
				break
			
	def on_connect(self, data): pass
	def on_data(self, data): pass
	def on_disconnect(self): pass

