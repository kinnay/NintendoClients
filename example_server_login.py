
from nintendo.nex import backend
from nintendo.games import Friends
from nintendo import settings

import logging
logging.basicConfig(level=logging.INFO)

backend = backend.BackEndClient("friends.cfg")
backend.configure(Friends.ACCESS_KEY, Friends.NEX_VERSION)
backend.connect("127.0.0.1", 1223)
backend.login_guest()
backend.close()
