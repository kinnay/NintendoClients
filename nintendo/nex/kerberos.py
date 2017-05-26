
from nintendo.common.crypto import RC4
import hmac


class KerberosEncryption:
	def __init__(self, key):
		self.key = key
		self.rc4 = RC4(key)
		
	def decrypt(self, buffer):
		data = buffer[:-0x10] #Remove checksum
		return self.rc4.crypt(data)
		
	def encrypt(self, buffer):
		encrypted = self.rc4.crypt(buffer)
		mac = hmac.HMAC(self.key)
		mac.update(encrypted)
		return encrypted + mac.digest()


class Ticket:
	def __init__(self, key, data):
		self.key = key
		self.data = data
