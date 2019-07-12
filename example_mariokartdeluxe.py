
from nintendo.nex import backend, ranking
from nintendo.games import MK8Deluxe

TRACK_ID = 10 #Sunshine airport

HOST = "g%08x-lp1.s.n.srv.nintendo.net" %MK8Deluxe.GAME_SERVER_ID
PORT = 443

backend = backend.BackEndClient("switch.cfg")
backend.configure(MK8Deluxe.ACCESS_KEY, MK8Deluxe.NEX_VERSION)
backend.connect(HOST, PORT)
backend.login_guest()

order_param = ranking.RankingOrderParam()
order_param.order_calc = ranking.RankingOrderCalc.ORDINAL
order_param.offset = 0 #Start with world record
order_param.count = 20 #Download 20 highscores

ranking_client = ranking.RankingClient(backend.secure_client)
rankings = ranking_client.get_ranking(
	ranking.RankingMode.GLOBAL, TRACK_ID,
	order_param, 0, 0
)

stats = ranking_client.get_stats(
	TRACK_ID, order_param, ranking.RankingStatFlags.ALL
).stats

def format_time(score):
	millisec = score % 1000
	seconds = score // 1000 % 60
	minutes = score // 1000 // 60
	return "%i:%02i.%03i" %(minutes, seconds, millisec)
	
#Print some interesting stats
print("Total:", int(stats[0]))
print("Total time:", format_time(stats[1]))
print("Average time:", format_time(stats[2]))
print("Lowest time:", format_time(stats[3]))
print("Highest time:", format_time(stats[4]))

print("Rankings:")
for rankdata in rankings.data:
	time = format_time(rankdata.score)
	print("\t%5i   %016X   %s" %(rankdata.rank, rankdata.pid, time))

#Close connection
backend.close()
