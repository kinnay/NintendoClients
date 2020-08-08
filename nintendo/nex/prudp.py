
from nintendo.common import udp, tls, websocket, socketutils, \
	scheduler, crypto, streams
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


def encode_options(options):
	data = b""
	for k, v in options.items():
		size, name, type = OPTIONS[k]
		data += struct.pack("<BB%s" %type, k, size, v)
	return data

def decode_options(data):
	options = {}
	stream = streams.StreamIn(data)
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
		
		self.source_port = None
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
		self.local_stream_type = settings["prudp.local_stream_type"]
		self.remote_stream_type = settings["prudp.remote_stream_type"]
	
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
		stream = streams.StreamOut()
		stream.u8(packet.source_port | (self.local_stream_type << 4))
		stream.u8(packet.dest_port | (self.remote_stream_type << 4))
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
		
		stream = streams.StreamIn(data)
		while not stream.eof():
			start = stream.tell()
		
			source = stream.u8()
			dest = stream.u8()
			
			if source >> 4 != self.remote_stream_type:
				raise ValueError("(V0) Received packet with invalid source stream type")
			if dest >> 4 != self.local_stream_type:
				raise ValueError("(V0) Received packet with invalid destination stream type")
			
			packet = PRUDPPacket()
			packet.source_port = source & 0xF
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
		self.local_stream_type = settings["prudp.local_stream_type"]
		self.remote_stream_type = settings["prudp.remote_stream_type"]
		
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
		stream = streams.StreamOut()
		stream.u8(1) # PRUDP version
		stream.u8(option_size)
		stream.u16(len(packet.payload))
		stream.u8(packet.source_port | (self.local_stream_type << 4))
		stream.u8(packet.dest_port | (self.remote_stream_type << 4))
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
		
		stream = streams.StreamIn(data)
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
			
			if source >> 4 != self.remote_stream_type:
				raise ValueError("(V1) Received packet with invalid source stream type")
			if dest >> 4 != self.local_stream_type:
				raise ValueError("(V1) Received packet with invalid destination stream type")
			
			packet = PRUDPPacket()
			packet.source_port = source & 0xF
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
		self.local_stream_type = settings["prudp.local_stream_type"]
		self.remote_stream_type = settings["prudp.remote_stream_type"]
		
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
		stream = streams.StreamOut()
		stream.u8(0x80)
		stream.u8(option_size)
		stream.u16(len(packet.payload))
		stream.u8((self.local_stream_type << 4) | self.remote_stream_type)
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
			
			stream = streams.StreamIn(self.buffer)
			if stream.u8() != 0x80:
				raise ValueError("(Lite) Invalid magic number")
			
			option_size = stream.u8()
			payload_size = stream.u16()
			if len(self.buffer) < 12 + option_size + payload_size:
				return packets
			
			self.buffer = self.buffer[12 + option_size + payload_size:]
			
			packet = PRUDPPacket()
			
			stream_types = stream.u8()
			if stream_types >> 4 != self.remote_stream_type:
				raise ValueError("(Lite) Received packet with invalid source stream type")
			if stream_types & 0xF != self.local_stream_type:
				raise ValueError("(Lite) Received packet with invalid destination stream type")
			
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
		

