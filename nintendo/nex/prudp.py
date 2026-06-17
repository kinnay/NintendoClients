
from Crypto.Cipher import ARC4

from anynet import queue, scheduler, streams, tls, udp, util, websocket
from dataclasses import dataclass
from nintendo.nex import kerberos, settings, streams as streams_nex
from typing import Any, AsyncContextManager, AsyncIterator, Awaitable, \
	Callable, Iterator

import anyio
import anyio.abc
import contextlib
import hashlib
import hmac
import random
import socket
import struct
import time
import typing
import zlib

import logging
logger = logging.getLogger(__name__)


type PRUDPTransport = PRUDPClientTransport | PRUDPServerTransport


TYPE_SYN = 0
TYPE_CONNECT = 1
TYPE_DATA = 2
TYPE_DISCONNECT = 3
TYPE_PING = 4
TYPE_USER = 5
TYPE_ROUTE = 6
TYPE_RAW = 7

FLAG_ACK = 1
FLAG_RELIABLE = 2
FLAG_NEED_ACK = 4
FLAG_HAS_SIZE = 8
FLAG_MULTI_ACK = 0x200

TYPE_NAMES = [
	"TYPE_SYN", "TYPE_CONNECT", "TYPE_DATA", "TYPE_DISCONNECT", "TYPE_PING",
	"TYPE_USER", "TYPE_ROUTE", "TYPE_RAW"
]

FLAG_NAMES = {
	FLAG_ACK: "ACK",
	FLAG_NEED_ACK: "NEED_ACK",
	FLAG_MULTI_ACK: "MULTI_ACK",
	FLAG_RELIABLE: "RELIABLE",
	FLAG_HAS_SIZE: "HAS_SIZE"
}

FLAG_LIST = [
	FLAG_ACK, FLAG_NEED_ACK, FLAG_MULTI_ACK, FLAG_RELIABLE, FLAG_HAS_SIZE
]

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


def encode_options(options: dict[int, int | bytes]) -> bytes:
	data = b""
	for k, v in options.items():
		size, name, type = OPTIONS[k]
		data += struct.pack("<BB%s" %type, k, size, v)
	return data

def decode_options(data: bytes) -> dict[int, Any]:
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
	

@dataclass
class PRUDPPacket:
	type: int = 0
	flags: int = 0
	version: int = 0
	source_type: int = 0
	source_port: int = 0
	dest_type: int = 0
	dest_port: int = 0
	session_id: int = 0
	packet_id: int = 0
	fragment_id: int = 0
	substream_id: int = 0
	connection_signature: bytes = b""
	initial_unreliable_id: int = 0
	max_substream_id: int = 0
	supported_functions: int = 0
	minor_version: int = 0
	signature: bytes = b""
		
	payload: bytes = b""
		
	def __repr__(self) -> str:
		flags = []
		for flag in FLAG_LIST:
			if self.flags & flag:
				flags.append(FLAG_NAMES[flag])
		
		flags_text = ",".join(flags)
		
		return "<PRUDPPacket type=%s flags=%s seq=%i frag=%i>" %(
			TYPE_NAMES[self.type], flags_text, self.packet_id, self.fragment_id
		)
	

class PRUDPMessageEncoder(typing.Protocol):
	def signature_size(self) -> int:
		...
	
	def calc_packet_signature(
		self, packet: PRUDPPacket, session_key: bytes,
		connection_signature: bytes
	) -> bytes:
		...

	def calc_connection_signature(self, addr: tuple[str, int]) -> bytes:
		...

	def encode(self, packet: PRUDPPacket) -> bytes:
		...
	
	def decode(self, data: bytes) -> list[PRUDPPacket]:
		...

		
