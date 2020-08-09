
from nintendo.common import streams
import pytest


class TestStreamOut:
	def test_get(self):
		stream = streams.StreamOut()
		assert stream.get() == b""
		
	def test_write(self):
		stream = streams.StreamOut()
		stream.write(b"Hello")
		stream.write(b"World")
		assert stream.get() == b"HelloWorld"
	
	def test_size(self):
		stream = streams.StreamOut()
		assert stream.size() == 0
		stream.write(b"HelloWorld")
		assert stream.size() == 10
	
	def test_seek(self):
		stream = streams.StreamOut()
		stream.write(b"HelloWorld")
		stream.seek(5)
		stream.write(b"WORLD")
		assert stream.get() == b"HelloWORLD"
		
		stream.seek(12)
		assert stream.get() == b"HelloWORLD\0\0"
	
	def test_tell(self):
		stream = streams.StreamOut()
		assert stream.tell() == 0
		stream.write(b"HelloWorld")
		assert stream.tell() == 10
		
	def test_pushpop(self):
		stream = streams.StreamOut()
		stream.write(b"Hello")
		stream.push()
		stream.write(b"World")
		stream.pop()
		stream.write(b"WORLD")
		assert stream.get() == b"HelloWORLD"
	
	def test_skip(self):
		stream = streams.StreamOut()
		stream.write(b"HelloWorld")
		stream.seek(8)
		stream.skip(4)
		assert stream.get() == b"HelloWorld\0\0"
		
	def test_align(self):
		stream = streams.StreamOut()
		stream.write(b"HelloWorld")
		stream.align(5)
		assert stream.tell() == 10
		stream.align(6)
		assert stream.tell() == 12
		assert stream.get() == b"HelloWorld\0\0"
		
	def test_available(self):
		stream = streams.StreamOut()
		assert stream.available() == 0
		stream.write(b"HelloWorld")
		assert stream.available() == 0
		stream.seek(5)
		assert stream.available() == 5

	def test_eof(self):
		stream = streams.StreamOut()
		assert stream.eof()
		stream.write(b"HelloWorld")
		assert stream.eof()
		stream.seek(5)
		assert not stream.eof()
		
	def test_pad(self):
		stream = streams.StreamOut()
		stream.pad(4)
		stream.pad(4, b"\xFF")
		assert stream.get() == b"\0\0\0\0\xFF\xFF\xFF\xFF"
		
	def test_ascii(self):
		stream = streams.StreamOut()
		stream.ascii("HelloWorld")
		assert stream.get() == b"HelloWorld"
	
	def test_uint(self):
		stream = streams.StreamOut()
		stream.u8(0x7F)
		stream.u16(0x8000)
		stream.u24(0xFFFFFF)
		stream.u32(0)
		stream.u64(0x123456789ABCDEF)
		assert stream.get() == b"\x7F\x00\x80\xFF\xFF\xFF\0\0\0\0\xEF\xCD\xAB\x89\x67\x45\x23\x01"
		
	def test_sint(self):
		stream = streams.StreamOut()
		stream.s8(0x7F)
		stream.s16(-0x8000)
		stream.s32(-1)
		stream.s64(0x123456789ABCDEF)
		assert stream.get() == b"\x7F\x00\x80\xFF\xFF\xFF\xFF\xEF\xCD\xAB\x89\x67\x45\x23\x01"
		
	def test_float(self):
		stream = streams.StreamOut()
		stream.float(0)
		stream.float(2)
		stream.double(-2)
		assert stream.get() == b"\0\0\0\0\0\0\0\x40\0\0\0\0\0\0\0\xC0"
		
	def test_endian(self):
		stream = streams.StreamOut("<")
		stream.u32(0x12345678)
		assert stream.get() == b"\x78\x56\x34\x12"
		
		stream = streams.StreamOut(">")
		stream.u32(0x12345678)
		assert stream.get() == b"\x12\x34\x56\x78"
		
	def test_bool(self):
		stream = streams.StreamOut()
		stream.bool(True)
		stream.bool(False)
		assert stream.get() == b"\x01\x00"
	
	def test_char(self):
		stream = streams.StreamOut()
		stream.char("H")
		stream.wchar("W")
		assert stream.get() == b"HW\0"
	
	def test_chars(self):
		stream = streams.StreamOut()
		stream.chars("Hello")
		stream.wchars("World")
		assert stream.get() == b"HelloW\0o\0r\0l\0d\0"
	
	def test_repeat(self):
		stream = streams.StreamOut()
		stream.repeat([1, 2, 3], stream.u16)
		assert stream.get() == b"\x01\x00\x02\x00\x03\x00"
		
		
