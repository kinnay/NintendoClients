
from nintendo.nex import common
from nintendo.pia import types

def test_range():
	r = types.Range()
	assert r.min == 0
	assert r.max == 10
	
	assert 0 in r
	assert 10 in r
	assert 11 not in r
	assert -1 not in r
	
	r = types.Range(1, 20)
	assert r.min == 1
	assert r.max == 20
	
	assert 0 not in r
	assert 10 in r
	assert 11 in r
	assert 20 in r


def test_result_range():
	r = types.ResultRange()
	assert r.offset == 0
	assert r.size == 10
	
	r = types.ResultRange(5, 20)
	assert r.offset == 5
	assert r.size == 20


def test_inet_address():
	addr = types.InetAddress()
	assert addr.host == "0.0.0.0"
	assert addr.port == 0
	
	addr = types.InetAddress("127.0.0.1", 30000)
	assert addr.host == "127.0.0.1"
	assert addr.port == 30000


def test_station_address():
	addr = types.StationAddress()
	assert addr.inet.host == "0.0.0.0"
	assert addr.inet.port == 0
	assert addr.extension_id == 0
	
	addr = types.StationAddress("127.0.0.1", 30000)
	assert addr.inet.host == "127.0.0.1"
	assert addr.inet.port == 30000


def test_station_location():
	loc = types.StationLocation()
	assert isinstance(loc.public, types.StationAddress)
	assert isinstance(loc.local, types.StationAddress)
	assert isinstance(loc.relay, types.InetAddress)
	assert loc.pid == 0
	assert loc.cid == 0
	assert loc.rvcid == 0
	assert loc.scheme == 0
	assert loc.sid == 0
	assert loc.stream_type == 0
	assert loc.natm == 0
	assert loc.natf == 0
	assert loc.type == 3
	assert loc.probeinit == 0
	
	copy = loc.copy()
	
	loc.scheme = 3
	loc.pid = 100
	url = loc.get_station_url()
	assert url["PID"] == 100
	assert url.scheme() == "udp"
	
	assert copy.scheme == 0
	assert copy.pid == 0
	
	url = common.StationURL(natm=1, natf=2, type=5)
	loc.set_station_url(url)
	assert loc.scheme == 1
	assert loc.natm == 1
	assert loc.natf == 2
	assert loc.type == 5
