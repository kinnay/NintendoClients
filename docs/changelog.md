
## Changelog

### 2.0.1
* **Bug fix**: added `nintendo.switch` to setup.py. The whole `nintendo.switch` folder was missing in the previous release.

*Released on 2023-11-12*

### 2.0.0
* **Breaking change:** moved all Switch-related clients into their own namespace. For example, `nintendo.dauth` is now `nintendo.switch.dauth`.
* **Breaking change:** dauth client ids are now global constants instead of members of `DAuthClient`.
* Implemented a client for the sun server (system update metadata).
* Implemented a client for the atumn server (system update content).

*Released on 2023-10-29*

### 1.1.0
* Added support for system version 17.0.0.
* Added default values to `RankingOrderParam.offset` and `RankingOrderParam.count`.

*Released on 2023-10-19*

### 1.0.0
First release with a changelog. Currently, the package implements everything that is required to communicate with NEX servers.

*Released on 2023-10-13*