class TestStreamIn:
	def test_get(self):
		stream = streams.StreamIn(b"HelloWorld")
		assert stream.get() == b"HelloWorld"
	
	def test_size(self):
		stream = streams.StreamIn(b"HelloWorld")
		assert stream.size() == 10
		
	def test_peek(self):
		stream = streams.StreamIn(b"HelloWorld")
		assert stream.peek(5) == b"Hello"
		assert stream.peek(10) == b"HelloWorld"
		with pytest.raises(OverflowError):
			stream.peek(11)
		
	def test_read(self):
		stream = streams.StreamIn(b"HelloWorld")
		assert stream.read(5) == b"Hello"
		assert stream.read(5) == b"World"
		with pytest.raises(OverflowError):
			stream.read(1)
			
	def test_seek(self):
		stream = streams.StreamIn(b"HelloWorld")
		assert stream.read(10) == b"HelloWorld"
		stream.seek(5)
		assert stream.read(5) == b"World"
		stream.seek(10)
		
		with pytest.raises(OverflowError):
			stream.seek(11)
	
	def test_skip(self):
		stream = streams.StreamIn(b"HelloWorld")
		stream.skip(2)
		assert stream.read(5) == b"lloWo"
		
		stream.skip(3)
		with pytest.raises(OverflowError):
			stream.skip(1)
	
	def test_tell(self):
		stream = streams.StreamIn(b"HelloWorld")
		assert stream.tell() == 0
		stream.skip(5)
		assert stream.tell() == 5
	
	def test_pushpop(self):
		stream = streams.StreamIn(b"HelloWorld")
		stream.seek(5)
		stream.push()
		assert stream.read(5) == b"World"
		stream.pop()
		assert stream.read(5) == b"World"

	def test_align(self):
		stream = streams.StreamIn(b"HelloWorld")
		stream.align(100)
		assert stream.tell() == 0
		
		stream.skip(1)
		stream.align(4)
		assert stream.tell() == 4
		assert stream.read(5) == b"oWorl"
		
	def test_available(self):
		stream = streams.StreamIn(b"HelloWorld")
		assert stream.available() == 10
		stream.skip(5)
		assert stream.available() == 5
		stream.seek(2)
		assert stream.available() == 8
		
	def test_eof(self):
		stream = streams.StreamIn(b"HelloWorld")
		assert not stream.eof()
		stream.seek(10)
		assert stream.eof()
	
	def test_readall(self):
		stream = streams.StreamIn(b"HelloWorld")
		stream.skip(2)
		assert stream.readall() == b"lloWorld"
		assert stream.readall() == b""
	
	def test_pad(self):
		stream = streams.StreamIn(b"\0\0\0AAABBB")
		stream.pad(3)
		stream.pad(3, b"A")
		with pytest.raises(ValueError):
			stream.pad(3, b"A")
			
	def test_ascii(self):
		stream = streams.StreamIn(b"HelloWorld")
		assert stream.ascii(10) == "HelloWorld"
		
	def test_uint(self):
		stream = streams.StreamIn(b"\x7F\x00\x80\xFF\xFF\xFF\0\0\0\0\xEF\xCD\xAB\x89\x67\x45\x23\x01")
		assert stream.u8() == 127
		assert stream.u16() == 0x8000
		assert stream.u24() == 0xFFFFFF
		assert stream.u32() == 0
		assert stream.u64() == 0x123456789ABCDEF
		stream.skip(-1)
		with pytest.raises(OverflowError):
			stream.u16()
			
	def test_sint(self):
		stream = streams.StreamIn(b"\x7F\x00\x80\0\0\0\0\xEF\xCD\xAB\x89\x67\x45\x23\x01")
		assert stream.s8() == 127
		assert stream.s16() == -0x8000
		assert stream.s32() == 0
		assert stream.s64() == 0x123456789ABCDEF
		
	def test_float(self):
		stream = streams.StreamIn(b"\0\0\0\x40\0\0\0\0\0\0\0\xC0")
		assert stream.float() == 2
		assert stream.double() == -2
		
	def test_bool(self):
		stream = streams.StreamIn(b"\x00\x01\x80")
		assert stream.bool() is False
		assert stream.bool() is True
		assert stream.bool() is True
		
	def test_char(self):
		stream = streams.StreamIn(b"ABC\0D\0")
		assert stream.char() == "A"
		assert stream.char() == "B"
		assert stream.wchar() == "C"
		assert stream.wchar() == "D"
		
	def test_chars(self):
		stream = streams.StreamIn(b"ABC\0D\0")
		assert stream.chars(2) == "AB"
		assert stream.wchars(2) == "CD"
		
	def test_repeat(self):
		stream = streams.StreamIn(b"HelloWorld")
		assert stream.repeat(stream.char, 5) == ["H", "e", "l", "l", "o"]
		

