
from nintendo.nex import backend, authentication, ranking, datastore
from nintendo.games import DKCTF
from nintendo import account
import requests

import logging
logging.basicConfig(level=logging.INFO)

#Device id can be retrieved with a call to MCP_GetDeviceId on the Wii U
#Serial number can be found on the back of the Wii U
DEVICE_ID = 12345678
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x220
REGION = 4 #EUR
COUNTRY = "NL"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password


api = account.AccountAPI()
api.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION, COUNTRY) #Can't login without this
api.set_title(DKCTF.TITLE_ID_EUR, DKCTF.LATEST_VERSION) #This is necessary to request a token for the game server
api.login(USERNAME, PASSWORD)

#Each game server has its own game server id and access token
nex_token = api.get_nex_token(DKCTF.GAME_SERVER_ID)

backend = backend.BackEndClient()
backend.configure(DKCTF.ACCESS_KEY, DKCTF.NEX_VERSION)
backend.connect(nex_token.host, nex_token.port)
backend.login(nex_token.username, nex_token.password)

order_param = ranking.RankingOrderParam()
order_param.offset = 0 #Start with the world record
order_param.count = 20 #Download 20 highscores

ranking_client = ranking.RankingClient(backend.secure_client)
rankings = ranking_client.get_ranking(
	ranking.RankingMode.GLOBAL, #Get the global leaderboard
	0x893EB726, #Category, this is 3-A (Magrove Cove)
	order_param,
	0, 0
)

print("Total:", rankings.total)
print("Rankings:")
for rankdata in rankings.data:
	seconds = (rankdata.score >> 1) / 60
	time = "%i:%02i.%02i" %(seconds / 60, seconds % 60, (seconds * 100) % 100)
	damage = " Damaged " if rankdata.score & 1 else "No damage"
	kong = ["No Kong", "Diddy", "Dixie", "Cranky"][rankdata.groups[1]]
	name = rankdata.common_data.decode("ascii")[:-1]

	print("\t%2i   %20s   %s (%s)   %s" %(rankdata.rank, name, time, damage, kong))
	
	
#Now download the world record replay file if available
world_record = rankings.data[0]
if world_record.param: #If world record has a replay file	
	store = datastore.DataStoreClient(backend.secure_client)
	
	get_param = datastore.DataStorePrepareGetParam()
	get_param.data_id = world_record.param
	
	req_info = store.prepare_get_object(get_param)
	headers = {header.key: header.value for header in req_info.headers}
	replay_data = requests.get("http://" + req_info.url, headers=headers).content
	
	with open("replay.bin", "wb") as f:
		f.write(replay_data)

#Close connection
backend.close()
