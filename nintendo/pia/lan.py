
from Crypto.Cipher import AES
from nintendo.pia import streams, types
from anynet import udp, util
import contextlib
import itertools
import secrets
import hashlib
import socket
import struct
import anyio
import hmac

import logging
logger = logging.getLogger(__name__)


nonce_counter = itertools.count()


def encrypt_key(kek, key):
	aes = AES.new(kek, AES.MODE_ECB)
	return aes.encrypt(key)

def generate_nonce(nonce_id):
	addr = util.broadcast_address()
	return struct.pack(">IQ", util.ip_to_hex(addr), nonce_id)

def generate_challenge_reply(game_key, challenge_key, challenge_data, nonce):
	key = hmac.digest(game_key, challenge_key, hashlib.sha256)[:16]
	data = hmac.digest(game_key, challenge_data, hashlib.sha256)[:16]
	
	aes = AES.new(key, AES.MODE_GCM, nonce=nonce)
	ciphertext, tag = aes.encrypt_and_digest(data)
	return tag + ciphertext

def make_browse_request(settings, search_criteria, game_key, challenge_key, challenge_data):
	stream = streams.StreamOut(settings)
	stream.add(search_criteria)
	buffer = stream.get()
	
	stream = streams.StreamOut(settings)
	stream.u8(0) #Packet type
	stream.u32(len(buffer))
	stream.write(buffer)
	
	if settings["pia.lan_version"] != 0:
		nonce_id = next(nonce_counter)
		stream.u8(settings["pia.lan_version"])
		stream.bool(game_key is not None)
		stream.u64(nonce_id)
		stream.write(challenge_key)
		
		if game_key is not None:
			key = encrypt_key(game_key, challenge_key)
			nonce = generate_nonce(nonce_id)
			
			aes = AES.new(key, AES.MODE_GCM, nonce=nonce)
			ciphertext, tag = aes.encrypt_and_digest(challenge_data)
			challenge = tag + ciphertext
		else:
			challenge = secrets.token_bytes(16 + 256)
		stream.write(challenge)
	return stream.get()

def verify_challenge_reply(stream, game_key, challenge_key, challenge_data):
	if stream.settings["pia.lan_version"] == 0:
		return True
	
	version = stream.u8()
	expected = stream.settings["pia.lan_version"]
	if version != expected:
		logger.warning("Unexpected version in challenge reply header (%i != %i)", version, expected)
		return False
		
	enabled = stream.bool()
	if enabled and game_key is None:
		logger.warning("Received encrypted challenge reply but no game key was provided")
		return False
	
	if not enabled:
		stream.skip(8 + 16 + 32)
		return True
	
	nonce_id = stream.u64()
	key = stream.read(16) + challenge_key
	reply = stream.read(32)
	
	nonce = generate_nonce(nonce_id)
	expected = generate_challenge_reply(game_key, key, challenge_data, nonce)
	
	if reply != expected:
		logger.warning("Incorrect challenge reply received")
		return False
	return True

def parse_browse_reply(settings, data, game_key, challenge_key, challenge_data):
	stream = streams.StreamIn(data, settings)
	if stream.u8() != 1:
		logger.warning("Received packet that is not a browse reply")
		return None
	
	size = stream.u32()
	data = stream.read(size)
	
	if not verify_challenge_reply(stream, game_key, challenge_key, challenge_data):
		return None
	
	if not stream.eof():
		logger.warning("Browse reply is bigger than expected")
		return None
	
	stream = streams.StreamIn(data, settings)
	try:
		session_info = stream.extract(LanSessionInfo)
	except Exception as e:
		logger.warning("Failed to parse LanSessionInfo: %s", e)
		return None
	
	if not stream.eof():
		logger.warning("LanSessionInfo has unexpected size")
		return None
	
	return session_info
	

def default(value, default):
	if value is None:
		return default
	return value

