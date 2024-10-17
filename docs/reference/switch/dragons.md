
# Module: <code>nintendo.switch.dragons</code>
Provides a client for the [dragons servers](https://github.com/kinnay/nintendo/wiki/Dragons-Servers).

<code>**class** [DragonsError](#dragonserror)(Exception)</code><br>
<span class="docs">Raised when the dragons server returns an error code.</span>

<code>**class** [DragonsClient](#dragonsclient)</code><br>
<span class="docs">The dragons client.</span>

## DragonsError
<code>response: [HTTPResponse](https://anynet.readthedocs.io/en/latest/reference/http/#httpresponse)</code><br>
`type: str`<br>
`name: str`<br>
`title: str`<br>
`detail: str`<br>
`status: int`<br>
`invalid_params: list | None`

If present, the `invalid_params` field contains a list of dictionaries, each of which provides two keys: `name` and `reason`.

## DragonsClient
<code>**def _\_init__**(device_id: int = None)</code><br>
<span class="docs">Creates a new dragons client. The device id is required for all methods except for `contents_authorization_token_for_aauth`.</span>

<code>**def set_request_callback**(callback: Callable) -> None</code><br>
<span class="docs">By default, requests are performed with [`http.request`](https://anynet.readthedocs.io/en/latest/reference/http). This method lets you provide a custom callback instead.</span>

<code>**def set_context**(context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext)) -> None</code><br>
<span class="docs">Changes the TLS context. By default, the server certificate is verified with `Nintendo Class 2 CA - G3` and no client certificate is used.</span>

<code>**def set_certificate**(cert: [TLSCertificate](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscertificate), key: [TLSPrivateKey](https://anynet.readthedocs.io/en/latest/reference/tls/#tlsprivatekey)) -> None</code>
<span class="docs">Changes the client certificate of the current TLS context. The server rejects all requests without a valid client certificate.</span>

<code>**def set_hosts**(dragons: str, dragonst: str, tigers: str) -> None</code><br>
<span class="docs">Changes the servers to which the HTTP requests are sent. The defaults are:<br>
* `dragons.hac.lp1.dragons.nintendo.net`<br>
* `dragonst.hac.lp1.dragons.nintendo.net`<br>
* `tigers.hac.lp1.dragons.nintendo.net`
</span>

<code>**def set_system_version**(version: int) -> None</code></br>
<span class="docs">Changes the system version that is emulated by the client. The system version should be given as a decimal integer. For example, `1002` indicates system version `10.0.2`. All system versions from `9.0.0` up to `19.0.0` are supported.</span>

<code>**async def publish_device_linked_elicenses**(device_token: str) -> dict</code><br>
<span class="docs">Requests all elicenses that are linked to the given device. The device token can be obtained from the [`dauth server`](dauth.md).</span>

<code>**async def exercise_elicense**(device_token: str, elicense_ids: list[str], account_ids: list[int], current_account_id: int) -> None</code><br>
<span class="docs">Calls `/v1/elicenses/exercise` with the given parameters.</span>

<code>**async def contents_authorization_token_for_aauth**(device_token: str, elicense_id: str, na_id: int, title_id: int) -> dict</code><br>
<span class="docs">Requests a contents authorization token for [aauth](aauth.md). The device token can be obtained from the [`dauth server`](dauth.md).</span>
