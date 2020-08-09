
from nintendo import switch

def test_ndaserror():
	error = switch.NDASError(200)
	assert isinstance(error, Exception)
	assert error.status_code == 200
	assert error.errors is None

def test_b64encode():
	assert switch.b64encode(b"\xFE\xFF\xFE\xFF") == "_v_-_w"

def test_b64decode():
	assert switch.b64decode("_v_-_w") == b"\xFE\xFF\xFE\xFF"
