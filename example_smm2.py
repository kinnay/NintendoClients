
from nintendo.baas import BAASClient
from nintendo.dauth import DAuthClient
from nintendo.aauth import AAuthClient
from nintendo.switch import ProdInfo, KeySet, TicketList
from nintendo.nex import backend, authentication, datastore_smm2 as datastore
from nintendo.games import SMM2
import requests

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

COURSE_ID = "2J53K2Y9G"


GameStyles = ["SMB1", "SMB3", "SMW", "NSMBU", "SM3DW"]

Difficulties = ["Easy", "Normal", "Expert", "Super expert"]

CourseThemes = [
	"Overworld", "Underground", "Castle", "Airship",
	"Underwater", "Ghost house", "Snow", "Desert",
	"Sky", "Forest"
]

TagNames = [
	"None", "Standard", "Puzzle solving", "Speedrun",
	"Autoscroll", "Auto mario", "Short and sweet",
	"Multiplayer versus", "Themed", "Music"
]


HOST = "g%08x-lp1.s.n.srv.nintendo.net" %SMM2.GAME_SERVER_ID
PORT = 443

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

# Download a specific course
store = datastore.DataStoreClientSMM2(backend.secure_client)

param = datastore.GetUserOrCourseParam()
param.code = COURSE_ID
param.course_option = datastore.CourseOption.ALL

response = store.get_user_or_course(param)
course = response.course

# Print information about the course
def format_time(milliseconds):
	seconds = (milliseconds // 1000) % 60
	minutes = (milliseconds // 1000) // 60
	milliseconds = milliseconds % 1000
	return "%02i:%02i.%03i" %(minutes, seconds, milliseconds)

print("Level info:")
print("\tName:", course.name)
print("\tDescription:", course.description)
print("\tUploaded at:", course.upload_time)
print("\tGame:", GameStyles[course.game_style])
print("\tTheme:", CourseThemes[course.course_theme])
print("\tDifficulty:", Difficulties[course.difficulty])
print("\tFirst tag:", TagNames[course.tag1])
print("\tSecond tag:", TagNames[course.tag2])
print("\tWorld record:", format_time(course.time_stats.world_record))
print("\tNumber of comments:", course.comment_stats[0])

# Request information about its uploader
param = datastore.GetUsersParam()
param.pids = [course.owner_id]

response = store.get_users(param)

user = response.users[0]
print("Uploader:")
print("\tCode:", user.code)
print("\tName:", user.name)
print("\tCountry:", user.country)
print("\tLast active:", user.last_active)

# Download thumbnails
def download_thumbnail(info, filename):
	response = store.get_req_get_info_headers_info(info.data_type)
	headers = {h.key: h.value for h in response.headers}
	data = requests.get(info.url, headers=headers).content
	with open(filename, "wb") as f:
		f.write(data)

download_thumbnail(course.one_screen_thumbnail, "thumbnail_onescreen.jpg")
download_thumbnail(course.entire_thumbnail, "thumbnail_entire.jpg")

# Download level file
param = datastore.DataStorePrepareGetParam()
param.data_id = course.data_id

req_info = store.prepare_get_object(param)
data = requests.get(req_info.url).content
with open("level.bin", "wb") as f:
	f.write(data)

# Disconnect from game server
backend.close()