class LanSessionSearchCriteria:
	def __init__(self):
		self.reset()
		
	def reset(self):
		self.min_participants = None
		self.max_participants = None
		self.opened_only = None
		self.vacant_only = None
		self.result_range = types.ResultRange()
		self.game_mode = None
		self.session_type = None
		self.attributes = [None] * 6
		
	def check(self, info):
		if self.min_participants is not None:
			if info.min_participants not in self.min_participants:
				logger.info("Search criteria miss: min_participants")
				return False
		if self.max_participants is not None:
			if info.max_participants not in self.max_participants:
				logger.info("Search criteria miss: max_participants")
				return False
		if self.opened_only and not info.is_opened:
			logger.info("Search criteria miss: session is not opened")
			return False
		if self.vacant_only and info.num_participants >= info.max_participants:
			logger.info("Search criteria miss: session is full")
			return False
		if self.game_mode is not None and self.game_mode != info.game_mode:
			logger.info("Search criteria miss: different game mode")
			return False
		if self.session_type is not None and self.session_type != info.session_type:
			logger.info("Search criteria miss: different session type")
			return False
		for i in range(6):
			if self.attributes[i] is not None:
				if info.attributes[i] not in self.attributes[i]:
					logger.info("Search criteria miss: different attributes")
					return False
		return True
		
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
			stream.u16(self.min_participants.max)
			stream.u16(self.min_participants.min)
		else:
			stream.u32(0)
			
		if self.max_participants:
			stream.u16(self.max_participants.max)
			stream.u16(self.max_participants.min)
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
			if isinstance(attrib, types.Range):
				stream.u32(attrib.min)
			else:
				stream.u32(0)
		
		for attrib in self.attributes:
			if isinstance(attrib, types.Range):
				stream.u32(attrib.max)
			else:
				stream.u32(0)
				
		for attrib in self.attributes:
			if isinstance(attrib, types.Range):
				stream.bool(True)
			else:
				stream.bool(False)
				
		stream.u32(self.calc_flags())
		
	def decode(self, stream):
		self.reset()
		
		min_participants = types.Range()
		max_participants = types.Range()
		
		min_participants.max = stream.u16()
		min_participants.min = stream.u16()
		max_participants.max = stream.u16()
		max_participants.min = stream.u16()
		opened_only = stream.bool()
		vacant_only = stream.bool()
		result_range = stream.extract(types.ResultRange)
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
					self.attributes[i] = types.Range(attrib_range_min[i], attrib_range_max[i])
				else:
					self.attributes[i] = attrib_values[i][:attrib_sizes[i]]
					

class LanStationInfo:

	NONE = 0
	UTF8 = 1
	UTF16 = 2
	
	HOST = 1
	PLAYER = 2
	
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
		self.host_location = types.StationLocation()
		self.stations = [LanStationInfo() for i in range(16)]
		self.session_param = bytes(32)
	
	def get_session_key(self, key):
		param = self.session_param
		param = param[:31] + bytes([(param[31] + 1) & 0xFF])
		return hmac.digest(key, param, hashlib.sha256)
		
	def encode(self, stream):
		if len(self.attributes) != 6: raise ValueError("Attributes must contain exactly 6 integers")
		if len(self.stations) != 16:
			raise ValueError("Session must contain exactly 16 station entries")
		
		stream.u32(self.game_mode)
		stream.u32(self.session_id)
		stream.repeat(self.attributes, stream.u32)
		stream.u16(self.num_participants)
		stream.u16(self.min_participants)
		stream.u16(self.max_participants)
		if stream.settings["pia.version"] < 503:
			stream.u32(self.session_type)
		else:
			stream.u8(self.system_version)
			stream.u8(self.application_version)
			stream.u16(self.session_type)
		stream.write(self.application_data.ljust(0x180, b"\0"))
		stream.u32(len(self.application_data))
		stream.bool(self.is_opened)
		if stream.settings["pia.version"] < 510:
			stream.add(self.host_location)
		else:
			type = types.InetAddress.IPV4
			if stream.settings["pia.lan_version"] == 2:
				type = types.InetAddress.IPV6
			stream.add(self.host_location.local, type)
			stream.pid(self.host_location.pid)
			stream.u32(self.host_location.cid)
			stream.u32(self.host_location.rvcid)
		stream.repeat(self.stations, stream.add)
		if stream.settings["pia.lan_version"] >= 1:
			stream.write(self.session_param)
		
	def decode(self, stream):
		self.game_mode = stream.u32()
		self.session_id = stream.u32()
		self.attributes = stream.repeat(stream.u32, 6)
		self.num_participants = stream.u16()
		self.min_participants = stream.u16()
		self.max_participants = stream.u16()
		if stream.settings["pia.version"] < 503:
			self.session_type = stream.u32()
		else:
			self.system_version = stream.u8()
			self.application_version = stream.u8()
			self.session_type = stream.u16()
		self.application_data = stream.read(0x180)
		self.application_data = self.application_data[:stream.u32()]
		self.is_opened = stream.bool()
		if stream.settings["pia.version"] < 510:
			self.host_location = stream.extract(types.StationLocation)
		else:
			type = types.InetAddress.IPV4
			if stream.settings["pia.lan_version"] == 2:
				type = types.InetAddress.IPV6
			self.host_location = types.StationLocation()
			self.host_location.local = stream.extract(types.StationAddress, type)
			self.host_location.pid = stream.pid()
			self.host_location.cid = stream.u32()
			self.host_location.rvcid = stream.u32()
		self.players = stream.repeat(
			lambda: stream.extract(LanStationInfo), 16
		)
		if stream.settings["pia.lan_version"] >= 1:
			self.session_param = stream.read(32)


