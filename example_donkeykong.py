
from nintendo.nex import backend, authentication, ranking, datastore
from nintendo.games import DKCTF
from nintendo import account

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
backend = backend.BackEndClient(DKCTF.GAME_SERVER_ID, DKCTF.ACCESS_KEY, DKCTF.NEX_VERSION)
backend.connect(nex_token.host, nex_token.port)
backend.login(
	nex_token.username, nex_token.password,
	authentication.AuthenticationInfo(nex_token.token, DKCTF.SERVER_VERSION)
)

ranking_client = ranking.RankingClient(backend)
rankings = ranking_client.get_ranking(
	ranking.RankingClient.MODE_GLOBAL, #Get the global leaderboard
	0x893EB726, #Category, this is 3-A (Magrove Cove)
	ranking.RankingOrderParam(
		ranking.RankingOrderParam.STANDARD, #"1224" ranking
		0, 13, 2,
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
	kong = ["No Kong", "Diddy", "Dixie", "Cranky"][rankdata.groups[1]]
	name = rankdata.common_data.decode("ascii")[:-1]

	print("\t%2i   %20s   %s (%s)   %s" %(rankdata.rank, name, time, damage, kong))
	
	
#Now download the world record replay file if available
world_record = rankings.datas[0]
if world_record.param: #If world record has a replay file	
	store = datastore.DataStore(backend)
	replay_data = store.get_object(
		datastore.DataStorePrepareGetParam(
			world_record.param, 0, datastore.PersistenceTarget(0, 0xFFFF), 0
		)
	)
	
	with open("replay.bin", "wb") as f:
		f.write(replay_data)

#Close connection
backend.close()
