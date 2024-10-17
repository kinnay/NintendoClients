
# Module: <code>nintendo.switch.aauth</code>
Provides a client for the [application authentication server](https://github.com/kinnay/nintendo/wiki/AAuth-Server).

<code>**class** [AAuthError](#aautherror)(Exception)</code><br>
<span class="docs">Raised when the `aauth` server returns an error code.</span>

<code>**class** [AAuthClient](#aauthclient)</code><br>
<span class="docs">The `aauth` client.</span>

## AAuthError
This exception is raised when the `aauth` server returns an error code. The following constants are defined in this class:

`DEVICE_TOKEN_EXPIRED: int = 103`<br>
`ROMID_BANNED: int = 105`<br>
`UNAUTHORIZED_APPLICATION: int = 106`<br>
`SERVICE_CLOSED: int = 109`<br>
`APPLICATION_UPDATE_REQUIRED: int = 111`<br>
`INTERNAL_SERVER_ERROR: int = 112`<br>
`GENERIC: int = 118`<br>
`REGION_MISMATCH: int = 121`

The error can be inspected using the following attributes:

<code>response: [HTTPResponse](https://anynet.readthedocs.io/en/latest/reference/http/#httpresponse)</code><br>
`code: int`<br>
`message: str`

## AAuthClient
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `aauth` client.</span>

<code>**def set_request_callback**(callback: Callable) -> None</code><br>
<span class="docs">By default, requests are performed with [`http.request`](https://anynet.readthedocs.io/en/latest/reference/http). This method lets you provide a custom callback instead.</span>

<code>**def set_context**(context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext)) -> None</code><br>
<span class="docs">Changes the TLS context. By default, the server certificate is verified with `Nintendo CA - G3`.</span>

<code>**def set_host**(url: str) -> None</code><br>
<span class="docs">Changes the server to which the HTTP requests are sent. The default is `aauth-lp1.ndas.srv.nintendo.net`.

<code>**def set_power_state**(state: str) -> None</code><br>
<span class="docs">Changes the content of the `X-Nintendo-PowerState` header. The default is `"FA"`.

<code>**def set_system_version**(version: int) -> None</code></br>
<span class="docs">Changes the system version that is emulated by the client. The system version should be given as a decimal integer. For example, `1002` indicates system version `10.0.2`. All system versions from `9.0.0` up to `19.0.0` are supported.</span>

<code>**async def get_time**() -> tuple[int, str]</code><br>
<span class="docs">Requests the current server time with `/v1/time`. Returns a tuple that contains the current server time and your public IP address.</span>

<code>**async def challenge**(device_token: str) -> dict</code><br>
<span class="docs">Requests a challenge from the `aauth` server. The device token can be obtained from the [`dauth server`](dauth.md). The challenge is used for gamecard authentication.</span>

<code>**async def auth_system**(title_id: int, title_version: int, device_token: str) -> dict</code><br>
<span class="docs">Requests an application token from the `aauth` server for a system title. The device token can be obtained from the [`dauth server`](dauth.md).</span>

<code>**async def auth_digital**(title_id: int, title_version: int, device_token: str, cert: bytes | str) -> dict</code><br>
<span class="docs">Requests an application token from the `aauth` server for a digital title. The device token can be obtained from the [`dauth server`](dauth.md). Prior to system version `15.0.0`, the `cert` parameter must contain the raw ticket (which can be dumped with nxdumptool). In system version `15.0.0` and later, it must contain a contents authorization token instead (which can be obtained from the [`dragons server`](dragons.md)).</span>

<code>**async def auth_gamecard**(title_id: int, title_version: int, device_token: str, cert: bytes, gvt: bytes) -> dict</code><br>
<span class="docs">Requests an application token from the `aauth` server for a gamecard. The device token can be obtained from the [`dauth server`](dauth.md). The certificate can be obtained with nxdumptool. The `gvt` parameter must contain the challenge response. Unless you have the [Lotus](https://switchbrew.org/wiki/Lotus3) encryption keys, the challenge cannot be solved offline, but EpicUsername12 made [a tool](https://github.com/EpicUsername12/nx-netauth-link) that solves the challenge on a real Switch.</span>

<code>**async def auth_nocert**(title_id: int, title_version: int, device_token): str -> dict</code><br>
<span class="docs">Requests an application token from the `aauth` server for a title for which no ticket was found on the Switch.<br><br><b><span style="color: red">WARNING:</span></b> Do not use `auth_nocert` on a production server, because it will immediately ban your Switch.</span>
