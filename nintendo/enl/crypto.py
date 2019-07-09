
from nintendo.sead import Random
import struct

def create_key_value(rand, table):
	value = 0
	for i in range(4):
		index = rand.uint(len(table))
		shift = rand.uint(4) * 8
		byte = (table[index] >> shift) & 0xFF
		value = (value << 8) | byte
	return value

def create_key(rand, table, size):
	if size % 4:
		raise ValueError("Key size must be multiple of 4")
	
	key = b""
	for i in range(size // 4):
		value = create_key_value(rand, table)
		key += struct.pack("<I", value)
	return key
