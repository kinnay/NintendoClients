
# Module: <code>nintendo.switch</code>

Provides useful functions and classes related to Nintendo Switch.

<code>**class** [NDASError](#ndaserror)(Exception)</code><br>
<span class="docs">Raised when an error occurs in the [`dauth`](../dauth) or [`aauth`](../aauth) client.</span>

<code>**class** [KeySet](#keyset)</code><br>
<span class="docs">Reads a keyset file like `prod.keys`.</span>

<code>**class** [ProdInfo](#prodinfo)</code><br>
<span class="docs">Reads a decrypted `PRODINFO` file.</span>

<code>**def b64encode**(data: bytes) -> str</code><br>
<span class="docs">Encodes the given data with `base64url` without trailing `'='` characters.

<code>**def b64decode**(text: str) -> bytes</code><br>
<span class="docs">Decodes the given string with `base64url`. `text` does not have to be padded with `'='`.

## NDASError
`status_code: int`<br>
`errors: list[dict[str, str]]`

<code>**def _\_init__**(status_code: int, errors: list[dict[str, str]] = [])</code><br>
<span class="docs">Creates a new [NDASError](#ndaserror).</span>

## KeySet
<code>**def _\_init__**()</code><br>
<span class="docs">Creates an empty keyset.</span>

<code>**def _\_getitem__**(key: str) -> bytes</code><br>
<span class="docs">Returns the key with the given name.</span>

<code>**def _\_setitem__**(key: str, value: bytes) -> None</code><br>
<span class="docs">Adds or changes a key.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def load**(filename: str) -> [KeySet](#keyset)</code><br>
<span class="docs">Loads the keyset from the given file.</span>


## ProdInfo
<code>**def _\_init__**(keyset: [KeySet](#keyset), filename: str)</code><br>
<span class="docs">Creates a new [ProdInfo](#prodinfo) object from the given file with the given keyset.</span>

<code>**def get_tls_cert**() -> [TLSCertificate](https://anynet.readthedocs.io/en/latest/reference/tls#tlscertificate)</code><br>
<span class="docs">Extracts the device certificate.</span>

<code>**def get_tls_key**() -> [TLSPrivateKey](https://anynet.readthedocs.io/en/latest/reference/tls#tlsprivatekey)</code><br>
<span class="docs">Extract the private key that belongs to the device certificate.</span>
