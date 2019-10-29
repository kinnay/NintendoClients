# Nintendo Clients
Python package to communicate with Nintendo servers

To import this into your code, run `python setup.py install` or place the `nintendo` folder somewhere Python can find it.

You might need to adjust your scripts if you pull new commits from this package (it may receive backwards compatibility breaking changes at any time).

### Documentation
https://github.com/Kinnay/NintendoClients/wiki

### Requirements
* Python 3.6 or higher
* Python requests (http://docs.python-requests.org)
* BeautifulSoup4 and lxml
* For `nintendo.pia.lan`:
    * PyCryptodome
    * netifaces

### Example scripts
* **Wii U**
    * **example_donkeykong.py:** Downloads DKC Tropical Freeze rankings and the replay file of the world record.
    * **example_mariokart.py:** Downloads Mario Kart 8 rankings and the replay file of whoever is in 500th place.
    * **example_miis.py:** Requests all kinds of information about the primary mii associated with a NNID.
    * **example_friend_list.py:** Requests your friend list, incoming and outgoing friend requests, and blacklist.
    * **example_friend_notifications.py:** Listens for friend notifications (a friend starting a game for example).
    * **example_createroom.py:** Shows how to create a friend room in Mario Kart 8. You'll get an error if you try to join it on a real Wii U though, because this package doesn't support P2P connections yet.<br><br>
* **Switch**
    * **example_mariokartdeluxe.py:** Downloads Mario Kart 8 Deluxe rankings. This script does not work anymore. Nintendo deleted the guest account around 22 July 2019.
    * **example_lan_mode.py:** Searches for a Splatoon 2 LAN session and prints information about it.<br><br>
* **Custom**
    * **example_server.py:** Shows how to create a simple game server with both an authentication server and a secure server.
    * **example_server_login.py:** Logs in on a game server and disconnects immediately. This can be used to test custom servers (such as example_server.py).
