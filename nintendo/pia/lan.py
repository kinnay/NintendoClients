
from Crypto.Cipher import AES
from nintendo.pia.streams import StreamOut, StreamIn
from nintendo.pia.common import ResultRange, Range
from nintendo.pia.station import StationLocation
from nintendo.common.socket import UDPSocket
from nintendo.common import scheduler
import netifaces
import socket
import struct
import secrets
import hashlib
import hmac
import time

import logging
logger = logging.getLogger(__name__)


def default(value, default):
	if value is None:
		return default
	return value

class LanSessionSearchCriteria:
	def __init__(self):
		self.clear()
		
	def clear(self):
		self.min_participants = None
		self.max_participants = None
		self.opened_only = None
		self.vacant_only = None
		self.result_range = ResultRange()
		self.game_mode = None
		self.session_type = None
		self.attributes = [None] * 6
		
	def calc_flags(self):
		flags = 0
		if self.min_participants is not None: flags |= 1
		if self.max_participants is not None: flags |= 2
		if self.opened_only is not None: flags |= 4
		if self.vacant_only is not None: flags |= 8
		if self.game_mode is not None: flags |= 16
		if self.session_type is not None: flags |= 32
		for i in range(6):
			if self.attributes[i] is not None:
				flags |= 64 << i
		return flags
	
	def encode(self, stream):
		if self.min_participants:
			stream.u16(self.min_participants.min)
			stream.u16(self.min_participants.max)
		else:
			stream.u32(0)
			
		if self.max_participants:
			stream.u16(self.max_participants)
			stream.u16(self.max_participants)
		else:
			stream.u32(0)
		
		stream.bool(default(self.opened_only, False))
		stream.bool(default(self.vacant_only, False))
		stream.add(self.result_range)
		stream.u32(default(self.game_mode, 0))
		stream.u32(default(self.session_type, 0))
		
		for attrib in self.attributes:
			if isinstance(attrib, list):
				if len(attrib) > 20:
					raise ValueError("Attribute list may only contain up to 20 values")
				stream.repeat(attrib + [0] * (20 - len(attrib)), stream.u32)
			else:
				stream.repeat([0] * 20, stream.u32)
				
		for attrib in self.attributes:
			if isinstance(attrib, list):
				stream.u8(len(attrib))
			else:
				stream.u8(0)
				
		for attrib in self.attributes:
			if isinstance(attrib, Range):
				stream.u32(attrib.min)
			else:
				stream.u32(0)
		
		for attrib in self.attributes:
			if isinstance(attrib, Range):
				stream.u32(attrib.max)
			else:
				stream.u32(0)
				
		for attrib in self.attributes:
			if isinstance(attrib, Range):
				stream.bool(True)
			else:
				stream.bool(False)
				
		stream.u32(self.calc_flags())
		
	def decode(self, stream):
		self.clear()
		
		min_participants = Range()
		max_participants = Range()
		
		min_participants.min = stream.u16()
		min_participants.max = stream.u16()
		max_participants.min = stream.u16()
		max_participants.max = stream.u16()
		opened_only = stream.bool()
		vacant_only = stream.bool()
		result_range = stream.extract(ResultRange)
		game_mode = stream.u32()
		session_type = stream.u32()
		
		attrib_values = stream.repeat(
			lambda: stream.repeat(stream.u32, 20), 6
		)
		attrib_sizes = stream.repeat(stream.u8, 6)
		attrib_range_min = stream.repeat(stream.u32, 6)
		attrib_range_max = stream.repeat(stream.u32, 6)
		attrib_mode = stream.repeat(stream.bool, 6)
		
		flags = stream.u32()
		if flags & 1: self.min_participants = min_participants
		if flags & 2: self.max_participants = max_participants
		if flags & 4: self.opened_only = opened_only
		if flags & 8: self.vacant_only = vacant_only
		self.result_range = result_range
		if flags & 16: self.game_mode = game_mode
		if flags & 32: self.session_type = session_type
		
		for i in range(6):
			if flags & (64 << i):
				if attrib_mode[i]:
					self.attribs[i] = Range(attrib_range_min[i], attrib_range_max[i])
				else:
					self.attribs[i] = attrib_values[i][:attrib_sizes[i]]
					

class LanStationInfo:

	NONE = 0
	UTF8 = 1
	UTF16 = 2
	
	def __init__(self):
		self.role = 0
		self.encoding = self.UTF8
		self.username = ""
		self.id = 0
		
	def decode(self, stream):
		self.role = stream.u8()
		self.encoding = stream.u8()
		
		username = stream.read(40)
		if self.encoding == self.NONE:
			username = ""
		elif self.encoding == self.UTF8:
			username = username.decode("utf8")
		elif self.encoding == self.UTF16:
			username = username.decode("utf16")
		else:
			raise ValueError("Invalid username encoding: %i" %self.encoding)
		self.username = username.split("\0")[0]
		
		self.id = stream.u64()
		
	def encode(self, stream):
		stream.u8(self.role)
		stream.u8(self.encoding)
		
		if self.encoding == self.UTF8:
			username = self.username.encode("utf8")
		else:
			username = self.username.encode("utf16")
		username = username.ljust(40, b"\0")
		stream.write(username)
		
		stream.u64(self.id)


