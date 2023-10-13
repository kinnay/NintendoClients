
from Crypto.Cipher import ARC4
from anynet import udp, tls, websocket, util, \
	scheduler, streams, queue
from nintendo.nex import kerberos, streams as streams_nex
import contextlib
import hashlib
import struct
import random
import socket
import anyio
import zlib
import hmac
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
	OPTION_CONNECTION_SIG: (16, "OPTION_CONNECTION_SIG", "16s"),
	OPTION_FRAGMENT_ID: (1, "OPTION_FRAGMENT_ID", "B"),
	OPTION_UNRELIABLE_SEQ_ID: (2, "OPTION_UNRELIABLE_SEQ_ID", "H"),
	OPTION_MAX_SUBSTREAM_ID: (1, "OPTION_MAX_SUBSTREAM_ID", "B"),
	OPTION_CONNECTION_SIG_LITE: (16, "OPTION_CONNECTION_SIG_LITE", "16s")
}

STATE_CONNECTING = 0
STATE_CONNECTED = 1
STATE_DISCONNECTING = 2
STATE_DISCONNECTED = 3


def encode_options(options):
	data = b""
	for k, v in options.items():
		size, name, type = OPTIONS[k]
		data += struct.pack("<BB%s" %type, k, size, v)
	return data

def decode_options(data):
	options = {}
	stream = streams.StreamIn(data, "<")
	while not stream.eof():
		type = stream.u8()
		length = stream.u8()
		
		if type not in OPTIONS:
			raise ValueError("(Opt) Unrecognized option type: %i" %type)
		
		expected_length, name, format = OPTIONS[type]
		if length != expected_length:
			raise ValueError("(Opt) Invalid option length in %s" %name)
		
		if type in options:
			raise ValueError("(Opt) %s is present more than once" %name)
		
		value = struct.unpack("<" + format, stream.read(length))[0]
		options[type] = value
	return options
	

class PRUDPPacket:
	def __init__(self, type=None, flags=None):
		self.type = type
		self.flags = flags
		
		self.version = None
		self.source_type = None
		self.source_port = None
		self.dest_type = None
		self.dest_port = None
		self.session_id = 0
		self.packet_id = 0
		self.fragment_id = 0
		self.substream_id = 0
		self.connection_signature = None
		self.initial_unreliable_id = 0
		self.max_substream_id = 0
		self.supported_functions = 0
		self.minor_version = 0
		self.signature = None
		
		self.payload = b""
		
	def __repr__(self):
		flags = []
		for flag in FLAG_LIST:
			if self.flags & flag:
				flags.append(FLAG_NAMES[flag])
		flags = ",".join(flags)
		
		return "<PRUDPPacket type=%s flags=%s seq=%i frag=%i>" %(
			TYPE_NAMES[self.type], flags, self.packet_id, self.fragment_id
		)

		
