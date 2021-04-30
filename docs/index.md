
## Welcome to NintendoClients

This package lets you communicate with various Wii U and Switch servers. For documentation about the servers and protocols click [here](https://github.com/kinnay/nintendo/wiki).

* [Features](#features)
* [Contributing](#contributing)
* [API Reference](#api-reference)

## Features
This package is able to do everything that's required to access a game server. It also provides a framework to host your own game servers. For example scripts, check out the [github repository](https://github.com/kinnay/nintendo). The following servers are currently supported:

* Wii U:
	* Game servers (`nex`)
	* `account.nintendo.net`<br><br>
* Switch:
	* Game servers (`nex`)
	* `dauth-lp1.ndas.srv.nintendo.net`
	* `aauth-lp1.ndas.srv.nintendo.net`
	* `e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com`

## Contributing
Feel free to open a pull request or issue on [github](https://github.com/kinnay/nintendo). If you open a pull request, please try to follow the current code style as much as possible, and consider writing a test for new features and bug fixes.

## API Reference

* enl
	* [crypto](reference/enl/crypto)
* nex
	* [aauser](reference/nex/aauser)
	* [account](reference/nex/account)
	* [authentication](reference/nex/authentication)
	* [backend](reference/nex/backend)
	* [common](reference/nex/common)
	* [datastore](reference/nex/datastore)
	* [datastore_smm](reference/nex/datastore_smm)
	* [datastore_smm2](reference/nex/datastore_smm2)
	* [debug](reference/nex/debug)
	* [errors](reference/nex/errors)
	* [friends](reference/nex/friends)
	* [health](reference/nex/health)
	* [hpp](reference/nex/hpp)
	* [kerberos](reference/nex/kerberos)
	* [matchmaking](reference/nex/matchmaking)
	* [matchmaking_eagle](reference/nex/matchmaking_eagle)
	* [messaging](reference/nex/messaging)
	* [monitoring](reference/nex/monitoring)
	* [nattraversal](reference/nex/nattraversal)
	* [nintendonotification](reference/nex/nintendonotification)
	* [notification](reference/nex/notification)
	* [prudp](reference/nex/prudp)
	* [ranking](reference/nex/ranking)
	* [ranking2](reference/nex/ranking2)
	* [remotelog](reference/nex/remotelog)
	* [rmc](reference/nex/rmc)
	* [screening](reference/nex/screening)
	* [secure](reference/nex/secure)
	* [streams](reference/nex/streams)
	* [subscriber](reference/nex/subscriber)
	* [utility](reference/nex/utility)
* pia
	* [lan](reference/pia/lan)
	* [settings](reference/pia/settings)
	* [types](reference/pia/types)
* [aauth](reference/aauth)
* [baas](reference/baas)
* [dauth](reference/dauth)
* [games](reference/games)
* [miis](reference/miis)
* [nnas](reference/nnas)
* [sead](reference/sead)
* [switch](reference/switch)
