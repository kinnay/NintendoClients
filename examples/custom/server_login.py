
from nintendo.nex import backend, settings
from nintendo.games import Friends
import anyio

import logging
logging.basicConfig(level=logging.INFO)


async def main():
	s = settings.load("friends")
	s.configure(Friends.ACCESS_KEY, Friends.NEX_VERSION)
	
	async with backend.connect(s, "127.0.0.1", 1223) as be:
		async with be.login_guest() as client:
			pass

anyio.run(main)
