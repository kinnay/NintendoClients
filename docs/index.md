
## Welcome to NintendoClients

This package lets you communicate with various 3DS, Wii U and Switch servers. For documentation about the servers and protocols click [here](https://github.com/kinnay/nintendo/wiki).

* [Features](#features)
* [Contributing](#contributing)
* [API Reference](#api-reference)
* [Changelog](changelog.md)

## Features
This package is able to do everything that's required to access a game server. It also provides a framework to host your own game servers. For example scripts, check out the [github repository](https://github.com/kinnay/nintendo). The following servers are currently supported:

* Switch:
	* Game servers (`nex`)
	* https://dauth-lp1.ndas.srv.nintendo.net
	* https://aauth-lp1.ndas.srv.nintendo.net
	* https://dragons.hac.lp1.dragons.nintendo.net
	* https://e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com
	* https://app.lp1.five.nintendo.net
	* https://sun.hac.lp1.d4c.nintendo.net
	* https://atumn.hac.lp1.d4c.nintendo.net
* Wii U:
	* Game servers (`nex`)
	* https://account.nintendo.net
* 3DS:
	* Game servers (`nex`)
	* https://nasc.nintendowifi.net

## Contributing
Feel free to open a pull request or issue on [github](https://github.com/kinnay/nintendo). If you open a pull request, please try to follow the current code style as much as possible, and consider writing a test for new features and bug fixes.

## API Reference

* nex
	* [aauser](reference/nex/aauser.md)
	* [account](reference/nex/account.md)
	* [authentication](reference/nex/authentication.md)
	* [backend](reference/nex/backend.md)
	* [common](reference/nex/common.md)
	* [datastore](reference/nex/datastore.md)
	* [datastore_smm](reference/nex/datastore_smm.md)
	* [datastore_smm2](reference/nex/datastore_smm2.md)
	* [debug](reference/nex/debug.md)
	* [errors](reference/nex/errors.md)
	* [friends](reference/nex/friends.md)
	* [health](reference/nex/health.md)
	* [hpp](reference/nex/hpp.md)
	* [kerberos](reference/nex/kerberos.md)
	* [matchmaking](reference/nex/matchmaking.md)
	* [matchmaking_eagle](reference/nex/matchmaking_eagle.md)
	* [messaging](reference/nex/messaging.md)
	* [monitoring](reference/nex/monitoring.md)
	* [nattraversal](reference/nex/nattraversal.md)
	* [nintendonotification](reference/nex/nintendonotification.md)
	* [notification](reference/nex/notification.md)
	* [prudp](reference/nex/prudp.md)
	* [ranking](reference/nex/ranking.md)
	* [ranking2](reference/nex/ranking2.md)
	* [remotelog](reference/nex/remotelog.md)
	* [rmc](reference/nex/rmc.md)
	* [screening](reference/nex/screening.md)
	* [secure](reference/nex/secure.md)
	* [streams](reference/nex/streams.md)
	* [subscriber](reference/nex/subscriber.md)
	* [utility](reference/nex/utility.md)
* [switch](reference/switch.md)
	* [aauth](reference/switch/aauth.md)
	* [atumn](reference/switch/atumn.md)
	* [baas](reference/switch/baas.md)
	* [dauth](reference/switch/dauth.md)
	* [dragons](reference/switch/dragons.md)
	* [five](reference/switch/five.md)
	* [sun](reference/switch/sun.md)
* [miis](reference/miis.md)
* [nasc](reference/nasc.md)
* [nnas](reference/nnas.md)
