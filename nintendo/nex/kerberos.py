
from nintendo.common import crypto
import hmac


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
			raise ValueError("Invalid Kerberos checksum")
		return self.rc4.crypt(buffer[:-0x10])
		
	def encrypt(self, buffer):
		encrypted = self.rc4.crypt(buffer)
		mac = hmac.HMAC(self.key, encrypted)
		return encrypted + mac.digest()


class Ticket:
	def __init__(self, key, data):
		self.key = key
		self.data = data
