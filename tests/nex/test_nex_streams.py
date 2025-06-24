from nintendo.nex import streams, settings, common


class TestStreamOut:
	def test_pid(self):
		stream = streams.StreamOut(settings.default())
		stream.pid(12345)
		assert stream.get() == bytes.fromhex("39300000")

		stream = streams.StreamOut(settings.load("switch"))
		stream.pid(12345)
		assert stream.get() == bytes.fromhex("3930000000000000")

	def test_result(self):
		stream = streams.StreamOut(settings.default())
		stream.result(common.Result.success())
		assert stream.get() == bytes.fromhex("01000100")

	def test_list(self):
		stream = streams.StreamOut(settings.default())
		stream.list([1, 2, 3, 4], stream.u8)
		assert stream.get() == bytes.fromhex("0400000001020304")

	def test_map(self):
		stream = streams.StreamOut(settings.default())
		stream.map({1: 10, 2: 11}, stream.u8, stream.u16)
		assert stream.get() == bytes.fromhex("02000000010a00020b00")

	def test_string(self):
		stream = streams.StreamOut(settings.default())
		stream.string("test string")
		assert stream.get() == b"\x0c\0test string\0"

	def test_stationurl(self):
		stream = streams.StreamOut(settings.default())
		stream.stationurl(common.StationURL("prudps", PID=1, CID=100))
		assert stream.get() == b"\x16\0prudps:/PID=1;CID=100\0"

	def test_datetime(self):
		stream = streams.StreamOut(settings.default())
		stream.datetime(common.DateTime(135605968896))
		assert stream.get() == bytes.fromhex("00e0be921f000000")

	def test_buffer(self):
		stream = streams.StreamOut(settings.default())
		stream.buffer(b"test buffer")
		assert stream.get() == b"\x0b\0\0\0test buffer"

	def test_qbuffer(self):
		stream = streams.StreamOut(settings.default())
		stream.qbuffer(b"test qbuffer")
		assert stream.get() == b"\x0c\0test qbuffer"

	def test_add(self):
		stream = streams.StreamOut(settings.default())
		stream.add(common.ResultRange())
		assert stream.get() == bytes.fromhex("000000000a000000")

		stream = streams.StreamOut(settings.load("switch"))
		stream.add(common.ResultRange())
		assert stream.get() == bytes.fromhex("0008000000000000000a000000")

	def test_anydata(self):
		stream = streams.StreamOut(settings.default())
		stream.anydata(common.NullData())
		assert stream.get() == b"\x09\0NullData\0\x04\0\0\0\0\0\0\0"

		stream = streams.StreamOut(settings.load("switch"))
		stream.anydata(common.NullData())
		assert (
			stream.get() == b"\x09\0NullData\0\x0e\0\0\0\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0"
		)

	def test_variant(self):
		stream = streams.StreamOut(settings.default())
		stream.variant(None)
		assert stream.get() == b"\0"

		stream = streams.StreamOut(settings.default())
		stream.variant(-12345)
		assert stream.get() == bytes.fromhex("01c7cfffffffffffff")

		stream = streams.StreamOut(settings.default())
		stream.variant(123.45)
		assert stream.get() == bytes.fromhex("02cdccccccccdc5e40")

		stream = streams.StreamOut(settings.default())
		stream.variant(True)
		stream.variant(False)
		assert stream.get() == bytes.fromhex("03010300")

		stream = streams.StreamOut(settings.default())
		stream.variant("hello")
		assert stream.get() == b"\x04\x06\0hello\0"

		stream = streams.StreamOut(settings.default())
		stream.variant(common.DateTime.never())
		assert stream.get() == bytes.fromhex("050000000000000000")

		stream = streams.StreamOut(settings.default())
		stream.variant(12345)
		assert stream.get() == bytes.fromhex("063930000000000000")


