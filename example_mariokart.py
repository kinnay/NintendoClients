
from nintendo.nex.backend import BackEndClient
from nintendo.nex.ranking import RankingClient, RankingOrderParam
from nintendo.nex.datastore import DataStore, DataStoreGetParam, PersistenceTarget
from nintendo.common.scheduler import Scheduler
from nintendo.act import AccountAPI
from nintendo.games import MK8

#Device id can be retrieved with a call to MCP_GetDeviceId on the Wii U
#Serial number can be found on the back of the Wii U
DEVICE_ID = 12345678
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x220
REGION_ID = 4
COUNTRY_ID = 94
REGION_NAME = "EUR"
COUNTRY_NAME = "NL"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password


#See the donkey kong example for more comments on this code
scheduler = Scheduler()
scheduler.start()

api = AccountAPI()
api.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_NAME)
api.set_title(MK8.TITLE_ID_EUR, MK8.LATEST_VERSION)
api.login(USERNAME, PASSWORD)

nex_token = api.get_nex_token(MK8.GAME_SERVER_ID)
backend = BackEndClient(MK8.ACCESS_KEY, MK8.NEX_VERSION)
backend.connect(nex_token.host, nex_token.port)
backend.login(nex_token.username, nex_token.password, nex_token.token)

ranking_client = RankingClient(backend)
rankings = ranking_client.get_ranking(
	RankingClient.MODE_GLOBAL,
	0x1B, #Mario Kart Stadium
	RankingOrderParam(
		RankingOrderParam.ORDINAL, #"1234" ranking
		0xFF, 0, 2, #Unknown
		499, 20 #Download 500th to 520th place
	),
	0, 0 #Unknown
)

names = api.get_nnids([data.user_id for data in rankings.datas])
print("Total:", rankings.total)
print("Rankings:")
for rankdata in rankings.datas:
	millisec = rankdata.score % 1000
	seconds = rankdata.score // 1000 % 60
	minutes = rankdata.score // 1000 // 60
	time = "%i:%02i.%03i" %(minutes, seconds, millisec)
	print("\t%5i   %20s   %s" %(rankdata.rank, names[rankdata.user_id], time))
	
#Let's download the replay file of whoever is in 500th place
datastore = DataStore(backend)
rankdata = rankings.datas[0]
filedata = datastore.get_object(
	DataStoreGetParam(
		0, 0, PersistenceTarget(rankdata.user_id, TRACK_ID - 16), 0,
		["WUP", str(REGION_ID), REGION_NAME, str(COUNTRY_ID), COUNTRY_NAME, ""]
	)
)

with open("mk8_replay.bin", "wb") as f:
	f.write(filedata)


#Close connection and stop thread
backend.close()
scheduler.stop()
