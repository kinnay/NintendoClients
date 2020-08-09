
## Welcome to NintendoClients

This package lets you communicate with various Wii U and Switch servers. For documentation about the servers and protocols go here: [https://github.com/Kinnay/NintendoClients/wiki](https://github.com/Kinnay/NintendoClients/wiki).

* [Features](#features)
* [Contributing](#contributing)
* [API Reference](#api-reference)

## Features
This package is able to do everything that's required to access a game server. It also provides a framework to host your own game servers. For example scripts, check out the [github repository](https://github.com/Kinnay/NintendoClients). The following servers are currently supported:

* Wii U:
	* Game servers (`nex`)
	* `account.nintendo.net`
	* `idbe-wup.cdn.nintendo.net`<br><br>
* Switch:
	* Game servers (`nex`)
	* `dauth-lp1.ndas.srv.nintendo.net`
	* `aauth-lp1.ndas.srv.nintendo.net`
	* `e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com`

## Contributing
If you would like to contribute code or knowledge in any way, feel free to open a pull request or issue on [github](https://github.com/Kinnay/NintendoClients). If you open a pull request, please try to follow the current code style as much as possible.

Some important points:

* Use tabs for indentation, and spaces for alignment.
* Use double quotes for strings, unless the string contains a double quote itself. In that case, using single quotes is ok.
* Use the following naming convention:

```python
GLOBAL_CONSTANT = "hi"

class ClassName:
	def method_name(self):
		self.variable_name = 0
```

* There is no hard limit on line lengths, but try to keep it somewhat reasonable.<br><br>

* Before you submit a pull request, run the tests to make sure that you did not break something. Simply run `pytest` in the root directory of the repository. This shouldn't take longer than a few seconds.
* If you fix a bug, consider writing a new test to make sure that this bug does not happen again.
* If you implement a new function or feature, add it to the documentation. After that, write a test to make sure that it works correctly. The test should only be based on the documentation, not on the code. We don't want to test implementation details. If the documentation is not clear enough to write a test, update the documentation.

## API Reference

* nintendo
	* common
		* [crypto](reference/common/crypto)
		* [http](reference/common/http)
		* [streams](reference/common/streams)
		* [tcp](reference/common/tcp)
		* [tls](reference/common/tls)
		* [types](reference/common/types)
		* [udp](reference/common/udp)
		* [util](reference/common/util)
		* [websocket](reference/common/websocket)
		* [xml](reference/common/xml)
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
	* [idbe](reference/idbe)
	* [miis](reference/miis)
	* [nnas](reference/nnas)
	* [sead](reference/sead)
	* [switch](reference/switch)
