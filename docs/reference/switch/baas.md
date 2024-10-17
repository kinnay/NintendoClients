
# Module: <code>nintendo.switch.baas</code>
Provides a client for the [BaaS server](https://github.com/kinnay/nintendo/wiki/BAAS-Server).

<code>**class** [PresenceState](#presencestate)</code><br>
<span class="docs">Provides predefined constants for the presence state.</span>

<code>**class** [BAASError](#baaserror)(Exception)</code><br>
<span class="docs">Raised when the `BaaS` server returns an error code.</span>

<code>**class** [BAASClient](#baasclient)</code><br>
<span class="docs">The `BaaS` client.</span>

## PresenceState
`INACTIVE: str = "INACTIVE"`<br>
`ONLINE: str = "ONLINE"`<br>
`PLAYING: str = "PLAYING"`

## BAASError
<code>response: [HTTPResponse](https://anynet.readthedocs.io/en/latest/reference/http/#httpresponse)</code><br>
`type: str`<br>
`name: str`<br>
`title: str`<br>
`detail: str`<br>
`status: int`<br>
`instance: str`

## BAASClient
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `BaaS` client.</span>

<code>**def set_request_callback**(callback: Callable) -> None</code><br>
<span class="docs">By default, requests are performed with [`http.request`](https://anynet.readthedocs.io/en/latest/reference/http). This method lets you provide a custom callback instead.</span>

<code>**def set_context**(context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext)) -> None</code><br>
<span class="docs">Changes the TLS context. By default, the server certificate is verified with default authorities.</span>

<code>**def set_host**(host: str) -> None</code><br>
<span class="docs">Changes the server to which the HTTP requests are sent. The default is `e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com`.

<code>**def set_power_state**(state: str) -> None</code><br>
<span class="docs">Changes the content of the `X-Nintendo-PowerState` header. The default is `"FA"`.

<code>**def set_system_version**(version: int) -> None</code></br>
<span class="docs">Changes the system version that is emulated by the client. The system version should be given as a decimal integer. For example, `1002` indicates system version `10.0.2`. All system versions from `9.0.0` up to `19.0.0` are supported.</span>

<code>**async def authenticate**(device_token: str) -> dict</code><br>
<span class="docs">Requests an authorization token with `/1.0.0/application/token`. This method must be called before any other requests can be made. The device token can be obtained from the [`dauth server`](dauth.md).</span>

<code>**async def login**(id: int, password: str, access_token: str, app_token: str = None, skip_verification: bool = False) -> dict</code><br>
<span class="docs">Logs in with the given user id and password, using `/1.0.0/login`. If an app token is provided, the server returns an id token that can be used to log in on a game server. App tokens can be obtained from the [`aauth server`](aauth.md). If `skip_verification` is `True` the client asks the server to skip NSO verification.</span>

<code>**async def register**(access_token: str) -> dict</code><br>
<span class="docs">Registers a new device account on the `BaaS` server.</span>

<code>**async def update_presence**(user_id: int, device_account_id: int, access_token: str, state: str, title_id: int, presence_group_id: int, app_fields: dict[str, str] = {}) -> dict</code><br>
<span class="docs">Updates your presence state by patching `/1.0.0/users/<id>/device_accounts/<id>`.</span>

<code>**async def get_friends**(user_id: int, access_token: str, count: int = 300)</code><br>
<span class="docs">Requests your friend list with `/2.0.0/users/<id>/friends`.</span>
