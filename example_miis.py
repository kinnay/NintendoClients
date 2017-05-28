
from nintendo.act import AccountAPI

api = AccountAPI()
pid = api.get_pid("Kinnay-WiiU") #That's me
mii = api.get_mii(pid)
print("NNID:", mii.nnid)
print("Name:", mii.name)
print("PID:", pid) #Same as mii.pid
print("Images:")
for url in mii.images.values():
	print("\t%s" %url)