class PRUDPMessageV0:
	def __init__(self, settings):
		self.signature_version = settings["prudp_v0.signature_version"]
		self.checksum_version = settings["prudp_v0.checksum_version"]
		self.flags_version = settings["prudp_v0.flags_version"]
		
		self.access_key = settings["prudp.access_key"].encode()
	
	def signature_size(self): return 4
	
	def calc_checksum(self, data):
		checksum = sum(self.access_key)
		if self.checksum_version == 0:
			data = data.ljust((len(data) + 3) & ~3, b"\0")
			words = struct.unpack("<%iI" %(len(data) // 4), data)
			return ((checksum & 0xFF) + sum(words)) & 0xFFFFFFFF

		else:
			words = struct.unpack_from("<%iI" %(len(data) // 4), data)
			temp = sum(words) & 0xFFFFFFFF
			
			checksum += sum(data[len(data) & ~3:])
			checksum += sum(struct.pack("<I", temp))
			return checksum & 0xFF
	
	def calc_data_signature(self, packet, session_key):
		data = packet.payload
		if self.signature_version == 0:
			header = struct.pack("<HB", packet.packet_id, packet.fragment_id)
			data = session_key + header + data

		if data:
			key = hashlib.md5(self.access_key).digest()
			digest = hmac.digest(key, data, hashlib.md5)
			return digest[:4]
		return struct.pack("<I", 0x12345678)
		
	def calc_packet_signature(self, packet, session_key, connection_signature):
		if packet.type == TYPE_DATA:
			return self.calc_data_signature(packet, session_key)
		if packet.type == TYPE_DISCONNECT and self.signature_version == 0:
			return self.calc_data_signature(packet, session_key)
		if connection_signature:
			return connection_signature
		return bytes(4)
	
	def calc_connection_signature(self, addr):
		data = socket.inet_aton(addr[0]) + struct.pack(">H", addr[1])
		return hashlib.md5(data).digest()[3::-1]
		
	def encode(self, packet):
		stream = streams.StreamOut("<")
		stream.u8(packet.source_port | (packet.source_type << 4))
		stream.u8(packet.dest_port | (packet.dest_type << 4))
		if self.flags_version == 0:
			stream.u8(packet.type | (packet.flags << 3))
		else:
			stream.u16(packet.type | (packet.flags << 4))
		stream.u8(packet.session_id)
		stream.write(packet.signature)
		stream.u16(packet.packet_id)
		self.encode_options(packet, stream)
		stream.write(packet.payload)
		
		data = stream.get()
		if self.checksum_version == 0:
			data += struct.pack("<I", self.calc_checksum(data))
		else:
			data += struct.pack("<B", self.calc_checksum(data))
		return data
	
	def encode_options(self, packet, stream):
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			stream.write(packet.connection_signature)
		if packet.type == TYPE_DATA:
			stream.u8(packet.fragment_id)
		if packet.flags & FLAG_HAS_SIZE:
			stream.u16(len(packet.payload))
	
	def decode(self, data):
		packets = []
		
		stream = streams.StreamIn(data, "<")
		while not stream.eof():
			start = stream.tell()
		
			source = stream.u8()
			dest = stream.u8()
			
			packet = PRUDPPacket()
			packet.version = 0
			packet.source_type = source >> 4
			packet.source_port = source & 0xF
			packet.dest_type = dest >> 4
			packet.dest_port = dest & 0xF
			
			if self.flags_version == 0:
				type_flags = stream.u8()
				packet.flags = type_flags >> 3
				packet.type = type_flags & 7
			else:
				type_flags = stream.u16()
				packet.flags = type_flags >> 4
				packet.type = type_flags & 0xF
				
			packet.session_id = stream.u8()
			packet.signature = stream.read(4)
			packet.packet_id = stream.u16()
			
			if packet.type in [TYPE_SYN, TYPE_CONNECT]:
				packet.connection_signature = stream.read(4)
			if packet.type == TYPE_DATA:
				packet.fragment_id = stream.u8()
			
			if packet.flags & FLAG_HAS_SIZE:
				payload_size = stream.u16()
			else:
				if self.checksum_version == 0:
					payload_size = stream.available() - 4
				else:
					payload_size = stream.available() - 1
			packet.payload = stream.read(payload_size)
			
			# Check packet checkusm
			end = stream.tell()
			checksum_data = stream.get()[start : end]
			expected_checksum = self.calc_checksum(checksum_data)
			
			if self.checksum_version == 0:
				checksum = stream.u32()
			else:
				checksum = stream.u8()
				
			if checksum != expected_checksum:
				raise ValueError("(V0) Invalid checksum (expected %i, got %i)" %(expected_checksum, checksum))
			
			# Checksum is good!
			packets.append(packet)
		return packets


class PRUDPMessageV1:
	def __init__(self, settings):
		self.access_key = settings["prudp.access_key"].encode()
	
	def signature_size(self): return 16
	
	def calc_packet_signature(self, packet, session_key, connection_signature):
		options = self.encode_options(packet)
		header = self.encode_header(packet, len(options))
		
		key = hashlib.md5(self.access_key).digest()
		mac = hmac.new(key, digestmod=hashlib.md5)
		mac.update(header[4:])
		mac.update(session_key)
		mac.update(struct.pack("<I", sum(self.access_key)))
		mac.update(connection_signature)
		mac.update(options)
		mac.update(packet.payload)
		return mac.digest()
		
	def calc_connection_signature(self, addr):
		key = bytes.fromhex("26c31f381e46d6eb38e1af6ab70d11")
		data = socket.inet_aton(addr[0]) + struct.pack(">H", addr[1])
		return hmac.digest(key, data, hashlib.md5)
	
	def encode(self, packet):
		options = self.encode_options(packet)
		header = self.encode_header(packet, len(options))
		return b"\xEA\xD0" + header + packet.signature + options + packet.payload
	
	def encode_header(self, packet, option_size):
		stream = streams.StreamOut("<")
		stream.u8(1) # PRUDP version
		stream.u8(option_size)
		stream.u16(len(packet.payload))
		stream.u8(packet.source_port | (packet.source_type << 4))
		stream.u8(packet.dest_port | (packet.dest_type << 4))
		stream.u16(packet.type | (packet.flags << 4))
		stream.u8(packet.session_id)
		stream.u8(packet.substream_id)
		stream.u16(packet.packet_id)
		return stream.get()
	
	def encode_options(self, packet):
		options = {}
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			options[OPTION_SUPPORT] = packet.minor_version | (packet.supported_functions << 8)
			options[OPTION_CONNECTION_SIG] = packet.connection_signature
			if packet.type == TYPE_CONNECT:
				options[OPTION_UNRELIABLE_SEQ_ID] = packet.initial_unreliable_id
			options[OPTION_MAX_SUBSTREAM_ID] = packet.max_substream_id
		elif packet.type == TYPE_DATA:
			options[OPTION_FRAGMENT_ID] = packet.fragment_id
		return encode_options(options)
		
	def verify_options(self, packet, options):
		keys = set(options)
		if packet.type == TYPE_SYN:
			return keys == {OPTION_SUPPORT, OPTION_CONNECTION_SIG, OPTION_MAX_SUBSTREAM_ID}
		if packet.type == TYPE_CONNECT:
			return keys == {OPTION_SUPPORT, OPTION_CONNECTION_SIG, OPTION_UNRELIABLE_SEQ_ID, OPTION_MAX_SUBSTREAM_ID}
		if packet.type == TYPE_DATA:
			return keys == {OPTION_FRAGMENT_ID}
		return keys == set()
		
	def decode(self, data):
		packets = []
		
		stream = streams.StreamIn(data, "<")
		while not stream.eof():
			if stream.read(2) != b"\xEA\xD0":
				raise ValueError("(V1) Invalid magic number")
				
			header = stream.peek(12)
			
			if stream.u8() != 1:
				raise ValueError("(V1) Version check failed")
			
			option_size = stream.u8()
			payload_size = stream.u16()
			source = stream.u8()
			dest = stream.u8()
			type_flags = stream.u16()
			
			packet = PRUDPPacket()
			packet.version = 1
			packet.source_type = source >> 4
			packet.source_port = source & 0xF
			packet.dest_type = dest >> 4
			packet.dest_port = dest & 0xF
			packet.flags = type_flags >> 4
			packet.type = type_flags & 0xF
			packet.session_id = stream.u8()
			packet.substream_id = stream.u8()
			packet.packet_id = stream.u16()
			
			packet.signature = stream.read(16)
			
			option_data = stream.read(option_size)
			options = decode_options(option_data)
			
			if not self.verify_options(packet, options):
				raise ValueError("(V1) Received unexpected set of options")
			
			if packet.type in [TYPE_SYN, TYPE_CONNECT]:
				packet.minor_version = options[OPTION_SUPPORT] & 0xFF
				packet.supported_functions = options[OPTION_SUPPORT] >> 8
				packet.connection_signature = options[OPTION_CONNECTION_SIG]
				packet.max_substream_id = options[OPTION_MAX_SUBSTREAM_ID]
			if packet.type == TYPE_CONNECT:
				packet.initial_unreliable_id = options[OPTION_UNRELIABLE_SEQ_ID]
			if packet.type == TYPE_DATA:
				packet.fragment_id = options[OPTION_FRAGMENT_ID]
			
			packet.payload = stream.read(payload_size)
			
			packets.append(packet)
		return packets
		

class PRUDPLiteMessage:
	def __init__(self, settings):
		self.access_key = settings["prudp.access_key"].encode()
		
		self.buffer = b""
		
	def signature_size(self): return 16

	def calc_packet_signature(self, packet, session_key, connection_signature):
		if packet.type == TYPE_CONNECT and packet.flags & FLAG_NEED_ACK:
			key = hashlib.md5(self.access_key).digest()
			return hmac.digest(key, key + connection_signature, hashlib.md5)
		return None
	
	def calc_connection_signature(self, addr):
		key = bytes.fromhex("26c31f381e46d6eb38e1af6ab70d11")
		data = socket.inet_aton(addr[0]) + struct.pack(">H", addr[1])
		return hmac.digest(key, data, hashlib.md5)
	
	def encode(self, packet):
		options = self.encode_options(packet)
		header = self.encode_header(packet, len(options))
		return header + options + packet.payload
	
	def encode_header(self, packet, option_size):
		stream = streams.StreamOut("<")
		stream.u8(0x80)
		stream.u8(option_size)
		stream.u16(len(packet.payload))
		stream.u8((packet.source_type << 4) | packet.dest_type)
		stream.u8(packet.source_port)
		stream.u8(packet.dest_port)
		stream.u8(packet.fragment_id)
		stream.u16(packet.type | (packet.flags << 4))
		stream.u16(packet.packet_id)
		return stream.get()
	
	def encode_options(self, packet):
		options = {}
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			options[OPTION_SUPPORT] = packet.minor_version | (packet.supported_functions << 8)
		if packet.type == TYPE_SYN and packet.flags & FLAG_ACK:
			options[OPTION_CONNECTION_SIG] = packet.connection_signature
		if packet.type == TYPE_CONNECT and not packet.flags & FLAG_ACK:
			options[OPTION_CONNECTION_SIG_LITE] = packet.signature
		return encode_options(options)
	
	def verify_options(self, packet, options):
		keys = set(options)
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			if packet.type == TYPE_SYN and packet.flags & FLAG_ACK:
				return keys == {OPTION_SUPPORT, OPTION_CONNECTION_SIG}
			if packet.type == TYPE_CONNECT and not packet.flags & FLAG_ACK:
				return keys == {OPTION_SUPPORT, OPTION_CONNECTION_SIG_LITE}
			return keys == {OPTION_SUPPORT}
		return keys == set()
	
	def decode(self, data):
		self.buffer += data
		
		packets = []
		while self.buffer:
			if len(self.buffer) < 12: return packets
			
			stream = streams.StreamIn(self.buffer, "<")
			if stream.u8() != 0x80:
				raise ValueError("(Lite) Invalid magic number")
			
			option_size = stream.u8()
			payload_size = stream.u16()
			if len(self.buffer) < 12 + option_size + payload_size:
				return packets
			
			self.buffer = self.buffer[12 + option_size + payload_size:]
			
			packet = PRUDPPacket()
			
			stream_types = stream.u8()
			packet.source_type = stream_types >> 4
			packet.dest_type = stream_types & 0xF
			
			packet.source_port = stream.u8()
			packet.dest_port = stream.u8()
			packet.fragment_id = stream.u8()
			
			type_flags = stream.u16()
			packet.flags = type_flags >> 4
			packet.type = type_flags & 0xF
			
			packet.packet_id = stream.u16()
			packet.session_id = 0
			
			option_data = stream.read(option_size)
			options = decode_options(option_data)
			
			if not self.verify_options(packet, options):
				raise ValueError("(Lite) Received unexpected set of options")
			
			packet.connection_signature = b""
			if packet.type in [TYPE_SYN, TYPE_CONNECT]:
				packet.minor_version = options[OPTION_SUPPORT] & 0xFF
				packet.supported_functions = options[OPTION_SUPPORT] >> 8
			if packet.type == TYPE_SYN and packet.flags & FLAG_ACK:
				packet.connection_signature = options[OPTION_CONNECTION_SIG]
			if packet.type == TYPE_CONNECT and not packet.flags & FLAG_ACK:
				packet.signature = options[OPTION_CONNECTION_SIG_LITE]
			
			packet.payload = stream.read(payload_size)
			packets.append(packet)
		return packets
		
		
class PRUDPMessageSelector:
	def __init__(self, settings):
		self.settings = settings
		self.v0 = PRUDPMessageV0(settings)
		self.v1 = PRUDPMessageV1(settings)
		self.lite = PRUDPLiteMessage(settings)
		
	def select(self, version):
		if self.settings["prudp.transport"] == self.settings.TRANSPORT_UDP:
			if version == 0:
				return self.v0
			return self.v1
		return self.lite
	
	def analyze(self, data):
		if self.settings["prudp.transport"] == self.settings.TRANSPORT_UDP:
			if self.settings["prudp.version"] == 2:
				if data[:3] == b"\xEA\xD0\x01":
					return self.v1
				return self.v0
		return self.select(self.settings["prudp.version"])
	
	def signature_size(self, version=None):
		return self.select(version).signature_size()
	def calc_packet_signature(self, packet, session_key, connection_signature):
		return self.select(packet.version).calc_packet_signature(packet, session_key, connection_signature)
	def calc_connection_signature(self, addr, version=None):
		return self.select(version).calc_connection_signature(addr)
	def encode(self, packet):
		return self.select(packet.version).encode(packet)
	def decode(self, data):
		return self.analyze(data).decode(data)
	
	
class RC4Encryption:
	def __init__(self, key):
		self.rc4enc = ARC4.new(key)
		self.rc4dec = ARC4.new(key)
	
	def set_key(self, key):
		self.rc4enc = ARC4.new(key)
		self.rc4dec = ARC4.new(key)
		
	def encrypt(self, data): return self.rc4enc.encrypt(data)
	def decrypt(self, data): return self.rc4dec.decrypt(data)
	
	
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
			raise ValueError("Unexpected compression ratio (expected %i, got %i)" %ratio, data[0])
		return decompressed
		
		
class DummyCompression:
	def compress(self, data): return data
	def decompress(self, data): return data


class PayloadEncoder:

	DEFAULT_KEY = b"CD&ML"

	def __init__(self, settings):
		substreams = settings["prudp.max_substream_id"] + 1
		
		self.reliable_encryption = [self.create_encryption(settings) for i in range(substreams)]
		self.unreliable_encryption = self.create_encryption(settings)
		
		self.unreliable_key = bytes(0x20)
		
		if settings["prudp.compression"] == settings.COMPRESSION_NONE:
			self.compression = DummyCompression()
		else:
			self.compression = ZlibCompression()
			
	def create_encryption(self, settings):
		if settings["prudp.transport"] == settings.TRANSPORT_UDP:
			return RC4Encryption(self.DEFAULT_KEY)
		return DummyEncryption()
		
	def encode(self, packet):
		data = packet.payload
		if packet.type == TYPE_DATA and data:
			data = self.compression.compress(data)
			if packet.flags & FLAG_RELIABLE:
				data = self.reliable_encryption[packet.substream_id].encrypt(data)
			else:
				key = self.make_unreliable_key(packet)
				self.unreliable_encryption.set_key(key)
				
				data = self.unreliable_encryption.encrypt(data)
		return data
	
	def decode(self, packet):
		data = packet.payload
		if packet.type == TYPE_DATA and data:
			if packet.flags & FLAG_RELIABLE:
				data = self.reliable_encryption[packet.substream_id].decrypt(data)
			else:
				key = self.make_unreliable_key(packet)
				self.unreliable_encryption.set_key(key)
				
				data = self.unreliable_encryption.decrypt(data)
			data = self.compression.decompress(data)
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
	
	def set_session_key(self, key):
		self.reliable_encryption[0].set_key(key)
		
		temp_key = key
		for encryption in self.reliable_encryption[1:]:
			temp_key = self.modify_key(temp_key)
			encryption.set_key(temp_key)
		
		self.unreliable_key = self.init_unreliable_key(key)


class SequenceCounter:
	def __init__(self, initial = 1):
		self.next_id = initial
	
	def next(self):
		current = self.next_id
		self.next_id = (self.next_id + 1) & 0xFFFF
		return current
		
		
class SequenceMgr:
	def __init__(self, settings):	
		substreams = settings["prudp.max_substream_id"] + 1
		
		self.initial_unreliable_id = 1
		if settings["prudp.transport"] == settings.TRANSPORT_UDP:
			if settings["prudp.version"] != 0:
				self.initial_unreliable_id = random.randint(0, 0xFFFF)
		
		self.counters = [SequenceCounter() for i in range(substreams)]
		self.unreliable_counter = SequenceCounter(self.initial_unreliable_id)
		self.ping_counter = SequenceCounter()
		
	def assign(self, packet):
		if packet.flags & FLAG_RELIABLE:
			return self.counters[packet.substream_id].next()
		if packet.type == TYPE_DATA:
			return self.unreliable_counter.next()
		if packet.type == TYPE_PING:
			return self.ping_counter.next()
		return 0


class SlidingWindow:
	def __init__(self):
		self.next = 1
		self.packets = {}
	
	def skip(self):
		self.next = (self.next + 1) & 0xFFFF
	
	def update(self, packet):
		packets = []
		if packet.packet_id < self.next or packet.packet_id in self.packets:
			logger.debug("Received duplicate packet: %s", packet)
		else:
			self.packets[packet.packet_id] = packet
			while self.next in self.packets:
				packet = self.packets.pop(self.next)
				packets.append(packet)
				self.skip()
		return packets


class PRUDPClient:
	def __init__(self, settings, transport, version):
		self.fragment_size = settings["prudp.fragment_size"]
		self.resend_timeout = settings["prudp.resend_timeout"]
		self.resend_limit = settings["prudp.resend_limit"]
		self.ping_timeout = settings["prudp.ping_timeout"]
		self.max_substream_id = settings["prudp.max_substream_id"]
		self.supported_functions = settings["prudp.supported_functions"]
		self.minor_ver = settings["prudp.minor_version"]
		
		self.settings = settings
		self.transport = transport
		self.version = version
		
		self.packet_encoder = PRUDPMessageSelector(settings).select(version)
		self.payload_encoder = PayloadEncoder(settings)
		self.sequence_mgr = SequenceMgr(settings)
		
		substreams = self.max_substream_id + 1
		self.sliding_windows = [SlidingWindow() for i in range(substreams)]
		self.fragment_buffers = [b""] * substreams
		
		self.packets = [queue.create() for i in range(substreams)]
		self.unreliable_packets = queue.create()
		
		self.group = None
		self.scheduler = None
		self.ping_event = None
		self.ack_events = {}
		
		self.connection_check = random.randint(0, 0xFFFFFFFF)
		
		self.local_session_id = random.randint(0, 0xFF)
		self.remote_session_id = None
		self.remote_signature = None
		
		self.local_addr = None
		self.local_port = None
		self.local_type = None
		
		self.remote_addr = None
		self.remote_port = None
		self.remote_type = None
		
		self.user_pid = None
		self.user_cid = None
		self.session_key = b""
		
		self.credentials = None
		
		self.handshake_event = anyio.Event()
		self.close_event = anyio.Event()
		
		self.state = STATE_CONNECTING
	
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tb):
		await self.cleanup()
		
	def bind(self, addr, port, type):
		self.local_addr = addr
		self.local_port = port
		self.local_type = type
	
	def connect(self, addr, port, type):
		self.remote_addr = addr
		self.remote_port = port
		self.remote_type = type
	
	def login(self, pid, cid, session_key):
		self.user_pid = pid
		self.user_cid = cid
		self.session_key = session_key
		
		self.payload_encoder.set_session_key(session_key)
	
	def configure(self, max_substream_id, supported_functions, minor_version):
		self.max_substream_id = max_substream_id
		self.supported_functions = supported_functions
		self.minor_ver = minor_version
	
	def remote(self, connection_signature, session_id):
		self.remote_signature = connection_signature
		self.remote_session_id = session_id
		
	async def handshake(self, credentials, group):
		self.group = group
		
		self.scheduler = scheduler.Scheduler(group)
		self.scheduler.start()
		
		self.credentials = credentials
		if self.credentials:
			self.login(credentials.pid, credentials.cid, credentials.ticket.session_key)
		
		await self.send_syn()
		await self.handshake_event.wait()
		
		if self.state != STATE_CONNECTED:
			raise RuntimeError("PRUDP connection failed")
		
		self.ping_event = self.scheduler.repeat(self.send_ping, self.ping_timeout)
	
	async def serve(self, group):
		self.group = group
		
		self.state = STATE_CONNECTED
		
		self.sliding_windows[0].skip()
		
		self.scheduler = scheduler.Scheduler(group)
		self.scheduler.start()
		
		self.ping_event = self.scheduler.repeat(self.send_ping, self.ping_timeout)
	
	async def send(self, data, substream=0):
		if self.state != STATE_CONNECTED:
			raise anyio.ClosedResourceError("PRUDP connection is closed")
		
		if not 0 <= substream <= self.max_substream_id:
			raise ValueError("Substream id is invalid")
		
		fragment_id = 1
		while data:
			if len(data) <= self.fragment_size:
				fragment_id = 0
			await self.send_fragment(data[:self.fragment_size], fragment_id, substream)
			data = data[self.fragment_size:]
			fragment_id += 1
	
	async def send_fragment(self, data, fragment_id, substream):
		packet = PRUDPPacket(TYPE_DATA, FLAG_RELIABLE | FLAG_NEED_ACK | FLAG_HAS_SIZE)
		packet.fragment_id = fragment_id
		packet.substream_id = substream
		packet.payload = data
		await self.send_packet(packet)
	
	async def send_unreliable(self, data):
		if self.state != STATE_CONNECTED:
			raise anyio.ClosedResourceError("PRUDP connection is closed")
		
		packet = PRUDPPacket(TYPE_DATA, FLAG_NEED_ACK | FLAG_HAS_SIZE)
		packet.payload = data
		await self.send_packet(packet)
	
	async def send_ping(self):
		packet = PRUDPPacket(TYPE_PING, FLAG_RELIABLE | FLAG_NEED_ACK)
		await self.send_packet(packet)
	
	async def send_syn(self):
		packet = PRUDPPacket(TYPE_SYN, FLAG_NEED_ACK)
		packet.connection_signature = bytes(self.packet_encoder.signature_size())
		packet.max_substream_id = self.max_substream_id
		packet.supported_functions = self.supported_functions
		packet.minor_version = self.minor_ver
		await self.send_packet(packet)
	
	async def send_connect(self):
		connection_signature = self.packet_encoder.calc_connection_signature(self.remote_addr)
		packet = PRUDPPacket(TYPE_CONNECT, FLAG_RELIABLE | FLAG_NEED_ACK | FLAG_HAS_SIZE)
		packet.connection_signature = connection_signature
		packet.initial_unreliable_id = self.sequence_mgr.initial_unreliable_id
		packet.max_substream_id = self.max_substream_id
		packet.minor_version = self.minor_ver
		packet.supported_functions = self.supported_functions
		packet.payload = self.build_connection_request()
		await self.send_packet(packet)
	
	async def send_ack(self, packet):
		ack = PRUDPPacket(packet.type, FLAG_ACK)
		ack.packet_id = packet.packet_id
		ack.fragment_id = packet.fragment_id
		ack.substream_id = packet.substream_id
		
		await self.send_packet(ack)
		if packet.type == TYPE_DISCONNECT:
			await self.send_packet(ack)
			await self.send_packet(ack)
	
	async def send_packet(self, packet):
		packet.version = self.version
		packet.source_port = self.local_port
		packet.source_type = self.local_type
		packet.dest_port = self.remote_port
		packet.dest_type = self.remote_type
		if not packet.flags & (FLAG_ACK | FLAG_MULTI_ACK):
			packet.packet_id = self.sequence_mgr.assign(packet)
		if packet.type != TYPE_SYN:
			packet.session_id = self.local_session_id
		
		if packet.type == TYPE_DATA and not packet.flags & (FLAG_ACK | FLAG_MULTI_ACK):
			packet.payload = self.payload_encoder.encode(packet)
		
		if packet.type == TYPE_SYN:
			packet.signature = self.packet_encoder.calc_packet_signature(packet, b"", b"")
		elif packet.type == TYPE_CONNECT:
			packet.signature = self.packet_encoder.calc_packet_signature(packet, b"", self.remote_signature)
		else:
			packet.signature = self.packet_encoder.calc_packet_signature(packet, self.session_key, self.remote_signature)
		
		try:
			await self.transport.send(packet, self.remote_addr)
		except util.StreamError:
			await self.cleanup()
			return
		
		if (packet.flags & FLAG_RELIABLE or packet.type == TYPE_SYN) and packet.flags & FLAG_NEED_ACK:
			self.schedule_timeout(packet)
			
	async def resend_packet(self, packet, counter):
		key = (packet.type, packet.substream_id, packet.packet_id)
		if counter < self.resend_limit:
			logger.debug("[%i] Resending packet: %s", self.local_session_id, packet)
			
			try:
				await self.transport.send(packet, self.remote_addr)
			except util.StreamError:
				await self.cleanup()
				return
			
			handle = self.scheduler.schedule(self.resend_packet, self.resend_timeout, packet, counter + 1)
			self.ack_events[key] = handle
		else:
			logger.error("Packet timed out: %s" %packet)
			await self.cleanup()
	
	def schedule_timeout(self, packet):
		key = (packet.type, packet.substream_id, packet.packet_id)
		handle = self.scheduler.schedule(self.resend_packet, self.resend_timeout, packet, 0)
		self.ack_events[key] = handle
		
	def build_connection_request(self):
		if self.credentials is None:
			return b""
		
		stream = streams_nex.StreamOut(self.settings)
		stream.buffer(self.credentials.ticket.internal)
		
		substream = streams_nex.StreamOut(self.settings)
		substream.pid(self.credentials.pid)
		substream.u32(self.credentials.cid)
		substream.u32(self.connection_check)
		
		kerb = kerberos.KerberosEncryption(self.credentials.ticket.session_key)
		stream.buffer(kerb.encrypt(substream.get()))
		return stream.get()
	
	def check_connection_response(self, data):
		if self.credentials is not None:
			if len(data) != 8:
				raise ValueError("Connection response has wrong size")
			
			length, check_value = struct.unpack("<II", data)
			if length != 4:
				raise ValueError("Invalid connection response size")
			if check_value != (self.connection_check + 1) & 0xFFFFFFFF:
				raise ValueError("Connection response check failed")
		elif data:
			raise ValueError("Expected empty connection response")
		
	async def handle(self, packet):
		if self.state == STATE_DISCONNECTED: return
		
		if self.state == STATE_CONNECTING and packet.type != TYPE_SYN:
			raise ValueError("Expected SYN packet")
		
		if packet.type == TYPE_SYN:
			await self.process_syn(packet)
		elif packet.type == TYPE_CONNECT:
			await self.process_connect(packet)
		else:
			await self.process_other(packet)
		
		if packet.flags & FLAG_ACK:
			key = (packet.type, packet.substream_id, packet.packet_id)
			if key in self.ack_events:
				handle = self.ack_events.pop(key)
				self.scheduler.remove(handle)
				
				if packet.type == TYPE_DISCONNECT:
					await self.cleanup()
	
	async def process_syn(self, packet):
		if packet.signature != self.packet_encoder.calc_packet_signature(packet, b"", b""):
			raise ValueError("Received SYN packet with invalid signature")
		if not packet.flags & FLAG_ACK:
			raise ValueError("Received unexpected SYN packet")
		if packet.session_id != 0 or packet.packet_id != 0 or \
		   packet.fragment_id != 0 or packet.substream_id != 0:
			raise ValueError("Received invalid SYN/ACK packet")
		if packet.max_substream_id > self.max_substream_id or \
		   packet.minor_version > self.minor_ver or \
		   packet.supported_functions & ~self.supported_functions:
			raise ValueError("Received SYN/ACK packet with invalid negotiation parameters")
		
		key = (packet.type, packet.substream_id, packet.packet_id)
		if key in self.ack_events:
			self.state = STATE_CONNECTED
			
			self.max_substream_id = packet.max_substream_id
			self.minor_ver = packet.minor_version
			self.supported_functions = packet.supported_functions
			
			self.remote_signature = packet.connection_signature
			
			await self.send_connect()
	
	async def process_connect(self, packet):
		connection_signature = self.packet_encoder.calc_connection_signature(self.remote_addr)
		if packet.signature != self.packet_encoder.calc_packet_signature(packet, b"", connection_signature):
			raise ValueError("Received CONNECT packet with invalid signature")
		if not packet.flags & FLAG_ACK:
			raise ValueError("Received unexpected CONNECT packet")
		if packet.packet_id != 1 or packet.fragment_id != 0 or \
		   packet.substream_id != 0 or any(packet.connection_signature):
			raise ValueError("Received invalid CONNECT/ACK packet")
		if packet.max_substream_id != self.max_substream_id or \
		   packet.minor_version != self.minor_ver or \
		   packet.supported_functions != self.supported_functions:
			raise ValueError("Received CONNECT/ACK packet with invalid negotiation parameters")
		
		key = (packet.type, packet.substream_id, packet.packet_id)
		if key in self.ack_events:
			self.check_connection_response(packet.payload)
			self.remote_session_id = packet.session_id
			self.handshake_event.set()
	
	async def process_other(self, packet):
		connection_signature = self.packet_encoder.calc_connection_signature(self.remote_addr)
		if packet.signature != self.packet_encoder.calc_packet_signature(packet, self.session_key, connection_signature):
			raise ValueError("Received packet with invalid signature")
		
		if packet.flags & FLAG_MULTI_ACK:
			self.handle_aggregate_ack(packet)
		else:
			if packet.substream_id > self.max_substream_id:
				raise ValueError("Received packet with invalid substream id: %i", packet.substream_id)
			if packet.session_id != self.remote_session_id:
				raise ValueError("Received packet with invalid session id")
			
			if not packet.flags & FLAG_ACK:
				if packet.flags & FLAG_NEED_ACK:
					await self.send_ack(packet)
				if packet.flags & FLAG_RELIABLE:
					await self.process_reliable(packet)
				else:
					if packet.type == TYPE_DATA:
						data = self.payload_encoder.decode(packet)
						await self.unreliable_packets.put(data)
					elif packet.type == TYPE_DISCONNECT:
						logger.info("Connection closed by other end point (forcefully)")
						await self.cleanup()
	
	async def process_reliable(self, packet):
		substream = packet.substream_id
		for packet in self.sliding_windows[substream].update(packet):
			if packet.type == TYPE_DATA:
				self.fragment_buffers[substream] += self.payload_encoder.decode(packet)
				if packet.fragment_id == 0:
					await self.packets[substream].put(self.fragment_buffers[substream])
					self.fragment_buffers[substream] = b""
			elif packet.type == TYPE_DISCONNECT:
				logger.info("Connection closed by other end point")
				await self.cleanup()
	
	def is_new_aggregate_ack(self, packet):
		if self.settings["prudp.transport"] == self.settings.TRANSPORT_UDP:
			if self.version == 0:
				return False
			return packet.substream_id == 1
		return True
	
	def verify_aggregate_ack(self, packet):
		if packet.type != TYPE_DATA:
			raise ValueError("Aggregate ack must be a DATA packet")
		
		if len(packet.payload) % 2:
			raise ValueError("Aggregate ack payload size must be a multiple of 2")
		if packet.substream_id not in [0, 1]:
			raise ValueError("Aggregate ack packet has invalid stream id: %i" %packet.substream_id)
		
		if self.is_new_aggregate_ack(packet):
			if len(packet.payload) != 4 + packet.payload[1] * 2:
				raise ValueError("Aggregate ack payload has incorrect size")
		elif len(packet.payload) < 4:
			raise ValueError("Aggregate ack payload is too small")
	
	def handle_aggregate_ack(self, packet):
		self.verify_aggregate_ack(packet)
		if self.is_new_aggregate_ack(packet):
			substream = packet.payload[0]
			base_id = struct.unpack_from("<H", packet.payload, 2)[0]
			extra_ids = struct.unpack_from("<%iH" %packet.payload[1], packet.payload, 4)
		else:
			substream = 0
			base_id = packet.packet_id
			extra_ids = struct.unpack("<%iH" %(len(packet.payload) // 2), packet.payload)
		
		for key in list(self.ack_events):
			if key[0] == TYPE_DATA and key[1] == substream and key[2] <= base_id:
				self.scheduler.remove(self.ack_events.pop(key))
		
		for packet_id in extra_ids:
			key = (TYPE_DATA, substream, packet_id)
			if key in self.ack_events:
				self.scheduler.remove(self.ack_events.pop(key))
				
	async def cleanup(self):
		self.state = STATE_DISCONNECTED
		self.scheduler.remove_all()
		self.handshake_event.set()
		self.close_event.set()
		for queue in self.packets:
			await queue.eof()
		await self.unreliable_packets.eof()
	
	async def close(self):
		if self.state == STATE_DISCONNECTED: return
		
		logger.debug("[%i] Closing PRUDP connection forcefully", self.local_session_id)
		
		packet = PRUDPPacket(TYPE_DISCONNECT, 0)
		for i in range(3):
			await self.send_packet(packet)
		await self.cleanup()
	
	async def disconnect(self):
		if self.state != STATE_CONNECTED: return
		
		try:
			logger.debug("[%i] Closing PRUDP connection", self.local_session_id)
			self.state = STATE_DISCONNECTING
			
			packet = PRUDPPacket(TYPE_DISCONNECT, FLAG_RELIABLE | FLAG_NEED_ACK)
			await self.send_packet(packet)
			await self.close_event.wait()

			logger.debug("PRUDP connection is closed")
		finally:
			await self.cleanup()
	
	async def recv(self, substream=0):
		return await self.packets[substream].get()
	
	async def recv_unreliable(self):
		return await self.unreliable_packets.get()
	
	def pid(self):
		return self.user_pid
	def minor_version(self):
		return self.minor_ver
	
	def local_address(self):
		return self.local_addr
	def remote_address(self):
		return self.remote_addr
		
	def local_sid(self):
		return self.local_port
	def remote_sid(self):
		return self.remote_port


class PRUDPPortTable:
	def __init__(self, settings):
		self.num_ports = 32
		if settings["prudp.transport"] == settings.TRANSPORT_UDP:
			self.num_ports = 16
		self.ports = {}
	
	def __iter__(self):
		return iter(self.ports.values())
	
	def get(self, port, type):
		port |= type << 8
		if port not in self.ports:
			raise ValueError("Port is not bound")
		return self.ports[port]
	
	def allocate(self, type):
		for i in reversed(range(self.num_ports)):
			if i | (type << 8) not in self.ports:
				return i
		raise ValueError("All ports are in use")
	
	@contextlib.contextmanager
	def bind(self, obj, port=None, type=10):
		if port is None:
			port = self.allocate(type)
		
		port |= type << 8
		if port in self.ports:
			raise ValueError("Port is in use: %i" %port)
		
		self.ports[port] = obj
		try:
			yield port & 0xFF
		finally:
			del self.ports[port]


class PRUDPServerStream:
	def __init__(self, settings, transport, handler, key, group, disconnect_timeout):
		self.settings = settings
		self.transport = transport
		self.handler = handler
		self.key = key
		self.group = group
		self.disconnect_timeout = disconnect_timeout
		
		self.packet_encoder = PRUDPMessageSelector(settings)
		
		self.supported_functions = settings["prudp.supported_functions"]
		self.max_substream_id = settings["prudp.max_substream_id"]
		self.minor_ver = settings["prudp.minor_version"]
		
		self.addr = None
		self.port = None
		self.type = None
		
		self.clients = {}
	
	def bind(self, addr, port, type):
		self.addr = addr
		self.port = port
		self.type = type
	
	def get_client(self, packet, addr):
		key = (addr, packet.source_port, packet.source_type)
		return self.clients.get(key)
	
	async def start_client(self, client):
		key = (client.remote_address(), client.remote_port, client.remote_type)
		try:
			await self.serve_client(client)
		except Exception as e:
			logger.warning("An exception occurred while serving a client: %s" %e)
		finally:
			del self.clients[key]
	
	async def serve_client(self, client):
		async with util.create_task_group() as group:
			async with client:
				await client.serve(group)
				await self.handler(client)
				with anyio.move_on_after(self.disconnect_timeout):
					await client.disconnect()
	
	async def handle(self, packet, addr):
		if packet.type == TYPE_SYN and not packet.flags & FLAG_ACK:
			await self.process_syn(packet, addr)
		elif packet.type == TYPE_CONNECT and not packet.flags & FLAG_ACK:
			await self.process_connect(packet, addr)
		else:
			await self.process_other(packet, addr)
	
	async def process_other(self, packet, addr):
		client = self.get_client(packet, addr)
		if client is not None:
			await client.handle(packet)
		else:
			logger.warning("Received unexpected packet: %s", packet)
			
	async def process_syn(self, packet, addr):
		if packet.signature != self.packet_encoder.calc_packet_signature(packet, b"", b""):
			raise ValueError("Received packet with invalid signature")
		if not packet.flags & FLAG_NEED_ACK:
			raise ValueError("Received SYN packet without FLAG_NEED_ACK")
		if packet.session_id != 0 or packet.packet_id != 0 or packet.fragment_id != 0 or \
		   packet.substream_id != 0 or any(packet.connection_signature):
			raise ValueError("Received invalid SYN packet: %s" %packet)
		
		ack = PRUDPPacket(TYPE_SYN, FLAG_ACK)
		ack.version = packet.version
		ack.source_type = self.type
		ack.source_port = self.port
		ack.dest_type = packet.source_type
		ack.dest_port = packet.source_port
		ack.connection_signature = self.packet_encoder.calc_connection_signature(addr, ack.version)
		ack.max_substream_id = min(self.max_substream_id, packet.max_substream_id)
		ack.minor_version = min(self.minor_ver, packet.minor_version)
		ack.supported_functions = self.supported_functions & packet.supported_functions
		ack.signature = self.packet_encoder.calc_packet_signature(ack, b"", b"")
		await self.transport.send(ack, addr)
	
	async def process_connect(self, packet, addr):
		connection_signature = self.packet_encoder.calc_connection_signature(addr, packet.version)
		if packet.signature != self.packet_encoder.calc_packet_signature(packet, b"", connection_signature):
			raise ValueError("Received packet with invalid signature")
		
		if not packet.flags & FLAG_NEED_ACK or packet.packet_id != 1 or \
		   packet.fragment_id != 0 or packet.substream_id != 0:
			raise ValueError("Received invalid CONNECT packet")
		if packet.max_substream_id > self.max_substream_id or \
		   packet.minor_version > self.minor_ver or \
		   packet.supported_functions & ~self.supported_functions != 0:
			raise ValueError("Received CONNECT packet with invalid negotiation parameters")
		
		key = (addr, packet.source_port, packet.source_type)
		client = self.clients.get(key)
		if client is None:
			client = PRUDPClient(self.settings, self.transport, packet.version)
			client.bind(self.addr, self.port, self.type)
			client.connect(addr, packet.source_port, packet.source_type)
			client.configure(packet.max_substream_id, packet.supported_functions, packet.minor_version)
			client.remote(packet.connection_signature, packet.session_id)
		
		response = self.process_login_request(packet.payload, client)
		
		if key not in self.clients:
			self.clients[key] = client
			self.group.start_soon(self.start_client, client)
		
		ack = PRUDPPacket(TYPE_CONNECT, FLAG_ACK | FLAG_HAS_SIZE)
		ack.version = packet.version
		ack.source_type = self.type
		ack.source_port = self.port
		ack.dest_type = packet.source_type
		ack.dest_port = packet.source_port
		ack.connection_signature = bytes(len(connection_signature))
		ack.max_substream_id = packet.max_substream_id
		ack.supported_functions = packet.supported_functions
		ack.minor_version = packet.minor_version
		ack.session_id = client.local_session_id
		ack.packet_id = 1
		ack.payload = response
		ack.signature = self.packet_encoder.calc_packet_signature(ack, b"", packet.connection_signature)
		await self.transport.send(ack, addr)
	
	def process_login_request(self, data, client):
		if self.key is None:
			return b""
		
		stream = streams_nex.StreamIn(data, self.settings)
		ticket_data = stream.buffer()
		request_data = stream.buffer()
		
		ticket = kerberos.ServerTicket.decrypt(ticket_data, self.key, self.settings)
		if ticket.timestamp.timestamp() < time.time() - 120:
			raise ValueError("Ticket has expired")
		
		kerb = kerberos.KerberosEncryption(ticket.session_key)
		decrypted = kerb.decrypt(request_data)
		
		if len(decrypted) != self.settings["nex.pid_size"] + 8:
			raise ValueError("Invalid ticket size")
		
		stream = streams_nex.StreamIn(decrypted, self.settings)
		if stream.pid() != ticket.source:
			raise ValueError("Invalid pid in kerberos ticket")
		
		client.login(ticket.source, stream.u32(), ticket.session_key)
		
		check_value = stream.u32()
		return struct.pack("<II", 4, (check_value + 1) & 0xFFFFFFFF)
		
		
class PRUDPClientTransport:
	def __init__(self, settings, socket, group):
		self.settings = settings
		self.socket = socket
		self.group = group
		
		self.ports = PRUDPPortTable(settings)
		self.packet_encoder = PRUDPMessageSelector(settings).select(settings["prudp.version"])
	
	@contextlib.asynccontextmanager
	async def connect(self, port, type=10, credentials=None, *, disconnect_timeout=None):
		client = PRUDPClient(self.settings, self, self.settings["prudp.version"])
		with self.ports.bind(client, type=type) as local_port:
			client.bind(self.socket.local_address(), local_port, type)
			client.connect(self.socket.remote_address(), port, type)
			
			async with util.create_task_group() as group:
				async with client:
					await client.handshake(credentials, group)
					yield client
					with anyio.move_on_after(disconnect_timeout):
						await client.disconnect()
	
	def start(self):
		self.group.start_soon(self.process)
	
	async def process(self):
		while True:
			data = await self.socket.recv()
			await self.process_data(data)
			
	async def process_data(self, data):
		try:
			packets = self.packet_encoder.decode(data)
			for packet in packets:
				await self.process_packet(packet)
		except Exception as e:
			logger.warning("[CLI] An exception occurred while processing a packet: %s" %e)
	
	async def process_packet(self, packet):
		logger.debug("[CLI] Received packet: %s" %packet)
		await self.ports.get(packet.dest_port, packet.dest_type).handle(packet)
			
	async def send(self, packet, addr):
		if addr != self.socket.remote_address():
			raise ValueError("Destination address is invalid")
		
		logger.debug("[CLI] Sending packet: %s" %packet)
		
		data = self.packet_encoder.encode(packet)
		await self.socket.send(data)
	
	def local_address(self): return self.socket.local_address()
	def remote_address(self): return self.socket.remote_address()


class PRUDPServerTransport:
	def __init__(self, settings):
		self.settings = settings
		
		self.ports = PRUDPPortTable(settings)
		self.packet_encoder = PRUDPMessageSelector(settings)
	
	@contextlib.asynccontextmanager
	async def serve(self, handler, port, type=10, key=None, *, disconnect_timeout=None):
		async with util.create_task_group() as group:
			stream = PRUDPServerStream(self.settings, self, handler, key, group, disconnect_timeout)
			with self.ports.bind(stream, port, type) as port:
				stream.bind(self.local_address(), port, type)
				yield
			
	async def send(self, packet, addr):
		logger.debug("[SRV] Sending packet to %s: %s" %(addr, packet))
		
		data = self.packet_encoder.encode(packet)
		await self.sendto(data, addr)
		
	async def process_data(self, data, addr):
		try:
			packets = self.packet_encoder.decode(data)
			for packet in packets:
				await self.process_packet(packet, addr)
		except Exception as e:
			logger.warning("[SRV] An exception occurred while processing a packet: %s" %e)
	
	async def process_packet(self, packet, addr):
		logger.debug("[SRV] Received packet from %s: %s" %(addr, packet))
		await self.ports.get(packet.dest_port, packet.dest_type).handle(packet, addr)


class PRUDPDatagramTransport(PRUDPServerTransport):
	def __init__(self, settings, socket, group):
		super().__init__(settings)
		self.socket = socket
		self.group = group
		
	def start(self):
		self.group.start_soon(self.process)
		
	async def process(self):
		while True:
			data, addr = await self.socket.recv()
			await self.process_data(data, addr)
	
	async def sendto(self, data, addr):
		await self.socket.send(data, addr)
	
	def local_address(self):
		return self.socket.local_address()


class PRUDPSocketTransport(PRUDPServerTransport):
	def __init__(self, settings, addr):
		super().__init__(settings)
		self.clients = {}
		self.addr = addr
	
	async def handle(self, client):
		address = client.remote_address()
		self.clients[address] = client
		try:
			await self.process(client, address)
		finally:
			del self.clients[address]
	
	async def process(self, client, addr):
		while True:
			try:
				data = await client.recv()
			except util.StreamError:
				logger.debug("[SRV] underlying connection was closed")
				return
			
			await self.process_data(data, addr)
	
	async def sendto(self, data, addr):
		if addr not in self.clients:
			raise anyio.BrokenResourceError("Transport connection is closed")
		await self.clients[addr].send(data)
	
	def local_address(self):
		return self.addr


def connect_transport_socket(settings, host, port, context):
	transport = settings["prudp.transport"]
	if transport == settings.TRANSPORT_UDP:
		return udp.connect(host, port)
	elif transport == settings.TRANSPORT_TCP:
		return tls.connect(host, port, context)
	return websocket.connect("%s:%i" %(host, port), context, protocols=["NEX"], disconnect_timeout=0)

def serve_transport_socket(handler, settings, host, port, context):
	transport = settings["prudp.transport"]
	if transport == settings.TRANSPORT_TCP:
		return tls.serve(handler, host, port, context)
	return websocket.serve(handler, host, port, context, protocol="NEX", disconnect_timeout=0)

@contextlib.asynccontextmanager
async def connect_transport(settings, host, port, context=None):
	logger.debug("Connecting PRUDP transport to %s:%i", host, port)
	async with connect_transport_socket(settings, host, port, context) as socket:
		async with util.create_task_group() as group:
			transport = PRUDPClientTransport(settings, socket, group)
			transport.start()
			yield transport

@contextlib.asynccontextmanager
async def serve_transport(settings, host="", port=0, context=None):
	logger.debug("Serving PRUDP transport at %s:%i", host, port)
	transport = settings["prudp.transport"]
	if transport == settings.TRANSPORT_UDP:
		async with udp.bind(host, port) as socket:
			async with util.create_task_group() as group:
				transport = PRUDPDatagramTransport(settings, socket, group)
				transport.start()
				yield transport
	else:
		transport = PRUDPSocketTransport(settings, (host, port))
		async with serve_transport_socket(transport.handle, settings, host, port, context):
			yield transport

@contextlib.asynccontextmanager
async def connect(settings, host, port, vport=1, type=10, context=None, credentials=None, *, disconnect_timeout=None):
	async with connect_transport(settings, host, port, context) as transport:
		async with transport.connect(vport, type, credentials, disconnect_timeout=disconnect_timeout) as client:
			yield client

@contextlib.asynccontextmanager
async def serve(handler, settings, host="", port=0, vport=1, type=10, context=None, key=None, *, disconnect_timeout=None):
	async with serve_transport(settings, host, port, context) as transport:
		async with transport.serve(handler, vport, type, key, disconnect_timeout=disconnect_timeout):
			yield