class TestStreamIn:
	def test_pid(self):
		data = bytes.fromhex("39300000")
		stream = streams.StreamIn(data, settings.default())
		assert stream.pid() == 12345
		assert stream.eof()

		data = bytes.fromhex("3930000000000000")
		stream = streams.StreamIn(data, settings.load("switch"))
		assert stream.pid() == 12345
		assert stream.eof()

	def test_result(self):
		data = bytes.fromhex("01000100")
		stream = streams.StreamIn(data, settings.default())
		assert stream.result().code() == 0x10001

	def test_repeat(self):
		data = bytes.fromhex("0102030400000000140000001400000020000000")
		stream = streams.StreamIn(data, settings.default())

		ints = stream.repeat(stream.u8, 4)
		rrs = stream.repeat(common.ResultRange, 2)
		assert ints == [1, 2, 3, 4]
		assert rrs[0].offset == 0 and rrs[0].size == 20
		assert rrs[1].offset == 20 and rrs[1].size == 32

	def test_list(self):
		data = bytes.fromhex("0400000001020304")
		stream = streams.StreamIn(data, settings.default())
		assert stream.list(stream.u8) == [1, 2, 3, 4]

		data = bytes.fromhex("020000000000000014000000280000003c000000")
		stream = streams.StreamIn(data, settings.default())
		rrs = stream.list(common.ResultRange)
		assert rrs[0].offset == 0 and rrs[0].size == 20
		assert rrs[1].offset == 40 and rrs[1].size == 60

	def test_map(self):
		value = {1: 10, 2: 11}
		data = bytes.fromhex("02000000010a00020b00")
		stream = streams.StreamIn(data, settings.default())
		assert stream.map(stream.u8, stream.u16) == value

		data = bytes.fromhex("01000000393000001400000005000000")
		stream = streams.StreamIn(data, settings.default())
		map = stream.map(stream.pid, common.ResultRange)
		assert map[12345].offset == 20
		assert map[12345].size == 5

	def test_string(self):
		data = b"\x0c\0test string\0"
		stream = streams.StreamIn(data, settings.default())
		assert stream.string() == "test string"

	def test_stationurl(self):
		data = b"\x16\0prudps:/PID=1;CID=100\0"
		stream = streams.StreamIn(data, settings.default())
		url = stream.stationurl()
		assert url.scheme() == "prudps"
		assert url["PID"] == 1
		assert url["CID"] == 100

	def test_datetime(self):
		data = bytes.fromhex("00e0be921f000000")
		stream = streams.StreamIn(data, settings.default())
		assert stream.datetime().value() == 135605968896

	def test_buffer(self):
		data = b"\x0b\0\0\0test buffer"
		stream = streams.StreamIn(data, settings.default())
		assert stream.buffer() == b"test buffer"

	def test_qbuffer(self):
		data = b"\x0c\0test qbuffer"
		stream = streams.StreamIn(data, settings.default())
		assert stream.qbuffer() == b"test qbuffer"

	def test_substream(self):
		data = b"\x08\0\0\0\x64\0\0\0\xc8\0\0\0\xff\0\0\0"
		stream = streams.StreamIn(data, settings.default())
		substream = stream.substream()

		assert stream.u32() == 255
		assert substream.u32() == 100
		assert substream.u32() == 200
		assert substream.eof()

	def test_extract(self):
		data = b"\0\0\0\0\x0a\0\0\0"
		stream = streams.StreamIn(data, settings.default())
		rr = stream.extract(common.ResultRange)
		assert rr.offset == 0
		assert rr.size == 10

		data = b"\0\x08\0\0\0\0\0\0\0\x0a\0\0\0"
		stream = streams.StreamIn(data, settings.load("switch"))
		rr = stream.extract(common.ResultRange)
		assert rr.offset == 0
		assert rr.size == 10

	def test_anydata(self):
		data = b"\x09\0NullData\0\x04\0\0\0\0\0\0\0"
		stream = streams.StreamIn(data, settings.default())
		assert isinstance(stream.anydata(), common.NullData)
		assert stream.eof()

		data = b"\x09\0NullData\0\x0e\0\0\0\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0"
		stream = streams.StreamIn(data, settings.load("switch"))
		assert isinstance(stream.anydata(), common.NullData)
		assert stream.eof()

	def test_variant(self):
		data = b"\0"
		stream = streams.StreamIn(data, settings.default())
		assert stream.variant() is None

		data = bytes.fromhex("01c7cfffffffffffff")
		stream = streams.StreamIn(data, settings.default())
		assert stream.variant() == -12345

		data = bytes.fromhex("02cdccccccccdc5e40")
		stream = streams.StreamIn(data, settings.default())
		assert stream.variant() == 123.45

		data = bytes.fromhex("03010300")
		stream = streams.StreamIn(data, settings.default())
		assert stream.variant() is True
		assert stream.variant() is False

		data = b"\x04\x06\0hello\0"
		stream = streams.StreamIn(data, settings.default())
		assert stream.variant() == "hello"

		data = bytes.fromhex("050000000000000000")
		stream = streams.StreamIn(data, settings.default())
		assert stream.variant().value() == 0

		data = bytes.fromhex("06c7cfffffffffffff")
		stream = streams.StreamIn(data, settings.default())
		assert stream.variant() == 0xFFFFFFFFFFFFCFC7
