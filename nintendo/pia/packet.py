
from nintendo.pia.streams import StreamIn, StreamOut
from nintendo.common.socket import UDPSocket
from nintendo.common import scheduler, util
from Crypto.Cipher import AES
import random
import errno
import hmac
import time

import logging
logger = logging.getLogger(__name__)


class SignatureMethod:
	NONE = 0
	HMAC = 1
	
class EncryptionMethod:
	AES_ECB = 0
	AES_GCM = 1


class PIAPacket:
	def __init__(self, session):
		self.settings = session.settings
		self.session = session
		
		self.connection_id = 0
		self.sequence_id = 0
		self.session_timer = 0
		self.rtt_timer = 0
		self.payload = b""
		self.nonce = 0
		
		self.signature = None
		self.address = None
		
	def decrypt(self, data):
		key = self.session.get_session_key()
		
		method = self.settings.get("pia.encryption_method")
		if method == EncryptionMethod.AES_ECB:
			aes = AES.new(key, AES.MODE_ECB)
			return aes.decrypt(data)
		else:
			nonce = self.session.generate_nonce(self)
			aes = AES.new(key, AES.MODE_GCM, nonce=nonce)
			try:
				data = aes.decrypt_and_verify(data, self.signature)
			except ValueError:
				logger.warning("Received incorrect AES-GCM tag")
				return None
			return data
		
	def encrypt(self, data):
		key = self.session.get_session_key()
		
		method = self.settings.get("pia.encryption_method")
		if method == EncryptionMethod.AES_ECB:
			aes = AES.new(key, AES.MODE_ECB)
			return aes.encrypt(data)
		else:
			if len(data) % 16:
				data += b"\xFF" * (16 - len(data) % 16)
			nonce = self.session.generate_nonce(self)
			aes = AES.new(key, AES.MODE_GCM, nonce=nonce)
			data, self.signature = aes.encrypt_and_digest(data)
			return data
			
	def calc_signature(self, data):
		key = self.session.get_session_key()
		
		method = self.settings.get("pia.signature_method")
		if method == SignatureMethod.HMAC:
			return hmac.new(key, data, hashlib.md5).digest()
		return b""
		
	def check_signature(self, data):
		key = self.session.get_session_key()
		
		method = self.settings.get("pia.signature_method")
		if method == SignatureMethod.HMAC:
			mac = self.calc_signature(data[:-16], key)
			if mac != data[-16:]:
				logger.error("Packet has incorrect HMAC")
				return None
			return data[:-16]
		return data
		
	def decode(self, data):
		data = self.check_signature(data)
		if data is None:
			logger.error("Invalid packet signature")
			return False
			
		stream = StreamIn(data, self.settings)
		if stream.u32() != 0x32AB9864:
			logger.error("Invalid packet identifier")
			return False
			
		if self.settings.get("pia.header_version") > 0:
			byte = stream.u8()
			encrypted = byte >> 7
			version = byte & 0x7F
			
			if version != self.settings.get("pia.header_version"):
				logger.error("Unexpected packet version: %i", version)
				return False
		else:
			encryption = stream.u8()
			if encryption not in [1, 2]:
				logger.error("Invalid encryption mode")
				return False
			
			encrypted = encryption == 2
		
		self.connection_id = stream.u8()
		self.sequence_id = stream.u16()
		
		if self.settings.get("pia.header_version") == 0:
			self.session_timer = stream.u16()
			self.rtt_timer = stream.u16()
		
		if self.settings.get("pia.encryption_method") == EncryptionMethod.AES_GCM:
			self.nonce = stream.u64()
			self.signature = stream.read(16)
			
		payload = stream.read(stream.available())
		if encrypted:
			payload = self.decrypt(payload)
			if payload is None:
				return False
		
		self.payload = payload
		return True
	
	def encode(self):
		payload = self.encrypt(self.payload)
	
		stream = StreamOut(self.settings)
		stream.u32(0x32AB9864)
		
		header_version = self.settings.get("pia.header_version")
		crypto_enabled = self.settings.get("pia.crypto_enabled")
		if header_version > 0:
			stream.u8((crypto_enabled << 7) | header_version)
		else:
			stream.u8(crypto_enabled + 1)
			
		stream.u8(self.connection_id)
		stream.u16(self.sequence_id)
		
		if header_version == 0:
			stream.u16(self.session_timer)
			stream.u16(self.rtt_timer)
			
		if self.settings.get("pia.encryption_method") == EncryptionMethod.AES_GCM:
			stream.u64(self.nonce)
			stream.write(self.signature)
			
		stream.write(payload)
		stream.write(self.calc_signature(stream.get()))
		
		return stream.get()
		
		
