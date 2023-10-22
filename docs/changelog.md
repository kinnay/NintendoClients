
## Changelog

### 2.0.0 (upcoming)
* **Breaking change:** moved all Switch-related clients into their own namespace. For example, `nintendo.dauth` is now `nintendo.switch.dauth`.
* Implemented a client for the sun server (system update metadata).
* Implemented a client for the atumn server (system update content).

TODO: move dauth constants to top-level?

### 1.1.0
* Added support for system version 17.0.0.
* Added default values to `RankingOrderParam.offset` and `RankingOrderParam.count`.

*Released on 2023-10-19*

### 1.0.0
First release with a changelog. Currently, the package implements everything that is required to communicate with NEX servers.

*Released on 2023-10-13*
