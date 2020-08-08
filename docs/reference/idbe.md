
# Module: <code>nintendo.idbe</code>

Provides a client for the 3DS/Wii U [idbe server](https://github.com/Kinnay/NintendoClients/wiki/IDBE-Server) (icon databases).

<code>**class** [IDBEFile](#idbefile)</code><br>
<span class="docs">An `idbe` file.</span>

<code>**def get_platform**(title_id: int) -> str</code><br>
<span class="docs">Returns the platform name of the given title id, either `"ctr"` or `"wup"`.

<code>**async def download**(title_id: int, title_version: int = None) -> bytes</code><br>
<span class="docs">Downloads an encrypted `idbe` file from the server. If `title_version` is `None`, the latest title version is used.</span>

<code>**def decrypt**(data: bytes) -> bytes</code><br>
<span class="docs">Decrypts an `idbe` file.</span>

## Global Constants
Note that an `idbe` file has room for 16 different languages, but only 12 languages are defined. The remaining entries contain empty strings.<br>

<span class="docs">
<code>JAPANESE (0)</code><br>
<code>ENGLISH (1)</code><br>
<code>FRENCH (2)</code><br>
<code>GERMAN (3)</code><br>
<code>ITALIAN (4)</code><br>
<code>SPANISH (5)</code><br>
<code>CHINESE_SIMPLIFIED (6)</code><br>
<code>KOREAN (7)</code><br>
<code>DUTCH (8)</code><br>
<code>PORTUGUESE (9)</code><br>
<code>RUSSIAN (10)</code><br>
<code>CHINESE_TRADITIONAL (11)</code>
</span>

## IDBEFile
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `idbe` file.</span>

<code>**title_id**: int</code><br>
<span class="docs">The title id of the `idbe` file.</span>

<code>**title_version**: int</code><br>
<span class="docs">The title version of the `idbe` file.</span>

<code>**strings**: list[[IDBEStrings](#idbestrings)]</code><br>
<span class="docs">Strings from the `idbe` file in 16 different languages.</span>

<code>**tga**: bytes</code><br>
<span class="docs">The icon image as a `tga` file. Only defined if the `idbe` file belongs to a Wii U title.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def parse**(data: bytes) -> [IDBEFile](#idbefile)</code><br>
<span class="docs">Parses an `idbe` file.</span>

## IDBEStrings

<code>**short_name**: str</code><br>
<span class="docs">The short title name.</span>

<code>**long_name**: str</code><br>
<span class="docs">The full title name.</span>

<code>**publisher**: str</code><br>
<span class="docs">The name of the publisher.</span>