class PRUDPMessageV0:
	_signature_version: int
	_checksum_version: int
	_flags_version: int

	_access_key: bytes
	
	def __init__(self, settings: settings.Settings):
		self._signature_version = settings["prudp_v0.signature_version"]
		self._checksum_version = settings["prudp_v0.checksum_version"]
		self._flags_version = settings["prudp_v0.flags_version"]
		
		self._access_key = settings["prudp.access_key"].encode()
	
	def signature_size(self) -> int:
		return 4
	
	def calc_checksum(self, data: bytes) -> int:
		checksum = sum(self._access_key)
		if self._checksum_version == 0:
			data = data.ljust((len(data) + 3) & ~3, b"\0")
			words = struct.unpack("<%iI" %(len(data) // 4), data)
			return ((checksum & 0xFF) + sum(words)) & 0xFFFFFFFF

		else:
			words = struct.unpack_from("<%iI" %(len(data) // 4), data)
			temp = sum(words) & 0xFFFFFFFF
			
			checksum += sum(data[len(data) & ~3:])
			checksum += sum(struct.pack("<I", temp))
			return checksum & 0xFF
	
	def calc_data_signature(
		self, packet: PRUDPPacket, session_key: bytes
	) -> bytes:
		data = packet.payload
		if self._signature_version == 0:
			header = struct.pack("<HB", packet.packet_id, packet.fragment_id)
			data = session_key + header + data

		if data:
			key = hashlib.md5(self._access_key).digest()
			digest = hmac.digest(key, data, hashlib.md5)
			return digest[:4]
		return struct.pack("<I", 0x12345678)
		
	def calc_packet_signature(
		self, packet: PRUDPPacket, session_key: bytes,
		connection_signature: bytes
	) -> bytes:
		if packet.type == TYPE_DATA:
			return self.calc_data_signature(packet, session_key)
		if packet.type == TYPE_DISCONNECT and self._signature_version == 0:
			return self.calc_data_signature(packet, session_key)
		if connection_signature:
			return connection_signature
		return bytes(4)
	
	def calc_connection_signature(self, addr: tuple[str, int]) -> bytes:
		data = socket.inet_aton(addr[0]) + struct.pack(">H", addr[1])
		return hashlib.md5(data).digest()[3::-1]
		
	def encode(self, packet: PRUDPPacket) -> bytes:
		stream = streams.StreamOut("<")
		stream.u8(packet.source_port | (packet.source_type << 4))
		stream.u8(packet.dest_port | (packet.dest_type << 4))
		if self._flags_version == 0:
			stream.u8(packet.type | (packet.flags << 3))
		else:
			stream.u16(packet.type | (packet.flags << 4))
		stream.u8(packet.session_id)
		stream.write(packet.signature)
		stream.u16(packet.packet_id)
		self.encode_options(packet, stream)
		stream.write(packet.payload)
		
		data = stream.get()
		if self._checksum_version == 0:
			data += struct.pack("<I", self.calc_checksum(data))
		else:
			data += struct.pack("<B", self.calc_checksum(data))
		return data
	
	def encode_options(
		self, packet: PRUDPPacket, stream: streams.StreamOut
	) -> None:
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			stream.write(packet.connection_signature)
		if packet.type == TYPE_DATA:
			stream.u8(packet.fragment_id)
		if packet.flags & FLAG_HAS_SIZE:
			stream.u16(len(packet.payload))
	
	def decode(self, data: bytes) -> list[PRUDPPacket]:
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
			
			if self._flags_version == 0:
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
				if self._checksum_version == 0:
					payload_size = stream.available() - 4
				else:
					payload_size = stream.available() - 1
			packet.payload = stream.read(payload_size)
			
			# Check packet checksum
			end = stream.tell()
			checksum_data = stream.get()[start : end]
			expected_checksum = self.calc_checksum(checksum_data)
			
			if self._checksum_version == 0:
				checksum = stream.u32()
			else:
				checksum = stream.u8()
				
			if checksum != expected_checksum:
				raise ValueError("(V0) Invalid checksum (expected %i, got %i)" %(expected_checksum, checksum))
			
			# Checksum is good!
			packets.append(packet)
		return packets


class PRUDPMessageV1:
	_access_key: bytes

	def __init__(self, settings: settings.Settings):
		self._access_key = settings["prudp.access_key"].encode()
	
	def signature_size(self) -> int:
		return 16
	
	def calc_packet_signature(
		self, packet: PRUDPPacket, session_key: bytes,
		connection_signature: bytes
	) -> bytes:
		options = self.encode_options(packet)
		header = self.encode_header(packet, len(options))
		
		key = hashlib.md5(self._access_key).digest()
		mac = hmac.new(key, digestmod=hashlib.md5)
		mac.update(header[4:])
		mac.update(session_key)
		mac.update(struct.pack("<I", sum(self._access_key)))
		mac.update(connection_signature)
		mac.update(options)
		mac.update(packet.payload)
		return mac.digest()
		
	def calc_connection_signature(self, addr: tuple[str, int]) -> bytes:
		key = bytes.fromhex("26c31f381e46d6eb38e1af6ab70d11")
		data = socket.inet_aton(addr[0]) + struct.pack(">H", addr[1])
		return hmac.digest(key, data, hashlib.md5)
	
	def encode(self, packet: PRUDPPacket) -> bytes:
		options = self.encode_options(packet)
		header = self.encode_header(packet, len(options))
		return b"\xEA\xD0" + header + packet.signature + options + packet.payload
	
	def encode_header(self, packet: PRUDPPacket, option_size: int) -> bytes:
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
	
	def encode_options(self, packet: PRUDPPacket) -> bytes:
		options: dict[int, int | bytes] = {}
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			options[OPTION_SUPPORT] = packet.minor_version | (packet.supported_functions << 8)
			options[OPTION_CONNECTION_SIG] = packet.connection_signature
			if packet.type == TYPE_CONNECT:
				options[OPTION_UNRELIABLE_SEQ_ID] = packet.initial_unreliable_id
			options[OPTION_MAX_SUBSTREAM_ID] = packet.max_substream_id
		elif packet.type == TYPE_DATA:
			options[OPTION_FRAGMENT_ID] = packet.fragment_id
		return encode_options(options)
		
	def verify_options(
		self, packet: PRUDPPacket, options: dict[int, bytes]
	) -> bool:
		keys = set(options)
		if packet.type == TYPE_SYN:
			return keys == {OPTION_SUPPORT, OPTION_CONNECTION_SIG, OPTION_MAX_SUBSTREAM_ID}
		if packet.type == TYPE_CONNECT:
			return keys == {OPTION_SUPPORT, OPTION_CONNECTION_SIG, OPTION_UNRELIABLE_SEQ_ID, OPTION_MAX_SUBSTREAM_ID}
		if packet.type == TYPE_DATA:
			return keys == {OPTION_FRAGMENT_ID}
		return keys == set()
		
	def decode(self, data: bytes) -> list[PRUDPPacket]:
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
	_access_key: bytes
	_buffer: bytes

	def __init__(self, settings: settings.Settings):
		self._access_key = settings["prudp.access_key"].encode()
		
		self._buffer = b""
		
	def signature_size(self) -> int:
		return 16

	def calc_packet_signature(
		self, packet: PRUDPPacket, session_key: bytes,
		connection_signature: bytes
	) -> bytes:
		if packet.type == TYPE_CONNECT and packet.flags & FLAG_NEED_ACK:
			key = hashlib.md5(self._access_key).digest()
			return hmac.digest(key, key + connection_signature, hashlib.md5)
		return b""
	
	def calc_connection_signature(self, addr: tuple[str, int]) -> bytes:
		key = bytes.fromhex("26c31f381e46d6eb38e1af6ab70d11")
		data = socket.inet_aton(addr[0]) + struct.pack(">H", addr[1])
		return hmac.digest(key, data, hashlib.md5)
	
	def encode(self, packet: PRUDPPacket) -> bytes:
		options = self.encode_options(packet)
		header = self.encode_header(packet, len(options))
		return header + options + packet.payload
	
	def encode_header(self, packet: PRUDPPacket, option_size: int) -> bytes:
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
	
	def encode_options(self, packet: PRUDPPacket) -> bytes:
		options: dict[int, int | bytes] = {}
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			options[OPTION_SUPPORT] = packet.minor_version | (packet.supported_functions << 8)
		if packet.type == TYPE_SYN and packet.flags & FLAG_ACK:
			options[OPTION_CONNECTION_SIG] = packet.connection_signature
		if packet.type == TYPE_CONNECT and not packet.flags & FLAG_ACK:
			options[OPTION_CONNECTION_SIG_LITE] = packet.signature
		return encode_options(options)
	
	def verify_options(
		self, packet: PRUDPPacket, options: dict[int, bytes]
	) -> bool:
		keys = set(options)
		if packet.type in [TYPE_SYN, TYPE_CONNECT]:
			if packet.type == TYPE_SYN and packet.flags & FLAG_ACK:
				return keys == {OPTION_SUPPORT, OPTION_CONNECTION_SIG}
			if packet.type == TYPE_CONNECT and not packet.flags & FLAG_ACK:
				return keys == {OPTION_SUPPORT, OPTION_CONNECTION_SIG_LITE}
			return keys == {OPTION_SUPPORT}
		return keys == set()
	
	def decode(self, data: bytes) -> list[PRUDPPacket]:
		self._buffer += data
		
		packets: list[PRUDPPacket] = []
		while self._buffer:
			if len(self._buffer) < 12: return packets
			
			stream = streams.StreamIn(self._buffer, "<")
			if stream.u8() != 0x80:
				raise ValueError("(Lite) Invalid magic number")
			
			option_size = stream.u8()
			payload_size = stream.u16()
			if len(self._buffer) < 12 + option_size + payload_size:
				return packets
			
			self._buffer = self._buffer[12 + option_size + payload_size:]
			
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
	_settings: settings.Settings

	_v0: PRUDPMessageV0
	_v1: PRUDPMessageV1
	_lite: PRUDPLiteMessage
	
	def __init__(self, settings: settings.Settings):
		self._settings = settings

		self._v0 = PRUDPMessageV0(settings)
		self._v1 = PRUDPMessageV1(settings)
		self._lite = PRUDPLiteMessage(settings)
		
	def select(self, version: int | None) -> PRUDPMessageEncoder:
		if self._settings["prudp.transport"] == self._settings.TRANSPORT_UDP:
			if version == 0:
				return self._v0
			return self._v1
		return self._lite
	
	def analyze(self, data: bytes) -> PRUDPMessageEncoder:
		if self._settings["prudp.transport"] == self._settings.TRANSPORT_UDP:
			if self._settings["prudp.version"] == 2:
				if data[:3] == b"\xEA\xD0\x01":
					return self._v1
				return self._v0
		return self.select(self._settings["prudp.version"])
	
	def signature_size(self, version: int | None = None):
		return self.select(version).signature_size()
	
	def calc_packet_signature(
		self, packet: PRUDPPacket, session_key: bytes,
		connection_signature: bytes
	) -> bytes:
		encoder = self.select(packet.version)
		return encoder.calc_packet_signature(
			packet, session_key, connection_signature
		)
	
	def calc_connection_signature(
		self, addr: tuple[str, int], version: int | None = None
	) -> bytes:
		return self.select(version).calc_connection_signature(addr)

	def encode(self, packet: PRUDPPacket) -> bytes:
		return self.select(packet.version).encode(packet)
	
	def decode(self, data: bytes) -> list[PRUDPPacket]:
		return self.analyze(data).decode(data)
	

class EncryptionAlgorithm(typing.Protocol):
	def set_key(self, key: bytes) -> None: ...
	def encrypt(self, data: bytes) -> bytes: ...
	def decrypt(self, data: bytes) -> bytes: ...


class CompressionAlgorithm(typing.Protocol):
	def compress(self, data: bytes) -> bytes: ...
	def decompress(self, data: bytes) -> bytes: ...


class RC4Encryption:
	def __init__(self, key: bytes):
		self.rc4enc = ARC4.new(key)
		self.rc4dec = ARC4.new(key)
	
	def set_key(self, key: bytes) -> None:
		self.rc4enc = ARC4.new(key)
		self.rc4dec = ARC4.new(key)
		
	def encrypt(self, data: bytes) -> bytes: return self.rc4enc.encrypt(data)
	def decrypt(self, data: bytes) -> bytes: return self.rc4dec.decrypt(data)
	
	
class DummyEncryption:
	def set_key(self, key: bytes) -> None: pass
	def encrypt(self, data: bytes) -> bytes: return data
	def decrypt(self, data: bytes) -> bytes: return data
	
	
class ZlibCompression:
	def compress(self, data: bytes) -> bytes:
		compressed = zlib.compress(data)
		ratio = int(len(data) / len(compressed) + 1)
		return bytes([ratio]) + compressed
		
	def decompress(self, data: bytes) -> bytes:
		if data[0] == 0:
			return data[1:]
		
		decompressed = zlib.decompress(data[1:])
		ratio = int(len(decompressed) / (len(data) - 1) + 1)
		if ratio != data[0]:
			raise ValueError(
				f"Unexpected compression ratio (expected {ratio}, " \
				f"got {data[0]})"
			)
		return decompressed
		
		
class DummyCompression:
	def compress(self, data: bytes) -> bytes: return data
	def decompress(self, data: bytes) -> bytes: return data


class PayloadEncoder:

	DEFAULT_KEY = b"CD&ML"

	_reliable_encryption: list[EncryptionAlgorithm]
	_unreliable_encryption: EncryptionAlgorithm
	_unreliable_key: bytes

	_compression: CompressionAlgorithm

	def __init__(self, settings: settings.Settings):
		substreams = settings["prudp.max_substream_id"] + 1
		
		self._reliable_encryption = [
			self._create_encryption(settings) for i in range(substreams)
		]
		self._unreliable_encryption = self._create_encryption(settings)

		self._unreliable_key = bytes(0x20)
		
		if settings["prudp.compression"] == settings.COMPRESSION_NONE:
			self._compression = DummyCompression()
		else:
			self._compression = ZlibCompression()
			
	def _create_encryption(
		self, settings: settings.Settings
	) -> EncryptionAlgorithm:
		if settings["prudp.transport"] == settings.TRANSPORT_UDP:
			return RC4Encryption(self.DEFAULT_KEY)
		return DummyEncryption()
		
	def encode(self, packet: PRUDPPacket) -> bytes:
		data = packet.payload
		if packet.type == TYPE_DATA and data:
			data = self._compression.compress(data)
			if packet.flags & FLAG_RELIABLE:
				encryption = self._reliable_encryption[packet.substream_id]
			else:
				encryption = self._unreliable_encryption
				encryption.set_key(self._make_unreliable_key(packet))
			data = encryption.encrypt(data)
		return data
	
	def decode(self, packet: PRUDPPacket) -> bytes:
		data = packet.payload
		if packet.type == TYPE_DATA and data:
			if packet.flags & FLAG_RELIABLE:
				encryption = self._reliable_encryption[packet.substream_id]
			else:
				encryption = self._unreliable_encryption
				encryption.set_key(self._make_unreliable_key(packet))
			data = encryption.decrypt(data)
			data = self._compression.decompress(data)
		return data
	
	def _make_unreliable_key(self, packet: PRUDPPacket) -> bytes:
		key = list(self._unreliable_key)
		key[0] = (key[0] + packet.packet_id) & 0xFF
		key[1] = (key[1] + (packet.packet_id >> 8)) & 0xFF
		key[31] = (key[31] + packet.session_id) & 0xFF
		return bytes(key)
		
	def _modify_key(self, key: bytes) -> bytes:
		chars = list(key)
		
		add = len(chars) // 2 + 1
		for i in range(len(chars) // 2):
			chars[i] = (chars[i] + add - i) & 0xFF
		
		return bytes(chars)
		
	def _combine_keys(self, key1: bytes, key2: bytes) -> bytes:
		return hashlib.md5(key1 + key2).digest()
		
	def _init_unreliable_key(self, key: bytes) -> bytes:
		part1 = self._combine_keys(key, bytes.fromhex("18d8233437e4e3fe"))
		part2 = self._combine_keys(key, bytes.fromhex("233e600123cdab80"))
		return part1 + part2
	
	def set_session_key(self, key: bytes) -> None:
		self._reliable_encryption[0].set_key(key)
		
		temp_key = key
		for encryption in self._reliable_encryption[1:]:
			temp_key = self._modify_key(temp_key)
			encryption.set_key(temp_key)
		
		self._unreliable_key = self._init_unreliable_key(key)


class SequenceCounter:
	_next_id: int

	def __init__(self, initial: int = 1):
		self._next_id = initial
	
	def next(self) -> int:
		current = self._next_id
		self._next_id = (self._next_id + 1) & 0xFFFF
		return current
		
		
class SequenceMgr:
	_initial_unreliable_id: int
	_counters: list[SequenceCounter]
	_unreliable_counter: SequenceCounter
	_ping_counter: SequenceCounter
	
	def __init__(self, settings: settings.Settings):	
		substreams = settings["prudp.max_substream_id"] + 1
		
		self._initial_unreliable_id = 1
		if settings["prudp.transport"] == settings.TRANSPORT_UDP:
			if settings["prudp.version"] != 0:
				self._initial_unreliable_id = random.randint(0, 0xFFFF)
		
		self._counters = [SequenceCounter() for i in range(substreams)]
		self._unreliable_counter = SequenceCounter(self._initial_unreliable_id)
		self._ping_counter = SequenceCounter()
	
	def initial_unreliable_id(self) -> int:
		return self._initial_unreliable_id
		
	def assign(self, packet: PRUDPPacket) -> int:
		if packet.flags & FLAG_RELIABLE:
			return self._counters[packet.substream_id].next()
		if packet.type == TYPE_DATA:
			return self._unreliable_counter.next()
		if packet.type == TYPE_PING:
			return self._ping_counter.next()
		return 0


class SlidingWindow:
	_next: int
	_packets: dict[int, PRUDPPacket]
	
	def __init__(self):
		self._next = 1
		self._packets = {}
	
	def skip(self) -> None:
		self._next = (self._next + 1) & 0xFFFF
	
	def update(self, packet):
		packets = []
		if packet.packet_id < self._next or packet.packet_id in self._packets:
			logger.debug("Received duplicate packet: %s", packet)
		else:
			self._packets[packet.packet_id] = packet
			while self._next in self._packets:
				packet = self._packets.pop(self._next)
				packets.append(packet)
				self.skip()
		return packets


class PRUDPClient:
	_fragment_size: int
	_resend_timeout: int
	_resend_limit: int
	_ping_timeout: int
	_max_substream_id: int
	_supported_functions: int
	_minor_ver: int

	_settings: settings.Settings
	_transport: PRUDPTransport
	_version: int

	_packet_encoder: PRUDPMessageEncoder
	_payload_encoder: PayloadEncoder
	_sequence_mgr: SequenceMgr
	
	_sliding_windows: list[SlidingWindow]
	_fragment_buffers: list[bytes]

	_packets: list[queue.Queue[bytes]]
	_unreliable_packets: queue.Queue[bytes]

	_scheduler: scheduler.Scheduler
	_ping_event: int | None
	_ack_events: dict[tuple[int, int, int], int]

	_connection_check: int

	_local_session_id: int
	_remote_session_id: int | None
	_remote_signature: bytes

	_local_addr: tuple[str, int]
	_local_port: int
	_local_type: int

	_remote_addr: tuple[str, int]
	_remote_port: int
	_remote_type: int

	_user_pid: int | None
	_user_cid: int | None
	_session_key: bytes

	_credentials: kerberos.Credentials | None

	_handshake_event: anyio.abc.Event
	_close_event: anyio.abc.Event

	_state: int

	def __init__(
		self, settings: settings.Settings, transport: PRUDPTransport,
		version: int, local_addr: tuple[str, int], local_port: int,
		local_type: int, remote_addr: tuple[str, int], remote_port: int,
		remote_type: int, group: anyio.abc.TaskGroup
	):
		self._fragment_size = settings["prudp.fragment_size"]
		self._resend_timeout = settings["prudp.resend_timeout"]
		self._resend_limit = settings["prudp.resend_limit"]
		self._ping_timeout = settings["prudp.ping_timeout"]
		self._max_substream_id = settings["prudp.max_substream_id"]
		self._supported_functions = settings["prudp.supported_functions"]
		self._minor_ver = settings["prudp.minor_version"]
		
		self._settings = settings
		self._transport = transport
		self._version = version
		
		self._packet_encoder = PRUDPMessageSelector(settings).select(version)
		self._payload_encoder = PayloadEncoder(settings)
		self._sequence_mgr = SequenceMgr(settings)
		
		substreams = self._max_substream_id + 1
		self._sliding_windows = [SlidingWindow() for i in range(substreams)]
		self._fragment_buffers = [b""] * substreams
		
		self._packets = [queue.create() for i in range(substreams)]
		self._unreliable_packets = queue.create()
		
		self._scheduler = scheduler.Scheduler(group)
		self._ping_event = None
		self._ack_events = {}
		
		self._connection_check = random.randint(0, 0xFFFFFFFF)
		
		self._local_session_id = random.randint(0, 0xFF)
		self._remote_session_id = None
		self._remote_signature = b""
		
		self._local_addr = local_addr
		self._local_port = local_port
		self._local_type = local_type
		
		self._remote_addr = remote_addr
		self._remote_port = remote_port
		self._remote_type = remote_type
		
		self._user_pid = None
		self._user_cid = None
		self._session_key = b""
		
		self._credentials = None
		
		self._handshake_event = anyio.Event()
		self._close_event = anyio.Event()
		
		self._state = STATE_CONNECTING
	
	async def __aenter__(self): return self
	async def __aexit__(self, typ, val, tb):
		await self.cleanup()
	
	def login(self, pid: int, cid: int, session_key: bytes):
		self._user_pid = pid
		self._user_cid = cid
		self._session_key = session_key
		
		self._payload_encoder.set_session_key(session_key)
	
	def configure(
		self, max_substream_id: int, supported_functions: int,
		minor_version: int
	) -> None:
		self._max_substream_id = max_substream_id
		self._supported_functions = supported_functions
		self._minor_ver = minor_version
	
	def remote(self, connection_signature: bytes, session_id: int) -> None:
		self._remote_signature = connection_signature
		self._remote_session_id = session_id
		
	async def handshake(self, credentials: kerberos.Credentials | None) -> None:
		self._scheduler.start()
		
		self._credentials = credentials

		if credentials:
			self.login(
				credentials.pid, credentials.cid,
				credentials.ticket.session_key
			)
		
		await self.send_syn()
		await self._handshake_event.wait()
		
		if self._state != STATE_CONNECTED:
			raise RuntimeError("PRUDP connection failed")
		
		self._ping_event = self._scheduler.repeat(
			self.send_ping, self._ping_timeout
		)
	
	async def serve(self) -> None:
		self._state = STATE_CONNECTED
		
		self._sliding_windows[0].skip()
		
		self._scheduler.start()
		
		self._ping_event = self._scheduler.repeat(
			self.send_ping, self._ping_timeout
		)
	
	async def send(self, data: bytes, substream: int = 0) -> None:
		if self._state != STATE_CONNECTED:
			raise anyio.ClosedResourceError("PRUDP connection is closed")
		
		if not 0 <= substream <= self._max_substream_id:
			raise ValueError("Substream id is invalid")
		
		fragment_id = 1
		while data:
			if len(data) <= self._fragment_size:
				fragment_id = 0
			await self.send_fragment(
				data[:self._fragment_size], fragment_id, substream
			)
			data = data[self._fragment_size:]
			fragment_id += 1
	
	async def send_fragment(
		self, data: bytes, fragment_id: int, substream: int
	) -> None:
		packet = PRUDPPacket(TYPE_DATA, FLAG_RELIABLE | FLAG_NEED_ACK | FLAG_HAS_SIZE)
		packet.fragment_id = fragment_id
		packet.substream_id = substream
		packet.payload = data
		await self.send_packet(packet)
	
	async def send_unreliable(self, data: bytes) -> None:
		if self._state != STATE_CONNECTED:
			raise anyio.ClosedResourceError("PRUDP connection is closed")
		
		packet = PRUDPPacket(TYPE_DATA, FLAG_NEED_ACK | FLAG_HAS_SIZE)
		packet.payload = data
		await self.send_packet(packet)
	
	async def send_ping(self) -> None:
		packet = PRUDPPacket(TYPE_PING, FLAG_RELIABLE | FLAG_NEED_ACK)
		await self.send_packet(packet)
	
	async def send_syn(self) -> None:
		packet = PRUDPPacket(TYPE_SYN, FLAG_NEED_ACK)
		packet.connection_signature = \
			bytes(self._packet_encoder.signature_size())
		packet.max_substream_id = self._max_substream_id
		packet.supported_functions = self._supported_functions
		packet.minor_version = self._minor_ver
		await self.send_packet(packet)
	
	async def send_connect(self) -> None:
		connection_signature = \
			self._packet_encoder.calc_connection_signature(self._remote_addr)
		
		packet = PRUDPPacket(
			TYPE_CONNECT, FLAG_RELIABLE | FLAG_NEED_ACK | FLAG_HAS_SIZE
		)
		packet.connection_signature = connection_signature
		packet.initial_unreliable_id = \
			self._sequence_mgr.initial_unreliable_id()
		packet.max_substream_id = self._max_substream_id
		packet.minor_version = self._minor_ver
		packet.supported_functions = self._supported_functions
		packet.payload = self.build_connection_request()
		await self.send_packet(packet)
	
	async def send_ack(self, packet: PRUDPPacket) -> None:
		ack = PRUDPPacket(packet.type, FLAG_ACK)
		ack.packet_id = packet.packet_id
		ack.fragment_id = packet.fragment_id
		ack.substream_id = packet.substream_id
		
		await self.send_packet(ack)
		if packet.type == TYPE_DISCONNECT:
			await self.send_packet(ack)
			await self.send_packet(ack)
	
	async def send_packet(self, packet: PRUDPPacket) -> None:
		packet.version = self._version
		packet.source_port = self._local_port
		packet.source_type = self._local_type
		packet.dest_port = self._remote_port
		packet.dest_type = self._remote_type
		if not packet.flags & (FLAG_ACK | FLAG_MULTI_ACK):
			packet.packet_id = self._sequence_mgr.assign(packet)
		if packet.type != TYPE_SYN:
			packet.session_id = self._local_session_id
		
		if packet.type == TYPE_DATA and not packet.flags & (FLAG_ACK | FLAG_MULTI_ACK):
			packet.payload = self._payload_encoder.encode(packet)
		
		if packet.type == TYPE_SYN:
			packet.signature = self._packet_encoder.calc_packet_signature(packet, b"", b"")
		elif packet.type == TYPE_CONNECT:
			packet.signature = self._packet_encoder.calc_packet_signature(packet, b"", self._remote_signature)
		else:
			packet.signature = self._packet_encoder.calc_packet_signature(packet, self._session_key, self._remote_signature)
		
		try:
			await self._transport.send(packet, self._remote_addr)
		except util.StreamError:
			await self.cleanup()
			return
		
		if (packet.flags & FLAG_RELIABLE or packet.type == TYPE_SYN) and packet.flags & FLAG_NEED_ACK:
			self.schedule_timeout(packet)
			
	async def resend_packet(self, packet: PRUDPPacket, counter: int) -> None:
		key = (packet.type, packet.substream_id, packet.packet_id)
		if counter < self._resend_limit:
			logger.debug("[%i] Resending packet: %s", self._local_session_id, packet)
			
			try:
				await self._transport.send(packet, self._remote_addr)
			except util.StreamError:
				await self.cleanup()
				return
			
			handle = self._scheduler.schedule(
				self.resend_packet, self._resend_timeout, packet, counter + 1
			)
			self._ack_events[key] = handle
		else:
			logger.error(f"Packet timed out: {packet}")
			await self.cleanup()
	
	def schedule_timeout(self, packet: PRUDPPacket) -> None:
		key = (packet.type, packet.substream_id, packet.packet_id)
		handle = self._scheduler.schedule(
			self.resend_packet, self._resend_timeout, packet, 0
		)
		self._ack_events[key] = handle
		
	def build_connection_request(self) -> bytes:
		if self._credentials is None:
			return b""
		
		stream = streams_nex.StreamOut(self._settings)
		stream.buffer(self._credentials.ticket.internal)
		
		substream = streams_nex.StreamOut(self._settings)
		substream.pid(self._credentials.pid)
		substream.u32(self._credentials.cid)
		substream.u32(self._connection_check)
		
		kerb = kerberos.KerberosEncryption(self._credentials.ticket.session_key)
		stream.buffer(kerb.encrypt(substream.get()))
		return stream.get()
	
	def check_connection_response(self, data: bytes) -> None:
		if self._credentials is not None:
			if len(data) != 8:
				raise ValueError("Connection response has wrong size")
			
			length, check_value = struct.unpack("<II", data)
			if length != 4:
				raise ValueError("Invalid connection response size")
			if check_value != (self._connection_check + 1) & 0xFFFFFFFF:
				raise ValueError("Connection response check failed")
		elif data:
			raise ValueError("Expected empty connection response")
		
	async def handle(self, packet: PRUDPPacket) -> None:
		if self._state == STATE_DISCONNECTED: return
		
		if self._state == STATE_CONNECTING and packet.type != TYPE_SYN:
			raise ValueError("Expected SYN packet")
		
		if packet.type == TYPE_SYN:
			await self.process_syn(packet)
		elif packet.type == TYPE_CONNECT:
			await self.process_connect(packet)
		else:
			await self.process_other(packet)
		
		if packet.flags & FLAG_ACK:
			key = (packet.type, packet.substream_id, packet.packet_id)
			if key in self._ack_events:
				handle = self._ack_events.pop(key)
				self._scheduler.remove(handle)
				
				if packet.type == TYPE_DISCONNECT:
					await self.cleanup()
	
	async def process_syn(self, packet: PRUDPPacket) -> None:
		if packet.signature != self._packet_encoder.calc_packet_signature(packet, b"", b""):
			raise ValueError("Received SYN packet with invalid signature")
		if not packet.flags & FLAG_ACK:
			raise ValueError("Received unexpected SYN packet")
		if packet.session_id != 0 or packet.packet_id != 0 or \
		   packet.fragment_id != 0 or packet.substream_id != 0:
			raise ValueError("Received invalid SYN/ACK packet")
		if packet.max_substream_id > self._max_substream_id or \
		   packet.minor_version > self._minor_ver or \
		   packet.supported_functions & ~self._supported_functions:
			raise ValueError("Received SYN/ACK packet with invalid negotiation parameters")
		
		key = (packet.type, packet.substream_id, packet.packet_id)
		if key in self._ack_events:
			self._state = STATE_CONNECTED
			
			self._max_substream_id = packet.max_substream_id
			self._minor_ver = packet.minor_version
			self._supported_functions = packet.supported_functions
			
			self._remote_signature = packet.connection_signature
			
			await self.send_connect()
	
	async def process_connect(self, packet: PRUDPPacket) -> None:
		connection_signature = self._packet_encoder.calc_connection_signature(self._remote_addr)
		if packet.signature != self._packet_encoder.calc_packet_signature(packet, b"", connection_signature):
			raise ValueError("Received CONNECT packet with invalid signature")
		if not packet.flags & FLAG_ACK:
			raise ValueError("Received unexpected CONNECT packet")
		if packet.packet_id != 1 or packet.fragment_id != 0 or \
		   packet.substream_id != 0 or any(packet.connection_signature):
			raise ValueError("Received invalid CONNECT/ACK packet")
		if packet.max_substream_id != self._max_substream_id or \
		   packet.minor_version != self._minor_ver or \
		   packet.supported_functions != self._supported_functions:
			raise ValueError("Received CONNECT/ACK packet with invalid negotiation parameters")
		
		key = (packet.type, packet.substream_id, packet.packet_id)
		if key in self._ack_events:
			self.check_connection_response(packet.payload)
			self._remote_session_id = packet.session_id
			self._handshake_event.set()
	
	async def process_other(self, packet: PRUDPPacket) -> None:
		connection_signature = self._packet_encoder.calc_connection_signature(self._remote_addr)
		if packet.signature != self._packet_encoder.calc_packet_signature(packet, self._session_key, connection_signature):
			raise ValueError("Received packet with invalid signature")
		
		if packet.flags & FLAG_MULTI_ACK:
			self.handle_aggregate_ack(packet)
		else:
			if packet.substream_id > self._max_substream_id:
				raise ValueError("Received packet with invalid substream id: %i", packet.substream_id)
			if packet.session_id != self._remote_session_id:
				raise ValueError("Received packet with invalid session id")
			
			if not packet.flags & FLAG_ACK:
				if packet.flags & FLAG_NEED_ACK:
					await self.send_ack(packet)
				if packet.flags & FLAG_RELIABLE:
					await self.process_reliable(packet)
				else:
					if packet.type == TYPE_DATA:
						data = self._payload_encoder.decode(packet)
						await self._unreliable_packets.put(data)
					elif packet.type == TYPE_DISCONNECT:
						logger.info("Connection closed by other end point (forcefully)")
						await self.cleanup()
	
	async def process_reliable(self, packet: PRUDPPacket) -> None:
		substream = packet.substream_id
		for packet in self._sliding_windows[substream].update(packet):
			if packet.type == TYPE_DATA:
				self._fragment_buffers[substream] += self._payload_encoder.decode(packet)
				if packet.fragment_id == 0:
					await self._packets[substream].put(self._fragment_buffers[substream])
					self._fragment_buffers[substream] = b""
			elif packet.type == TYPE_DISCONNECT:
				logger.info("Connection closed by other end point")
				await self.cleanup()
	
	def is_new_aggregate_ack(self, packet: PRUDPPacket) -> bool:
		if self._settings["prudp.transport"] == self._settings.TRANSPORT_UDP:
			if self._version == 0:
				return False
			return packet.substream_id == 1
		return True
	
	def verify_aggregate_ack(self, packet: PRUDPPacket) -> None:
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
	
	def handle_aggregate_ack(self, packet: PRUDPPacket) -> None:
		self.verify_aggregate_ack(packet)
		if self.is_new_aggregate_ack(packet):
			substream = packet.payload[0]
			base_id = struct.unpack_from("<H", packet.payload, 2)[0]
			extra_ids = struct.unpack_from("<%iH" %packet.payload[1], packet.payload, 4)
		else:
			substream = 0
			base_id = packet.packet_id
			extra_ids = struct.unpack("<%iH" %(len(packet.payload) // 2), packet.payload)
		
		for key in list(self._ack_events):
			if key[0] == TYPE_DATA and key[1] == substream and key[2] <= base_id:
				self._scheduler.remove(self._ack_events.pop(key))
		
		for packet_id in extra_ids:
			key = (TYPE_DATA, substream, packet_id)
			if key in self._ack_events:
				self._scheduler.remove(self._ack_events.pop(key))
				
	async def cleanup(self) -> None:
		self._state = STATE_DISCONNECTED
		self._scheduler.remove_all()
		self._handshake_event.set()
		self._close_event.set()
		for queue in self._packets:
			await queue.eof()
		await self._unreliable_packets.eof()
	
	async def close(self) -> None:
		if self._state == STATE_DISCONNECTED: return
		
		logger.debug("[%i] Closing PRUDP connection forcefully", self._local_session_id)
		
		packet = PRUDPPacket(TYPE_DISCONNECT, 0)
		for i in range(3):
			await self.send_packet(packet)
		await self.cleanup()
	
	async def disconnect(self) -> None:
		if self._state != STATE_CONNECTED: return
		
		try:
			logger.debug("[%i] Closing PRUDP connection", self._local_session_id)
			self._state = STATE_DISCONNECTING
			
			packet = PRUDPPacket(TYPE_DISCONNECT, FLAG_RELIABLE | FLAG_NEED_ACK)
			await self.send_packet(packet)
			await self._close_event.wait()

			logger.debug("PRUDP connection is closed")
		finally:
			await self.cleanup()
	
	async def recv(self, substream: int = 0) -> bytes:
		return await self._packets[substream].get()
	
	async def recv_unreliable(self) -> bytes:
		return await self._unreliable_packets.get()
	
	def pid(self) -> int | None:
		return self._user_pid
	
	def minor_version(self) -> int:
		return self._minor_ver
	
	def local_address(self) -> tuple[str, int]:
		return self._local_addr
	
	def remote_address(self) -> tuple[str, int]:
		return self._remote_addr
		
	def local_sid(self) -> int:
		return self._local_port
	
	def remote_sid(self) -> int:
		return self._remote_port


class PRUDPPortTable[T]:
	_num_ports: int
	_ports: dict[int, T]

	def __init__(self, settings: settings.Settings):
		self._num_ports = 32
		if settings["prudp.transport"] == settings.TRANSPORT_UDP:
			self._num_ports = 16
		self._ports = {}
	
	def __iter__(self):
		return iter(self._ports.values())
	
	def get(self, port: int, type: int) -> T:
		port |= type << 8
		if port not in self._ports:
			raise ValueError("Port is not bound")
		return self._ports[port]
	
	def allocate(self, type: int) -> int:
		for i in reversed(range(self._num_ports)):
			if i | (type << 8) not in self._ports:
				return i
		raise ValueError("All ports are in use")
	
	@contextlib.contextmanager
	def bind(
		self, obj: T, port: int | None = None, type: int = 10
	) -> Iterator[int]:
		if port is None:
			port = self.allocate(type)
		
		port |= type << 8
		if port in self._ports:
			raise ValueError("Port is in use: %i" %port)
		
		self._ports[port] = obj
		try:
			yield port & 0xFF
		finally:
			del self._ports[port]


class PRUDPServerStream:
	_settings: settings.Settings
	_transport: PRUDPServerTransport
	_handler: Callable[[PRUDPClient], Awaitable[None]]
	_key: bytes | None
	_group: anyio.abc.TaskGroup
	_disconnect_timeout: float | None

	_packet_encoder: PRUDPMessageSelector
	
	_supported_functions: int
	_max_substream_id: int
	_minor_ver: int

	_addr: tuple[str, int]
	_port: int
	_type: int

	_clients: dict[tuple[tuple[str, int], int, int], PRUDPClient]

	def __init__(
		self, settings: settings.Settings, transport: PRUDPServerTransport,
		handler: Callable[[PRUDPClient], Awaitable[None]], key: bytes | None,
		group: anyio.abc.TaskGroup, disconnect_timeout: float | None,
		address: tuple[str, int], port: int, type: int
	):
		self._settings = settings
		self._transport = transport
		self._handler = handler
		self._key = key
		self._group = group
		self._disconnect_timeout = disconnect_timeout
		
		self._packet_encoder = PRUDPMessageSelector(settings)
		
		self._supported_functions = settings["prudp.supported_functions"]
		self._max_substream_id = settings["prudp.max_substream_id"]
		self._minor_ver = settings["prudp.minor_version"]
		
		self._addr = address
		self._port = port
		self._type = type
		
		self._clients = {}
	
	def get_client(
		self, packet: PRUDPPacket, addr: tuple[str, int]
	) -> PRUDPClient | None:
		key = (addr, packet.source_port, packet.source_type)
		return self._clients.get(key)
	
	async def start_client(self, client: PRUDPClient) -> None:
		key = (client.remote_address(), client._remote_port, client._remote_type)
		try:
			await self.serve_client(client)
		except Exception as e:
			logger.warning("An exception occurred while serving a client: %s" %e)
		finally:
			del self._clients[key]
	
	async def serve_client(self, client: PRUDPClient) -> None:
		async with client:
			await client.serve()
			await self._handler(client)
			with anyio.move_on_after(self._disconnect_timeout):
				await client.disconnect()
	
	async def handle(self, packet: PRUDPPacket, addr: tuple[str, int]) -> None:
		if packet.type == TYPE_SYN and not packet.flags & FLAG_ACK:
			await self.process_syn(packet, addr)
		elif packet.type == TYPE_CONNECT and not packet.flags & FLAG_ACK:
			await self.process_connect(packet, addr)
		else:
			await self.process_other(packet, addr)
	
	async def process_other(
		self, packet: PRUDPPacket, addr: tuple[str, int]
	) -> None:
		client = self.get_client(packet, addr)
		if client is not None:
			await client.handle(packet)
		else:
			logger.warning("Received unexpected packet: %s", packet)
			
	async def process_syn(
		self, packet: PRUDPPacket, addr: tuple[str, int]
	) -> None:
		if packet.signature != self._packet_encoder.calc_packet_signature(packet, b"", b""):
			raise ValueError("Received packet with invalid signature")
		if not packet.flags & FLAG_NEED_ACK:
			raise ValueError("Received SYN packet without FLAG_NEED_ACK")
		if packet.session_id != 0 or packet.packet_id != 0 or packet.fragment_id != 0 or \
		   packet.substream_id != 0 or any(packet.connection_signature):
			raise ValueError("Received invalid SYN packet: %s" %packet)
		
		ack = PRUDPPacket(TYPE_SYN, FLAG_ACK)
		ack.version = packet.version
		ack.source_type = self._type
		ack.source_port = self._port
		ack.dest_type = packet.source_type
		ack.dest_port = packet.source_port
		ack.connection_signature = self._packet_encoder.calc_connection_signature(addr, ack.version)
		ack.max_substream_id = min(self._max_substream_id, packet.max_substream_id)
		ack.minor_version = min(self._minor_ver, packet.minor_version)
		ack.supported_functions = self._supported_functions & packet.supported_functions
		ack.signature = self._packet_encoder.calc_packet_signature(ack, b"", b"")
		await self._transport.send(ack, addr)
	
	async def process_connect(
		self, packet: PRUDPPacket, addr: tuple[str, int]
	) -> None:
		connection_signature = self._packet_encoder.calc_connection_signature(addr, packet.version)
		if packet.signature != self._packet_encoder.calc_packet_signature(packet, b"", connection_signature):
			raise ValueError("Received packet with invalid signature")
		
		if not packet.flags & FLAG_NEED_ACK or packet.packet_id != 1 or \
		   packet.fragment_id != 0 or packet.substream_id != 0:
			raise ValueError("Received invalid CONNECT packet")
		if packet.max_substream_id > self._max_substream_id or \
		   packet.minor_version > self._minor_ver or \
		   packet.supported_functions & ~self._supported_functions != 0:
			raise ValueError("Received CONNECT packet with invalid negotiation parameters")
		
		key = (addr, packet.source_port, packet.source_type)
		client = self._clients.get(key)
		if client is None:
			client = PRUDPClient(
				self._settings, self._transport, packet.version,
				self._addr, self._port, self._type,
				addr, packet.source_port, packet.source_type,
				self._group
			)
			client.configure(packet.max_substream_id, packet.supported_functions, packet.minor_version)
			client.remote(packet.connection_signature, packet.session_id)
		
		response = self.process_login_request(packet.payload, client)
		
		if key not in self._clients:
			self._clients[key] = client
			self._group.start_soon(self.start_client, client)
		
		ack = PRUDPPacket(TYPE_CONNECT, FLAG_ACK | FLAG_HAS_SIZE)
		ack.version = packet.version
		ack.source_type = self._type
		ack.source_port = self._port
		ack.dest_type = packet.source_type
		ack.dest_port = packet.source_port
		ack.connection_signature = bytes(len(connection_signature))
		ack.max_substream_id = packet.max_substream_id
		ack.supported_functions = packet.supported_functions
		ack.minor_version = packet.minor_version
		ack.session_id = client._local_session_id
		ack.packet_id = 1
		ack.payload = response
		ack.signature = self._packet_encoder.calc_packet_signature(ack, b"", packet.connection_signature)
		await self._transport.send(ack, addr)
	
	def process_login_request(self, data: bytes, client: PRUDPClient) -> bytes:
		if self._key is None:
			return b""
		
		stream = streams_nex.StreamIn(data, self._settings)
		ticket_data = stream.buffer()
		request_data = stream.buffer()
		
		ticket = kerberos.ServerTicket.decrypt(ticket_data, self._key, self._settings)
		if ticket.timestamp.timestamp() < time.time() - 120:
			raise ValueError("Ticket has expired")
		
		kerb = kerberos.KerberosEncryption(ticket.session_key)
		decrypted = kerb.decrypt(request_data)
		
		if len(decrypted) != self._settings["nex.pid_size"] + 8:
			raise ValueError("Invalid ticket size")
		
		stream = streams_nex.StreamIn(decrypted, self._settings)
		if stream.pid() != ticket.source:
			raise ValueError("Invalid pid in kerberos ticket")
		
		client.login(ticket.source, stream.u32(), ticket.session_key)
		
		check_value = stream.u32()
		return struct.pack("<II", 4, (check_value + 1) & 0xFFFFFFFF)
		

class PRUDPClientTransport:
	_settings: settings.Settings
	_socket: udp.UDPClient | tls.TLSClient | websocket.WebSocketClient
	_group: anyio.abc.TaskGroup

	_ports: PRUDPPortTable[PRUDPClient]
	_packet_encoder: PRUDPMessageEncoder

	def __init__(
		self, settings: settings.Settings,
		socket: udp.UDPClient | tls.TLSClient | websocket.WebSocketClient,
		group: anyio.abc.TaskGroup
	):
		self._settings = settings
		self._socket = socket
		self._group = group
		
		self._ports = PRUDPPortTable(settings)
		self._packet_encoder = \
			PRUDPMessageSelector(settings).select(settings["prudp.version"])
	
	@contextlib.asynccontextmanager
	async def connect(
		self, port: int, type: int = 10,
		credentials: kerberos.Credentials | None = None, *,
		disconnect_timeout: float | None = None
	) -> AsyncIterator[PRUDPClient]:
		async with util.create_task_group() as group:
			local_port = self._ports.allocate(type)
			client = PRUDPClient(
				self._settings, self, self._settings["prudp.version"],
				self._socket.local_address(), local_port, type,
				self._socket.remote_address(), port, type, group
			)
			with self._ports.bind(client, local_port, type):
				async with client:
					await client.handshake(credentials)
					yield client
					with anyio.move_on_after(disconnect_timeout):
						await client.disconnect()
	
	def start(self) -> None:
		self._group.start_soon(self._process)
	
	async def _process(self) -> None:
		while True:
			data = await self._socket.recv()
			await self._process_data(data)
			
	async def _process_data(self, data: bytes) -> None:
		try:
			packets = self._packet_encoder.decode(data)
			for packet in packets:
				await self._process_packet(packet)
		except Exception as e:
			logger.warning("[CLI] An exception occurred while processing a packet: %s" %e)
	
	async def _process_packet(self, packet: PRUDPPacket) -> None:
		logger.debug("[CLI] Received packet: %s" %packet)
		await self._ports.get(packet.dest_port, packet.dest_type).handle(packet)
			
	async def send(self, packet: PRUDPPacket, addr: tuple[str, int]) -> None:
		if addr != self._socket.remote_address():
			raise ValueError("Destination address is invalid")
		
		logger.debug("[CLI] Sending packet: %s" %packet)
		
		data = self._packet_encoder.encode(packet)
		await self._socket.send(data)
	
	def local_address(self) -> tuple[str, int]:
		return self._socket.local_address()
	
	def remote_address(self) -> tuple[str, int]:
		return self._socket.remote_address()


class PRUDPServerTransport:
	_settings: settings.Settings

	_ports: PRUDPPortTable[PRUDPServerStream]
	_packet_encoder: PRUDPMessageSelector

	def __init__(self, settings: settings.Settings):
		self._settings = settings
		
		self._ports = PRUDPPortTable(settings)
		self._packet_encoder = PRUDPMessageSelector(settings)
	
	@contextlib.asynccontextmanager
	async def serve(
		self, handler: Callable[[PRUDPClient], Awaitable[None]], port: int,
		type: int = 10, key: bytes | None = None, *,
		disconnect_timeout: float | None = None
	) -> AsyncIterator[None]:
		async with util.create_task_group() as group:
			stream = PRUDPServerStream(
				self._settings, self, handler, key, group, disconnect_timeout,
				self.local_address(), port, type
			)
			with self._ports.bind(stream, port, type):
				yield
			
	async def send(self, packet: PRUDPPacket, addr: tuple[str, int]) -> None:
		logger.debug("[SRV] Sending packet to %s: %s" %(addr, packet))
		
		data = self._packet_encoder.encode(packet)
		await self._sendto(data, addr)
	
	async def _process_data(self, data: bytes, addr: tuple[str, int]) -> None:
		try:
			packets = self._packet_encoder.decode(data)
			for packet in packets:
				await self._process_packet(packet, addr)
		except Exception as e:
			logger.warning("[SRV] An exception occurred while processing a packet: %s" %e)
	
	async def _process_packet(
		self, packet: PRUDPPacket, addr: tuple[str, int]
	) -> None:
		logger.debug("[SRV] Received packet from %s: %s" %(addr, packet))

		stream = self._ports.get(packet.dest_port, packet.dest_type)
		await stream.handle(packet, addr)

	def local_address(self) -> tuple[str, int]:
		raise NotImplementedError(f"{self.__class__.__name__}.local_address()")

	async def _sendto(self, data: bytes, addr: tuple[str, int]) -> None:
		raise NotImplementedError(f"{self.__class__.__name__}._sendto()")


class PRUDPDatagramTransport(PRUDPServerTransport):
	_socket: udp.UDPSocket
	_group: anyio.abc.TaskGroup

	def __init__(
		self, settings: settings.Settings, socket: udp.UDPSocket,
		group: anyio.abc.TaskGroup
	):
		super().__init__(settings)
		self._socket = socket
		self._group = group
	
	def start(self) -> None:
		self._group.start_soon(self._process)
		
	async def _process(self) -> None:
		while True:
			data, addr = await self._socket.recv()
			await self._process_data(data, addr)
	
	async def _sendto(self, data: bytes, addr: tuple[str, int]) -> None:
		await self._socket.send(data, addr)
	
	def local_address(self) -> tuple[str, int]:
		return self._socket.local_address()


class PRUDPSocketTransport(PRUDPServerTransport):
	_clients: dict[tuple[str, int], tls.TLSClient | websocket.WebSocketClient]
	_addr: tuple[str, int]

	def __init__(self, settings: settings.Settings, addr: tuple[str, int]):
		super().__init__(settings)
		self._clients = {}
		self._addr = addr
	
	async def handle(self, client: tls.TLSClient | websocket.WebSocketClient) -> None:
		address = client.remote_address()
		self._clients[address] = client
		try:
			await self._process(client, address)
		finally:
			del self._clients[address]
	
	async def _process(
		self, client: tls.TLSClient | websocket.WebSocketClient,
		addr: tuple[str, int]
	) -> None:
		while True:
			try:
				data = await client.recv()
			except util.StreamError:
				logger.debug("[SRV] underlying connection was closed")
				return
			
			await self._process_data(data, addr)
	
	async def _sendto(self, data: bytes, addr: tuple[str, int]) -> None:
		if addr not in self._clients:
			raise anyio.BrokenResourceError("Transport connection is closed")
		await self._clients[addr].send(data)
	
	def local_address(self) -> tuple[str, int]:
		return self._addr


def connect_transport_socket(
	settings: settings.Settings, host: str, port: int,
	context: tls.TLSContext | None
) -> AsyncContextManager[
	udp.UDPClient | tls.TLSClient | websocket.WebSocketClient
]:
	transport = settings["prudp.transport"]
	if transport == settings.TRANSPORT_UDP:
		return udp.connect(host, port)
	elif transport == settings.TRANSPORT_TCP:
		return tls.connect(host, port, context)
	return websocket.connect("%s:%i" %(host, port), context, protocols=["NEX"], disconnect_timeout=0)

def serve_transport_socket(
	handler: Callable[
		[tls.TLSClient | websocket.WebSocketClient], Awaitable[None]
	],
	settings: settings.Settings,
	host: str, port: int, context: tls.TLSContext | None
) -> AsyncContextManager[None]:
	transport = settings["prudp.transport"]
	if transport == settings.TRANSPORT_TCP:
		return tls.serve(handler, host, port, context)
	return websocket.serve(handler, host, port, context, protocol="NEX", disconnect_timeout=0)

@contextlib.asynccontextmanager
async def connect_transport(
	settings: settings.Settings, host: str, port: int,
	context: tls.TLSContext | None = None
) -> AsyncIterator[PRUDPClientTransport]:
	logger.debug("Connecting PRUDP transport to %s:%i", host, port)
	async with connect_transport_socket(settings, host, port, context) as socket:
		async with util.create_task_group() as group:
			transport = PRUDPClientTransport(settings, socket, group)
			transport.start()
			yield transport

@contextlib.asynccontextmanager
async def serve_transport(
	settings: settings.Settings, host: str = "", port: int = 0,
	context: tls.TLSContext | None = None
) -> AsyncIterator[PRUDPDatagramTransport | PRUDPSocketTransport]:
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
async def connect(
	settings: settings.Settings, host: str, port: int, vport: int = 1,
	type: int = 10, context: tls.TLSContext | None = None,
	credentials: kerberos.Credentials | None = None, *,
	disconnect_timeout: float | None = None
) -> AsyncIterator[PRUDPClient]:
	async with connect_transport(settings, host, port, context) as transport:
		async with transport.connect(vport, type, credentials, disconnect_timeout=disconnect_timeout) as client:
			yield client

@contextlib.asynccontextmanager
async def serve(
	handler: Callable[[PRUDPClient], Awaitable[None]],
	settings: settings.Settings, host: str = "", port: int = 0, vport: int = 1,
	type: int = 10, context: tls.TLSContext | None = None,
	key: bytes | None = None, *, disconnect_timeout: float | None = None
) -> AsyncIterator[None]:
	async with serve_transport(settings, host, port, context) as transport:
		async with transport.serve(handler, vport, type, key, disconnect_timeout=disconnect_timeout):
			yield
