
# Module: <code>nintendo.aauth</code>
Provides a client for the [application authentication server](https://github.com/kinnay/nintendo/wiki/AAuth-Server).

<code>**class** AAuthError([NDASError](switch.md#ndaserror))</code><br>
<span class="docs">Raised when the `aauth` server returns an error code.</span>

<code>**class** [AAuthClient](#aauthclient)</code><br>
<span class="docs">The `aauth` client.</span>

## AAuthClient
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `aauth` client.</span>

<code>**def set_url**(url: str) -> None</code><br>
<span class="docs">Changes the server to which the HTTP requests are sent. The default is `aauth-lp1.ndas.srv.nintendo.net`.

<code>**def set_user_agent**(user_agent: str) -> None</code><br>
<span class="docs">Changes the user agent of the `aauth` client. The default depends on the latest system version.

<code>**def set_power_state**(state: str) -> None</code><br>
<span class="docs">Changes the content of the `X-Nintendo-PowerState` header. The default is `"FA"`.

<code>**def set_system_version**(version: int) -> None</code></br>
<span class="docs">Updates the user agent for the given system version. The system version should be given as a decimal integer. For example, `1002` indicates system version `10.0.2`. All system versions from `9.0.0` and later are supported.</span>

<code>**def set_context**(context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext)) -> None</code><br>
<span class="docs">Changes the TLS context. By default, the server certificate is verified with `Nintendo CA - G3`.</span>

<code>**async def auth_system**(title_id: int, title_version: int, device_token: str) -> dict</code><br>
<span class="docs">Requests an application token from the `aauth` server for a system title with `/v3/application_auth_token`. The device token can be obtained from the [`dauth server`](dauth.md).</span>

<code>**async def auth_digital**(title_id: int, title_version: int, device_token: str, ticket: bytes) -> dict</code><br>
<span class="docs">Requests an application token from the `aauth` server for a digital title with `/v3/application_auth_token`. The device token can be obtained from the [`dauth server`](dauth.md).</span>
