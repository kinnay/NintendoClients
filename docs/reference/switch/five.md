
# Module: <code>nintendo.switch.five</code>
Provides a client for the [online play invitation server](https://github.com/kinnay/nintendo/wiki/Online-Play-Invitation-Server).

<code>**class** [FiveError](#fiveerror)(Exception)</code><br>
<span class="docs">Raised when the server returns an error code.</span>

<code>**class** [FiveClient](#fiveclient)</code><br>
<span class="docs">The client.</span>

## FiveError
This exception is raised when the server returns an error code. The following constants are defined in this class:

`INVALID_PARAMETER: int = 2`<br>
`INVALID_REQUEST_URI: int = 3`<br>
`UNAUTHORIZED: int = 6`<br>
`RESOURCE_NOT_FOUND: int = 10`<br>
`APPLICATION_DATA_TOO_LARGE: int = 11`

The error can be inspected using the following attributes:

<code>response: [HTTPResponse](https://anynet.readthedocs.io/en/latest/reference/http/#httpresponse)</code><br>
`code: int`<br>
`message: str`

## FiveClient
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new online play invitation client.</span>

<code>**def set_request_callback**(callback: Callable) -> None</code><br>
<span class="docs">By default, requests are performed with [`http.request`](https://anynet.readthedocs.io/en/latest/reference/http). This method lets you provide a custom callback instead.</span>

<code>**def set_context**(context: [TLSContext](https://anynet.readthedocs.io/en/latest/reference/tls/#tlscontext)) -> None</code><br>
<span class="docs">Changes the TLS context. By default, the server certificate is verified with `Nintendo CA - G3`.</span>

<code>**def set_host**(url: str) -> None</code><br>
<span class="docs">Changes the server to which the HTTP requests are sent. The default is `app.lp1.five.nintendo.net`.

<code>**def set_system_version**(version: int) -> None</code></br>
<span class="docs">Changes the system version that is emulated by the client. The system version should be given as a decimal integer. For example, `1002` indicates system version `10.0.2`. All system versions from `9.0.0` up to `19.0.0` are supported.</span>

<code>**async def get_unread_invitation_count**(access_token: str, user_id: int) -> int</code><br>
<span class="docs">Requests the number of unread invitations with `/v1/users/<id>/invitations/inbox?fields=count&read=false`.</span>

<code>**async def get_inbox**(access_token: str, user_id: int) -> dict</code><br>
<span class="docs">Requests the list of received online play invitations.</span>

<code>**async def get_invitation_group**(access_token: str, invitation_group_id: int) -> dict</code><br>
<span class="docs">Requests details about a specific invitation group.</span>

<code>**async def mark_as_read**(access_token: str, ids: list[int]) -> None</code><br>
<span class="docs">Marks the given list of invitations as read.</span>

<code>**async def mark_all_as_read**(access_token: str, user_id: int) -> None</code><br>
<span class="docs">Marks all received invitations as read.</span>

<code>**async def send_invitation**(access_token: str, receivers: list[int], application_id: int, application_group_id: int, application_data: bytes, messages: dict[str, str], application_id_match: bool = False) -> dict</code><br>
<span class="docs">Sends an online play invitation to at most 16 users. The application group id is usually the same as the application id (title id). The application data is game-specific and may contain at most 1024 bytes.</span>
