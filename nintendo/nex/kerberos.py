
from Crypto.Cipher import ARC4
from dataclasses import dataclass
from nintendo.nex import settings, streams
from typing import Self

import hashlib
import hmac
import secrets
import struct


class KeyDerivationOld:
	_base_count: int
	_pid_count: int

	def __init__(self, base_count: int = 65000, pid_count: int = 1024):
		self._base_count = base_count
		self._pid_count = pid_count
		
	def derive_key(self, password: bytes, pid: int) -> bytes:
		key = password
		for i in range(self._base_count + pid % self._pid_count):
			key = hashlib.md5(key).digest()
		return key
		
		
class KeyDerivationNew:
	_base_count: int
	_pid_count: int

	def __init__(self, base_count: int = 1, pid_count: int = 1):
		self._base_count = base_count
		self._pid_count = pid_count
	
	def derive_key(self, password: bytes, pid: int) -> bytes:
		key = password
		for i in range(self._base_count):
			key = hashlib.md5(key).digest()
			
		key += struct.pack("<Q", pid)
		for i in range(self._pid_count):
			key = hashlib.md5(key).digest()
			
		return key


class KerberosEncryption:
	_key: bytes

	def __init__(self, key: bytes):
		self._key = key
		
	def check(self, buffer: bytes) -> bool:
		data = buffer[:-0x10]
		checksum = buffer[-0x10:]
		mac = hmac.digest(self._key, data, "md5")
		return checksum == mac
		
	def decrypt(self, buffer: bytes) -> bytes:
		if not self.check(buffer):
			raise ValueError("Invalid Kerberos checksum (incorrect password)")
		return ARC4.new(self._key).decrypt(buffer[:-0x10])
		
	def encrypt(self, buffer: bytes) -> bytes:
		encrypted = ARC4.new(self._key).encrypt(buffer)
		mac = hmac.digest(self._key, encrypted, "md5")
		return encrypted + mac


class ClientTicket:
	def __init__(self):
		self.session_key = None
		self.target = None
		self.internal = b""
	
	@classmethod
	def decrypt(
		cls, data: bytes, key: bytes, settings: settings.Settings
	) -> Self:
		kerberos = KerberosEncryption(key)
		decrypted = kerberos.decrypt(data)

		stream = streams.StreamIn(decrypted, settings)
		
		ticket = cls()
		ticket.session_key = stream.read(settings["kerberos.key_size"])
		ticket.target = stream.pid()
		ticket.internal = stream.buffer()
		return ticket

	def encrypt(self, key: bytes, settings: settings.Settings) -> bytes:
		stream = streams.StreamOut(settings)
		if settings["kerberos.key_size"] != len(self.session_key):
			raise ValueError("Incorrect session_key size")
		stream.write(self.session_key)
		stream.pid(self.target)
		stream.buffer(self.internal)

		data = stream.get()
		kerberos = KerberosEncryption(key)
		return kerberos.encrypt(data)
		
		
class ServerTicket:
	def __init__(self):
		self.timestamp = None
		self.source = None
		self.session_key = None
	
	@classmethod
	def decrypt(
		cls, data: bytes, key: bytes, settings: settings.Settings
	) -> Self:
		if settings["kerberos.ticket_version"] == 1:
			stream = streams.StreamIn(data, settings)
			ticket_key = stream.buffer()
			data = stream.buffer()
			key = hashlib.md5(key + ticket_key).digest()

		kerberos = KerberosEncryption(key)
		decrypted = kerberos.decrypt(data)
		
		stream = streams.StreamIn(decrypted, settings)
		
		ticket = cls()
		ticket.timestamp = stream.datetime()
		ticket.source = stream.pid()
		ticket.session_key = stream.read(settings["kerberos.key_size"])
		return ticket

	def encrypt(self, key: bytes, settings: settings.Settings) -> bytes:
		stream = streams.StreamOut(settings)
		stream.datetime(self.timestamp)
		stream.pid(self.source)
		if len(self.session_key) != settings["kerberos.key_size"]:
			raise ValueError("Incorrect session_key length")
		stream.write(self.session_key)

		data = stream.get()
		if settings["kerberos.ticket_version"] == 1:
			ticket_key = secrets.token_bytes(16)
			final_key = hashlib.md5(key + ticket_key).digest()

			kerberos = KerberosEncryption(final_key)
			encrypted = kerberos.encrypt(data)
			
			stream = streams.StreamOut(settings)
			stream.buffer(ticket_key)
			stream.buffer(encrypted)
			return stream.get()
		
		kerberos = KerberosEncryption(key)
		encrypted = kerberos.encrypt(data)
		return encrypted


@dataclass
class Credentials:
	ticket: ClientTicket
	pid: int
	cid: int
