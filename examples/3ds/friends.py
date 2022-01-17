
from nintendo import nasc
from nintendo.nex import backend, friends, settings
from nintendo.games import Friends3DS
import anyio

import logging
logging.basicConfig(level=logging.INFO)


SERIAL_NUMBER = "..." # Serial number on console minus the last digit
MAC_ADDRESS = "..." # Console MAC address (see WiFi settings), all lowercase with no colons
FCDCERT = "..." # Unique console certificate. Get from sniffing traffic

PID_HMAC = "..." # Sniff console traffic or dump from friends title save (bytes 66-84)

# 3DS does NOT send NEX credentials over NASC
# They are generated once when the account is created and stored on the device
# Homebrew like https://github.com/Stary2001/nex-dissector/tree/master/get_3ds_pid_password
# can be used to dump the PID and password
PID = 0
NEX_PASSWORD = "..."


async def main():
	client = nasc.NASCClient()

	client.set_device(SERIAL_NUMBER, MAC_ADDRESS, FCDCERT)
	client.set_user(PID, PID_HMAC)
	client.set_title(Friends3DS.TITLE_ID_EUR, Friends3DS.LATEST_VERSION, Friends3DS.PRODUCT_CODE_EUR)
	nasc_data = await client.get_nasc_data(Friends3DS.GAME_SERVER_ID)

	s = settings.load("friends")
	s.configure(Friends3DS.ACCESS_KEY, Friends3DS.NEX_VERSION)
	async with backend.connect(s, nasc_data.locator.host, nasc_data.locator.port) as be:
		async with be.login(str(PID), NEX_PASSWORD) as client:
			friends_client = friends.FriendsClientV1(client)
			await friends_client.update_comment("Hello World")

anyio.run(main)
