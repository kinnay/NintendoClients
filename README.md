# Nintendo Clients
Python package to communicate with Nintendo servers

To import this into your code, run `pip install .` or place the `nintendo` folder somewhere Python can find it.

You might need to adjust your scripts if you pull new commits from this package (it may receive backwards compatibility breaking changes at any time).

Keep in mind that Nintendo is still banning Switch devices. This package tries to mimic the behavior of a real Switch as closely as possible, but using it is at your own risk. If you want to avoid unnecessary requests, adjust the scripts to reuse the tokens: the dauth and aauth tokens are valid for 24 hours and the id token is valid for 3 hours.

The Switch examples that require application authentication only support digital titles (no game cards).

### Documentation
* [Nintendo's servers and protocols](https://github.com/Kinnay/NintendoClients/wiki)
* [The classes and functions in this package](https://nintendoclients.readthedocs.io)

### Requirements
* Python 3.8 or higher
* https://github.com/kinnay/anynet

If you install this package with `pip install .` all requirements (except for Python itself) will be installed automatically.

### Example scripts
* **switch/**
    * **smm2_lan.py:** Searches for Super Mario Maker 2 LAN sessions and prints information about them.
    * **smm2_level.py:** Downloads a Super Mario Maker 2 level and its thumbnails, and prints information about both the level and its creator.
    * **smm2_ninji.py:** Requests the list of ninji courses and downloads a replay file.
    * **animalcrossing.py:** Searches for an island by dodo code and prints information about it.
    * **gamebuilder.py:** Downloads a game from Game Builder Garage, and requests basic metadata such as its creation date.
    * **lan_host.py:** Makes your name show up on your Switch if you search for LAN sessions in Splatoon 2.
    <br><br>
* **wiiu/**
    * **donkeykong.py:** Downloads DKC Tropical Freeze rankings and the replay file of the world record.
    * **mariokart.py:** Downloads Mario Kart 8 rankings and the replay file of whoever is in 500th place.
    * **miis.py:** Requests all kinds of information about the primary mii associated with a NNID.
    * **friends.py:** Requests your friend list, incoming and outgoing friend requests, and blacklist.
    <br><br>
* **3ds/**
	* **friends.py:** Changes your comment to 'Hello World'.
	<br><br>
* **custom/**
    * **server.py:** Shows how to create a simple game server with both an authentication server and a secure server.
    * **server_login.py:** Logs in on a game server and disconnects immediately. This can be used to test custom servers.
