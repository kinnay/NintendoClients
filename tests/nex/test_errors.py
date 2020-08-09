
from nintendo.nex import errors

def test_basic():
	assert errors.error_names[0x10001] == "Core::Unknown"
	assert errors.error_codes["Core::Unknown"] == 0x10001
