
from proto.nintendo.nex.backend import BackEndClient
from proto.nintendo.nex.ranking import RankingClient, RankingOrderParam
from proto.nintendo.nex.datastore import DataStore, DataStoreGetParam, PersistenceTarget
from proto.nintendo.act import AccountAPI
from proto.nintendo.games import DKCTF
from proto.common.scheduler import Scheduler

#Device id can be retrieved with a call to MCP_GetDeviceId on the Wii U
#Serial number can be found on the back of the Wii U
DEVICE_ID = 12345678
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x220
REGION = 4
COUNTRY = "NL"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password


#This thing handles the PRUDP connection in the background
scheduler = Scheduler()
scheduler.start()

api = AccountAPI()
api.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION, COUNTRY) #Can't login without this
api.set_title(DKCTF.TITLE_ID_EUR, DKCTF.LATEST_VERSION) #This is necessary to request a token for the game server
api.login(USERNAME, PASSWORD)

#Each game server has its own game server id and access token
nex_token = api.get_nex_token(DKCTF.GAME_SERVER_ID)
backend = BackEndClient(DKCTF.ACCESS_TOKEN, DKCTF.NEX_VERSION)
backend.connect(nex_token.host, nex_token.port)
backend.login(nex_token.username, nex_token.password, nex_token.token)

ranking_client = RankingClient(backend)
rankings = ranking_client.get_ranking(
	RankingClient.MODE_GLOBAL, #Get the global leaderboard
	0x893EB726, #Level id, this is 3-A (Magrove Cove)
	RankingOrderParam(
		RankingOrderParam.STANDARD, #"1224" ranking (https://en.wikipedia.org/wiki/Ranking)
		0, 13, 2, #Unknown purpose
		0, 20 #Download 20 highscores, starting at the world record
	),
	0, 0 #Unknown
)

print("Total:", rankings.total)
print("Rankings:")
for rankdata in rankings.datas:
	seconds = (rankdata.score >> 1) / 60
	time = "%i:%02i.%02i" %(seconds / 60, seconds % 60, (seconds * 100) % 100)
	damage = " Damaged " if rankdata.score & 1 else "No damage"
	kong = ["No Kong", "Diddy", "Dixie", "Cranky"][rankdata.data[1]]

	print("\t%5i   %20s   %s (%s)   %s" %(rankdata.rank, rankdata.name, time, damage, kong))
	
	
#Now download the world record replay file if available
world_record = rankings.datas[0]
if world_record.file_id: #If world record has a replay file	
	datastore = DataStore(backend)
	replay_data = datastore.get_object(
		#I don't know what most of these values mean, this is what Donkey Kong does
		DataStoreGetParam(world_record.file_id, 0, PersistenceTarget(0, 0xFFFF), 0)
	)
	
	with open("replay.bin", "wb") as f:
		f.write(replay_data)

backend.close()
scheduler.stop()
