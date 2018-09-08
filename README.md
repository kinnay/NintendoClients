# Nintendo Clients
Python package to communicate with Nintendo servers

To import this into your code, run `python setup.py install` or place the `nintendo` folder somewhere Python can find it.

You might need to adjust your scripts if you pull new commits from this package (it may receive backwards compatibility breaking changes at any time).

### Documentation
https://github.com/Kinnay/NintendoClients/wiki

### Requirements
* Python 3 (tested with 3.6.4)
* Python requests (http://docs.python-requets.org)
* BeautifulSoup4 and lxml

### Example scripts
* example_donkeykong.py downloads and prints DKC Tropical Freeze rankings, and downloads the replay file of the world record
* example_mariokart.py downloads and prints Mario Kart 8 rankings, and downloads a replay file
* example_miis.py requests and prints all kinds of information about the primary mii associated with a NNID
* example_friend_list.py requests and prints your friend list, incoming and outgoing friend requests, and blacklist
* example_friend_notifications.py listens for and prints friend notifications (when a friend starts a game for example)
* example_createroom.py shows how to create a friend room in Mario Kart 8. You'll get an error if you try to join it on a real Wii U though, because this package doesn't support P2P connections yet.
* example_mariokartdeluxe.py (which was supposed to download Mario Kart 8 Deluxe rankings) doesn't work anymore. The guest account is disabled on most Switch servers, and, while MK8 Deluxe used to be one of the few games it still worked on this no longer seems to be the case. Logging in with a real account is quite complicated on Switch servers (see [here](https://github.com/Kinnay/NintendoClients/wiki/Game-Server-Overview#switch)).

### More information
Some functions of the account server are only available after authentication. Authentication requires your Nintendo Network ID and password and serial number, device id, system version, region and country of your Wii U. To access specific game servers, you also need the game server id and sandbox access key of the server.
