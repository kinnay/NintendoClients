from nintendo import nasc
from nintendo.nex import backend, friends, settings
import anyio

import logging

logging.basicConfig(level=logging.INFO)


SERIAL_NUMBER = "..."  # Serial number on console minus the last digit
MAC_ADDRESS = "aabbccddeeff"  # Console MAC address (see WiFi settings), all lowercase with no colons
DEVICE_CERT = bytes.fromhex(
	"..."
)  # Unique console certificate. Get from sniffing traffic
DEVICE_NAME = "..."  # Doesn't matter

# 3DS does NOT send NEX credentials over NASC
# They are generated once when the account is created and stored on the device
# Homebrew like https://github.com/Stary2001/nex-dissector/tree/master/get_3ds_pid_password
# can be used to dump the PID and password
PID = 0
PID_HMAC = "..."  # Sniff console traffic or dump from friends title save (bytes 66-84)

NEX_PASSWORD = "..."

REGION = 3  # EUR
LANGUAGE = 2


async def main():
	client = nasc.NASCClient()
	client.set_title(0x0004013000003202, 20000)
	client.set_device(SERIAL_NUMBER, MAC_ADDRESS, DEVICE_CERT, DEVICE_NAME)
	client.set_locale(REGION, LANGUAGE)
	client.set_user(PID, PID_HMAC)

	response = await client.login(0x3200)

	s = settings.load("friends")
	s.configure("ridfebb9", 20000)
	async with backend.connect(s, response.host, response.port) as be:
		async with be.login(str(PID), NEX_PASSWORD) as client:
			friends_client = friends.FriendsClientV1(client)
			await friends_client.update_comment("Hello World")


anyio.run(main)
