# Nintendo Clients
> :warning: Keep in mind that Nintendo bans Switch devices that show suspicious behavior. This package tries to mimic the behavior of a real Switch as closely as possible, but using it is at your own risk. Make sure that you know what you are doing.

This package implements a client for various 3DS, Wii U and Switch servers. Check out the [documentation](https://nintendoclients.readthedocs.io) for the list of servers that are currently supported.

### Installation
This package requires Python 3.8 or later and can be installed with pip: `pip install nintendoclients`. This package uses [semantic versioning](https://semver.org/).

### Documentation
* [Nintendo's servers and protocols](https://github.com/Kinnay/NintendoClients/wiki)
* [The classes and functions in this package](https://nintendoclients.readthedocs.io)

### Example scripts
* **switch/**
    * **smm2_level.py:** Downloads a Super Mario Maker 2 level and its thumbnails, and prints information about both the level and its creator.
    * **smm2_ninji.py:** Requests the list of ninji courses and downloads a replay file.
    * **animalcrossing.py:** Searches for an island by dodo code and prints information about it.
    * **system_update.py:** Downloads the latest system update and unpacks it into exefs and romfs.
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
