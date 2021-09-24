
from nintendo.games import Splatoon2
from nintendo.pia import lan, settings, types
from nintendo.nex import common
import secrets
import random
import anyio
import math

import logging
logging.basicConfig(level=logging.INFO)


SESSION_ID = random.randint(1, 0xFFFFFFFF)
HOST_ID = random.randint(1, 0xFFFFFFFFFFFFFFFF)
HOST_NAME = "Yannik"

def handler():
	host_address = types.StationLocation()
	
	host = lan.LanStationInfo()
	host.role = lan.LanStationInfo.HOST
	host.username = HOST_NAME
	host.id = HOST_ID
	
	session = lan.LanSessionInfo()
	session.game_mode = 0
	session.session_id = SESSION_ID
	session.attributes = [0, 0, 0, 0, 0, 0]
	session.num_participants = 1
	session.min_participants = 1
	session.max_participants = 10
	session.system_version = 5
	session.application_version = 65
	session.session_type = 0
	session.application_data = HOST_NAME.encode("utf-16le").ljust(74, b"\0")
	session.is_opened = True
	session.host_location = host_address
	session.stations[0] = host
	session.session_param = secrets.token_bytes(32)
	
	return [session]

async def main():
	s = settings.default(Splatoon2.PIA_VERSION)
	async with lan.serve(s, handler, Splatoon2.PIA_KEY):
		print("LAN server is running...")
		await anyio.sleep(math.inf)

anyio.run(main)
