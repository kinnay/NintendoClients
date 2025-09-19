
# Module: <code>nintendo.switch.dauth</code>
Provides a client for the [device authentication server](https://github.com/kinnay/nintendo/wiki/DAuth-Server).

<code>**class** [DAuthError](#dautherror)(Exception)</code><br>
<span class="docs">Raised when the `dauth` server returns an error code.</span>

<code>**class** [DAuthClient](#dauthclient)</code><br>
<span class="docs">The `dauth` client.</span>

<code>**class** [DAuthCache](#dauthcache)</code><br>
<span class="docs">A cache for the dauth client that remembers preloaded tokens.</span>

## Global Constants
`CLIENT_ID_SCSI: int = 0x146C8AC7B8A0DB52`<br>
`CLIENT_ID_ER: int = 0x16E96F76850156D1`<br>
`CLIENT_ID_ATUM: int = 0x3117B250CAB38F45`<br>
`CLIENT_ID_ESHOP: int = 0x41F4A6491028E3C4`<br>
`CLIENT_ID_BCAT: int = 0x67BF9945B45248C6`<br>
`CLIENT_ID_SATA: int = 0x6AC5A6873FE5F68C`<br>
`CLIENT_ID_ACCOUNT_APPLET: int = 0x75FE236362FF5F8B`<br>
`CLIENT_ID_ACCOUNT: int = 0x81333C548B2E876D`<br>
`CLIENT_ID_NPNS: int = 0x83B72B05DC3278D7`<br>
`CLIENT_ID_BAAS: int = 0x8F849B5D34778D8E`<br>
`CLIENT_ID_BEACH: int = 0x93AF0ACB26258DE9`<br>
`CLIENT_ID_SPROFILE: int = 0xBAD8156F44AC935A`<br>
`CLIENT_ID_DRAGONS: int = 0xD5B6CAC2C1514C56`<br>
`CLIENT_ID_SCSI_POLICY: int = 0xD98185ACB55994B4`<br>
`CLIENT_ID_PCTL: int = 0xDC656EA03B63CF68`<br>
`CLIENT_ID_PREPO: int = 0xDF51C436BC01C437`<br>
`CLIENT_ID_PENNE: int = 0xE58171FE439390CE`

## DAuthError
This exception is raised when the `dauth` server returns an error code. The following constants are defined in this class:

`UNAUTHORIZED_DEVICE: int = 4`<br>
`SYSTEM_UPDATE_REQUIRED: int = 7`<br>
`BANNED_DEVICE: int = 8`<br>
`INTERNAL_SERVER_ERROR: int = 9`<br>
`GENERIC: int = 14`<br>
`CHALLENGE_EXPIRED: int = 15`<br>
`WRONG_MAC: int = 16`<br>
`BROKEN_DEVICE: int = 17`

The error can be inspected using the following attributes:

<code>response: [HTTPResponse](https://anynet.readthedocs.io/en/latest/reference/http/#httpresponse)</code><br>
`code: int`<br>
`message: str`

## DAuthClient
<b><span style="color: red">NOTE:</span></b> On system version 20.0.0 and later, it is recommended to request tokens through a [`DAuthCache`](#dauthcache) instead of using the `DAuthClient` directly. This is because the Switch requests multiple tokens at once on those system versions, and the `DAuthCache` makes it easier to mimic that behavior.</span>

<code>**def _\_init__**(keys: dict[str, bytes])</code><br>
<span class="docs">Creates a new `dauth` client with the given keys. The `dauth` client requires the `aes_kek_generation_source` and `master_key_XX` keys.</span>

<code>**def set_request_callback**(callback: Callable) -> None</code><br>
<span class="docs">By default, requests are performed with [`http.request`](https://anynet.readthedocs.io/en/latest/reference/http). This method lets you provide a custom callback instead.</span>

<code>**def set_context**(context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext)) -> None</code><br>
<span class="docs">Changes the TLS context. By default, the server certificate is verified with `Nintendo CA - G3` and no client certificate is used.</span>

<code>**def set_certificate**(cert: [TLSCertificate](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscertificate), key: [TLSPrivateKey](https://anynet.readthedocs.io/en/latest/reference/tls/#tlsprivatekey)) -> None</code>
<span class="docs">Changes the client certificate of the current TLS context. The server rejects all requests without a valid client certificate.</span>

<code>**def set_power_state**(state: str) -> None</code><br>
<span class="docs">Changes the content of the `X-Nintendo-PowerState` header. The default is `"FA"`.</span>

<code>**def set_platform_region**(region: int) -> None</code><br>
<span class="docs">Changes the platform region. This affects the `ist` parameter in the device authentication request. The default is `1`.</span>

<code>**def set_host**(host: str) -> None</code><br>
<span class="docs">Changes the server to which the HTTP requests are sent. The default is `dauth-lp1.ndas.srv.nintendo.net`.

<code>**def set_system_version**(version: int) -> None</code></br>
<span class="docs">Changes the system version that is emulated by the client. The system version should be given as a decimal integer. For example, `1002` is system version `10.0.2`. All system versions from `9.0.0` up to `20.4.0` are supported.</span>

<code>**async def challenge**() -> dict</code><br>
<span class="docs">Requests a challenge from the `dauth` server.</span>

<code>**async def device_token**(client_id: int) -> dict</code><br>
<span class="docs">Requests a device token from the `dauth` server. The challenge is done automatically. This method is available up to system version 19.0.1.<br><br>

<code>**async def edge_token**(client_id: int, vendor_id: str = "akamai") -> dict</code><br>
<span class="docs">Requests an edge token from the `dauth` server. The challenge is done automatically. This method is available up to system version 19.0.1.<br><br>

<code>**async def device_tokens**(client_ids: list[int]) -> dict</code><br>
<span class="docs">Requests a multiple device tokens from the `dauth` server. This method is available on system version 20.0.0 and later.</span>

<code>**async def edge_tokens**(token_requests: list[tuple[int, str]]) -> dict</code><br>
<span class="docs">Requests a multiple edge tokens from the `dauth` server. The `token_requests` parameter should contain a list of `(client_id, vendor_id)` tuples. This method is available on system version 20.0.0 and later.</span>

<code>**async def preload_device_tokens**() -> dict</code><br>
<span class="docs">Requests all device tokens that are preloaded by the Switch at once. This method is available on system version 20.0.0 and later.</span>

<code>**async def preload_edge_tokens**() -> dict</code><br>
<span class="docs">Requests all edge tokens that are preloaded by the Switch at once. This method is available on system version 20.0.0 and later.</span>

## DAuthCache
<code>**def _\_init__**(client: [DAuthClient](#dauthclient), expiration=None)</code><br>
<span class="docs">Creates a new dauth cache for the given client. If `expiration` is provided, tokens are discarded after the given number of seconds. Otherwise, the `expires_in` field that is returned by the server is used.</span>

<code>**async def device_token**(client_id: int) -> dict</code><br>
<span class="docs">Returns a device token from the cache or requests it from the dauth server if it is not present in the cache.</span>

<code>**async def edge_token**(client_id: int, vendor_id: str = "akamai") -> dict</code><br>
<span class="docs">Returns an edge token from the cache or requests it from the dauth server if it is not present in the cache.</span>
