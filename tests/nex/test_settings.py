from nintendo.nex import settings


def test_constants():
	s = settings.default()
	assert s.TRANSPORT_UDP == 0
	assert s.TRANSPORT_TCP == 1
	assert s.TRANSPORT_WEBSOCKET == 2

	assert s.COMPRESSION_NONE == 0
	assert s.COMPRESSION_ZLIB == 1

	assert s.ENCRYPTION_NONE == 0
	assert s.ENCRYPTION_RC4 == 1


def test_basic():
	s = settings.default()
	assert s["kerberos.key_size"] == 32

	copy = s.copy()

	s["kerberos.key_size"] = 100
	assert s["kerberos.key_size"] == 100
	assert copy["kerberos.key_size"] == 32

	s.reset()
	assert s["kerberos.key_size"] == 32

	s.load("friends")
	assert s["kerberos.key_size"] == 16
