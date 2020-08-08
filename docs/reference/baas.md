
# Module: <code>nintendo.baas</code>
Provides a client for the [BaaS server](https://github.com/Kinnay/NintendoClients/wiki/BAAS-Server).

<code>**class** [BAASError](#baaserror)(Exception)</code><br>
<span class="docs">Raised when the `BaaS` server returns an error code.</span>

<code>**class** [BAASClient](#baasclient)</code><br>
<span class="docs">The `BaaS` client.</span>

## BAASError
`status: int`<br>
`name: str`<br>
`title: str`<br>
`detail: str`<br>
`instance: str`<br>
`type: str`

## BAASClient
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `BaaS` client.</span>

<code>**def set_url**(url: str) -> None</code><br>
<span class="docs">Changes the server to which the HTTP requests are sent. The default is `e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com`.

<code>**def set_user_agent**(url: str) -> None</code><br>
<span class="docs">Changes the user agent of the `BaaS` client. The default depends on the latest system version.

<code>**def set_power_state**(state: str) -> None</code><br>
<span class="docs">Changes the content of the `X-Nintendo-PowerState` header. The default is `"FA"`.

<code>**def set_system_version**(version: int) -> None</code></br>
<span class="docs">Updates the user agent for the given system version. The system version should be given as a decimal integer. For example, `1002` indicates system version `10.0.2`. All system versions from `9.0.0` and later are supported.</span>

<code>**def set_context**(context: [TLSContext](../common/tls#tlscontext)) -> None</code><br>
<span class="docs">Changes the TLS context. By default, the server certificate is verified with default authorities.</span>

<code>**async def authenticate**(device_token: str) -> dict</code><br>
<span class="docs">Requests an authorization token with `/1.0.0/application/token`. This method must be called before any other requests can be made. The device token can be obtained from the [`dauth server`](../dauth).</span>

<code>**async def login**(id: int, password: str, access_token: str, app_token: str = None) -> dict</code><br>
<span class="docs">Logs in with the given user id and password, using `/1.0.0/login`. If an app token is provided, the server returns an id token that can be used to log in on a game server. App tokens can be obtained from the [`aauth server`](../aauth).</span>
