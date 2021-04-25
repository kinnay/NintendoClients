
# Module: <code>nintendo.nex.settings</code>

Defines settings for `nex` classes.

<code>**class** [Settings](#settings)</code><br>
<span class="docs">Holds the settings.</span>

<code>**def default**() -> [Settings](#settings)</code><br>
<span class="docs">Creates a settings object with default settings.</span>

<code>**def load**(name: str) -> [Settings](#settings)</code><br>
<span class="docs">Loads the settings from the given configuration file. The following files are provided:<br>
<span class="docs">
`- 3ds`: provides reasonable defaults for 3DS applications.<br>
`- default`: provides reasonable defaults for Wii U applications.<br>
`- friends`: provides reasonable defaults for the 3DS / Wii U friend server.<br>
`- switch`: provides reasonable defaults for Switch applications.
</span></span>

## Settings
<code>TRANSPORT_UDP (0)</code><br>
<code>TRANSPORT_TCP (1)</code><br>
<code>TRANSPORT_WEBSOCKET (2)</code>

<code>COMPRESSION_NONE (0)</code><br>
<code>COMPRESSION_ZLIB (1)</code><br>

<code>ENCRYPTION_NONE (0)</code><br>
<code>ENCRYPTION_RC4 (1)</code><br>

<code>**def _\_getitem__**(name: str) -> object</code><br>
<span class="docs">Returns the value of a specific setting.</span>

<code>**def _\_setitem__**(name: str, value: object) -> None</code><br>
<span class="docs">Changes the value of a specific setting. The value is automatically converted to the appropriate type.</span>

<code>**def configure**(access_key: str, nex_version: int, client_version: int = None) -> None</code><br>
<span class="docs">Configures the `prudp.access_key`, `nex.version` and `nex.client_version` settings.</span>

<code>**def reset**() -> None</code><br>
<span class="docs">Resets all fields back to their defaults.</span>

<code>**def copy**() -> [Settings](#settings)</code><br>
<span class="docs">Returns a copy of the settings object.</span>

<code>**def load**(name: str) -> None</code><br>
<span class="docs">Loads the settings from the given configuration file and applies them on top of the current settings. Only the settings that are defined in the file are replaced.</span>

## Fields
The following fields are currently defined:

<code>nex.version: int = 0</code><br>
<span class="docs">The version of the `nex` library.</span><br>
<code>nex.client_version: int = 0</code><br>
<span class="docs">The client version sent to the server in `ValidateAndRequestTicketWithParam`.</span><br>
<code>nex.struct_header: int = 0</code><br>
<span class="docs">Enables structure headers.</span><br>
<code>nex.pid_size: int = 4</code><br>
<span class="docs">The size of a user id in bytes (`4` or `8`).</span><br>

<code>prudp.access_key: str = ""</code><br>
<span class="docs">The access key of the game server.</span>

<code>prudp.version: int = 2</code><br>
<span class="docs">The major version of the `prudp` protocol with UDP transport:<br>
<span class="docs">
`- 0`: both client and server use only `prudp v0`<br>
`- 1`: both client and server use only `prudp v1`<br>
`- 2`: client uses only `prudp v1`, server supports both `v0` and `v1`.
</span><br>
If the transport is different from UDP, the `lite` encoding is always used.
</span><br>
<code>prudp.minor_version: int = 4</code><br>
<span class="docs">The minor version of the `prudp` protocol. 
This is only relevant for `prudp v1` and `lite`.</span>

<code>prudp.transport: int = TRANSPORT_UDP</code><br>
<span class="docs">The underlying transport protocol for `prudp`.</span><br>
<code>prudp.compression: int = COMPRESSION_NONE</code><br>
<span class="docs">The compression algorithm used for data packets.</span><br>
<code>prudp.encryption: int = ENCRYPTION_RC4</code><br>
<span class="docs">The encryption algorithm used for data packets.</span>

<code>prudp.resend_timeout: float = 1</code><br>
<span class="docs">Time after which a packet is resent if no acknowledgement is received (in seconds).</span><br>
<code>prudp.resend_limit: int = 2</code><br>
<span class="docs">Number of retransmissions after which the connection is considered dead.</span><br>
<code>prudp.ping_timeout: float = 5</code><br>
<span class="docs">Time after which a ping packet is sent to keep the connection alive (in seconds).</span>

<code>prudp.fragment_size: int = 1300</code><br>
<span class="docs">The maximum size of a packet payload before it is split up into fragments.</span><br>
<code>prudp.max_substream_id: int = 0</code><br>
<span class="docs">The maximum substream id in `prudp v1`.</span><br>

<code>prudp_v0.signature_version: int = 0</code><br>
<span class="docs">The version of the packet signature in the `prudp v0` protocol.</span><br>
<code>prudp_v0.flags_version: int = 1</code><br>
<span class="docs"></span>The version of the `flags` field in the `prudp v0` protocol.<br>
<code>prudp_v0.checksum_version: int = 1</code><br>
<span class="docs">The version of the checksum algorithm in the `prudp v0` protocol.</span><br>

<code>kerberos.key_size: int = 32</code><br>
<span class="docs">The size of the session key in bytes.</span><br>
<code>kerberos.key_derivation: int = 0</code><br>
<span class="docs">The version of the key derivation algorithm for kerberos tickets.</span><br>
<code>kerberos.ticket_version: int = 1</code><br>
<span class="docs">The version of the internal data in kerberos tickets.