class MessageEncoder:
	def __init__(self, settings):
		if settings["prudp.transport"] == settings.TRANSPORT_UDP:
			if settings["prudp.version"] == 0:
				self.encoder = PRUDPMessageV0(settings)
			else:
				self.encoder = PRUDPMessageV1(settings)
		else:
			self.encoder = PRUDPLiteMessage(settings)
			
	def signature_size(self):
		return self.encoder.signature_size()
	def calc_packet_signature(self, packet, session_key, connection_signature):
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			session_key = b""
			if packet.type == TYPE_SYN:
				connection_signature = b""
		return self.encoder.calc_packet_signature(packet, session_key, connection_signature)
	def calc_connection_signature(self, addr):
		return self.encoder.calc_connection_signature(addr)
	def encode(self, packet):
		return self.encoder.encode(packet)
	def decode(self, data):
		return self.encoder.decode(data)
	
	
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
	def __init__(self, settings, client, group):
		self.fragment_size = settings["prudp.fragment_size"]
		self.max_substream_id = settings["prudp.max_substream_id"]
		self.supported_functions = settings["prudp.supported_functions"]
		self.minor_ver = settings["prudp.minor_version"]
		self.resend_timeout = settings["prudp.resend_timeout"]
		self.resend_limit = settings["prudp.resend_limit"]
		self.ping_timeout = settings["prudp.ping_timeout"]
		self.version = settings["prudp.version"]
		
		self.settings = settings
		self.client = client
		self.group = group
		
		self.payload_encoder = PayloadEncoder(settings)
		self.packet_encoder = MessageEncoder(settings)
		self.sequence_mgr = SequenceMgr(settings)
		
		self.scheduler = scheduler.Scheduler(group)
		self.ack_events = {}
		self.ping_event = None
		
		self.local_port = None
		self.remote_port = None
		
		self.local_session_id = random.randint(0, 0xFF)
		self.remote_session_id = None
		
		self.local_signature = self.packet_encoder.calc_connection_signature(client.remote_address())
		self.remote_signature = None
		
		substreams = self.max_substream_id + 1
		self.sliding_windows = [SlidingWindow() for i in range(substreams)]
		self.fragment_buffers = [b""] * substreams
		
		self.packets = [socketutils.PacketQueue() for i in range(substreams)]
		self.unreliable_packets = socketutils.PacketQueue()
		
		self.credentials = None
		self.server_key = None
		self.session_key = b""
		self.user_pid = None
		self.user_cid = None
		
		self.connection_check = random.randint(0, 0xFFFFFFFF)
		
		self.serving = False
		self.syn_complete = False
		self.connect_ack = None
		self.closing = False
		
		self.handshake = anyio.create_event()
		self.closed = anyio.create_event()
	
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tb):
		if typ is None:
			try:
				await self.close()
			except:
				await self.abort()
				raise
		else:
			await self.abort()
	
	def set_session_key(self, key):
		self.session_key = key
		self.payload_encoder.set_session_key(key)
	
	async def start_handshake(self, vport, credentials):
		self.local_port = 0xF
		if self.settings["prudp.transport"] != self.settings.TRANSPORT_UDP:
			self.local_port = 0x1F
		
		self.remote_port = vport
		
		self.credentials = credentials
		if self.credentials:
			self.user_pid = self.credentials.pid
			self.user_cid = self.credentials.cid
		
		await self.scheduler.start()
		
		syn = PRUDPPacket(TYPE_SYN, FLAG_NEED_ACK)
		syn.connection_signature = bytes(self.packet_encoder.signature_size())
		syn.max_substream_id = self.max_substream_id
		syn.supported_functions = self.supported_functions
		syn.minor_version = self.minor_ver
		await self.send_packet(syn)
		
		await self.group.spawn(self.process)
		
		await self.handshake.wait()
	
	async def accept_handshake(self, vport, key):
		self.serving = True
		
		self.sliding_windows[0].skip()
		
		self.local_port = vport
		self.server_key = key
		
		await self.scheduler.start()
		await self.group.spawn(self.process)
		
		await self.handshake.wait()
	
	async def send(self, data, substream=0):
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
		packet = PRUDPPacket(TYPE_DATA, FLAG_NEED_ACK | FLAG_HAS_SIZE)
		packet.payload = data
		await self.send_packet(packet)
	
	async def send_ping(self):
		packet = PRUDPPacket(TYPE_PING, FLAG_RELIABLE | FLAG_NEED_ACK)
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
		packet.source_port = self.local_port
		packet.dest_port = self.remote_port
		if not packet.flags & FLAG_ACK:
			packet.packet_id = self.sequence_mgr.assign(packet)
		if packet.type != TYPE_SYN:
			packet.session_id = self.local_session_id
		
		if packet.type == TYPE_DATA and not packet.flags & FLAG_ACK:
			packet.payload = self.payload_encoder.encode(packet)
		
		packet.signature = self.packet_encoder.calc_packet_signature(packet, self.session_key, self.remote_signature)
		
		logger.debug("[%i] Sending packet: %s", self.local_session_id, packet)
		
		data = self.packet_encoder.encode(packet)
		await self.client.send(data)
		
		if packet.flags & FLAG_RELIABLE or packet.type == TYPE_SYN:
			if packet.flags & FLAG_NEED_ACK:
				key = (packet.type, packet.substream_id, packet.packet_id)
				handle = await self.scheduler.schedule(self.resend_packet, self.resend_timeout, packet, 0)
				self.ack_events[key] = handle
	
	async def resend_packet(self, packet, counter):
		key = (packet.type, packet.substream_id, packet.packet_id)
		if counter < self.resend_limit:
			logger.debug("[%i] Resending packet: %s", self.local_session_id, packet)
			
			data = self.packet_encoder.encode(packet)
			await self.client.send(data)
			
			handle = await self.scheduler.schedule(self.resend_packet, self.resend_timeout, packet, counter + 1)
			self.ack_events[key] = handle
		else:
			raise ValueError("Packet timed out: %s" %packet)
	
	async def process(self):
		while True:
			try:
				data = await self.client.recv()
			except anyio.exceptions.ClosedResourceError:
				async with anyio.open_cancel_scope(shield=True):
					await self.cleanup()
				return
			
			packets = self.packet_encoder.decode(data)
			for packet in packets:
				logger.debug("[%i] Packet received: %s", self.local_session_id, packet)
				await self.process_packet(packet)
	
	async def process_packet(self, packet):
		if packet.signature != self.packet_encoder.calc_packet_signature(packet, self.session_key, self.local_signature):
			raise ValueError("Received packet with invalid signature")
		if packet.dest_port != self.local_port:
			raise ValueError("Received packet with invalid destination port")
		if self.remote_port is not None and packet.source_port != self.remote_port:
			raise ValueError("Received packet with invalid source port")
		
		if packet.flags & FLAG_ACK:
			key = (packet.type, packet.substream_id, packet.packet_id)
			if key in self.ack_events:
				handle = self.ack_events.pop(key)
				self.scheduler.remove(handle)
		
		if packet.type == TYPE_SYN:
			if packet.flags & FLAG_ACK:
				await self.process_syn_ack(packet)
			else:
				await self.process_syn(packet)
		else:
			if not self.syn_complete:
				print("expected syn")
				raise ValueError("Expected SYN packet")
			if packet.type == TYPE_CONNECT:
				if packet.flags & FLAG_ACK:
					await self.process_connect_ack(packet)
				else:
					await self.process_connect(packet)
			else:
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
					else:
						if packet.type == TYPE_DISCONNECT:
							if self.closing:
								async with anyio.open_cancel_scope(shield=True):
									await self.cleanup()
									await self.client.close()
							else:
								raise ValueError("Received unexpected DISCONNECT/ACK")
	
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
				await self.abort()
	
	def check_syn(self, packet):
		if not self.serving:
			raise ValueError("Received unexpected SYN packet")
		if not packet.flags & FLAG_NEED_ACK:
			raise ValueError("Received SYN packet without FLAG_NEED_ACK")
		if packet.session_id != 0 or packet.packet_id != 0 or packet.fragment_id != 0 or \
		   packet.substream_id != 0 or any(packet.connection_signature):
			raise ValueError("Received invalid SYN packet: %s", packet)
	
	def check_syn_ack(self, packet):
		if self.serving:
			raise ValueError("Received unexpected SYN/ACK packet")
		if packet.session_id != 0 or packet.packet_id != 0 or packet.fragment_id != 0 or packet.substream_id != 0:
			raise ValueError("Received invalid SYN/ACK packet: %s", packet)
		if packet.max_substream_id > self.max_substream_id or \
		   packet.minor_version > self.minor_ver or \
		   packet.supported_functions & ~self.supported_functions != 0:
			raise ValueError("Received SYN/ACK with invalid negotiation parameters")
	
	def check_connect(self, packet):
		if not self.serving:
			raise ValueError("Received unexpected SYN packet")
		if not packet.flags & FLAG_NEED_ACK or packet.packet_id != 1 or \
		   packet.fragment_id != 0 or packet.substream_id != 0:
			raise ValueError("Received invalid CONNECT packet")
		if packet.max_substream_id > self.max_substream_id or \
		   packet.minor_version > self.minor_ver or \
		   packet.supported_functions & ~self.supported_functions != 0:
			raise ValueError("Received CONNECT packet with invalid negotiation parameters")
	
	def check_connect_ack(self, packet):
		if self.serving:
			raise ValueError("Received unexpected CONNECT/ACK packet")
		if packet.packet_id != 1 or packet.fragment_id != 0 or \
		   packet.substream_id != 0 or any(packet.connection_signature):
			raise ValueError("Received invalid CONNECT/ACK packet")
		if packet.max_substream_id != self.max_substream_id or \
		   packet.minor_version != self.minor_ver or \
		   packet.supported_functions != self.supported_functions:
			raise ValueError("Received CONNECT/ACK packet with invalid negotiation parameters")
	
	async def process_syn(self, packet):
		self.check_syn(packet)
		
		self.syn_complete = True
		self.remote_port = packet.source_port
		
		ack = PRUDPPacket(TYPE_SYN, FLAG_ACK)
		ack.connection_signature = self.local_signature
		ack.max_substream_id = min(self.max_substream_id, packet.max_substream_id)
		ack.minor_version = min(self.minor_ver, packet.minor_version)
		ack.supported_functions = self.supported_functions & packet.supported_functions
		await self.send_packet(ack)
	
	async def process_syn_ack(self, packet):
		self.check_syn_ack(packet)
		
		if self.syn_complete:
			logger.debug("Received SYN packet more than once")
			return
	
		self.syn_complete = True
			
		self.max_substream_id = packet.max_substream_id
		self.minor_ver = packet.minor_version
		self.supported_functions = packet.supported_functions
		
		self.remote_signature = packet.connection_signature
		
		connect = PRUDPPacket(TYPE_CONNECT, FLAG_RELIABLE | FLAG_NEED_ACK | FLAG_HAS_SIZE)
		connect.connection_signature = self.local_signature
		connect.initial_unreliable_id = self.sequence_mgr.initial_unreliable_id
		connect.max_substream_id = packet.max_substream_id
		connect.minor_version = packet.minor_version
		connect.supported_functions = packet.supported_functions
		connect.payload = self.build_connection_request()
		await self.send_packet(connect)
	
	async def process_connect(self, packet):
		self.check_connect(packet)
		
		if self.connect_ack:
			logger.debug("Received CONNECT more than once")
			await self.send_packet(self.connect_ack)
			return
		
		response = self.handle_connection_request(packet.payload)
		
		self.max_substream_id = packet.max_substream_id
		self.supported_functions = packet.supported_functions
		self.minor_ver = packet.minor_version
		self.remote_signature = packet.connection_signature
		self.remote_session_id = packet.session_id
		
		ack = PRUDPPacket(TYPE_CONNECT, FLAG_ACK | FLAG_HAS_SIZE)
		ack.connection_signature = bytes(self.packet_encoder.signature_size())
		ack.max_substream_id = self.max_substream_id
		ack.supported_functions = self.supported_functions
		ack.minor_version = self.minor_ver
		ack.payload = response
		ack.packet_id = 1
		
		self.connect_ack = ack
		await self.send_packet(ack)
		
		self.ping_event = await self.scheduler.repeat(self.send_ping, self.ping_timeout)
		await self.handshake.set()
	
	async def process_connect_ack(self, packet):
		self.check_connect_ack(packet)
		self.check_connection_response(packet.payload)
		
		if self.handshake.is_set():
			logger.debug("Received CONNECT/ACK more than once")
			return
		
		self.remote_session_id = packet.session_id
		if self.credentials:
			self.set_session_key(self.credentials.ticket.session_key)
		
		self.ping_event = await self.scheduler.repeat(self.send_ping, self.ping_timeout)
		await self.handshake.set()
	
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
	
	def handle_connection_request(self, data):
		logger.debug("Received connection request: %i bytes", len(data))
		if not self.server_key:
			logger.debug("No validation needed, accepting connection")
			return b""
		
		if not data:
			raise ValueError("Received empty connection request on secure server")
		
		stream = streams_nex.StreamIn(data, self.settings)
		ticket_data = stream.buffer()
		request_data = stream.buffer()
		
		ticket = kerberos.ServerTicket.decrypt(ticket_data, self.server_key, self.settings)
		if ticket.timestamp.timestamp() < time.time() - 120:
			raise ValueError("Ticket has expired")
		
		kerb = kerberos.KerberosEncryption(ticket.session_key)
		decrypted = kerb.decrypt(request_data)
		
		if len(decrypted) != self.settings["nex.pid_size"] + 8:
			raise ValueError("Invalid ticket size")
		
		stream = streams_nex.StreamIn(decrypted, self.settings)
		if stream.pid() != ticket.source:
			raise ValueError("Invalid pid in kerberos ticket")
		
		self.user_pid = ticket.source
		self.user_cid = stream.u32()
		
		check_value = stream.u32()
		
		logger.debug("Connection request was validated successfully")
		self.set_session_key(ticket.session_key)
		
		return struct.pack("<II", 4, (check_value + 1) & 0xFFFFFFFF)
	
	def check_connection_response(self, data):
		logger.debug("Validating connection response")
		if self.credentials:
			if len(data) != 8:
				raise ValueError("Connection response has wrong size")
			
			length, check_value = struct.unpack("<II", data)
			if length != 4:
				raise ValueError("Invalid connection response size")
			if check_value != (self.connection_check + 1) & 0xFFFFFFFF:
				raise ValueError("Connection response check failed")
		elif data:
			raise ValueError("Expected empty connection response")
		logger.debug("Connection response was valid")
	
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
	
	async def recv(self, substream=0):
		return await self.packets[substream].get()
	
	async def recv_unreliable(self):
		return await self.unreliable_packets.get()
	
	async def cleanup(self):
		await self.group.cancel_scope.cancel()
		await self.closed.set()
		for queue in self.packets:
			await queue.close()
		await self.unreliable_packets.close()
	
	async def close(self):
		if not self.closed.is_set():
			logger.debug("[%i] Closing PRUDP connection", self.local_session_id)
			self.closing = True
			
			packet = PRUDPPacket(TYPE_DISCONNECT, FLAG_RELIABLE | FLAG_NEED_ACK)
			await self.send_packet(packet)
			await self.closed.wait()
			logger.debug("PRUDP connection is closed")
	
	async def abort(self):
		async with anyio.open_cancel_scope(shield=True):
			await self.cleanup()
			await self.client.abort()
	
	def pid(self):
		return self.user_pid
	def minor_version(self):
		return self.minor_ver
	
	def local_address(self):
		return self.client.local_address()
	def remote_address(self):
		return self.client.remote_address()


