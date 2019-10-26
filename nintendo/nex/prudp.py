
from nintendo.common import crypto, socket, websocket, scheduler, signal
from nintendo.nex import kerberos, streams

import hashlib
import hmac
import struct
import random
import secrets
import zlib
import time

import logging
logger = logging.getLogger(__name__)


TYPE_SYN = 0
TYPE_CONNECT = 1
TYPE_DATA = 2
TYPE_DISCONNECT = 3
TYPE_PING = 4

FLAG_ACK = 1
FLAG_RELIABLE = 2
FLAG_NEED_ACK = 4
FLAG_HAS_SIZE = 8
FLAG_MULTI_ACK = 0x200

TYPE_NAMES = ["TYPE_SYN", "TYPE_CONNECT", "TYPE_DATA", "TYPE_DISCONNECT", "TYPE_PING"]

FLAG_NAMES = {
	FLAG_ACK: "ACK",
	FLAG_NEED_ACK: "NEED_ACK",
	FLAG_MULTI_ACK: "MULTI_ACK",
	FLAG_RELIABLE: "RELIABLE",
	FLAG_HAS_SIZE: "HAS_SIZE"
}

FLAG_LIST = [FLAG_ACK, FLAG_NEED_ACK, FLAG_MULTI_ACK, FLAG_RELIABLE, FLAG_HAS_SIZE]

OPTION_SUPPORT = 0
OPTION_CONNECTION_SIG = 1
OPTION_FRAGMENT_ID = 2
OPTION_UNRELIABLE_SEQ_ID = 3
OPTION_MAX_SUBSTREAM_ID = 4
OPTION_CONNECTION_SIG_LITE = 128

OPTIONS = {
	OPTION_SUPPORT: (4, "OPTION_SUPPORT", "I"),
	OPTION_CONNECTION_SIG: (16, "OPTION_CONNECTION_SIG", None),
	OPTION_FRAGMENT_ID: (1, "OPTION_FRAGMENT_ID", "B"),
	OPTION_UNRELIABLE_SEQ_ID: (2, "OPTION_UNRELIABLE_SEQ_ID", "H"),
	OPTION_MAX_SUBSTREAM_ID: (1, "OPTION_MAX_SUBSTREAM_ID", "B"),
	OPTION_CONNECTION_SIG_LITE: (16, "OPTION_CONNECTION_SIG_LITE", None)
}

STATE_READY = 0
STATE_ACCEPTING = 1
STATE_CONNECTING = 2
STATE_CONNECTED = 3
STATE_DISCONNECTING = 4
STATE_DISCONNECTED = 5


def decode_options(data):
	pos = 0
	options = {}
	while pos < len(data):
		if len(data) - pos < 2:
			logger.error("(Opt) Only one byte left in option data")
			return

		type = data[pos]
		length = data[pos + 1]
		pos += 2

		if len(data) - pos < length:
			logger.error("(Opt) Option length is greater than data size")
			return

		if type not in OPTIONS:
			logger.error("(Opt) Unrecognized option type %i" %type)
			return
		
		expected_length, name, format = OPTIONS[type]
		if length != expected_length:
			logger.error("(Opt) Invalid option length in %s" %name)
			return
			
		value = data[pos : pos + length]
		if format is not None:
			value = struct.unpack("<" + format, value)[0]
		
		options[type] = value
		
		pos += length
	return options
	
	
class PRUDPPacket:
	def __init__(self, type=None, flags=None):
		self.type = type
		self.flags = flags
		
		self.source_port = None
		self.source_type = None
		self.dest_port = None
		self.dest_type = None
		self.session_id = None
		self.packet_id = 0
		self.fragment_id = 0
		self.stream_id = 0
		self.connection_signature = None
		
		self.payload = b""
		
	def __repr__(self):
		flags = []
		for flag in FLAG_LIST:
			if self.flags & flag:
				flags.append(FLAG_NAMES[flag])
		flags = ",".join(flags)
		
		return "<PRUDPPacket type=%s flags=%s seq=%s frag=%s>" %(
			TYPE_NAMES[self.type], flags, self.packet_id, self.fragment_id
		)
	
	