class PacketTransport:
	def __init__(self, session):
		self.session = session
		self.settings = session.settings
		self.stations = session.get_station_table()
		
		self.socket = UDPSocket()
		
		self.packets = []
		
		self.event = None
		
		self.nonce = random.randint(0, 0xFFFFFFFFFFFFFFFF)
		
	def local_address(self): return self.socket.local_address()
	
	def get_session_time(self):
		return int((time.monotonic() - self.session_start) * 1000)
		
	def prepare(self):
		self.session_start = time.monotonic()
		
		for port in range(0xC000, 0xC004):
			try:
				self.socket.bind("", port)
				break
			except OSError as e:
				if e.errno != errno.EADDRINUSE:
					raise e
		else:
			raise RuntimeError("Couldn't find a free port to bind UDP socket")
		
		self.event = scheduler.add_socket(self.handle_recv, self.socket)
		
	def cleanup(self):
		scheduler.remove(self.event)
		self.socket.close()
		
	def send(self, station, packet):
		if self.settings.get("pia.header_version") == 0:
			session_time = self.get_session_time()
			packet.session_timer = session_time & 0xFFFF
			if station.rtt_timer is not None:
				time_diff = session_timer - station.base_timer
				packet.rtt_timer = (station.rtt_timer + time_diff) & 0xFFFF
			else:
				packet.rtt_timer = 0
		
		packet.connection_id = station.connection_id_out
		packet.sequence_id = station.next_sequence_id()
		
		self.nonce = (self.nonce + 1) & 0xFFFFFFFFFFFFFFFF
		packet.nonce = self.nonce
		
		packet.address = self.local_address()
		
		self.socket.send(packet.encode(), station.address)
		
	def broadcast(self, port, packet):
		self.nonce = (self.nonce + 1) & 0xFFFFFFFFFFFFFFFF
		packet.nonce = self.nonce
		
		packet.address = self.local_address()
		
		addr = (util.broadcast_address(), port)
		self.socket.send(packet.encode(), addr)
		
	def handle_recv(self, pair):
		data, addr = pair
		if addr == self.local_address():
			logger.debug("Received packet from self")
			return
		
		packet = PIAPacket(self.session)
		packet.address = addr
		if not packet.decode(data):
			return
		
		station = self.stations.find_by_address(addr, True)
		
		if self.settings.get("pia.header_version") == 0:
			station.rtt_timer = packet.session_timer
			station.base_timer = self.get_session_time()
		
		if packet.connection_id != 0:
			if packet.connection_id != station.connection_id_in:
				logger.error(
					"Packet has unexpected connection id: %i != %i",
					packet.connection_id, station.connection_id_in
				)
				return
		
		if packet.sequence_id != 0:
			if (packet.sequence_id - station.sequence_id_in) & 0xFFFF > 16:
				logger.warning("Packet has unexpected sequence id: %i", packet.sequence_id)
				return
			
			station.sequence_id_in = (packet.sequence_id + 1) & 0xFFFF
			if station.sequence_id_in == 0:
				station.sequence_id_in += 1
		
		self.packets.append((station, packet))
		
	def recv(self):
		if self.packets:
			return self.packets.pop(0)
