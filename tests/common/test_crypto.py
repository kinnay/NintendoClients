
from nintendo.common import crypto


KEY = b"Simple is better than complex."
PLAIN = b"Complex is better than complicated."
CIPHER = bytes.fromhex("6371ec07e1d7f0b1d142e0bb48b6117ac73901af340e32b90d234c0c2ded402d8ef76b")


class TestRC4:
	def test_encrypt(self):
		rc4 = crypto.RC4(KEY)
		assert rc4.crypt(PLAIN) == CIPHER

	def test_decrypt(self):
		rc4 = crypto.RC4(KEY)
		assert rc4.crypt(CIPHER) == PLAIN
		
	def test_stream(self):
		rc4 = crypto.RC4(KEY)
		assert rc4.crypt(PLAIN[:15]) == CIPHER[:15]
		assert rc4.crypt(PLAIN[15:]) == CIPHER[15:]
		
	def test_reset(self):
		rc4 = crypto.RC4(KEY, True)
		assert rc4.crypt(PLAIN) == CIPHER
		assert rc4.crypt(PLAIN) == CIPHER
		
		rc4 = crypto.RC4(KEY, False)
		assert rc4.crypt(PLAIN) == CIPHER
		rc4.reset()
		assert rc4.crypt(PLAIN) == CIPHER
		
	def test_set_key(self):
		rc4 = crypto.RC4(b"a" * 16)
		assert rc4.crypt(PLAIN) != CIPHER
		
		rc4.set_key(KEY)
		assert rc4.crypt(PLAIN) == CIPHER
