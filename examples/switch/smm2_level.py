
from nintendo.baas import BAASClient
from nintendo.dauth import DAuthClient
from nintendo.aauth import AAuthClient
from nintendo.dragons import DragonsClient
from nintendo.nex import backend, authentication, \
	settings, datastore_smm2 as datastore
from nintendo.games import SMM2
from nintendo import switch
from anynet import http
import anyio

import logging
logging.basicConfig(level=logging.INFO)


SYSTEM_VERSION = 1501 #15.0.1

# You can get your user id and password from
# su/baas/<guid>.dat in save folder 8000000000000010.

# Bytes 0x20 - 0x28 contain the user id in reversed
# byte order, and bytes 0x28 - 0x50 contain the
# password in plain text.

# Alternatively, you can set up a mitm on your Switch
# and extract them from the request to /1.0.0/login

BAAS_USER_ID = 0x0123456789abcdef # 16 hex digits
BAAS_PASSWORD = "..." # Should be 40 characters

# You can dump prod.keys with Lockpick_RCM and
# PRODINFO from hekate (decrypt it if necessary)
PATH_KEYS = "/path/to/prod.keys"
PATH_PRODINFO = "/path/to/PRODINFO"

# These can be obtained by calling publish_device_linked_elicenses (see docs)
# or with a mitm on your Switch (this is probably safer)
ELICENSE_ID = "..." # 32 hex digits
NA_ID = 0x0123456789abcdef # 16 hex digits


COURSE_ID = "2J53K2Y9G"

HOST = "g%08x-lp1.s.n.srv.nintendo.net" %SMM2.GAME_SERVER_ID
PORT = 443


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
	"Multiplayer versus", "Themed", "Music", "Art",
	"Technical", "Shooter", "Boss battle",
	"Single player", "Link"
]


def format_time(milliseconds):
	seconds = (milliseconds // 1000) % 60
	minutes = (milliseconds // 1000) // 60
	milliseconds = milliseconds % 1000
	return "%02i:%02i.%03i" %(minutes, seconds, milliseconds)
	

async def download_thumbnail(store, info, filename):
	response = await store.get_req_get_info_headers_info(info.data_type)
	headers = {h.key: h.value for h in response.headers}
	response = await http.get(info.url, headers=headers)
	response.raise_if_error()
	with open(filename, "wb") as f:
		f.write(response.body)


async def main():
	keys = switch.load_keys(PATH_KEYS)
	
	info = switch.ProdInfo(keys, PATH_PRODINFO)
	cert = info.get_tls_cert()
	pkey = info.get_tls_key()
	
	dauth = DAuthClient(keys)
	dauth.set_certificate(cert, pkey)
	dauth.set_system_version(SYSTEM_VERSION)
	
	dragons = DragonsClient()
	dragons.set_certificate(cert, pkey)
	dragons.set_system_version(SYSTEM_VERSION)
	
	aauth = AAuthClient()
	aauth.set_system_version(SYSTEM_VERSION)
	
	baas = BAASClient()
	baas.set_system_version(SYSTEM_VERSION)
	
	# Request a device authentication token for dragons
	response = await dauth.device_token(dauth.DRAGONS)
	device_token_dragons = response["device_auth_token"]
	
	# Request a device authentication token for aauth and bass
	response = await dauth.device_token(dauth.BAAS)
	device_token_baas = response["device_auth_token"]
	
	# Request a contents authorization token from dragons
	response = await dragons.contents_authorization_token_for_aauth(device_token_dragons, ELICENSE_ID, NA_ID, SMM2.TITLE_ID)
	contents_token = response["contents_authorization_token"]
	
	# Request an application authentication token
	response = await aauth.auth_digital(SMM2.TITLE_ID, SMM2.LATEST_VERSION, device_token_baas, contents_token)
	app_token = response["application_auth_token"]
	
	# Request an anonymous access token for baas
	response = await baas.authenticate(device_token_baas)
	access_token = response["accessToken"]
	
	# Log in on the baas server
	response = await baas.login(
		BAAS_USER_ID, BAAS_PASSWORD, access_token, app_token
	)
	user_id = int(response["user"]["id"], 16)
	id_token = response["idToken"]
	
	# Set up authentication info for nex server
	auth_info = authentication.AuthenticationInfo()
	auth_info.token = id_token
	auth_info.ngs_version = 4 #Switch
	auth_info.token_type = 2
	
	s = settings.load("switch")
	s.configure(SMM2.ACCESS_KEY, SMM2.NEX_VERSION, SMM2.CLIENT_VERSION)
	async with backend.connect(s, HOST, PORT) as be:
		async with be.login(str(user_id), auth_info=auth_info) as client:
			store = datastore.DataStoreClientSMM2(client)
			
			param = datastore.GetUserOrCourseParam()
			param.code = COURSE_ID
			param.course_option = datastore.CourseOption.ALL

			response = await store.get_user_or_course(param)
			course = response.course

			# Print information about the course
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

			response = await store.get_users(param)
			user = response.users[0]
			print("Uploader:")
			print("\tCode:", user.code)
			print("\tName:", user.name)
			print("\tCountry:", user.country)
			print("\tLast active:", user.last_active)

			# Download thumbnails
			await download_thumbnail(store, course.one_screen_thumbnail, "thumbnail_onescreen.jpg")
			await download_thumbnail(store, course.entire_thumbnail, "thumbnail_entire.jpg")

			# Download level file
			param = datastore.DataStorePrepareGetParam()
			param.data_id = course.data_id

			req_info = await store.prepare_get_object(param)
			response = await http.get(req_info.url)
			response.raise_if_error()
			with open("level.bin", "wb") as f:
				f.write(response.body)

anyio.run(main)
