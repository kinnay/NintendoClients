
from nintendo.common import crypto
from nintendo.nex import streams
import struct
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


class Ticket:
	def __init__(self, encrypted):
		self.encrypted = encrypted
		
		self.session_key = None
		self.target_pid = None
		self.internal = None
		
		self.source_pid = None
		self.target_cid = None
		
	def decrypt(self, key, settings):
		kerberos = KerberosEncryption(key)
		decrypted = kerberos.decrypt(self.encrypted)
		stream = streams.StreamIn(decrypted, settings)
		self.session_key = stream.read(settings.get("kerberos.key_size"))
		self.target_pid = stream.pid()
		self.internal = stream.buffer()
