# NintendoClients
Python package to communicate with Nintendo servers

The initial goal of this project was a client that downloads rankings from DKC:TF, but I have been experimenting with other games.

To import this into your Python code, simply place the "nintendo" folder somewhere Python can find it.

Requirements:
* Python 3 (tested with 3.5.2)
* Python requests (http://docs.python-requets.org)
* BeautifulSoup4
* Nintendo SSL certificate (see below)

This code lacks documentation, but it does have a few example scripts:
* example_donkeykong.py downloads and prints DKC Tropical Freeze rankings, and download the replay file of the world record
* example_mariokart.py downloads and prints Mario Kart 8 rankings
* example_miis.py requests and prints information about the primary mii associated with a NNID, including a few urls to images of that mii
* example_friends.py requests and prints your friend list, incoming and outgoing friend requests, and blacklist

Before you can access the account server, you have to place Nintendo's SSL client certificate in PEM format into the "files" folder named "wiiu_common_cert.pem" and "wiiu_commmon_key.pem". These can be downloaded from Nintendo's update server (title id 0005001B-10054000). Some functions of the account server are only available after authentication. Authentication requires your Nintendo Network ID and password and serial number, device id, system version, region and country of your Wii U. To access specific game servers, you also need the game server id and sandbox access key of the server.

Useful information:
* https://github.com/Kinnay/NintendoClients/wiki/DKC:TF-Level-IDs
* https://github.com/Kinnay/NintendoClients/wiki/Mario-Kart-8-Track-IDs
* https://github.com/Kinnay/NintendoClients/wiki/Network-Library-Versions

The PRUDP connection is not really reliable, as it's still missing some reliability features.

---

If you think this software infringes your copyright and would like me to delete it, please contact me here: ymarchand@me.com
