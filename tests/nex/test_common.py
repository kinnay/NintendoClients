from nintendo.nex import common
import pytest


def test_result():
	result = common.Result.success()
	assert result.is_success()
	assert not result.is_error()
	assert result.code() == 0x10001
	assert result.name() == "success"
	result.raise_if_error()

	result = common.Result.success(0x1000A)
	assert result.code() == 0x1000A
	assert result.name() == "success"

	result = common.Result.error("Core::InvalidArgument")
	assert not result.is_success()
	assert result.is_error()
	assert result.code() == 0x8001000A
	assert result.name() == "Core::InvalidArgument"

	with pytest.raises(common.RMCError):
		result.raise_if_error()


def test_rmcerror():
	error = common.RMCError()
	assert error.name() == "Core::Unknown"
	assert error.code() == 0x80010001

	result = common.RMCError().result()
	assert result.is_error()
	assert result.name() == "Core::Unknown"
	assert result.code() == 0x80010001

	result = common.RMCError("Core::InvalidArgument").result()
	assert result.name() == "Core::InvalidArgument"
	assert result.code() == 0x8001000A

	result = common.RMCError(0x8001000A).result()
	assert result.name() == "Core::InvalidArgument"
	assert result.code() == 0x8001000A


def test_resultrange():
	rr = common.ResultRange()
	assert rr.offset == 0
	assert rr.size == 10

	rr = common.ResultRange(50, 100)
	assert rr.offset == 50
	assert rr.size == 100


class TestStationURL:
	def test_repr(self):
		url = common.StationURL(PID=12345)
		assert repr(url) == "prudp:/PID=12345"

	def test_parse(self):
		url = common.StationURL.parse("prudp:/PID=12345")
		assert repr(url) == "prudp:/PID=12345"

	def test_parse_empty(self):
		url = common.StationURL.parse("")
		assert repr(url) == "prudp:/"

	def test_getitem(self):
		url = common.StationURL.parse("prudp:/address=1.2.3.4;port=12345")
		assert url["address"] == "1.2.3.4"
		assert url["port"] == 12345
		assert url["PID"] == 0
		with pytest.raises(KeyError):
			url["test"]

	def test_setitem(self):
		url = common.StationURL.parse("prudp:/address=1.2.3.4;port=12345")
		url["port"] = 12346
		url["natf"] = 1
		assert url["port"] == 12346
		assert url["natf"] == 1

	def test_scheme(self):
		url = common.StationURL.parse("prudps:/PID=100")
		assert url.scheme() == "prudps"

	def test_address(self):
		url = common.StationURL.parse("prudp:/address=1.2.3.4;port=12345")
		assert url.address() == ("1.2.3.4", 12345)

	def test_flags(self):
		url = common.StationURL(type=3)
		assert url.is_public()
		assert url.is_behind_nat()
		assert not url.is_global()

		url = common.StationURL(type=2)
		assert url.is_public()
		assert not url.is_behind_nat()
		assert url.is_global()


class TestDateTime:
	def test_value(self):
		datetime = common.DateTime(135593643393)
		assert datetime.value() == 135593643393

	def test_datetime(self):
		datetime = common.DateTime(135593643393)
		assert datetime.second() == 1
		assert datetime.minute() == 54
		assert datetime.hour() == 12
		assert datetime.day() == 1
		assert datetime.month() == 8
		assert datetime.year() == 2020

	def test_standard_datetime(self):
		import datetime

		dt = common.DateTime(135593643393).standard_datetime()
		assert dt == datetime.datetime(
			2020, 8, 1, 12, 54, 1, tzinfo=datetime.timezone.utc
		)

	def test_timestamp(self):
		datetime = common.DateTime(135593643393)
		assert datetime.timestamp() == 1596279241

	def test_make(self):
		datetime = common.DateTime.make(2020, 10, 31, 14)
		assert datetime.timestamp() == 1604149200

	def test_fromtimestamp(self):
		datetime = common.DateTime.fromtimestamp(1604149200)
		assert datetime.value() == 135605968896

	def test_now(self):
		datetime = common.DateTime.now()
		assert datetime.year() >= 2020

	def test_never(self):
		datetime = common.DateTime.never()
		assert datetime.value() == 0

	def test_future(self):
		datetime = common.DateTime.future()
		assert datetime.value() == 0x9C3F3F7EFB
