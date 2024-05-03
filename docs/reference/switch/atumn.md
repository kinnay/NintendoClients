
# Module: <code>nintendo.switch.atumn</code>
Provides a client for the [system update content server](https://github.com/kinnay/nintendo/wiki/Atumn-Server).

<code>**class** [AtumnClient](#atumnclient)</code><br>
<span class="docs">The `atumn` client.</span>

## Atumn
<code>**def _\_init__**(device_id: int)</code><br>
<span class="docs">Creates a new atumn client. The device id can be obtained from [PRODINFO](../switch.md).</span>

<code>**def set_request_callback**(callback: Callable) -> None</code><br>
<span class="docs">By default, requests are performed with [`http.request`](https://anynet.readthedocs.io/en/latest/reference/http). This method lets you provide a custom callback instead.</span>

<code>**def set_context**(context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext)) -> None</code><br>
<span class="docs">Changes the TLS context. By default, the server certificate is verified with `Nintendo Class 2 CA - G3` and no client certificate is used.</span>

<code>**def set_certificate**(cert: [TLSCertificate](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscertificate), key: [TLSPrivateKey](https://anynet.readthedocs.io/en/latest/reference/tls/#tlsprivatekey)) -> None</code>
<span class="docs">Changes the client certificate of the current TLS context. The server rejects all requests without a valid client certificate.</span>

<code>**def set_host**(host: str) -> None</code><br>
<span class="docs">Changes the server to which the HTTP requests are sent. The default is: `atumn.hac.lp1.d4c.nintendo.net`.
</span>

<code>**def set_system_version**(version: int) -> None</code></br>
<span class="docs">Changes the system version that is emulated by the client. The system version should be given as a decimal integer. For example, `1002` indicates system version `10.0.2`. All system versions from `9.0.0` up to `18.0.1` are supported.</span>

<code>**async def download_content_metadata**(title_id: int, title_version: int, *, system_update: bool = False) -> bytes</code><br>
<span class="docs">Downloads the metadata NCA for the given title id and version. The `system_update` parameter should only be set to `True` for the system update title (`0100000000000816`).</span>

<code>**async def download_content**(content_id: str) -> bytes</code><br>
<span class="docs">Downloads the NCA for the given content id.</span>
