
## Changelog

### 4.1.0
* Added support for Switch system version 20.2.0 up to 20.4.0.
* Added support for the matchmaking protocol of Monster Hunter XX (3DS).
* Implemented RankingClient::GetScorePack for MK8D.
* Minor bug fixes.

*Released on 2025-09-19*

### 4.0.2
* Disable `device_token` and `edge_token` on system version 20.0.0 and later to avoid accidental usage.

*Released on 2025-06-21*

### 4.0.1
* **Bug fix:** using `device_token` or `edge_token` on system version 20.0.0 and later would send an invalid request to the server. This is now fixed.

<span style="color:red">**NOTE:**</span> It is recommended to use one of the `preload_*` functions or the `DAuthCache` class on system version 20.0.0 and later, to mimic the behavior of a real Switch.

*Released on 2025-06-21*

### 4.0.0
* **Breaking change:** some unknown fields in the `nintendo.nex.friends` module were given a name. If you were using the placeholder names in your code, update your code to use the new names.
* Added support for Switch system version 20.0.0 up to 20.1.5.
* Added various client ids for dauth, such as `er`, `sprofile` and `penne`.
* Implemented a dauth cache that mimics the preloading behavior that was introduced in 20.0.0.
* Added support for the ranking and matchmaking protocols of Mario Kart 8 (Wii U).

*Released on 2025-06-21*

### 3.0.3
* **Bug fix:** fixed typo, changed `BANNED_DEIVCE` to `BANNED_DEVICE` in `DAuthError` class.

*Released on 2024-12-28*

### 3.0.2
* **Bug fix:** fixed base64 decoding of dauth challenge. This fixes a bug that caused dauth to fail after a recent server update.

*Released on 2024-12-26*

### 3.0.1
* **Bug fix:** 19.0.1 support was missing in the previous release.

*Released on 2024-12-02*

### 3.0.0
* **Breaking change:** replaced `pkg_resources` by `importlib.resources`. This increases the minimum Python version to 3.11.
* **Bug fix**: removed ampersand before `device_auth_token` parameter in aauth challenge requests for 18.0.0+.
* **Bug fix**: added missing `naCountry` parameter to baas login requests for 18.0.0+.
* Added support for system version 19.0.0 and 19.0.1.

*Released on 2024-12-02*

### 2.2.1
* Fixed the header order in the dauth flow for system version 18.0.0 and later.

*Released on 2024-08-06*

### 2.2.0
* Added support for system version 18.1.0.

*Released on 2024-06-29*

### 2.1.0
* Added support for system version 17.0.1, 18.0.0 and 18.0.1.
* Added support for Switch gamecard authentication.
* Added support for the data store protocol of Miitopia 3DS.

*Released on 2024-05-04*

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