class LanServer:
	def __init__(self, settings, handler, key, sock, group):
		self.settings = settings
		self.handler = handler
		self.game_key = key
		self.sock = sock
		self.group = group
	
	def start(self):
		self.group.start_soon(self.process)
	
	async def process(self):
		while True:
			data, addr = await self.sock.recv()
			await self.process_request(data, addr)
	
	async def process_request(self, data, addr):
		stream = streams.StreamIn(data, self.settings)
		if stream.u8() != 0:
			logger.debug("Message is not a browse request")
			return
		
		size = stream.u32()
		end = stream.tell() + size
		
		criteria = stream.extract(LanSessionSearchCriteria)
		if stream.tell() != end:
			logger.warning("LanSessionSearchCriteria has unexpected size")
			return
		
		challenge_response = self.process_challenge(stream)
		if challenge_response is None:
			return
		
		if not stream.eof():
			logger.warning("Browse request is bigger than expected")
			return
		
		logger.info("Received browse request")
		
		sessions = []
		for session in self.handler():
			if criteria.check(session):
				sessions.append(session)
		
		logger.info("%i sessions match search criteria", len(sessions))
		for session in sessions:
			data = self.make_browse_reply(session, challenge_response)
			await self.sock.send(data, addr)
	
	def make_browse_reply(self, session_info, challenge):
		stream = streams.StreamOut(self.settings)
		stream.add(session_info)
		buffer = stream.get()
		
		stream = streams.StreamOut(self.settings)
		stream.u8(1) #Packet type
		stream.u32(len(buffer))
		stream.write(buffer)
		
		if self.settings["pia.lan_version"] != 0:
			stream.u8(self.settings["pia.lan_version"])
			stream.bool(self.game_key is not None)
			stream.write(challenge)
		
		return stream.get()
	
	def process_challenge(self, stream):
		if self.settings["pia.lan_version"] == 0:
			return b""
		
		version = stream.u8()
		if version != self.settings["pia.lan_version"]:
			logger.warning("Browse request has unexpected version number")
			return None
		
		crypto = stream.bool()
		if crypto and self.game_key is None:
			logger.warning("Received crypto challenge but no game key was provided")
			return None
		
		nonce_id = stream.u64()
		key = stream.read(16)
		
		tag = stream.read(16)
		challenge = stream.read(256)
		
		if crypto:
			challenge_key = encrypt_key(self.game_key, key)
			nonce = generate_nonce(nonce_id)
			
			aes = AES.new(challenge_key, AES.MODE_GCM, nonce=nonce)
			try:
				challenge = aes.decrypt_and_verify(challenge, tag)
			except ValueError:
				logger.warning("Challenge has incorrect authentication tag")
				return None
			
			new_key = secrets.token_bytes(16)
			nonce_id = next(nonce_counter)
			nonce = generate_nonce(nonce_id)
			
			response = struct.pack(">Q", nonce_id) + new_key
			response += generate_challenge_reply(self.game_key, new_key + key, challenge, nonce)
		else:
			response = secrets.token_bytes(16 + 16 + 16)
		return response


async def browse(settings, search_criteria, key=None, timeout=1, max=0):
	challenge_key = secrets.token_bytes(16)
	challenge_data = secrets.token_bytes(256)
	async with udp.bind(broadcast=True) as sock:
		request = make_browse_request(settings, search_criteria, key, challenge_key, challenge_data)
		await sock.send(request, (util.broadcast_address(), 30000))
		
		sessions = []
		ids = []
		with anyio.move_on_after(timeout):
			while max == 0 or len(sessions) < max:
				data, addr = await sock.recv()
				session = parse_browse_reply(settings, data, key, challenge_key, challenge_data)
				if session and session.session_id not in ids:
					ids.append(session.session_id)
					sessions.append(session)
	return sessions

@contextlib.asynccontextmanager
async def serve(settings, handler, key=None):
	async with udp.bind("0.0.0.0", 30000) as sock:
		async with util.create_task_group() as group:
			server = LanServer(settings, handler, key, sock, group)
			server.start()
			yield server
