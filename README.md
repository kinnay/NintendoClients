# Nintendo Clients
Python package to communicate with Nintendo servers

To import this into your code, run `python setup.py install` or place the `nintendo` folder somewhere Python can find it.

You might need to adjust your scripts if you pull new commits from this package (it may receive backwards compatibility breaking changes at any time).

Keep in mind that Nintendo is still banning Switch devices. This package tries to mimic the behavior of a real Switch as closely as possible, but using it is at your own risk. If you want to avoid unnecessary requests, adjust the scripts to reuse tokens as long as possible: the dauth and aauth tokens are valid for 24 hours and the id token is valid for 3 hours.

The Switch examples that require a ticket only support digital titles (no game cards).

### Documentation
https://github.com/Kinnay/NintendoClients/wiki

### Requirements
* Python 3.6 or higher
* Python requests (http://docs.python-requests.org)
* BeautifulSoup4 and lxml
* PyCryptodome
* PyOpenSSL
* netifaces

### Example scripts
* **Wii U**
    * **example_donkeykong.py:** Downloads DKC Tropical Freeze rankings and the replay file of the world record.
    * **example_mariokart.py:** Downloads Mario Kart 8 rankings and the replay file of whoever is in 500th place.
    * **example_miis.py:** Requests all kinds of information about the primary mii associated with a NNID.
    * **example_friend_list.py:** Requests your friend list, incoming and outgoing friend requests, and blacklist.
    * **example_friend_notifications.py:** Listens for friend notifications (a friend starting a game for example).
    * **example_createroom.py:** Shows how to create a friend room in Mario Kart 8. You'll get an error if you try to join it on a real Wii U though, because this script does not implement the P2P protocol.<br><br>
* **Switch**
    * **example_lan_splatoon2.py:** Searches for Splatoon 2 LAN sessions and prints information about them.
    * **example_lan_smm2.py:** Searches for Super Mario Maker 2 LAN sessions and prints information about them.
    * **example_smm2.py:** Downloads a Super Mario Maker 2 level and its thumbnails, and prints information about both the level and its creator.
    * **example_smm2_ninji.py:** Requests the list of ninji courses and downloads a replay file.
    * **example_animalcrossing.py:** Searches for an island by dodo code and prints information about it.<br><br>
* **Custom**
    * **example_server.py:** Shows how to create a simple game server with both an authentication server and a secure server.
    * **example_server_login.py:** Logs in on a game server and disconnects immediately. This can be used to test custom servers (such as example_server.py).