class PRUDPMessageV0:
	def __init__(self, client, settings):
		self.client = client
		self.signature_version = settings.get("prudp_v0.signature_version")
		self.flags_version = settings.get("prudp_v0.flags_version")
		self.checksum_version = settings.get("prudp_v0.checksum_version")
		self.reset()
		
	def reset(self):
		self.buffer = b""
	def signature_size(self): return 4
	
	def checksum_size(self):
		if self.checksum_version == 0:
			return 4
		return 1
		
	def calc_checksum(self, data):
		if self.checksum_version == 0:
			data = data.ljust((len(data) + 3) & ~3, b"\0")
			base = self.client.signature_base & 0xFF
			words = struct.unpack("<%iI" %(len(data) // 4), data)
			return (base + sum(words)) & 0xFFFFFFFF

		else:
			words = struct.unpack_from("<%iI" %(len(data) // 4), data)
			temp = sum(words) & 0xFFFFFFFF
			
			checksum = self.client.signature_base
			checksum += sum(data[len(data) & ~3:])
			checksum += sum(struct.pack("<I", temp))
			return checksum & 0xFF
		
	def calc_data_signature(self, packet):
		data = packet.payload
		if self.signature_version == 0:
			session_key = b""
			if packet.type not in [TYPE_SYN, TYPE_CONNECT]:
				session_key = self.client.session_key
			data = session_key + struct.pack("<HB", packet.packet_id, packet.fragment_id) + data

		if data:
			return hmac.new(self.client.signature_key, data, digestmod=hashlib.md5).digest()[:4]
		return struct.pack("<I", 0x12345678)
		
	def calc_packet_signature(self, packet, signature):
		if packet.type == TYPE_DATA: return self.calc_data_signature(packet)
		if packet.type == TYPE_DISCONNECT and self.signature_version == 0:
			return self.calc_data_signature(packet)
		return signature if signature else bytes(4)
		
	def header_format(self):
		if self.flags_version == 0:
			return "<BBBB4sH"
		return "<BBHB4sH"
		
	def encode(self, packet):
		if packet.type == TYPE_DATA and not packet.flags & FLAG_ACK:
			packet.flags |= FLAG_HAS_SIZE
		
		if self.flags_version == 0:
			type_field = packet.type | (packet.flags << 3)
		else:
			type_field = packet.type | (packet.flags << 4)
		
		header = struct.pack(self.header_format(),
			packet.source_port | (packet.source_type << 4),
			packet.dest_port | (packet.dest_type << 4),
			packet.type | (packet.flags << 4),
			packet.session_id,
			self.calc_packet_signature(packet, self.client.remote_signature),
			packet.packet_id
		)
		
		options = self.encode_options(packet)
		data = header + options + packet.payload
		if self.checksum_size() == 1:
			data += struct.pack("<B", self.calc_checksum(data))
		elif self.checksum_size() == 4:
			data += struct.pack("<I", self.calc_checksum(data))
		return data
		
	def encode_options(self, packet):
		options = b""
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			options += packet.connection_signature
		if packet.type == TYPE_DATA:
			options += struct.pack("<B", packet.fragment_id)
		if packet.flags & FLAG_HAS_SIZE:
			options += struct.pack("<H", len(packet.payload))
		return options
		
	def decode(self, data):
		self.buffer += data
	
		packets = []
		while self.buffer:
			if len(self.buffer) < 12: return packets
			
			#Extract packet header
			source, dest, type_flags, session_id, signature, packet_id = \
				struct.unpack_from(self.header_format(), self.buffer)
				
			packet = PRUDPPacket()
			packet.source_type = source >> 4
			packet.source_port = source & 0xF
			packet.dest_type = dest >> 4
			packet.dest_port = dest & 0xF
			packet.session_id = session_id
			packet.packet_id = packet_id

			if self.flags_version == 0:
				packet.flags = type_flags >> 3
				packet.type = type_flags & 7
			else:
				packet.flags = type_flags >> 4
				packet.type = type_flags & 0xF

			offset = 11
			
			#Extract connection signature
			if packet.type in [TYPE_SYN, TYPE_CONNECT]:
				if len(self.buffer) < offset + 4: return packets
				packet.connection_signature = self.buffer[offset : offset + 4]
				offset += 4

			#Extract fragment id
			if packet.type == TYPE_DATA:
				if len(self.buffer) < offset + 1: return packets
				packet.fragment_id = self.buffer[offset]
				offset += 1

			#Extract payload size
			if packet.flags & FLAG_HAS_SIZE:
				if len(self.buffer) < offset + 2: return packets
				payload_size = struct.unpack_from("<H", self.buffer, offset)[0]
				offset += 2
			else:
				payload_size = len(self.buffer) - offset - self.checksum_size()

			if len(self.buffer) < offset + payload_size + self.checksum_size():
				return packets

			#Extract checksum
			if self.checksum_size() == 1:
				checksum = self.buffer[offset + payload_size]
			elif self.checksum_size() == 4:
				checksum = struct.unpack_from("<I", self.buffer, offset + payload_size)

			#Verify checksum
			expected_checksum = self.calc_checksum(self.buffer[:offset + payload_size])
			if checksum != expected_checksum:
				logger.error("(V0) Invalid checksum (expected %i, got %i)", checksum, expected_checksum)
				self.reset()
				return packets
			
			#Extract payload
			packet.payload = self.buffer[offset : offset + payload_size]
			
			#Verify packet signature
			expected_signature = self.calc_packet_signature(packet, self.client.local_signature)
			if signature != expected_signature:
				logger.error(
					"(V0) Invalid packet signature (expected %s, got %s)",
					signature.hex(), expected_signature.hex()
				)
				self.reset()
				return packets
			
			self.buffer = self.buffer[offset + payload_size + self.checksum_size():]
			packets.append(packet)
		return packets

	
class PRUDPMessageV1:
	def __init__(self, client, settings):
		self.client = client
		self.settings = settings
		self.reset()
		
	def reset(self):
		self.buffer = b""
	def signature_size(self): return 16

	def calc_packet_signature(self, session_key, header, options, signature, payload):
		mac = hmac.new(self.client.signature_key, digestmod=hashlib.md5)
		mac.update(header[4:])
		mac.update(session_key)
		mac.update(struct.pack("<I", self.client.signature_base))
		mac.update(signature)
		mac.update(options)
		mac.update(payload)
		return mac.digest()

	def encode(self, packet):
		packet.flags |= FLAG_HAS_SIZE
		
		session_key = b""
		if packet.type not in [TYPE_SYN, TYPE_CONNECT]:
			session_key = self.client.session_key
		
		options = self.encode_options(packet)
		header = self.encode_header(packet, len(options))
		checksum = self.calc_packet_signature(session_key, header, options, self.client.remote_signature, packet.payload)
		return b"\xEA\xD0" + header + checksum + options + packet.payload
		
	def encode_header(self, packet, option_size):
		return struct.pack("<BBHBBHBBH",
			1, #PRUDP version
			option_size,
			len(packet.payload),
			packet.source_port | (packet.source_type << 4),
			packet.dest_port | (packet.dest_type << 4),
			packet.type | (packet.flags << 4),
			packet.session_id, packet.stream_id, packet.packet_id
		)
		
	def encode_options(self, packet):
		options = b""
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			options += struct.pack("<BBI", OPTION_SUPPORT, 4, self.client.minor_version)
			options += struct.pack("<BB16s", OPTION_CONNECTION_SIG, 16, packet.connection_signature)
			if packet.type == TYPE_CONNECT:
				options += struct.pack("<BBH", OPTION_UNRELIABLE_SEQ_ID, 2, random.randint(0, 0xFFFF))
			options += struct.pack("<BBB", OPTION_MAX_SUBSTREAM_ID, 1, 0)
		elif packet.type == TYPE_DATA:
			options += struct.pack("<BBB", OPTION_FRAGMENT_ID, 1, packet.fragment_id)
		return options
		
	def decode(self, data):
		self.buffer += data

		packets = []
		while self.buffer:
			if len(self.buffer) < 30: return packets
			if self.buffer[:2] != b"\xEA\xD0":
				logger.error("(V1) Invalid magic number")
				self.reset()
				return packets
		
			packet = PRUDPPacket()

			header = self.buffer[2 : 14]
			signature = self.buffer[14 : 30]
			
			version, option_size, payload_size, source, dest, type_flags, session_id, \
				packet.stream_id, packet_id = struct.unpack("<BBHBBHBBH", header)

			if version != 1:
				logger.error("(V1) Version check failed")
				self.reset()
				return packets
			if len(self.buffer) < 30 + option_size + payload_size:
				return packets
				
			packet.source_type = source >> 4
			packet.source_port = source & 0xF
			packet.dest_type = dest >> 4
			packet.dest_port = dest & 0xF
			packet.flags = type_flags >> 4
			packet.type = type_flags & 0xF
			packet.session_id = session_id
			packet.packet_id = packet_id
			
			option_data = self.buffer[30 : 30 + option_size:]
			options = decode_options(option_data)
			if options is None:
				self.reset()
				return packets
			
			if packet.type in [TYPE_SYN, TYPE_CONNECT]:
				if OPTION_CONNECTION_SIG not in options:
					logger.error("(V1) Expected connection signature in SYN/CONNECT packet")
					self.reset()
					return packets
				packet.connection_signature = options[OPTION_CONNECTION_SIG]
			elif packet.type == TYPE_DATA:
				if OPTION_FRAGMENT_ID not in options:
					logger.error("(V1) Expected fragment id in DATA packet")
					self.reset()
					return packets
				packet.fragment_id = options[OPTION_FRAGMENT_ID]
			
			packet.payload = self.buffer[30 + option_size : 30 + option_size + payload_size]
			
			expected_signature = self.calc_packet_signature(
				self.client.session_key, header, option_data, self.client.local_signature, packet.payload
			)
			if expected_signature != signature:
				logger.error("(V1) Invalid packet signature")
				self.reset()
				return packets
			
			self.buffer = self.buffer[30 + option_size + payload_size:]
			packets.append(packet)
		return packets

		
class PRUDPLiteMessage:
	def __init__(self, client, settings):
		self.client = client
		self.settings = settings
		self.reset()
		
	def reset(self):
		self.buffer = b""
	def signature_size(self): return 16
		
	def encode(self, packet):
		options = self.encode_options(packet)
		header = self.encode_header(packet, len(options))
		return header + options + packet.payload
		
	def encode_header(self, packet, option_size):
		return struct.pack("<BBHBBBBHH",
			0x80, option_size,
			len(packet.payload),
			(packet.source_type << 4) | packet.dest_type,
			packet.source_port,
			packet.dest_port,
			packet.fragment_id,
			packet.type | (packet.flags << 4),
			packet.packet_id
		)
		
	def encode_options(self, packet):
		options = b""
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			options += struct.pack("<BBI", OPTION_SUPPORT, 4, self.client.minor_version)
		if packet.type == TYPE_SYN and packet.flags & FLAG_ACK:
			options += struct.pack("<BB16s", OPTION_CONNECTION_SIG, 16, packet.connection_signature)
		if packet.type == TYPE_CONNECT and not packet.flags & FLAG_ACK:
			options += struct.pack("<BB16s", OPTION_CONNECTION_SIG_LITE, 16, packet.connection_signature)
		return options
		
	def decode(self, data):
		self.buffer += data

		packets = []
		while self.buffer:
			if len(self.buffer) < 12: return packets
		
			packet = PRUDPPacket()
			
			magic, option_size, payload_size, stream_types, source_port, dest_port, \
				fragment_id, type_flags, packet_id = struct.unpack_from("<BBHBBBBHH", self.buffer)
			
			if magic != 0x80:
				logger.error("(Lite) Invalid magic number")
				self.reset()
				return packets
			if len(self.buffer) < 12 + option_size + payload_size:
				return packets
				
			packet.source_type = stream_types >> 4
			packet.dest_type = stream_types & 0xF
			packet.source_port = source_port
			packet.dest_port = dest_port
			packet.fragment_id = fragment_id
			packet.flags = type_flags >> 4
			packet.type = type_flags & 0xF
			packet.packet_id = packet_id
			packet.session_id = 0
			
			option_data = self.buffer[12 : 12 + option_size:]
			options = decode_options(option_data)
			if options is None:
				self.reset()
				return packets
			
			if packet.type == TYPE_SYN and packet.flags & FLAG_ACK:
				if OPTION_CONNECTION_SIG not in options:
					logger.error("(Lite) Expected connection signature in SYN/ACK packet")
					self.reset()
					return packets
				packet.connection_signature = options[OPTION_CONNECTION_SIG]
			
			packet.payload = self.buffer[12 + option_size : 12 + option_size + payload_size]
			self.buffer = self.buffer[12 + option_size + payload_size:]
			packets.append(packet)
		return packets

		
class RC4Encryption:
	def __init__(self, key):
		self.rc4enc = crypto.RC4(key)
		self.rc4dec = crypto.RC4(key)
		
	def set_key(self, key):
		self.rc4enc.set_key(key)
		self.rc4dec.set_key(key)
		
	def encrypt(self, data): return self.rc4enc.crypt(data)
	def decrypt(self, data): return self.rc4dec.crypt(data)
	

class DummyEncryption:
	def set_key(self, key): pass
	def encrypt(self, data): return data
	def decrypt(self, data): return data
	
	
class ZlibCompression:
	def compress(self, data):
		compressed = zlib.compress(data)
		ratio = int(len(data) / len(compressed) + 1)
		return bytes([ratio]) + compressed
		
	def decompress(self, data):
		if data[0] == 0:
			return data[1:]
		
		decompressed = zlib.decompress(data[1:])
		ratio = int(len(decompressed) / (len(data) - 1) + 1)
		if ratio != data[0]:
			logger.warning(
				"Unexpected compression ratio (expected %i, got %i)",
				ratio, data[0]
			)
		return decompressed
		
		
class DummyCompression:
	def compress(self, data): return data
	def decompress(self, data): return data
	
	
class SequenceCounter:
	def __init__(self):
		self.current = 0
		
	def next(self):
		self.current = (self.current + 1) & 0xFFFF
		return self.current
		
		
class SequenceMgr:
	def __init__(self, settings):	
		substreams = settings.get("prudp.substreams")
		
		self.counters = [SequenceCounter() for i in range(substreams)]
		self.unreliable_counter = SequenceCounter()
		self.ping_counter = SequenceCounter()
		
	def assign(self, packet):
		if packet.flags & FLAG_RELIABLE:
			return self.counters[packet.stream_id].next()
		if packet.type == TYPE_DATA:
			return self.unreliable_counter.next()
		if packet.type == TYPE_PING:
			return self.ping_counter.next()
		return 0
		
		
class PacketEncoder:
	
	DEFAULT_KEY = b"CD&ML"
	
	def __init__(self, settings):
		substreams = settings.get("prudp.substreams")
		
		self.reliable_encryption = [self.create_encryption(settings) for i in range(substreams)]
		self.unreliable_encryption = self.create_encryption(settings)
		
		self.unreliable_key = bytes(0x20)
		
		if settings.get("prudp.compression") == 0:
			self.compression = DummyCompression()
		else:
			self.compression = ZlibCompression()
			
	def create_encryption(self, settings):
		if settings.get("prudp.transport") == settings.TRANSPORT_UDP:
			return RC4Encryption(self.DEFAULT_KEY)
		return DummyEncryption()
		
	def encode(self, packet):
		data = packet.payload
		if packet.type == TYPE_DATA and data:
			data = self.compression.compress(data)
			
			if packet.flags & FLAG_RELIABLE:
				data = self.reliable_encryption[packet.stream_id].encrypt(data)
			else:
				key = self.make_unreliable_key(packet)
				self.unreliable_encryption.set_key(key)
				
				data = self.unreliable_encryption.encrypt(data)
		return data
			
	def decode(self, packet):
		data = packet.payload
		if packet.type == TYPE_DATA and data:
			if packet.flags & FLAG_RELIABLE:
				data = self.reliable_encryption[packet.stream_id].decrypt(data)
			else:
				key = self.make_unreliable_key(packet)
				self.unreliable_encryption.set_key(key)
				
				data = self.unreliable_encryption.decrypt(data)
		return data
			
	def make_unreliable_key(self, packet):
		key = list(self.unreliable_key)
		key[0] = (key[0] + packet.packet_id) & 0xFF
		key[1] = (key[1] + (packet.packet_id >> 8)) & 0xFF
		key[31] = (key[31] + packet.session_id) & 0xFF
		return bytes(key)
	
	def modify_key(self, key):
		chars = list(key)
		
		add = len(chars) // 2 + 1
		for i in range(len(chars) // 2):
			chars[i] = (chars[i] + add - i) & 0xFF
		
		return bytes(chars)
		
	def combine_keys(self, key1, key2):
		return hashlib.md5(key1 + key2).digest()
		
	def init_unreliable_key(self, key):
		part1 = self.combine_keys(key, bytes.fromhex("18d8233437e4e3fe"))
		part2 = self.combine_keys(key, bytes.fromhex("233e600123cdab80"))
		return part1 + part2
		
	def set_key(self, key):
		self.reliable_encryption[0].set_key(key)
		
		temp_key = key
		for encryption in self.reliable_encryption[1:]:
			temp_key = self.modify_key(temp_key)
			encryption.set_key(temp_key)
		
		self.unreliable_key = self.init_unreliable_key(key)
		
		
class SlidingWindow:
	def __init__(self):
		self.next = 1
		self.packets = {}
	
	def update(self, packet):
		packets = []
		if packet.packet_id < self.next or packet.packet_id in self.packets:
			logger.debug("Received duplicate packet: %s", packet)
		else:
			self.packets[packet.packet_id] = packet
			while self.next in self.packets:
				packet = self.packets.pop(self.next)
				packets.append(packet)
				self.next = (self.next + 1) & 0xFFFF
		return packets
		
	
class PRUDPStream:
	def __init__(self, client, settings, sock=None):
		self.settings = settings
		
		self.transport_type = settings.get("prudp.transport")
		self.resend_timeout = settings.get("prudp.resend_timeout")
		self.resend_limit = settings.get("prudp.resend_limit")
		self.substreams = settings.get("prudp.substreams")
		
		self.failure = signal.Signal()
		
		self.sock = sock
		if not self.sock:
			if self.transport_type == settings.TRANSPORT_UDP:
				self.sock = socket.Socket(socket.TYPE_UDP)
			elif self.transport_type == settings.TRANSPORT_TCP:
				self.sock = socket.Socket(socket.TYPE_TCP)
			else:
				self.sock = websocket.WebSocketClient(True)
				
		if self.transport_type == settings.TRANSPORT_UDP:
			if settings.get("prudp.version") == 0:
				self.packet_encoder = PRUDPMessageV0(client, settings)
			else:
				self.packet_encoder = PRUDPMessageV1(client, settings)
		else:
			self.packet_encoder = PRUDPLiteMessage(client, settings)
		
		self.sequence_mgr = SequenceMgr(settings)
		self.message_encoder = PacketEncoder(settings)
		
		self.ack_events = {}
		self.ack_packets = {}
		self.socket_event = None
		self.packets = []
	
	def local_address(self): return self.sock.local_address()
	def remote_address(self): return self.sock.remote_address()
		
	def signature_size(self):
		return self.packet_encoder.signature_size()
		
	def set_key(self, key):
		self.message_encoder.set_key(key)
		
	def cleanup(self):
		if self.socket_event:
			scheduler.remove(self.socket_event)
		for event, block in self.ack_events.values():
			scheduler.remove(event)
		self.ack_events = {}
		
	def connect(self, host, port):
		if not self.sock.connect(host, port):
			return False
			
		self.socket_event = scheduler.add_socket(self.handle_recv, self.sock)
		return True
		
	def accept(self):
		self.socket_event = scheduler.add_socket(self.handle_recv, self.sock)
		
	def close(self):
		self.sock.close()
		self.cleanup()
		
	def send(self, packet, block=False):
		if not packet.flags & FLAG_ACK:
			packet.packet_id = self.sequence_mgr.assign(packet)
			packet.payload = self.message_encoder.encode(packet)
		
		logger.debug("Sending packet: %s", packet)
		self.sock.send(self.packet_encoder.encode(packet))
		
		if packet.flags & FLAG_RELIABLE or packet.type == TYPE_SYN:
			if packet.flags & FLAG_NEED_ACK:
				key = (packet.type, packet.stream_id, packet.packet_id)
				event = scheduler.add_timeout(self.handle_timeout, self.resend_timeout, param=(packet, 0))
				self.ack_events[key] = (event, block)
				
				if block:
					while key in self.ack_events:
						scheduler.update()
						
					if key in self.ack_packets:
						return self.ack_packets.pop(key)
		
	def recv(self):
		if self.packets:
			return self.packets.pop(0)
		
	def acknowledge(self, key, packet):
		event, block = self.ack_events.pop(key)
		scheduler.remove(event)
		if block:
			self.ack_packets[key] = packet
		
	def handle_recv(self, data):
		if not data:
			logger.warning("Connection was closed unexpectedly")
			self.failure()
			return
			
		packets = self.packet_encoder.decode(data)
		for packet in packets:
			logger.debug("Packet received: %s", packet)
			
			if packet.flags & FLAG_ACK:
				key = (packet.type, packet.stream_id, packet.packet_id)
				if key in self.ack_events:
					self.acknowledge(key, packet)
				else:
					logger.debug("Received unexpected ack packet")
			
			elif packet.flags & FLAG_MULTI_ACK:
				self.handle_aggregate_ack(packet)
						
			else:
				if packet.stream_id < self.substreams:
					
					packet.payload = self.message_encoder.decode(packet)
					self.packets.append(packet)
				else:
					logger.error("Received packet with invalid substream id: %i", packet.stream_id)
					
	def verify_aggregate_ack(self, packet):
		if len(packet.payload) % 2:
			logger.error("Aggregate ack payload size must be a multiple of 2")
			return False

		if packet.stream_id not in [0, 1]:
			logger.error("Aggregate ack packet has invalid stream id: %i", packet.stream_id)
			return False
			
		if packet.stream_id == 1: #New version
			if len(packet.payload) < 4:
				logger.error("Aggregate ack payload is too small")
				return False
			if len(packet.payload) != 4 + packet.payload[1] * 2:
				logger.error("Aggregate ack payload has incorrect size")
				return False
		return True
					
	def handle_aggregate_ack(self, packet):
		if self.verify_aggregate_ack(packet):
			if packet.stream_id == 0:
				stream_id = 0
				base_id = packet.packet_id
				extra_ids = struct.unpack("<%iH" %(len(packet.payload) // 2), packet.payload)
			else:
				stream_id = packet.payload[0]
				base_id = struct.unpack_from("<H", packet.payload, 2)[0]
				extra_ids = struct.unpack_from("<%iH" %packet.payload[1], packet.payload, 4)
			
			for key in list(self.ack_events):
				if key[0] == TYPE_DATA and key[1] == stream_id and key[2] <= base_id:
					self.acknowledge(key, packet)
			
			for packet_id in extra_ids:
				key = (TYPE_DATA, stream_id, packet_id)
				if key in self.ack_events:
					self.acknowledge(key, packet)
	
	def handle_timeout(self, param):
		packet, counter = param
		
		key = (packet.type, packet.stream_id, packet.packet_id)
		
		if counter < self.resend_limit:
			logger.debug("Resending packet: %s" %packet)
			self.sock.send(self.packet_encoder.encode(packet))
			
			event = scheduler.add_timeout(self.handle_timeout, self.resend_timeout, param=(packet, counter+1))
			block = self.ack_events[key][1]
			
			self.ack_events[key] = (event, block)
		
		else:
			logger.error("Packet timed out: %s" %packet)
			del self.ack_events[key]
			self.failure()
		

class PRUDPClient:
	def __init__(self, settings, sock=None):
		self.settings = settings
		
		self.stream_type = settings.get("prudp.stream_type")
		self.transport_type = settings.get("prudp.transport")
		self.minor_version = settings.get("prudp.minor_version")
		self.fragment_size = settings.get("prudp.fragment_size")
		self.ping_timeout = settings.get("prudp.ping_timeout")
		
		self.stream = PRUDPStream(self, settings, sock)
		self.stream.failure.add(self.cleanup)
		
		self.set_access_key(settings.get("nex.access_key"))
		
		substreams = settings.get("prudp.substreams")
		
		self.sliding_windows = [SlidingWindow() for i in range(substreams)]
		self.fragment_buffers = [b""] * substreams
		
		self.packets = []
		for i in range(substreams):
			self.packets.append([])
		self.packets_unreliable = []
		
		self.session_key = b""
		
		self.local_port = 0
		self.remote_port = 0
		
		self.local_session_id = 0
		self.remote_session_id = 0
		
		self.local_signature = b""
		self.remote_signature = b""
		
		self.socket_event = None
		self.ping_event = None
		
		self.connect_response = None
		
		self.state = STATE_READY
		
	def is_connected(self): return self.state == STATE_CONNECTED
	def local_address(self): return self.stream.local_address()
	def remote_address(self): return self.stream.remote_address()
	
	def cleanup(self):
		logger.debug("Cleaning up PRUDP socket")
		self.state = STATE_DISCONNECTED
		self.stop_ping()
		if self.socket_event:
			scheduler.remove(self.socket_event)
		self.stream.cleanup()
		
	def set_access_key(self, access_key):
		key = access_key.encode()
		self.signature_key = hashlib.md5(key).digest()
		self.signature_base = sum(key)
		
	def set_session_key(self, key):
		self.session_key = key
		self.stream.set_key(key)
		
	def connect(self, host, port, sid, payload=b""):
		if self.state != STATE_READY:
			raise RuntimeError("PRUDP socket can only be used once")
		
		self.state = STATE_CONNECTING
		
		logger.info("Connecting to %s:%i:%i", host, port, sid)
		
		if not self.stream.connect(host, port):
			self.cleanup()
			return None
			
		self.local_port = 0xF
		if self.transport_type != self.settings.TRANSPORT_UDP:
			self.local_port = 0x1F
			
		self.remote_port = sid
		
		syn_packet = PRUDPPacket(TYPE_SYN, FLAG_NEED_ACK)
		syn_packet.connection_signature = bytes(self.stream.signature_size())
		syn_ack = self.send_packet(syn_packet, block=True)
		if not syn_ack:
			logger.error("SYN handshake failed")
			self.cleanup()
			return None
			
		self.remote_signature = syn_ack.connection_signature
			
		self.local_session_id = random.randint(0, 0xFF)
		if self.transport_type == self.settings.TRANSPORT_UDP:
			self.local_signature = secrets.token_bytes(self.stream.signature_size())
		else:
			self.local_signature = hmac.new(self.signature_key, self.signature_key + self.remote_signature, digestmod=hashlib.md5).digest()
			
		connect_packet = PRUDPPacket(TYPE_CONNECT, FLAG_RELIABLE | FLAG_NEED_ACK)
		connect_packet.connection_signature = self.local_signature
		connect_packet.payload = payload
		connect_ack = self.send_packet(connect_packet, block=True)
		if not connect_ack:
			logger.error("CONNECT handshake failed")
			self.cleanup()
			return None
			
		logger.debug("Connection established successfully")
		
		self.remote_session_id = connect_ack.session_id
		self.state = STATE_CONNECTED
		
		self.start_ping()
		
		self.socket_event = scheduler.add_socket(self.handle_packet, self.stream)
		return connect_ack.payload
		
	def accept(self, sid):
		if self.state != STATE_READY:
			raise RuntimeError("PRUDP socket can only be used once")
			
		host, port = self.remote_address()
		logger.info("Accepting PRUDP connection from %s:%i", host, port)
		
		self.state = STATE_ACCEPTING
		
		self.local_port = sid
		
		self.stream.accept()
		self.socket_event = scheduler.add_socket(self.handle_packet, self.stream)
		
		while self.state == STATE_ACCEPTING:
			scheduler.update()
			
		if self.state != STATE_CONNECTED:
			return False
			
		logger.debug("PRUDP connection accepted successfully")
		
		self.start_ping()
		return True
		
	def start_ping(self):
		self.ping_event = scheduler.add_timeout(self.handle_ping, self.ping_timeout, True)
		
	def stop_ping(self):
		if self.ping_event:
			scheduler.remove(self.ping_event)
			self.ping_event = None
			
	def handle_ping(self):
		packet = PRUDPPacket(TYPE_PING, FLAG_RELIABLE | FLAG_NEED_ACK)
		self.send_packet(packet)
		
	def close(self):
		logger.info("Closing PRUDP connection")
		self.stop_ping()
		
		if self.state == STATE_CONNECTED:
			self.state = STATE_DISCONNECTING
			
			packet = PRUDPPacket(TYPE_DISCONNECT, FLAG_RELIABLE | FLAG_NEED_ACK)
			self.send_packet(packet, block=True)
		
		self.stream.close()
		self.cleanup()
		
	def handle_packet(self, packet):
		if packet.type == TYPE_SYN:
			if self.state != STATE_ACCEPTING:
				logger.error("Unexpected SYN packet: %s", packet)
			else:
				if not self.local_signature:
					self.remote_port = packet.source_port
					self.local_signature = secrets.token_bytes(self.stream.signature_size())
				syn_ack = PRUDPPacket(TYPE_SYN, FLAG_ACK)
				syn_ack.connection_signature = self.local_signature
				self.send_packet(syn_ack)
		else:	
			if packet.flags & FLAG_RELIABLE:
				for packet in self.sliding_windows[packet.stream_id].update(packet):
					if packet.type == TYPE_CONNECT:
						if self.state != STATE_ACCEPTING:
							logger.error("Unexpected CONNECT packet: %s", packet)
						else:
							try:
								self.remote_signature = packet.connection_signature
								self.connect_response = self.handle_connection_request(packet)
								if self.connect_response is None:
									self.cleanup()
									return
								self.state = STATE_CONNECTED
							except:
								logger.error("An exception occurred while handling a connection request")
								import traceback
								traceback.print_exc()
								self.cleanup()
								return
					elif packet.type == TYPE_DATA:
						self.fragment_buffers[packet.stream_id] += packet.payload
						if packet.fragment_id == 0:
							self.packets[packet.stream_id].append(self.fragment_buffers[packet.stream_id])
							self.fragment_buffers[packet.stream_id] = b""
					elif packet.type == TYPE_DISCONNECT:
						logger.info("Connection closed by other end point")
						self.cleanup()
			else:
				if packet.type == TYPE_DATA:
					self.packets_unreliable.append(packet.payload)
					
			if packet.flags & FLAG_NEED_ACK:
				self.send_ack(packet)
				if packet.type == TYPE_DISCONNECT:
					self.send_ack(packet)
					self.send_ack(packet)
	
	def handle_connection_request(self, packet):
		return b""
		
	def send(self, data, stream_id=0):
		fragment_id = 1
		while data:
			if len(data) <= self.fragment_size:
				fragment_id = 0
			self.send_fragment(data[:self.fragment_size], fragment_id, stream_id)
			data = data[self.fragment_size:]
			fragment_id += 1
			
	def send_fragment(self, data, fragment_id, stream_id):
		packet = PRUDPPacket(TYPE_DATA, FLAG_RELIABLE | FLAG_NEED_ACK)
		packet.fragment_id = fragment_id
		packet.stream_id = stream_id
		packet.payload = data
		self.send_packet(packet)
		
	def send_unreliable(self, data):
		if len(data) > self.fragment_size:
			raise ValueError("Unreliable data is too large")
		packet = PRUDPPacket(TYPE_DATA, FLAG_NEED_ACK)
		packet.payload = data
		self.send_packet(packet)
		
	def recv(self, stream_id=0):
		if self.packets[stream_id]:
			return self.packets[stream_id].pop(0)
		
	def recv_unreliable(self):
		if self.packets_unreliable:
			return self.packets_unreliable.pop(0)
		
	def send_ack(self, packet):
		ack = PRUDPPacket(packet.type, FLAG_ACK)
		ack.packet_id = packet.packet_id
		ack.fragment_id = packet.fragment_id
		ack.stream_id = packet.stream_id
		if packet.type == TYPE_CONNECT:
			ack.payload = self.connect_response
			ack.connection_signature = bytes(self.stream.signature_size())
		self.send_packet(ack)
		
	def send_packet(self, packet, block=False):
		packet.source_port = self.local_port
		packet.source_type = self.stream_type
		packet.dest_port = self.remote_port
		packet.dest_type = self.stream_type
		packet.session_id = self.local_session_id
		return self.stream.send(packet, block)
		
		
class RVClient(PRUDPClient):
	def __init__(self, settings, sock=None):
		super().__init__(settings, sock)
		self.server_key = None
		self.pid = None
		
	def connect(self, host, port, sid, ticket=None):
		check_value = random.randint(0, 0xFFFFFFFF)
		
		request = b""
		if ticket:
			request = self.build_connection_request(ticket, check_value)
		
		response = super().connect(host, port, sid, request)
		if response is None:
			return False
			
		if ticket:
			if not self.check_connection_response(ticket, check_value, response):
				self.cleanup()
				return False
		return True
		
	def accept(self, sid, key=None):
		self.server_key = key
		return super().accept(sid)
		
	def build_connection_request(self, ticket, check_value):
		stream = streams.StreamOut(self.settings)
		stream.buffer(ticket.internal)
		
		substream = streams.StreamOut(self.settings)
		substream.pid(ticket.source_pid)
		substream.u32(ticket.target_cid)
		substream.u32(check_value)
		
		kerb = kerberos.KerberosEncryption(ticket.session_key)
		stream.buffer(kerb.encrypt(substream.get()))
		return stream.get()
		
	def check_connection_response(self, ticket, check_value, response):
		logger.debug("Validating connection response")
		
		if len(response) != 8:
			logger.error("Connection response payload has wrong size")
			return False
			
		length, check_response = struct.unpack("<II", response)
		if length != 4:
			logger.error("Invalid connection response size")
			return False
		if check_response != (check_value + 1) & 0xFFFFFFFF:
			logger.error("Connection response check failed")
			return False
		
		logger.debug("Connection response was valid")
		self.set_session_key(ticket.session_key)
		return True
	
	def handle_connection_request(self, packet):
		logger.debug("Received connection request: %i bytes", len(packet.payload))
		if not self.server_key:
			logger.debug("No validation needed, accepting connection")
			return b""
			
		if not packet.payload:
			logger.error("Received empty connection request for secure server")
			self.cleanup()
			return
		
		stream = streams.StreamIn(packet.payload, self.settings)
		ticket = stream.buffer()
		request = stream.buffer()
		
		server_ticket = kerberos.ServerTicket()
		try:
			server_ticket.decrypt(ticket, self.server_key, self.settings)
		except ValueError:
			logger.error("Server ticket decryption failed")
			self.cleanup()
			return
			
		if server_ticket.expiration.timestamp() < time.time():
			logger.error("Ticket has expired")
			self.cleanup()
			return
			
		kerb = kerberos.KerberosEncryption(server_ticket.session_key)
		try:
			decrypted = kerb.decrypt(request)
		except ValueError:
			logger.error("Ticket decryption failed")
			self.cleanup()
			return
		
		if len(decrypted) != self.settings.get("common.pid_size") + 8:
			logger.error("Invalid ticket size")
			self.cleanup()
			return
		
		stream = streams.StreamIn(decrypted, self.settings)
		if stream.pid() != server_ticket.source_pid:
			logger.error("Invalid pid in kerberos ticket")
			self.cleanup()
			return
			
		self.pid = server_ticket.source_pid
			
		stream.u32() #Don't care about cid
		
		check_value = stream.u32()
		
		logger.debug("Connection request was validated successfully")
		self.set_session_key(server_ticket.session_key)
		
		return struct.pack("<II", 4, (check_value + 1) & 0xFFFFFFFF)
		
		
class PRUDPServer:
	def __init__(self, settings, server=None):
		self.settings = settings
		self.server = server
		
		if not self.server:
			transport_type = settings.get("prudp.transport")
			if transport_type == settings.TRANSPORT_UDP:
				self.server = socket.SocketServer(socket.TYPE_UDP)
			elif transport_type == settings.TRANSPORT_TCP:
				self.server = socket.SocketServer(socket.TYPE_TCP)
			else:
				self.server = websocket.WebSocketServer(True)
				
		self.sockets = []
		
	def start(self, host, port, sid):
		logger.info("Starting PRUDP server at %s:%i:%i", host, port, sid)
		self.sid = sid
		self.server.start(host, port)
		scheduler.add_server(self.handle, self.server)
		
	def handle(self, socket):
		client = PRUDPClient(self.settings, socket)
		if client.accept(self.sid):
			self.sockets.append(client)
		
	def accept(self):
		if self.sockets:
			return self.sockets.pop(0)
			
			
class RVServer(PRUDPServer):
	def start(self, host, port, sid, key=None):
		self.server_key = key
		super().start(host, port, sid)
		
	def handle(self, socket):
		client = RVClient(self.settings, socket)
		if client.accept(self.sid, self.server_key):
			self.sockets.append(client)
