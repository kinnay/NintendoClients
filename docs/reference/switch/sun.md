
# Module: <code>nintendo.switch.sun</code>
Provides a client for the [system update meta server](https://github.com/kinnay/nintendo/wiki/Sun-Server).

<code>**class** [SunError](#sunerror)(Exception)</code><br>
<span class="docs">Raised when the `sun` server returns an error code.</span>

<code>**class** [SunClient](#sunclient)</code><br>
<span class="docs">The `sun` client.</span>

## SunError
<code>response: [HTTPResponse](https://anynet.readthedocs.io/en/latest/reference/http/#httpresponse)</code><br>
`code: str`<br>
`message: str`

## SunClient
<code>**def _\_init__**(device_id: int)</code><br>
<span class="docs">Creates a new sun client. The device id can be obtained from [PRODINFO](../switch.md).</span>

<code>**def set_request_callback**(callback: Callable) -> None</code><br>
<span class="docs">By default, requests are performed with [`http.request`](https://anynet.readthedocs.io/en/latest/reference/http). This method lets you provide a custom callback instead.</span>

<code>**def set_context**(context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext)) -> None</code><br>
<span class="docs">Changes the TLS context. By default, the server certificate is verified with `Nintendo Class 2 CA - G3` and no client certificate is used.</span>

<code>**def set_certificate**(cert: [TLSCertificate](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscertificate), key: [TLSPrivateKey](https://anynet.readthedocs.io/en/latest/reference/tls/#tlsprivatekey)) -> None</code>
<span class="docs">Changes the client certificate of the current TLS context. The server rejects all requests without a valid client certificate.</span>

<code>**def set_host**(host: str) -> None</code><br>
<span class="docs">Changes the server to which the HTTP requests are sent. The default is: `sun.hac.lp1.d4c.nintendo.net`.
</span>

<code>**def set_system_version**(version: int) -> None</code></br>
<span class="docs">Changes the system version that is emulated by the client. The system version should be given as a decimal integer. For example, `1002` indicates system version `10.0.2`. All system versions from `9.0.0` up to `19.0.0` are supported.</span>

<code>**async def system_update_meta**() -> dict</code><br>
<span class="docs">Requests the latest system update metadata.</span>
