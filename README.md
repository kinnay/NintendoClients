# Nintendo Clients
Python package to communicate with Nintendo servers

To import this into your code, run `python setup.py install` or place the `nintendo` folder somewhere Python can find it.

You might need to adjust your scripts if you pull new commits from this package (it may receive backwards compatibility breaking changes at any time).

### Documentation
https://github.com/Kinnay/NintendoClients/wiki

### Requirements
* Python 3 (tested with 3.6.4)
* Python requests (http://docs.python-requests.org)
* BeautifulSoup4 and lxml
* For `nintendo.pia.lan`:
    * PyCryptodome
    * netifaces

### Example scripts
* **Wii U:** example_donkeykong.py downloads and prints DKC Tropical Freeze rankings, and downloads the replay file of the world record
* **Wii U:** example_mariokart.py downloads and prints Mario Kart 8 rankings, and downloads a replay file
* **Wii U:** example_miis.py requests and prints all kinds of information about the primary mii associated with a NNID
* **Wii U:** example_friend_list.py requests and prints your friend list, incoming and outgoing friend requests, and blacklist
* **Wii U:** example_friend_notifications.py listens for and prints friend notifications (when a friend starts a game for example)
* **Wii U:** example_createroom.py shows how to create a friend room in Mario Kart 8. You'll get an error if you try to join it on a real Wii U though, because this package doesn't support P2P connections yet.
* **Switch:** example_mariokartdeluxe.py downloads and prints Mario Kart 8 Deluxe rankings. This script logs in as guest, so you don't need to dump any keys or other information from your Switch.
* **Switch:** example_lan_mode.py searches for a Splatoon 2 LAN session and prints information about it.
* **Custom:** example_server.py shows how to create a simple game server with both authentication and secure server.
* **Custom:** example_server_login.py logs in on a game server and disconnects immediately. This can be used to test custom servers (such as example_server.py).