class TestBitStreamOut:
	def test_bit(self):
		stream = streams.BitStreamOut()
		stream.bit(0)
		stream.bit(1)
		stream.bit(0)
		stream.bit(1)
		assert stream.get() == b"\x50"
	
	def test_bits(self):
		stream = streams.BitStreamOut()
		stream.bits(15, 4)
		stream.u8(15)
		stream.bits(1, 4)
		assert stream.get() == b"\xF0\xF1"
	
	def test_tellbits(self):
		stream = streams.BitStreamOut()
		assert stream.tellbits() == 0
		stream.bits(15, 4)
		assert stream.tellbits() == 4
		stream.u8(1)
		assert stream.tellbits() == 12
		
	def test_seekbits(self):
		stream = streams.BitStreamOut()
		stream.seekbits(100)
		assert stream.tellbits() == 100
		assert stream.get() == bytes(13)
	
	def test_bytealign(self):
		stream = streams.BitStreamOut()
		assert stream.tellbits() == 0
		stream.bytealign()
		assert stream.tellbits() == 0
		stream.bit(1)
		stream.bytealign()
		assert stream.tellbits() == 8


class TestBitStreamIn:
	def test_bit(self):
		stream = streams.BitStreamIn(b"\x5A")
		assert stream.bit() == 0
		assert stream.bit() == 1
		assert stream.bit() == 0
		assert stream.bit() == 1
		
	def test_bits(self):
		stream = streams.BitStreamIn(b"\x5A")
		assert stream.bits(4) == 5
		assert stream.bits(2) == 2
		
	def test_tellbits(self):
		stream = streams.BitStreamIn(b"\x5A")
		assert stream.tellbits() == 0
		stream.bits(4)
		assert stream.tellbits() == 4
	
	def test_seekbits(self):
		stream = streams.BitStreamIn(b"\x5A")
		stream.seekbits(1)
		assert stream.tellbits() == 1
		assert stream.bits(4) == 11
		
	def test_bytealign(self):
		stream = streams.BitStreamIn(b"\x5A")
		stream.bytealign()
		assert stream.tellbits() == 0
		stream.seekbits(1)
		stream.bytealign()
		assert stream.tellbits() == 8
		assert stream.eof()
