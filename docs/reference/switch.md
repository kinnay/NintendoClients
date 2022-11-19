
# Module: <code>nintendo.switch</code>

Provides useful functions and classes related to Nintendo Switch.

<code>**def load_keys**(filename: str) -> dict[str, bytes]</code><br>
<span class="docs">Loads encryption keys from a file such as `prod.keys`.</span>

<code>**class** [ProdInfo](#prodinfo)</code><br>
<span class="docs">Reads a decrypted `PRODINFO` file.</span>

## ProdInfo
<code>**def _\_init__**(keys: dict[str, bytes], filename: str)</code><br>
<span class="docs">Creates a new [ProdInfo](#prodinfo) object from the given file. The key set should contain at least `ssl_rsa_kek`.</span>

<code>**def get_device_id**() -> int</code><br>
<span class="docs">Extracts the device id.</span>

<code>**def get_tls_cert**() -> [TLSCertificate](https://anynet.readthedocs.io/en/latest/reference/tls#tlscertificate)</code><br>
<span class="docs">Extracts the device certificate.</span>

<code>**def get_tls_key**() -> [TLSPrivateKey](https://anynet.readthedocs.io/en/latest/reference/tls#tlsprivatekey)</code><br>
<span class="docs">Extract the private key that belongs to the device certificate.</span>