def connect_transport(settings, host, port, context):
	transport = settings["prudp.transport"]
	if transport == settings.TRANSPORT_UDP:
		return udp.connect(host, port)
	elif transport == settings.TRANSPORT_TCP:
		return tls.connect(host, port, context)
	return websocket.connect("NEX", host, port, context)

def serve_transport(handler, settings, host, port, context):
	transport = settings["prudp.transport"]
	if transport == settings.TRANSPORT_UDP:
		return udp.serve(handler, host, port)
	elif transport == settings.TRANSPORT_TCP:
		return tcp.serve(handler, host, port, context)
	return websocket.serve(handler, "NEX", host, port, context)

@contextlib.asynccontextmanager
async def connect(settings, host, port, vport=1, context=None, credentials=None):
	logger.debug("Connecting PRUDP client to %s:%i:%i", host, port, vport)
	async with connect_transport(settings, host, port, context) as client:
		async with anyio.create_task_group() as group:
			async with PRUDPClient(settings, client, group) as client:
				await client.start_handshake(vport, credentials)
				yield client
	logger.debug("PRUDP client is closed")

@contextlib.asynccontextmanager
async def serve(handler, settings, host="", port=0, vport=1, context=None, key=None):
	async def handle(client):
		host, port = client.remote_address()
		
		logger.debug("New PRUDP connection: %s:%i", host, port)
		async with anyio.create_task_group() as group:
			async with PRUDPClient(settings, client, group) as client:
				async with anyio.fail_after(4):
					await client.accept_handshake(vport, key)
				await handler(client)
		
	logger.info("Starting PRUDP server at %s:%i:%i", host, port, vport)
	async with serve_transport(handle, settings, host, port, context):
		yield
	logger.info("PRUDP server is closed")
