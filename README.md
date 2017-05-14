# NintendoClients
Python package to communicate with Nintendo servers

The goal of this project was a client that downloads rankings from DKC:TF, so you won't see much other features here.

To import this into your Python code, simply place the "proto" folder somewhere Python can find it.

Before you can access the account server, you have to place Nintendo's SSL client certificate in PEM format into the "files" folder named "wiiu_common_cert.pem" and "wiiu_commmon_key.pem". These can be downloaded from Nintendo's update server (title id 0005001B-10054000). Most functions of the account server are only available after authentication. Authentication requires your Nintendo Network ID and password and serial number, device id, system version, region and country of your Wii U. To access specific game servers, you also need the game server id and sandbox access key of the server.

An example script will be added later.

--
If you think this software infringes your copyright and would like me to delete it, please contact me here: ymarchand@me.com
