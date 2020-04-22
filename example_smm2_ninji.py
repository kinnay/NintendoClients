
from nintendo.baas import BAASClient
from nintendo.dauth import DAuthClient
from nintendo.aauth import AAuthClient
from nintendo.switch import ProdInfo, KeySet, TicketList
from nintendo.nex import backend, authentication, datastore_smm2 as datastore
from nintendo.games import SMM2
import requests
import zlib

import logging
logging.basicConfig(level=logging.INFO)


SYSTEM_VERSION = 1001 #10.0.1

# You can get your username and password from
# su/baas/<guid>.dat in save folder 8000000000000010.

# Bytes 0x20 - 0x28 contain the user id in reversed
# byte order, and bytes 0x28 - 0x50 contain the
# password in plain text.

# Alternatively, you can set up a mitm on your Switch
# and extract them from the request to /1.0.0/login

BAAS_USERNAME = "0123456789abcdef" # 16 hex digits
BAAS_PASSWORD = "..." # Should be 40 characters

# You can dump prod.keys with Lockpick_RCM and
# PRODINFO from hekate (decrypt it if necessary)
keys = KeySet("/path/to/prod.keys")
info = ProdInfo(keys, "/path/to/PRODINFO")

# Tickets can be dumped with nxdumptool.
# You need the base ticket, not an update ticket.
with open("/path/to/ticket", "rb") as f:
	ticket = f.read()


HOST = "g%08x-lp1.s.n.srv.nintendo.net" %SMM2.GAME_SERVER_ID
PORT = 443

ticket = tickets.get(SMM2.TITLE_ID)

cert = info.get_ssl_cert()
pkey = info.get_ssl_key()


# Request a dauth token
dauth = DAuthClient(keys)
dauth.set_certificate(cert, pkey)
dauth.set_system_version(SYSTEM_VERSION)
response = dauth.device_token()
device_token = response["device_auth_token"]

# Request an aauth token
aauth = AAuthClient()
response = aauth.auth_digital(
	SMM2.TITLE_ID, SMM2.TITLE_VERSION,
	device_token, ticket
)
app_token = response["application_auth_token"]

# Log in on baas server
baas = BAASClient()
baas.authenticate(device_token)
response = baas.login(BAAS_USERNAME, BAAS_PASSWORD, app_token)

user_id = int(response["user"]["id"], 16)
id_token = response["idToken"]

# Connect to game server
backend = backend.BackEndClient("switch.cfg")
backend.configure(SMM2.ACCESS_KEY, SMM2.NEX_VERSION, SMM2.CLIENT_VERSION)
backend.connect(HOST, PORT)

# Log in on game server
auth_info = authentication.AuthenticationInfo()
auth_info.token = id_token
auth_info.ngs_version = 4 #Switch
auth_info.token_type = 2
backend.login(str(user_id), auth_info=auth_info)

# Search for ninji courses
store = datastore.DataStoreClientSMM2(backend.secure_client)

param = datastore.SearchCoursesEventParam()
courses = store.search_courses_event(param)
print("Found %i ninji courses.\n" %len(courses))

# Print information about the most recent ninji course
course = courses[0]
print("Name:", course.name)
print("Description:", course.description)
print("Start time:", course.upload_time)
print("End time:", course.end_time)
print()

# Request ghost info
param = datastore.GetEventCourseGhostParam()
param.data_id = course.data_id
param.time = 30000 # Request ghosts with a time around 30 seconds
param.count = 1 # Only request a single ghost

ghost = store.get_event_course_ghost(param)[0]

# Request info about the ghost player
param = datastore.GetUsersParam()
param.pids = [ghost.pid]

user = store.get_users(param).users[0]
print("Player:", user.name)
print("Time: %i.%03i" %(ghost.time // 1000, ghost.time % 1000))
print()

# Download replay file
header_info = store.get_req_get_info_headers_info(ghost.replay_file.data_type)
headers = {h.key: h.value for h in header_info.headers}
data = requests.get(ghost.replay_file.url, headers=headers).content

# Decompress and save replay file
data = zlib.decompress(data)
with open("replay.bin", "wb") as f:
	f.write(data)

# Disconnect from game server
backend.close()
