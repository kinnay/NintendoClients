# NintendoClients
Python package to communicate with Nintendo servers

The initial goal of this project was a client that downloads rankings from DKC:TF, but I have been experimenting with other games (including non-Nintendo stuff, which is why you see the redundant nintendo namespace here).

To import this into your Python code, simply place the "proto" folder somewhere Python can find it.

Requirements:
* Python 3 (tested with 3.5.2)
* Python requests (http://docs.python-requets.org)
* BeautifulSoup4
* Nintendo SSL certificate (see below)

Unfortunately, there are many different version of the NEX library, and some games even got their own patches. To make sure I don't have to spend hours figuring out why I'm getting weird responses from the server, I'm raising an error if the nex version isn't explicitly added to a protocols version map. If you want to try this library with unsupported games, add the nex version number to the version_map variable of the class that throws the error.

Before you can access the account server, you have to place Nintendo's SSL client certificate in PEM format into the "files" folder named "wiiu_common_cert.pem" and "wiiu_commmon_key.pem". These can be downloaded from Nintendo's update server (title id 0005001B-10054000). Most functions of the account server are only available after authentication. Authentication requires your Nintendo Network ID and password and serial number, device id, system version, region and country of your Wii U. To access specific game servers, you also need the game server id and sandbox access key of the server.

Useful information:
* https://github.com/Kinnay/NintendoClients/wiki/DKC:TF-Level-IDs
* https://github.com/Kinnay/NintendoClients/wiki/Mario-Kart-8-Track-IDs
* https://github.com/Kinnay/NintendoClients/wiki/Network-Library-Versions

As with any software, this code probably contains some bugs.

---

If you think this software infringes your copyright and would like me to delete it, please contact me here: ymarchand@me.com
