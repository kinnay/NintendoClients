
from nintendo.nex import kerberos, settings, common

def test_key_derivation_old():
	keyderiv1 = kerberos.KeyDerivationOld()
	keyderiv2 = kerberos.KeyDerivationOld(5, 10)
	assert keyderiv1.derive_key(b"password", 123456) == bytes.fromhex("bd9d83b0d4102b72de3e14f44938c989")
	assert keyderiv2.derive_key(b"password", 123456) == bytes.fromhex("6ba537f0cc7e0d25813f2ea010eb2115")

def test_key_derivation_new():
	keyderiv1 = kerberos.KeyDerivationNew()
	keyderiv2 = kerberos.KeyDerivationNew(5, 10)
	assert keyderiv1.derive_key(b"password", 123456) == bytes.fromhex("591b45defe20abcd6ec412b63fbacff5")
	assert keyderiv2.derive_key(b"password", 123456) == bytes.fromhex("09409830bf949ab56fae81bd028fe18d")

def test_kerberos_encryption():
	kerb = kerberos.KerberosEncryption(b"key")
	
	data = kerb.encrypt(b"test message")
	assert data == bytes.fromhex("7f09479904e21e393b2a6f1ed5b96acc69a869dce66679d0cedb242d")
	assert kerb.check(data)
	assert not kerb.check(b"\x7e" + data[1:])
	assert kerb.decrypt(data) == b"test message"

def test_client_ticket():
	ticket = kerberos.ClientTicket()
	ticket.session_key = bytes(range(32))
	ticket.internal = b"internal buffer"
	ticket.target = 123456
	
	s = settings.default()
	data = ticket.encrypt(b"key", s)
	ticket = kerberos.ClientTicket.decrypt(data, b"key", s)
	
	assert ticket.session_key == bytes(range(32))
	assert ticket.internal == b"internal buffer"
	assert ticket.target == 123456
	
def test_server_ticket():
	ticket = kerberos.ServerTicket()
	ticket.timestamp = common.DateTime.fromtimestamp(1596279690)
	ticket.session_key = bytes(range(32))
	ticket.source = 123456
	
	s = settings.default()
	data = ticket.encrypt(b"key", s)
	ticket = kerberos.ServerTicket.decrypt(data, b"key", s)
	assert ticket.timestamp.timestamp() == 1596279690
	assert ticket.session_key == bytes(range(32))
	assert ticket.source == 123456

def test_credentials():
	ticket = kerberos.ClientTicket()
	creds = kerberos.Credentials(ticket, 1000, 2000)
	assert creds.ticket == ticket
	assert creds.pid == 1000
	assert creds.cid == 2000
