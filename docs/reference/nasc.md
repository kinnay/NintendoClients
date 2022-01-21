
# Module: <code>nintendo.nasc</code>

Provides a client for [nasc.nintendowifi.net](https://github.com/kinnay/nintendo/wiki/NASC-Server).

<code>**class** [NASCError](#nascerror)(Exception)</code><br>
<span class="docs">Raised when the server returns an error code.</span>

<code>**class** [NASCClient](#nascclient)</code><br>
<span class="docs">The NASC client.</span>

## Global Constants
`MEDIA_TYPE_SYSTEM = 0`<br>
`MEDIA_TYPE_DIGITAL = 1`<br>
`MEDIA_TYPE_CARTRIDGE = 2`

## NASCError
This exception is raised when the server returns an error code.

`status_code: int`<br>
`return_code: int`<br>
`retry: bool`<br>
`datetime: datetime.datetime`

## NASCClient
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new NASC client.</span>

<code>**def set_context**(context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext)) -> None</code><br>
<span class="docs">Changes the TLS context. By default, the server certificate is verified with `Nintendo CA - G3`, and `CTR Common Prod 1` is used as the client certificate.</span>

<code>**def set_url**(url: str) -> None</code><br>
<span class="docs">Changes the server to which requests are sent. The default is `nasc.nintendowifi.net`.</span>

<code>**def set_environment**(environment: str) -> None</code><br>
<span class="docs">Changes the `servertype` parameter. The default is `"L1"` (production).</span>

<code>**def set_title**(title_id: int, title_version: int, product_code: str = "----", maker_code: str = "00", media_type: int = MEDIA_TYPE_SYSTEM, rom_id: bytes = None) -> None</code><br>
<span class="docs">Configures the current title. The `rom_id` is required only for cartridges. This is required for calls to `login`.</span>

<code>**def set_device**(serial_number: str, mac_address: str, fcd_cert: bytes, name: str = "", unit_code: str = "2") -> None</code><br>
<span class="docs">Configures the device. This is required for calls to `login`.</span>

<code>**def set_network**(bss_id: str, ap_info: str) -> None</code><br>
<span class="docs">Changes the `bssid` and `ap_info` parameters. By default, the `bssid` is random and `ap_info` is `01:0000000000`.</span>

<code>**def set_locale**(region: int, language: int) -> None</code><br>
<span class="docs">Changes the `region` and `language` parameters.</span>

<code>**def set_user**(pid: int, pid_hmac: str) -> None</code><br>
<span class="docs">Configures the user for logging in. Either `set_user` or `set_password` must be called before `login`.</span>

<code>**def set_password**(password: str) -> None</code><br>
<span class="docs">Configures the `passwd` parameter. Either `set_user` or `set_password` must be called before `login`.</span>

<code>**def set_sdk_version**(major_version: int, minor_version: int) -> None</code><br>
<span class="docs">Changes the content of the `sdkver` parameter. The default is `000000`.</span>

<code>**def set_fpd_version**(version: int) -> None</code><br>
<span class="docs">Changes the content of the `fpdver` parameter and user agent. The default is `15`.</span>

<code>**async def login**(game_server_id: int, ingamesn: str = "") -> [LoginResponse](#loginresponse)</code><br>
<span class="docs">Calls the `LOGIN` action on the server and returns the response or raises an exception.</span>

## LoginResponse
`host: str`<br>
`port: int`<br>
`token: str`<br>
`datetime: datetime.datetime`
