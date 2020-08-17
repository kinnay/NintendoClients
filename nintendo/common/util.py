
import contextlib
import netifaces
import struct
import socket
import string
import anyio

import logging
logger = logging.getLogger(__name__)


def ip_to_hex(ip):
	try:
		data = socket.inet_aton(ip)
	except OSError:
		raise ValueError("IP address is invalid")
	return struct.unpack(">I", data)[0]

def ip_from_hex(value):
	return socket.inet_ntoa(struct.pack(">I", value))
	
def is_hexadecimal(s):
	return s and all(c in string.hexdigits for c in s)
	
def local_address():
	interface = netifaces.gateways()["default"][netifaces.AF_INET][1]
	addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
	return addresses["addr"]
	
def broadcast_address():
	interface = netifaces.gateways()["default"][netifaces.AF_INET][1]
	addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
	return addresses["broadcast"]

@contextlib.contextmanager
def catch_all():
	try:
		yield
	except anyio.exceptions.ExceptionGroup as e:
		filtered = []
		for exc in e.exceptions:
			if isinstance(exc, Exception):
				logger.error("An exception occurred", exc_info=exc)
			else:
				filtered.append(exc)
		e.exceptions = filtered
		if filtered:
			raise
	except Exception:
		logger.exception("An exception occurred")
