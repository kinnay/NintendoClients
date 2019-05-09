
from nintendo.nex import backend
from nintendo.games import Friends

import logging
logging.basicConfig(level=logging.INFO)

backend = backend.BackEndClient(
	Friends.ACCESS_KEY, Friends.NEX_VERSION,
	backend.Settings("friends.cfg")
)
backend.connect("127.0.0.1", 1223)
backend.login_guest()
backend.close()
