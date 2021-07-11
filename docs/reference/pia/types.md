
# Module: <code>nintendo.pia.types</code>

Provides types that are used by various `pia` modules.

<code>**class** [Range](#range)</code><br>
<span class="docs">Specifies a range of values.</span>

<code>**class** [ResultRange](#resultrange)</code><br>
<span class="docs">A result range. Limits queries to a specific range.</span>

<code>**class** [StationLocation](#stationlocation)</code><br>
<span class="docs">Holds information about the address of a station. This is `pia`'s replacement for `nex`'s [`StationURL`](../nex/common.md#stationurl).</span>

<code>**class** [StationAddress](#stationaddress)</code><br>
<span class="docs">Holds the address of a station.</span>

<code>**class** [InetAddress](#inetaddress)</code><br>
<span class="docs">Holds an internet address.</span>

## Range
`min: int`<br>
`max: int`

<code>**def _\_init__**(min: int = 0, max: int = 10)</code><br>
<span class="docs">Creates a new [Range](#range) object.</span>

<code>**def _\_contains__**(value: int) -> bool</code><br>
<span class="docs">Returns `True` if `value` is between `min` and `max`.</span>

## ResultRange
`offset: int`<br>
`size: int`

<code>**def _\_init__**(offset: int = 0, size: int = 10)</code><br>
<span class="docs">Creates a new result range.</span>

## StationLocation
<code>public: [StationAddress](#stationaddress) = [StationAddress](#stationaddress)()</code><br>
<code>local: [StationAddress](#stationaddress) = [StationAddress](#stationaddress)()</code><br>
`pid: int = 0`<br>
`cid: int = 0`<br>
`rvcid: int = 0`<br>
`scheme: int = 0`<br>
`sid: int = 0`<br>
`stream_type: int = 0`<br>
`natm: int = 0`<br>
`natf: int = 0`<br>
`type: int = 3`<br>
`probeinit: int = 0`<br>
<code>relay: [InetAddress](#inetaddress) = [InetAddress](#inetaddress)()</code>

<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new station location.</span>

<code>**def copy**() -> [StationLocation](#stationlocation)</code>
<span class="docs">Returns a copy of the station location.</span>

<code>**def set_station_url**(url: [StationURL](../nex/common.md#stationurl)) -> None</code><br>
<span class="docs">Replaces the station location with the given station url.</span>

<code>**def get_station_url**() -> [StationURL](../nex/common.md#stationurl)</code><br>
<span class="docs">Converts the station location to a station url.</span>

## StationAddress
<code>inet: [InetAddress](#inetaddress)</code><br>
`extension_id: int = 0`

<code>**def _\_init__**(host: str = "0.0.0.0", port: int = 0)</code><br>
<span class="docs">Creates a new station address.</span>

## InetAddress
`host: str`<br>
`port: int`

<code>**def _\_init__**(host: str = "0.0.0.0", port: int = 0)</code><br>
<span class="docs">Creates a new internet address. Currently, only IPv4 addresses are supported.</span>
