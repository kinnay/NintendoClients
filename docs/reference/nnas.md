
# Module: <code>nintendo.nnas</code>

Provides a client for the 3DS/Wii U [account server](https://github.com/kinnay/nintendo/wiki/Account-Server).

<code>**class** NNASError(Exception)</code><br>
<span class="docs">Raised when the server returns an error code.</span>

<code>**class** [NNASClient](#nnasclient)</code><br>
<span class="docs">The account server client.</span>

<code>**def calc_password_hash**(pid: int, password: str) -> str</code>
<span class="docs">Calculates the password hash for hash-based authentication and returns the hexdigest.</span>

## NNASClient
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new account server client.</span>

<code>**def set_context**(context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext)) -> None</code><br>
<span class="docs">Changes the TLS context. By default, the server certificate is verified with `Nintendo CA - G3`, and `Wii U Common Prod 1` is used as the client certificate.</span>

<code>**def set_url**(url: str) -> None</code><br>
<span class="docs">Changes the server to which requests are sent. The default is `account.nintendo.net`.</span>

<code>**def set_client_id**(client_id: str) -> None</code><br>
<span class="docs">Changes the content of the `X-Nintendo-Client-ID` header. The default is `"a2efa818a34fa16b8afbc8a74eba3eda"`.</span>

<code>**def set_client_secret**(client_secret: str) -> None</code><br>
<span class="docs">Changes the content of the `X-Nintendo-Client-Secret` header. The default is `"c91cdb5658bd4954ade78533a339cf9a"`.</span>

<code>**def set_platform_id**(platform_id: int) -> None</code><br>
<span class="docs">Changes the content of the `X-Nintendo-Platform-ID` header. The default is `1` (Wii U).</span>

<code>**def set_device_type**(device_type: int) -> None</code><br>
<span class="docs">Changes the content of the `X-Nintendo-Device-Type` header. The default is `2` (retail).</span>

<code>**def set_fpd_version**(version: int) -> None</code><br>
<span class="docs">Changes the content of the `X-Nintendo-FPD-Version` header. The default is `0`.</span>

<code>**def set_environment**(environment: str) -> None</code><br>
<span class="docs">Changes the content of the `X-Nintendo-Environment` header. The default is `"L1"` (production).</span>

<code>**def set_device**(device_id: int, serial_number: str, system_version: int, cert: str = None) -> None</code><br>
<span class="docs">Changes the `X-Nintendo-Device-ID`, `X-Nintendo-Serial-Number`, `X-Nintendo-System-Version` and `X-Nintendo-Device-Cert` headers. By default, the system version is set to `0x250` and the other headers are omitted.</span>

<code>**def set_locale**(region: int, country: str, language: str) -> None</code><br>
<span class="docs">Changes the `X-Nintendo-Region`, `X-Nintendo-Country` and `Accept-Language` headers. By default, the region is `4` (Europe), the country is `"NL"` (Netherlands) and the language is `"en"` (English).</span>

<code>**def set_title**(title_id: int, title_version: int) -> None</code><br>
<span class="docs">Changes the `X-Nintendo-Title-ID` and `X-Nintendo-Application-Version` headers. The `X-Nintendo-Unique-ID` header is also derived from the title id. By default, these headers are omitted.</span>

<code>**async def login**(username: str, password: str, password_type: str = None) -> [OAuth20](#oauth20)</code><br>
<span class="docs">Logs in on the account server. This method must be called prior to any method that accesses your account data.</span>

<code>**async def get_nex_token**(access_token: str, game_server_id: int) -> [NexToken](#nextoken)</code><br>
<span class="docs">Requests a `nex` token for the given game server.</span>

<code>**async def get_service_token**(access_token: str, client_id: str) -> str</code><br>
<span class="docs">Requests an independent service token for the given client id.</span>

<code>**async def get_profile**(access_token: str) -> [Profile](#profile)</code><br>
<span class="docs">Requests your profile.</span>

<code>**async def get_miis**(pids: list[int]) -> list[[Mii](#mii)]</code><br>
<span class="docs">Requests the miis for the given user ids.</span>

<code>**async def get_pids**(nnids: list[str]) -> dict[str, int]</code><br>
<span class="docs">Requests the user ids for the given Nintendo Network IDs.</span>

<code>**async def get_nnids**(pids: list[int]) -> dict[int, str]</code><br>
<span class="docs">Requests the Nintendo Network IDs for the given user ids.</span>

<code>**async def get_pid**(nnid: str) -> int</code><br>
<span class="docs">Requests the user id for the given Nintendo Network ID.</span>

<code>**async def get_nnid**(pid: int) -> str</code><br>
<span class="docs">Requests the Nintendo Network ID for the given user id.</span>

## Account
`domain: str`<br>
`type: str`<br>
`username: str`

## DeviceAttribute
`created_date: datetime.datetime`<br>
`name: str`<br>
`value: str`<br>

## Email
`id: int`<br>
`address: str`<br>
`primary: bool`<br>
`parent: bool`<br>
`reachable: bool`<br>
`type: str`<br>
`validated: bool`<br>
`validated_date: datetime.datetime`<br>

## Mii
`data: bytes`<br>
`id: int`<br>
`name: str`<br>
`images: list[MiiImage]`<br>
`primary: bool`<br>
`pid: int`<br>
`nnid: str`

## MiiImage
`id: int`<br>
`type: str`<br>
`url: str`<br>
`cached_url: str`<br>

## NexToken
`host: str`<br>
`port: int`<br>
`pid: int`<br>
`password: str`<br>
`token: str`

## OAuth20
`token: str`<br>
`refresh_token: str`<br>
`expires_in: int`

## Profile
<code>accounts: list[[Account](#account)]</code><br>
`active_flag: bool`<br>
`birth_date: datetime.datetime`<br>
`country: str`<br>
`create_date: datetime.datetime`<br>
<code>device_attributes: list[[DeviceAttribute](#deviceattribute)]</code><br>
`forgot_pw_email_sent: datetime.datetime`<br>
`gender: str`<br>
`language: str`<br>
`updated: datetime.datetime`<br>
`marketing_flag: bool`<br>
`off_device_flag: bool`<br>
`pid: int`<br>
<code>email: [Email](#email)</code><br>
<code>mii: [ProfileMii](#profilemii)</code><br>
`region: int`<br>
`temporary_password_expiration: datetime.datetime`<br>
`tz_name: str`<br>
`nnid: str`<br>
`utc_offset: int`<br>

## ProfileMii
`id: int`<br>
`name: str`<br>
`data: bytes`<br>
`primary: bool`<br>
`status: str`<br>
`hash: str`<br>
<code>images: list[[MiiImage](#miiimage)]</code><br>
