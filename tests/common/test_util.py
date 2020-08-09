
from nintendo.common import util
import pytest

def test_ip_to_hex():
	assert util.ip_to_hex("192.168.178.188") == 0xC0A8B2BC
	
	with pytest.raises(ValueError):
		util.ip_to_hex("")
	with pytest.raises(ValueError):
		util.ip_to_hex("192.168.178.256")
	with pytest.raises(ValueError):
		util.ip_to_hex("a.b.c.d")
	with pytest.raises(ValueError):
		util.ip_to_hex("1.1.1.")

def test_is_hexadecimal():
	assert util.is_hexadecimal("0")
	assert util.is_hexadecimal("ABCDEF")
	assert util.is_hexadecimal("c0a8b2bc")
	assert util.is_hexadecimal("0A1b2C3d")
	assert not util.is_hexadecimal("")
	assert not util.is_hexadecimal("ABCDEFG")
	assert not util.is_hexadecimal("0x12345")
	assert not util.is_hexadecimal("1.2")
	
def test_local_address():
	addr = util.local_address()
	util.ip_to_hex(addr) # Raises exception if ip address is invalid

def test_broadcast_address():
	addr = util.local_address()
	util.ip_to_hex(addr) # Raises exception if ip address is invalid