class LanSessionInfo:
	def __init__(self):
		self.game_mode = None
		self.session_id = None
		self.attributes = [0] * 6
		self.num_participants = 0
		self.min_participants = None
		self.max_participants = None
		self.system_version = None
		self.application_version = None
		self.session_type = None
		self.application_data = b""
		self.is_opened = None
		self.host_location = StationLocation()
		self.stations = [LanStationInfo() for i in range(16)]
		self.session_param = bytes(32)
		
	def encode(self, stream):
		stream.u32(self.game_mode)
		stream.u32(self.session_id)
		stream.repeat(self.attributes, stream.u32)
		stream.u16(self.num_participants)
		stream.u16(self.min_participants)
		stream.u16(self.max_participants)
		stream.u8(self.system_version)
		stream.u8(self.application_version)
		stream.u16(self.session_type)
		stream.write(self.application_data.ljust(0x180, b"\0"))
		stream.u32(len(self.application_data))
		stream.bool(self.is_opened)
		stream.add(self.host_location)
		stream.repeat(self.stations, stream.add)
		stream.write(self.session_param)
		
	def decode(self, stream):
		self.game_mode = stream.u32()
		self.session_id = stream.u32()
		self.attributes = stream.repeat(stream.u32, 6)
		self.num_participants = stream.u16()
		self.min_participants = stream.u16()
		self.max_participants = stream.u16()
		self.system_version = stream.u8()
		self.application_version = stream.u8()
		self.session_type = stream.u16()
		self.application_data = stream.read(0x180)
		self.application_data = self.application_data[:stream.u32()]
		self.is_opened = stream.bool()
		self.host_location = stream.extract(StationLocation)
		self.players = stream.repeat(
			lambda: stream.extract(LanStationInfo), 16
		)
		self.session_param = stream.read(32)

		
class LanBrowser:
	def __init__(self, settings, key):
		self.settings = settings
		self.key = key
		
		self.nonce_counter = 0
		
		self.s = UDPSocket()
		self.s.bind("", 30000)
		
		interface = netifaces.gateways()["default"][netifaces.AF_INET][1]
		addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
		self.broadcast = (addresses["broadcast"], 30000)
		
	def lan_version(self):
		if self.settings.get("pia.version") >= 51800:
			return 2
		return 1
	
	def browse(self, search_criteria, timeout=1, max=0):
		key = secrets.token_bytes(16)
		challenge = secrets.token_bytes(256)
		self.send_browse_request(search_criteria, key, challenge)
		return self.receive_browse_reply(timeout, max, key, challenge)
		
	def generate_nonce(self, counter):
		broadcast = socket.inet_aton(self.broadcast[0])
		return broadcast + struct.pack(">Q", counter)
		
	def generate_challenge_key(self, key):
		aes = AES.new(self.key, AES.MODE_ECB)
		return aes.encrypt(key)
		
	def generate_challenge(self, key, challenge):
		key = self.generate_challenge_key(key)
		nonce = self.generate_nonce(self.nonce_counter)
		
		aes = AES.new(key, AES.MODE_GCM, nonce=nonce)
		ciphertext, tag = aes.encrypt_and_digest(challenge)
		return tag + ciphertext
		
	def generate_challenge_reply(self, nonce, key, challenge):
		key = hmac.new(self.key, key, digestmod=hashlib.sha256).digest()[:16]
		data = hmac.new(self.key, challenge, digestmod=hashlib.sha256).digest()[:16]
		
		aes = AES.new(key, AES.MODE_GCM, nonce=nonce)
		ciphertext, tag = aes.encrypt_and_digest(data)
		return tag + ciphertext
		
	def verify_challenge_reply(self, stream, key, challenge):
		version = stream.u8()
		expected = self.lan_version()
		if version != expected:
			logger.warning("Unexpected version in challenge reply header (%i != %i)", version, expected)
			return False
			
		enabled = stream.bool()
		if not enabled:
			if self.settings.get("pia.crypto_required"):
				logger.warning("Crypto is required but received challenge reply with crypto disabled")
				return False
			return True
		
		nonce_counter = stream.u64()
		key = stream.read(16) + key
		reply = stream.read(32)
		
		nonce = self.generate_nonce(nonce_counter)
		expected = self.generate_challenge_reply(nonce, key, challenge)
		
		if reply != expected:
			logger.warning("Incorrect challenge reply received")
			return False
		return True
	
	def send_browse_request(self, search_criteria, key, challenge):
		stream = StreamOut(self.settings)
		stream.add(search_criteria)
		buffer = stream.get()
		
		stream = StreamOut(self.settings)
		stream.u8(0) #Packet type
		stream.u32(len(buffer))
		stream.write(buffer)
		
		self.nonce_counter += 1
		
		stream.u8(self.lan_version())
		stream.bool(self.settings.get("pia.crypto_enabled"))
		stream.u64(self.nonce_counter)
		stream.write(key)
		
		if self.settings.get("pia.crypto_enabled"):
			challenge = self.generate_challenge(key, challenge)
		else:
			challenge = secrets.token_bytes(16 + 256)
		stream.write(challenge)
		
		self.s.send(stream.get(), self.broadcast)
		
	def parse_browse_reply(self, data, key, challenge):
		stream = StreamIn(data, self.settings)
		if stream.u8() != 1:
			return None
		
		size = stream.u32()
		session_end = stream.tell() + size
		
		try:
			session_info = stream.extract(LanSessionInfo)
		except Exception as e:
			logger.warning("Failed to parse LanSessionInfo: %s", e)
			return None
			
		if stream.tell() != session_end:
			logger.warning("LanSessionInfo has unexpected size")
			return None
		
		if not self.verify_challenge_reply(stream, key, challenge):
			return None
		return session_info
		
	def receive_browse_reply(self, timeout, max, key, challenge):
		sessions = []
		ids = []
		
		start = time.monotonic()
		while time.monotonic() - start < timeout:
			result = self.s.recv()
			if result:
				data, addr = result
				session = self.parse_browse_reply(data, key, challenge)
				if session and session.session_id not in ids:
					ids.append(session.session_id)
					sessions.append(session)
			scheduler.update()
		
		return sessions
