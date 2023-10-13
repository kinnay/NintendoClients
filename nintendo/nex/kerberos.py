
from Crypto.Cipher import ARC4
from nintendo.nex import streams
import struct
import secrets
import hashlib
import hmac


class KeyDerivationOld:
	def __init__(self, base_count = 65000, pid_count = 1024):
		self.base_count = base_count
		self.pid_count = pid_count
		
	def derive_key(self, password, pid):
		key = password
		for i in range(self.base_count + pid % self.pid_count):
			key = hashlib.md5(key).digest()
		return key
		
		
class KeyDerivationNew:
	def __init__(self, base_count = 1, pid_count = 1):
		self.base_count = base_count
		self.pid_count = pid_count
		
	def derive_key(self, password, pid):
		key = password
		for i in range(self.base_count):
			key = hashlib.md5(key).digest()
			
		key += struct.pack("<Q", pid)
		for i in range(self.pid_count):
			key = hashlib.md5(key).digest()
			
		return key


class KerberosEncryption:
	def __init__(self, key):
		self.key = key
		
	def check(self, buffer):
		data = buffer[:-0x10]
		checksum = buffer[-0x10:]
		mac = hmac.new(self.key, data, digestmod=hashlib.md5)
		return checksum == mac.digest()
		
	def decrypt(self, buffer):
		if not self.check(buffer):
			raise ValueError("Invalid Kerberos checksum (incorrect password)")
		return ARC4.new(self.key).decrypt(buffer[:-0x10])
		
	def encrypt(self, buffer):
		encrypted = ARC4.new(self.key).encrypt(buffer)
		mac = hmac.new(self.key, encrypted, digestmod=hashlib.md5)
		return encrypted + mac.digest()


class ClientTicket:
	def __init__(self):
		self.session_key = None
		self.target = None
		self.internal = b""
	
	@classmethod
	def decrypt(cls, data, key, settings):
		kerberos = KerberosEncryption(key)
		decrypted = kerberos.decrypt(data)
		stream = streams.StreamIn(decrypted, settings)
		
		ticket = cls()
		ticket.session_key = stream.read(settings["kerberos.key_size"])
		ticket.target = stream.pid()
		ticket.internal = stream.buffer()
		return ticket

	def encrypt(self, key, settings):
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
	def decrypt(cls, data, key, settings):
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

	def encrypt(self, key, settings):
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


class Credentials:
	def __init__(self, ticket, pid, cid):
		self.ticket = ticket
		self.pid = pid
		self.cid = cid
