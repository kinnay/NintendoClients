
# Module: <code>nintendo.nex.kerberos</code>

Provides classes for Kerberos authentication. For details, click [here](https://github.com/Kinnay/NintendoClients/wiki/Kerberos-Authentication).

<code>**class** [KeyDerivationOld](#keyderivationold)</code><br>
<span class="docs">Implements the old key derivation method (used by 3DS and Wii U servers).</span>

<code>**class** [KeyDerivationNew](#keyderivationnew)</code><br>
<span class="docs">Implements the new key derivation method (used by Switch servers).</span>

<code>**class** [KerberosEncryption](#kerberosencryption)</code><br>
<span class="docs">Implements Kerberos encryption (RC4 + HMAC).</span>

<code>**class** [ClientTicket](#clientticket)</code><br>
<span class="docs">The Kerberos ticket that's visible to the client.</span>

<code>**class** [ServerTicket](#serverticket)</code><br>
<span class="docs">The internal part of the Kerberos ticket that's only visible to the server.</span>

<code>**class** [Credentials](#credentials)</code><br>
<span class="docs">Holds information that's required to log in on a secure server.</span>

## KeyDerivationOld
<code>**def _\_init__**(base_count: int = 65000, pid_count: int = 1024)</code><br>
<span class="docs">Creates a new key derivation instance.</span>

<code>**def derive_key**(password: bytes, pid: int) -> bytes</code><br>
<span class="docs">Derives the Kerberos key from the given password and user id.</span>

## KeyDerivationNew
<code>**def _\_init__**(base_count: int = 1, pid_count: int = 1)</code><br>
<span class="docs">Creates a new key derivation instance.</span>

<code>**def derive_key**(password: bytes, pid: int) -> bytes</code><br>
<span class="docs">Derives the Kerberos key from the given password and user id.</span>

## KerberosEncryption
<code>**def _\_init__**(key: bytes)</code><br>
<span class="docs">Creates a `KerberosEncryption` instance.</span>

<code>**def check**(data: bytes) -> bool</code><br>
<span class="docs">Checks the HMAC. Returns `True` if it is correct.</span>

<code>**def decrypt**(data: bytes) -> bytes</code><br>
<span class="docs">Checks the HMAC and decrypts the given data. Raises `ValueError` if the HMAC is incorrect.</span>

<code>**def encrypt**(data: bytes) -> bytes</code><br>
<span class="docs">Encrypts the given data and adds a HMAC.</span>

## ClientTicket
`session_key: bytes = None`<br>
<span class="docs">The session key of the ticket.</span><br>
`target: int = None`<br>
<span class="docs">The target user id of the ticket.</span><br>
`internal: bytes = None`<br>
<span class="docs">The internal ticket data that can only be decrypted by the target user.</span><br>

<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`ClientTicket`](#clientticket) instance. The attributes must be filled in manually.</span>

<code>**def encrypt**(key: bytes, settings: [Settings](../../settings#settings)) -> bytes</code><br>
<span class="docs">Encodes the ticket and encrypts it with the given Kerberos key.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def decrypt**(data: bytes, key: bytes, settings: [Settings](../../settings#settings)) -> [`ClientTicket`](#clientticket)</code><br>
<span class="docs">Decrypts `data` with the given Kerberos key and parses the ticket.</span>

## ServerTicket
<code>timestamp: [DateTime](../common#datetime) = None</code><br>
<span class="docs">Time at which the ticket was issued.</span><br>
`source: int = None`<br>
<span class="docs">The source user id of the ticket.</span><br>
`session_key: bytes = None`<br>
<span class="docs">The session key of the ticket.</span><br>

<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`ServerTicket`](#serverticket) instance. The attributes must be filled in manually.</span>

<code>**def encrypt**(key: bytes, settings: [Settings](../../settings#settings)) -> bytes</code><br>
<span class="docs">Encodes the ticket and encrypts it with the given Kerberos key.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def decrypt**(data: bytes, key: bytes, settings: [Settings](../../settings#settings)) -> [`ServerTicket`](#serverticket)</code><br>
<span class="docs">Decrypts `data` with the given Kerberos key and parses the ticket.</span>

## Credentials
<code>ticket: [ClientTicket](#clientticket)</code><br>
<span class="docs">The ticket received from the authentication server.</span><br>
`pid: int`<br>
<span class="docs">The source user id of the ticket.</span><br>
`cid: int`<br>
<span class="docs">The connection id.</span><br>

<code>**def _\_init__**(ticket: [ClientTicket](#clientticket), pid: int, cid: int)</code><br>
<span class="docs">Creates a new [`Credentials`](#credentials) object from the given ticket, user id and connection id.</span>
