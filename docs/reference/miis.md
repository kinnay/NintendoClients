
# Module: <code>nintendo.miis</code>

Provides a parser for FFL mii data.

<code>**class** [MiiData](#miidata)</code>
<span class="docs">The mii data class.</span>

## MiiData
`birth_platform: int`<br>
`mii_version: int`<br>
`font_region: int`<br>
`region_move: int`<br>
`copyable: bool`<br>
`local_only: bool`<br>
`author_id: list[int]`<br>
`mii_id: list[int]`<br>

`color: int`<br>
`birth_day: int`<br>
`birth_month: int`<br>
`gender: bool`<br>
`mii_name: str`<br>
`creator_name: str`<br>
`size: int`<br>
`fatness: int`<br>

`blush_type: int`<br>
`face_style: int`<br>
`face_color: int`<br>
`face_type: int`<br>

`hair_mirrored: bool`<br>
`hair_color: int`<br>
`hair_type: int`

`eye_thickness: int`<br>
`eye_scale: int`<br>
`eye_color: int`<br>
`eye_type: int`<br>
`eye_height: int`<br>
`eye_distance: int`<br>
`eye_rotation: int`

`eyebrow_thickness: int`<br>
`eyebrow_scale: int`<br>
`eyebrow_color: int`<br>
`eyebrow_type: int`<br>
`eyebrow_height: int`<br>
`eyebrow_distance: int`<br>
`eyebrow_rotation: int`

`nose_height: int`<br>
`nose_scale: int`<br>
`nose_type: int`

`mouth_thickness: int`<br>
`mouth_scale: int`<br>
`mouth_color: int`<br>
`mouth_type: int`<br>
`mouth_height: int`

`mustache_type: int`<br>
`mustache_height: int`<br>
`mustache_scale: int`

`beard_color: int`<br>
`beard_type: int`

`glass_height: int`<br>
`glass_scale: int`<br>
`glass_color: int`<br>
`glass_type: int`

`mole_ypos: int`<br>
`mole_xpos: int`<br>
`mole_scale: int`<br>
`mole_enabled: bool`

<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new mii instance.</span>

<code>**def build**() -> bytes</code><br>
<span class="docs">Encodes the mii data.</span>

<code style="color: blue">@classmethod</code><br>
<code>**def parse**(data: bytes) -> [MiiData](#miidata)</code><br>
<span class="docs">Parses the given mii data.</span>
