
# Module: <code>nintendo.nex.screening</code>

Provides a client and server for the `ScreeningProtocol`. This page was generated automatically from `screening.proto`.

<code>**class** [ScreeningClient](#screeningclient)</code><br>
<span class="docs">The client for the `ScreeningProtocol`.</span>

<code>**class** [ScreeningServer](#screeningserver)</code><br>
<span class="docs">The server for the `ScreeningProtocol`.</span>

<code>**class** [ReportCategory](#reportcategory)</code><br>

<code>**class** [ScreeningContextInfo](#screeningcontextinfo)([Structure](common.md))</code><br>
<code>**class** [ScreeningDataStoreContentParam](#screeningdatastorecontentparam)([Structure](common.md))</code><br>
<code>**class** [ScreeningUgcViolationParam](#screeningugcviolationparam)([Structure](common.md))</code><br>

## ScreeningClient
<code>**def _\_init__**(client: [RMCClient](rmc.md#rmcclient) / [HppClient](hpp.md#hppclient))</code><br>
<span class="docs">Creates a new [`ScreeningClient`](#screeningclient).</span>

<code>**async def report_data_store_content**(content_param: [ScreeningDataStoreContentParam](#screeningdatastorecontentparam), violation_param: [ScreeningUgcViolationParam](#screeningugcviolationparam)) -> None</code><br>
<span class="docs">Calls method `1` on the server.</span>

## ScreeningServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`ScreeningServer`](#screeningserver).</span>

<code>**async def logout**(client: [RMCClient](rmc.md#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def report_data_store_content**(client: [RMCClient](rmc.md#rmcclient), content_param: [ScreeningDataStoreContentParam](#screeningdatastorecontentparam), violation_param: [ScreeningUgcViolationParam](#screeningugcviolationparam)) -> None</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

## ReportCategory
This class defines the following constants:<br>
<span class="docs">
`INVALID = 0`<br>
`MIN = 1`<br>
`PERSONAL = 1`<br>
`CRIMINAL = 2`<br>
`IMMORAL = 3`<br>
`HARASSMENT = 4`<br>
`COMMERCIAL = 5`<br>
`SEXUALLY_EXPLICIT = 6`<br>
`OTHER = 7`<br>
`MAX = 7`<br>
</span>

## ScreeningContextInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `ScreeningContextInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>key: str</code><br>
<code>value: str</code><br>
</span><br>

## ScreeningDataStoreContentParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `ScreeningDataStoreContentParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>content_data_id: int</code><br>
<code>ugc_type: str</code><br>
<code>language: str</code><br>
<code>search_key: str</code><br>
</span><br>

## ScreeningUgcViolationParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `ScreeningUgcViolationParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>category: int</code><br>
<code>reason: str</code><br>
<code>context: list[[ScreeningContextInfo](#screeningcontextinfo)]</code><br>
<code>screenshot_data_id: int</code><br>
</span><br>

