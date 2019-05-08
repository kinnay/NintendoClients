
from nintendo.common import crypto
from nintendo.nex import streams
import struct
import secrets
import hashlib
import hmac


class KeyDerivationOld:
	def __init__(self, base_count, pid_count):
		self.base_count = base_count
		self.pid_count = pid_count
		
	def derive_key(self, password, pid):
		key = password
		for i in range(self.base_count + pid % self.pid_count):
			key = hashlib.md5(key).digest()
		return key
		
		
class KeyDerivationNew:
	def __init__(self, base_count, pid_count):
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
		self.rc4 = crypto.RC4(key, True)
		
	def check_hmac(self, buffer):
		data = buffer[:-0x10]
		checksum = buffer[-0x10:]
		mac = hmac.HMAC(self.key, data)
		return checksum == mac.digest()
		
	def decrypt(self, buffer):
		if not self.check_hmac(buffer):
			raise ValueError("Invalid Kerberos checksum (incorrect password)")
		return self.rc4.crypt(buffer[:-0x10])
		
	def encrypt(self, buffer):
		encrypted = self.rc4.crypt(buffer)
		mac = hmac.HMAC(self.key, encrypted)
		return encrypted + mac.digest()


class ClientTicket:
	def __init__(self):
		self.session_key = None
		self.target_pid = None
		self.internal = b""
		
		self.source_pid = None
		self.target_cid = None
		
	def decrypt(self, data, key, settings):
		kerberos = KerberosEncryption(key)
		decrypted = kerberos.decrypt(data)
		stream = streams.StreamIn(decrypted, settings)
		self.session_key = stream.read(settings.get("kerberos.key_size"))
		self.target_pid = stream.pid()
		self.internal = stream.buffer()

	def encrypt(self, key, settings):
		stream = streams.StreamOut(settings)
		if settings.get("kerberos.key_size") != len(self.session_key):
			raise ValueError("Incorrect session_key size")
		stream.write(self.session_key)
		stream.pid(self.target_pid)
		stream.buffer(self.internal)

		data = stream.get()
		kerberos = KerberosEncryption(key)
		return kerberos.encrypt(data)
		
		
class ServerTicket:
	def __init__(self):
		self.expiration = None
		self.source_pid = None
		self.session_key = None
		
	def decrypt(self, data, key, settings):
		stream = streams.StreamIn(self.encrypted, settings)
		ticket_key = stream.buffer()
		ticket_body = stream.buffer()
		final_key = hashlib.md5(key + ticket_key).digest()

		kerberos = KerberosEncryption(final_key)
		decrypted = kerberos.decrypt(ticket_body)
		
		stream = streams.StreamIn(decrypted, settings)
		self.expiration = stream.datetime()
		self.source_pid = stream.pid()
		self.session_key = stream.read(settings.get("kerberos.key_size"))

	def encrypt(self, key, settings):
		ticket_key = secrets.token_bytes(16)
		
		stream = streams.StreamOut(settings)
		stream.datetime(self.expiration)
		stream.pid(self.source_pid)
		if len(self.session_key) != settings.get("kerberos.key_size"):
			raise ValueError("Incorrect session_key length")
		stream.write(self.session_key)

		ticket_body = stream.get()

		final_key = hashlib.md5(key + ticket_key).digest()

		kerberos = KerberosEncryption(final_key)
		encrypted = kerberos.encrypt(ticket_body)

		stream = streams.StreamOut(settings)
		stream.buffer(ticket_key)
		stream.buffer(encrypted)
		return stream.get()
