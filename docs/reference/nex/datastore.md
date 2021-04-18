
# Module: <code>nintendo.nex.datastore</code>

Provides a client and server for the `DataStoreProtocol`. This page was generated automatically from `datastore.proto`.

<code>**class** [DataStoreClient](#datastoreclient)</code><br>
<span class="docs">The client for the `DataStoreProtocol`.</span>

<code>**class** [DataStoreServer](#datastoreserver)</code><br>
<span class="docs">The server for the `DataStoreProtocol`.</span>

<code>**class** [DataStoreChangeMetaCompareParam](#datastorechangemetacompareparam)([Structure](../common))</code><br>
<code>**class** [DataStoreChangeMetaParam](#datastorechangemetaparam)([Structure](../common))</code><br>
<code>**class** [DataStoreChangeMetaParamV1](#datastorechangemetaparamv1)([Structure](../common))</code><br>
<code>**class** [DataStoreCompletePostParam](#datastorecompletepostparam)([Structure](../common))</code><br>
<code>**class** [DataStoreCompletePostParamV1](#datastorecompletepostparamv1)([Structure](../common))</code><br>
<code>**class** [DataStoreCompleteUpdateParam](#datastorecompleteupdateparam)([Structure](../common))</code><br>
<code>**class** [DataStoreDeleteParam](#datastoredeleteparam)([Structure](../common))</code><br>
<code>**class** [DataStoreGetMetaParam](#datastoregetmetaparam)([Structure](../common))</code><br>
<code>**class** [DataStoreGetNewArrivedNotificationsParam](#datastoregetnewarrivednotificationsparam)([Structure](../common))</code><br>
<code>**class** [DataStoreGetNotificationUrlParam](#datastoregetnotificationurlparam)([Structure](../common))</code><br>
<code>**class** [DataStoreGetSpecificMetaParam](#datastoregetspecificmetaparam)([Structure](../common))</code><br>
<code>**class** [DataStoreGetSpecificMetaParamV1](#datastoregetspecificmetaparamv1)([Structure](../common))</code><br>
<code>**class** [DataStoreKeyValue](#datastorekeyvalue)([Structure](../common))</code><br>
<code>**class** [DataStoreMetaInfo](#datastoremetainfo)([Structure](../common))</code><br>
<code>**class** [DataStoreNotification](#datastorenotification)([Structure](../common))</code><br>
<code>**class** [DataStoreNotificationV1](#datastorenotificationv1)([Structure](../common))</code><br>
<code>**class** [DataStorePasswordInfo](#datastorepasswordinfo)([Structure](../common))</code><br>
<code>**class** [DataStorePermission](#datastorepermission)([Structure](../common))</code><br>
<code>**class** [DataStorePersistenceInfo](#datastorepersistenceinfo)([Structure](../common))</code><br>
<code>**class** [DataStorePersistenceInitParam](#datastorepersistenceinitparam)([Structure](../common))</code><br>
<code>**class** [DataStorePersistenceTarget](#datastorepersistencetarget)([Structure](../common))</code><br>
<code>**class** [DataStorePrepareGetParam](#datastorepreparegetparam)([Structure](../common))</code><br>
<code>**class** [DataStorePrepareGetParamV1](#datastorepreparegetparamv1)([Structure](../common))</code><br>
<code>**class** [DataStorePreparePostParam](#datastorepreparepostparam)([Structure](../common))</code><br>
<code>**class** [DataStorePreparePostParamV1](#datastorepreparepostparamv1)([Structure](../common))</code><br>
<code>**class** [DataStorePrepareUpdateParam](#datastoreprepareupdateparam)([Structure](../common))</code><br>
<code>**class** [DataStoreRateObjectParam](#datastorerateobjectparam)([Structure](../common))</code><br>
<code>**class** [DataStoreRatingInfo](#datastoreratinginfo)([Structure](../common))</code><br>
<code>**class** [DataStoreRatingInfoWithSlot](#datastoreratinginfowithslot)([Structure](../common))</code><br>
<code>**class** [DataStoreRatingInitParam](#datastoreratinginitparam)([Structure](../common))</code><br>
<code>**class** [DataStoreRatingInitParamWithSlot](#datastoreratinginitparamwithslot)([Structure](../common))</code><br>
<code>**class** [DataStoreRatingLog](#datastoreratinglog)([Structure](../common))</code><br>
<code>**class** [DataStoreRatingTarget](#datastoreratingtarget)([Structure](../common))</code><br>
<code>**class** [DataStoreReqGetAdditionalMeta](#datastorereqgetadditionalmeta)([Structure](../common))</code><br>
<code>**class** [DataStoreReqGetInfo](#datastorereqgetinfo)([Structure](../common))</code><br>
<code>**class** [DataStoreReqGetInfoV1](#datastorereqgetinfov1)([Structure](../common))</code><br>
<code>**class** [DataStoreReqGetNotificationUrlInfo](#datastorereqgetnotificationurlinfo)([Structure](../common))</code><br>
<code>**class** [DataStoreReqPostInfo](#datastorereqpostinfo)([Structure](../common))</code><br>
<code>**class** [DataStoreReqPostInfoV1](#datastorereqpostinfov1)([Structure](../common))</code><br>
<code>**class** [DataStoreReqUpdateInfo](#datastorerequpdateinfo)([Structure](../common))</code><br>
<code>**class** [DataStoreSearchParam](#datastoresearchparam)([Structure](../common))</code><br>
<code>**class** [DataStoreSearchResult](#datastoresearchresult)([Structure](../common))</code><br>
<code>**class** [DataStoreSpecificMetaInfo](#datastorespecificmetainfo)([Structure](../common))</code><br>
<code>**class** [DataStoreSpecificMetaInfoV1](#datastorespecificmetainfov1)([Structure](../common))</code><br>
<code>**class** [DataStoreTouchObjectParam](#datastoretouchobjectparam)([Structure](../common))</code><br>

## DataStoreClient
<code>**def _\_init__**(client: [RMCClient](../rmc#rmcclient) / [HppClient](../hpp#hppclient))</code><br>
<span class="docs">Creates a new [`DataStoreClient`](#datastoreclient).</span>

<code>**async def prepare_get_object_v1**(param: [DataStorePrepareGetParamV1](#datastorepreparegetparamv1)) -> [DataStoreReqGetInfoV1](#datastorereqgetinfov1)</code><br>
<span class="docs">Calls method `1` on the server.</span>

<code>**async def prepare_post_object_v1**(param: [DataStorePreparePostParamV1](#datastorepreparepostparamv1)) -> [DataStoreReqPostInfoV1](#datastorereqpostinfov1)</code><br>
<span class="docs">Calls method `2` on the server.</span>

<code>**async def complete_post_object_v1**(param: [DataStoreCompletePostParamV1](#datastorecompletepostparamv1)) -> None</code><br>
<span class="docs">Calls method `3` on the server.</span>

<code>**async def delete_object**(param: [DataStoreDeleteParam](#datastoredeleteparam)) -> None</code><br>
<span class="docs">Calls method `4` on the server.</span>

<code>**async def delete_objects**(param: list[[DataStoreDeleteParam](#datastoredeleteparam)], transactional: bool) -> list[[Result](../common#result)]</code><br>
<span class="docs">Calls method `5` on the server.</span>

<code>**async def change_meta_v1**(param: [DataStoreChangeMetaParamV1](#datastorechangemetaparamv1)) -> None</code><br>
<span class="docs">Calls method `6` on the server.</span>

<code>**async def change_metas_v1**(data_ids: list[int], param: list[[DataStoreChangeMetaParamV1](#datastorechangemetaparamv1)], transactional: bool) -> list[[Result](../common#result)]</code><br>
<span class="docs">Calls method `7` on the server.</span>

<code>**async def get_meta**(param: [DataStoreGetMetaParam](#datastoregetmetaparam)) -> [DataStoreMetaInfo](#datastoremetainfo)</code><br>
<span class="docs">Calls method `8` on the server.</span>

<code>**async def get_metas**(data_ids: list[int], param: [DataStoreGetMetaParam](#datastoregetmetaparam)) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `9` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>info: list[[DataStoreMetaInfo](#datastoremetainfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def prepare_update_object**(param: [DataStorePrepareUpdateParam](#datastoreprepareupdateparam)) -> [DataStoreReqUpdateInfo](#datastorerequpdateinfo)</code><br>
<span class="docs">Calls method `10` on the server.</span>

<code>**async def complete_update_object**(param: [DataStoreCompleteUpdateParam](#datastorecompleteupdateparam)) -> None</code><br>
<span class="docs">Calls method `11` on the server.</span>

<code>**async def search_object**(param: [DataStoreSearchParam](#datastoresearchparam)) -> [DataStoreSearchResult](#datastoresearchresult)</code><br>
<span class="docs">Calls method `12` on the server.</span>

<code>**async def get_notification_url**(param: [DataStoreGetNotificationUrlParam](#datastoregetnotificationurlparam)) -> [DataStoreReqGetNotificationUrlInfo](#datastorereqgetnotificationurlinfo)</code><br>
<span class="docs">Calls method `13` on the server.</span>

<code>**async def get_new_arrived_notifications_v1**(param: [DataStoreGetNewArrivedNotificationsParam](#datastoregetnewarrivednotificationsparam)) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `14` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: list[[DataStoreNotificationV1](#datastorenotificationv1)]</code><br>
<code>has_next: bool</code><br>
</span>
</span>

<code>**async def rate_object**(target: [DataStoreRatingTarget](#datastoreratingtarget), param: [DataStoreRateObjectParam](#datastorerateobjectparam), fetch_ratings: bool) -> [DataStoreRatingInfo](#datastoreratinginfo)</code><br>
<span class="docs">Calls method `15` on the server.</span>

<code>**async def get_rating**(target: [DataStoreRatingTarget](#datastoreratingtarget), access_password: int) -> [DataStoreRatingInfo](#datastoreratinginfo)</code><br>
<span class="docs">Calls method `16` on the server.</span>

<code>**async def get_ratings**(data_ids: list[int], access_password: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `17` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>ratings: list[list[[DataStoreRatingInfoWithSlot](#datastoreratinginfowithslot)]]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def reset_rating**(target: [DataStoreRatingTarget](#datastoreratingtarget), update_password: int) -> None</code><br>
<span class="docs">Calls method `18` on the server.</span>

<code>**async def reset_ratings**(data_ids: list[int], transactional: bool) -> list[[Result](../common#result)]</code><br>
<span class="docs">Calls method `19` on the server.</span>

<code>**async def get_specific_meta_v1**(param: [DataStoreGetSpecificMetaParamV1](#datastoregetspecificmetaparamv1)) -> list[[DataStoreSpecificMetaInfoV1](#datastorespecificmetainfov1)]</code><br>
<span class="docs">Calls method `20` on the server.</span>

<code>**async def post_meta_binary**(param: [DataStorePreparePostParam](#datastorepreparepostparam)) -> int</code><br>
<span class="docs">Calls method `21` on the server.</span>

<code>**async def touch_object**(param: [DataStoreTouchObjectParam](#datastoretouchobjectparam)) -> None</code><br>
<span class="docs">Calls method `22` on the server.</span>

<code>**async def get_rating_with_log**(target: [DataStoreRatingTarget](#datastoreratingtarget), access_password: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `23` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>rating: [DataStoreRatingInfo](#datastoreratinginfo)</code><br>
<code>log: [DataStoreRatingLog](#datastoreratinglog)</code><br>
</span>
</span>

<code>**async def prepare_post_object**(param: [DataStorePreparePostParam](#datastorepreparepostparam)) -> [DataStoreReqPostInfo](#datastorereqpostinfo)</code><br>
<span class="docs">Calls method `24` on the server.</span>

<code>**async def prepare_get_object**(param: [DataStorePrepareGetParam](#datastorepreparegetparam)) -> [DataStoreReqGetInfo](#datastorereqgetinfo)</code><br>
<span class="docs">Calls method `25` on the server.</span>

<code>**async def complete_post_object**(param: [DataStoreCompletePostParam](#datastorecompletepostparam)) -> None</code><br>
<span class="docs">Calls method `26` on the server.</span>

<code>**async def get_new_arrived_notifications**(param: [DataStoreGetNewArrivedNotificationsParam](#datastoregetnewarrivednotificationsparam)) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `27` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>result: list[[DataStoreNotification](#datastorenotification)]</code><br>
<code>has_next: bool</code><br>
</span>
</span>

<code>**async def get_specific_meta**(param: [DataStoreGetSpecificMetaParam](#datastoregetspecificmetaparam)) -> list[[DataStoreSpecificMetaInfo](#datastorespecificmetainfo)]</code><br>
<span class="docs">Calls method `28` on the server.</span>

<code>**async def get_persistence_info**(owner_id: int, slot_id: int) -> [DataStorePersistenceInfo](#datastorepersistenceinfo)</code><br>
<span class="docs">Calls method `29` on the server.</span>

<code>**async def get_persistence_infos**(owner_id: int, slot_ids: list[int]) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `30` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>infos: list[[DataStorePersistenceInfo](#datastorepersistenceinfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def perpetuate_object**(persistence_slot_id: int, data_id: int, delete_last_object: bool) -> None</code><br>
<span class="docs">Calls method `31` on the server.</span>

<code>**async def unperpetuate_object**(persistence_slot_id: int, delete_last_object: bool) -> None</code><br>
<span class="docs">Calls method `32` on the server.</span>

<code>**async def prepare_get_object_or_meta_binary**(param: [DataStorePrepareGetParam](#datastorepreparegetparam)) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `33` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>get_info: [DataStoreReqGetInfo](#datastorereqgetinfo)</code><br>
<code>additional_meta: [DataStoreReqGetAdditionalMeta](#datastorereqgetadditionalmeta)</code><br>
</span>
</span>

<code>**async def get_password_info**(data_id: int) -> [DataStorePasswordInfo](#datastorepasswordinfo)</code><br>
<span class="docs">Calls method `34` on the server.</span>

<code>**async def get_password_infos**(data_ids: list[int]) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `35` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>infos: list[[DataStorePasswordInfo](#datastorepasswordinfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def get_metas_multiple_param**(params: list[[DataStoreGetMetaParam](#datastoregetmetaparam)]) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `36` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>infos: list[[DataStoreMetaInfo](#datastoremetainfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def complete_post_objects**(data_ids: list[int]) -> None</code><br>
<span class="docs">Calls method `37` on the server.</span>

<code>**async def change_meta**(param: [DataStoreChangeMetaParam](#datastorechangemetaparam)) -> None</code><br>
<span class="docs">Calls method `38` on the server.</span>

<code>**async def change_metas**(data_ids: list[int], param: list[[DataStoreChangeMetaParam](#datastorechangemetaparam)], transactional: bool) -> list[[Result](../common#result)]</code><br>
<span class="docs">Calls method `39` on the server.</span>

<code>**async def rate_objects**(targets: list[[DataStoreRatingTarget](#datastoreratingtarget)], param: list[[DataStoreRateObjectParam](#datastorerateobjectparam)], transactional: bool, fetch_ratings: bool) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `40` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>infos: list[[DataStoreRatingInfo](#datastoreratinginfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def post_meta_binary_with_data_id**(data_id: int, param: [DataStorePreparePostParam](#datastorepreparepostparam)) -> None</code><br>
<span class="docs">Calls method `41` on the server.</span>

<code>**async def post_meta_binaries_with_data_id**(data_ids: list[int], param: list[[DataStorePreparePostParam](#datastorepreparepostparam)], transactional: bool) -> list[[Result](../common#result)]</code><br>
<span class="docs">Calls method `42` on the server.</span>

<code>**async def rate_object_with_posting**(target: [DataStoreRatingTarget](#datastoreratingtarget), rate_param: [DataStoreRateObjectParam](#datastorerateobjectparam), post_param: [DataStorePreparePostParam](#datastorepreparepostparam), fetch_ratings: bool) -> [DataStoreRatingInfo](#datastoreratinginfo)</code><br>
<span class="docs">Calls method `43` on the server.</span>

<code>**async def rate_objects_with_posting**(targets: list[[DataStoreRatingTarget](#datastoreratingtarget)], rate_param: list[[DataStoreRateObjectParam](#datastorerateobjectparam)], post_param: list[[DataStorePreparePostParam](#datastorepreparepostparam)], transactional: bool, fetch_ratings: bool) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `44` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>ratings: list[[DataStoreRatingInfo](#datastoreratinginfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def get_object_infos**(data_ids: list[int]) -> [RMCResponse](../common)</code><br>
<span class="docs">Calls method `45` on the server. The RMC response has the following attributes:<br>
<span class="docs">
<code>infos: list[[DataStoreReqGetInfo](#datastorereqgetinfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def search_object_light**(param: [DataStoreSearchParam](#datastoresearchparam)) -> [DataStoreSearchResult](#datastoresearchresult)</code><br>
<span class="docs">Calls method `46` on the server.</span>

## DataStoreServer
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new [`DataStoreServer`](#datastoreserver).</span>

<code>**async def logout**(client: [RMCClient](../rmc#rmcclient)) -> None</code><br>
<span class="docs">Called whenever a client is disconnected. May be overridden by a subclass.</span>

<code>**async def prepare_get_object_v1**(client: [RMCClient](../rmc#rmcclient), param: [DataStorePrepareGetParamV1](#datastorepreparegetparamv1)) -> [DataStoreReqGetInfoV1](#datastorereqgetinfov1)</code><br>
<span class="docs">Handler for method `1`. This method should be overridden by a subclass.</span>

<code>**async def prepare_post_object_v1**(client: [RMCClient](../rmc#rmcclient), param: [DataStorePreparePostParamV1](#datastorepreparepostparamv1)) -> [DataStoreReqPostInfoV1](#datastorereqpostinfov1)</code><br>
<span class="docs">Handler for method `2`. This method should be overridden by a subclass.</span>

<code>**async def complete_post_object_v1**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreCompletePostParamV1](#datastorecompletepostparamv1)) -> None</code><br>
<span class="docs">Handler for method `3`. This method should be overridden by a subclass.</span>

<code>**async def delete_object**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreDeleteParam](#datastoredeleteparam)) -> None</code><br>
<span class="docs">Handler for method `4`. This method should be overridden by a subclass.</span>

<code>**async def delete_objects**(client: [RMCClient](../rmc#rmcclient), param: list[[DataStoreDeleteParam](#datastoredeleteparam)], transactional: bool) -> list[[Result](../common#result)]</code><br>
<span class="docs">Handler for method `5`. This method should be overridden by a subclass.</span>

<code>**async def change_meta_v1**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreChangeMetaParamV1](#datastorechangemetaparamv1)) -> None</code><br>
<span class="docs">Handler for method `6`. This method should be overridden by a subclass.</span>

<code>**async def change_metas_v1**(client: [RMCClient](../rmc#rmcclient), data_ids: list[int], param: list[[DataStoreChangeMetaParamV1](#datastorechangemetaparamv1)], transactional: bool) -> list[[Result](../common#result)]</code><br>
<span class="docs">Handler for method `7`. This method should be overridden by a subclass.</span>

<code>**async def get_meta**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreGetMetaParam](#datastoregetmetaparam)) -> [DataStoreMetaInfo](#datastoremetainfo)</code><br>
<span class="docs">Handler for method `8`. This method should be overridden by a subclass.</span>

<code>**async def get_metas**(client: [RMCClient](../rmc#rmcclient), data_ids: list[int], param: [DataStoreGetMetaParam](#datastoregetmetaparam)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `9`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>info: list[[DataStoreMetaInfo](#datastoremetainfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def prepare_update_object**(client: [RMCClient](../rmc#rmcclient), param: [DataStorePrepareUpdateParam](#datastoreprepareupdateparam)) -> [DataStoreReqUpdateInfo](#datastorerequpdateinfo)</code><br>
<span class="docs">Handler for method `10`. This method should be overridden by a subclass.</span>

<code>**async def complete_update_object**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreCompleteUpdateParam](#datastorecompleteupdateparam)) -> None</code><br>
<span class="docs">Handler for method `11`. This method should be overridden by a subclass.</span>

<code>**async def search_object**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreSearchParam](#datastoresearchparam)) -> [DataStoreSearchResult](#datastoresearchresult)</code><br>
<span class="docs">Handler for method `12`. This method should be overridden by a subclass.</span>

<code>**async def get_notification_url**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreGetNotificationUrlParam](#datastoregetnotificationurlparam)) -> [DataStoreReqGetNotificationUrlInfo](#datastorereqgetnotificationurlinfo)</code><br>
<span class="docs">Handler for method `13`. This method should be overridden by a subclass.</span>

<code>**async def get_new_arrived_notifications_v1**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreGetNewArrivedNotificationsParam](#datastoregetnewarrivednotificationsparam)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `14`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: list[[DataStoreNotificationV1](#datastorenotificationv1)]</code><br>
<code>has_next: bool</code><br>
</span>
</span>

<code>**async def rate_object**(client: [RMCClient](../rmc#rmcclient), target: [DataStoreRatingTarget](#datastoreratingtarget), param: [DataStoreRateObjectParam](#datastorerateobjectparam), fetch_ratings: bool) -> [DataStoreRatingInfo](#datastoreratinginfo)</code><br>
<span class="docs">Handler for method `15`. This method should be overridden by a subclass.</span>

<code>**async def get_rating**(client: [RMCClient](../rmc#rmcclient), target: [DataStoreRatingTarget](#datastoreratingtarget), access_password: int) -> [DataStoreRatingInfo](#datastoreratinginfo)</code><br>
<span class="docs">Handler for method `16`. This method should be overridden by a subclass.</span>

<code>**async def get_ratings**(client: [RMCClient](../rmc#rmcclient), data_ids: list[int], access_password: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `17`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>ratings: list[list[[DataStoreRatingInfoWithSlot](#datastoreratinginfowithslot)]]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def reset_rating**(client: [RMCClient](../rmc#rmcclient), target: [DataStoreRatingTarget](#datastoreratingtarget), update_password: int) -> None</code><br>
<span class="docs">Handler for method `18`. This method should be overridden by a subclass.</span>

<code>**async def reset_ratings**(client: [RMCClient](../rmc#rmcclient), data_ids: list[int], transactional: bool) -> list[[Result](../common#result)]</code><br>
<span class="docs">Handler for method `19`. This method should be overridden by a subclass.</span>

<code>**async def get_specific_meta_v1**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreGetSpecificMetaParamV1](#datastoregetspecificmetaparamv1)) -> list[[DataStoreSpecificMetaInfoV1](#datastorespecificmetainfov1)]</code><br>
<span class="docs">Handler for method `20`. This method should be overridden by a subclass.</span>

<code>**async def post_meta_binary**(client: [RMCClient](../rmc#rmcclient), param: [DataStorePreparePostParam](#datastorepreparepostparam)) -> int</code><br>
<span class="docs">Handler for method `21`. This method should be overridden by a subclass.</span>

<code>**async def touch_object**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreTouchObjectParam](#datastoretouchobjectparam)) -> None</code><br>
<span class="docs">Handler for method `22`. This method should be overridden by a subclass.</span>

<code>**async def get_rating_with_log**(client: [RMCClient](../rmc#rmcclient), target: [DataStoreRatingTarget](#datastoreratingtarget), access_password: int) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `23`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>rating: [DataStoreRatingInfo](#datastoreratinginfo)</code><br>
<code>log: [DataStoreRatingLog](#datastoreratinglog)</code><br>
</span>
</span>

<code>**async def prepare_post_object**(client: [RMCClient](../rmc#rmcclient), param: [DataStorePreparePostParam](#datastorepreparepostparam)) -> [DataStoreReqPostInfo](#datastorereqpostinfo)</code><br>
<span class="docs">Handler for method `24`. This method should be overridden by a subclass.</span>

<code>**async def prepare_get_object**(client: [RMCClient](../rmc#rmcclient), param: [DataStorePrepareGetParam](#datastorepreparegetparam)) -> [DataStoreReqGetInfo](#datastorereqgetinfo)</code><br>
<span class="docs">Handler for method `25`. This method should be overridden by a subclass.</span>

<code>**async def complete_post_object**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreCompletePostParam](#datastorecompletepostparam)) -> None</code><br>
<span class="docs">Handler for method `26`. This method should be overridden by a subclass.</span>

<code>**async def get_new_arrived_notifications**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreGetNewArrivedNotificationsParam](#datastoregetnewarrivednotificationsparam)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `27`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>result: list[[DataStoreNotification](#datastorenotification)]</code><br>
<code>has_next: bool</code><br>
</span>
</span>

<code>**async def get_specific_meta**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreGetSpecificMetaParam](#datastoregetspecificmetaparam)) -> list[[DataStoreSpecificMetaInfo](#datastorespecificmetainfo)]</code><br>
<span class="docs">Handler for method `28`. This method should be overridden by a subclass.</span>

<code>**async def get_persistence_info**(client: [RMCClient](../rmc#rmcclient), owner_id: int, slot_id: int) -> [DataStorePersistenceInfo](#datastorepersistenceinfo)</code><br>
<span class="docs">Handler for method `29`. This method should be overridden by a subclass.</span>

<code>**async def get_persistence_infos**(client: [RMCClient](../rmc#rmcclient), owner_id: int, slot_ids: list[int]) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `30`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>infos: list[[DataStorePersistenceInfo](#datastorepersistenceinfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def perpetuate_object**(client: [RMCClient](../rmc#rmcclient), persistence_slot_id: int, data_id: int, delete_last_object: bool) -> None</code><br>
<span class="docs">Handler for method `31`. This method should be overridden by a subclass.</span>

<code>**async def unperpetuate_object**(client: [RMCClient](../rmc#rmcclient), persistence_slot_id: int, delete_last_object: bool) -> None</code><br>
<span class="docs">Handler for method `32`. This method should be overridden by a subclass.</span>

<code>**async def prepare_get_object_or_meta_binary**(client: [RMCClient](../rmc#rmcclient), param: [DataStorePrepareGetParam](#datastorepreparegetparam)) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `33`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>get_info: [DataStoreReqGetInfo](#datastorereqgetinfo)</code><br>
<code>additional_meta: [DataStoreReqGetAdditionalMeta](#datastorereqgetadditionalmeta)</code><br>
</span>
</span>

<code>**async def get_password_info**(client: [RMCClient](../rmc#rmcclient), data_id: int) -> [DataStorePasswordInfo](#datastorepasswordinfo)</code><br>
<span class="docs">Handler for method `34`. This method should be overridden by a subclass.</span>

<code>**async def get_password_infos**(client: [RMCClient](../rmc#rmcclient), data_ids: list[int]) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `35`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>infos: list[[DataStorePasswordInfo](#datastorepasswordinfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def get_metas_multiple_param**(client: [RMCClient](../rmc#rmcclient), params: list[[DataStoreGetMetaParam](#datastoregetmetaparam)]) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `36`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>infos: list[[DataStoreMetaInfo](#datastoremetainfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def complete_post_objects**(client: [RMCClient](../rmc#rmcclient), data_ids: list[int]) -> None</code><br>
<span class="docs">Handler for method `37`. This method should be overridden by a subclass.</span>

<code>**async def change_meta**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreChangeMetaParam](#datastorechangemetaparam)) -> None</code><br>
<span class="docs">Handler for method `38`. This method should be overridden by a subclass.</span>

<code>**async def change_metas**(client: [RMCClient](../rmc#rmcclient), data_ids: list[int], param: list[[DataStoreChangeMetaParam](#datastorechangemetaparam)], transactional: bool) -> list[[Result](../common#result)]</code><br>
<span class="docs">Handler for method `39`. This method should be overridden by a subclass.</span>

<code>**async def rate_objects**(client: [RMCClient](../rmc#rmcclient), targets: list[[DataStoreRatingTarget](#datastoreratingtarget)], param: list[[DataStoreRateObjectParam](#datastorerateobjectparam)], transactional: bool, fetch_ratings: bool) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `40`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>infos: list[[DataStoreRatingInfo](#datastoreratinginfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def post_meta_binary_with_data_id**(client: [RMCClient](../rmc#rmcclient), data_id: int, param: [DataStorePreparePostParam](#datastorepreparepostparam)) -> None</code><br>
<span class="docs">Handler for method `41`. This method should be overridden by a subclass.</span>

<code>**async def post_meta_binaries_with_data_id**(client: [RMCClient](../rmc#rmcclient), data_ids: list[int], param: list[[DataStorePreparePostParam](#datastorepreparepostparam)], transactional: bool) -> list[[Result](../common#result)]</code><br>
<span class="docs">Handler for method `42`. This method should be overridden by a subclass.</span>

<code>**async def rate_object_with_posting**(client: [RMCClient](../rmc#rmcclient), target: [DataStoreRatingTarget](#datastoreratingtarget), rate_param: [DataStoreRateObjectParam](#datastorerateobjectparam), post_param: [DataStorePreparePostParam](#datastorepreparepostparam), fetch_ratings: bool) -> [DataStoreRatingInfo](#datastoreratinginfo)</code><br>
<span class="docs">Handler for method `43`. This method should be overridden by a subclass.</span>

<code>**async def rate_objects_with_posting**(client: [RMCClient](../rmc#rmcclient), targets: list[[DataStoreRatingTarget](#datastoreratingtarget)], rate_param: list[[DataStoreRateObjectParam](#datastorerateobjectparam)], post_param: list[[DataStorePreparePostParam](#datastorepreparepostparam)], transactional: bool, fetch_ratings: bool) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `44`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>ratings: list[[DataStoreRatingInfo](#datastoreratinginfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def get_object_infos**(client: [RMCClient](../rmc#rmcclient), data_ids: list[int]) -> [RMCResponse](../common)</code><br>
<span class="docs">Handler for method `45`. This method should be overridden by a subclass. The RMC response must have the following attributes:<br>
<span class="docs">
<code>infos: list[[DataStoreReqGetInfo](#datastorereqgetinfo)]</code><br>
<code>results: list[[Result](../common#result)]</code><br>
</span>
</span>

<code>**async def search_object_light**(client: [RMCClient](../rmc#rmcclient), param: [DataStoreSearchParam](#datastoresearchparam)) -> [DataStoreSearchResult](#datastoresearchresult)</code><br>
<span class="docs">Handler for method `46`. This method should be overridden by a subclass.</span>

## DataStoreChangeMetaCompareParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreChangeMetaCompareParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>comparison_flag: int</code><br>
<code>name: str</code><br>
<code>permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>delete_permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>period: int</code><br>
<code>meta_binary: bytes</code><br>
<code>tags: list[str]</code><br>
<code>referred_count: int</code><br>
<code>data_type: int</code><br>
<code>status: int</code><br>
</span><br>

## DataStoreChangeMetaParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreChangeMetaParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>modifies_flag: int</code><br>
<code>name: str</code><br>
<code>permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>delete_permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>period: int</code><br>
<code>meta_binary: bytes</code><br>
<code>tags: list[str]</code><br>
<code>update_password: int</code><br>
<code>referred_count: int</code><br>
<code>data_type: int</code><br>
<code>status: int</code><br>
<code>compare_param: [DataStoreChangeMetaCompareParam](#datastorechangemetacompareparam) = [DataStoreChangeMetaCompareParam](#datastorechangemetacompareparam)()</code><br>
<code>persistence_target: [DataStorePersistenceTarget](#datastorepersistencetarget) = [DataStorePersistenceTarget](#datastorepersistencetarget)()</code><br>
</span><br>

## DataStoreChangeMetaParamV1
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreChangeMetaParamV1` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>modifies_flag: int</code><br>
<code>name: str</code><br>
<code>permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>delete_permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>period: int</code><br>
<code>meta_binary: bytes</code><br>
<code>tags: list[str]</code><br>
<code>update_password: int</code><br>
</span><br>

## DataStoreCompletePostParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreCompletePostParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>success: bool</code><br>
</span><br>

## DataStoreCompletePostParamV1
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreCompletePostParamV1` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>success: bool</code><br>
</span><br>

## DataStoreCompleteUpdateParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreCompleteUpdateParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>version: int</code><br>
<code>success: bool</code><br>
</span><br>

## DataStoreDeleteParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreDeleteParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>update_password: int</code><br>
</span><br>

## DataStoreGetMetaParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreGetMetaParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int = 0</code><br>
<code>persistence_target: [DataStorePersistenceTarget](#datastorepersistencetarget) = [DataStorePersistenceTarget](#datastorepersistencetarget)()</code><br>
<code>result_option: int = 0</code><br>
<code>access_password: int = 0</code><br>
</span><br>

## DataStoreGetNewArrivedNotificationsParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreGetNewArrivedNotificationsParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>last_notification_id: int</code><br>
<code>limit: int</code><br>
</span><br>

## DataStoreGetNotificationUrlParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreGetNotificationUrlParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>previous_url: str</code><br>
</span><br>

## DataStoreGetSpecificMetaParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreGetSpecificMetaParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_ids: list[int]</code><br>
</span><br>

## DataStoreGetSpecificMetaParamV1
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreGetSpecificMetaParamV1` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_ids: list[int]</code><br>
</span><br>

## DataStoreKeyValue
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreKeyValue` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>key: str</code><br>
<code>value: str</code><br>
</span><br>

## DataStoreMetaInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreMetaInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>owner_id: int</code><br>
<code>size: int</code><br>
<code>name: str</code><br>
<code>data_type: int</code><br>
<code>meta_binary: bytes</code><br>
<code>permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>delete_permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>create_time: [DateTime](../common#datetime)</code><br>
<code>update_time: [DateTime](../common#datetime)</code><br>
<code>period: int</code><br>
<code>status: int</code><br>
<code>referred_count: int</code><br>
<code>refer_data_id: int</code><br>
<code>flag: int</code><br>
<code>referred_time: [DateTime](../common#datetime)</code><br>
<code>expire_time: [DateTime](../common#datetime)</code><br>
<code>tags: list[str]</code><br>
<code>ratings: list[[DataStoreRatingInfoWithSlot](#datastoreratinginfowithslot)]</code><br>
</span><br>

## DataStoreNotification
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreNotification` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>notification_id: int</code><br>
<code>data_id: int</code><br>
</span><br>

## DataStoreNotificationV1
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreNotificationV1` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>notification_id: int</code><br>
<code>data_id: int</code><br>
</span><br>

## DataStorePasswordInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStorePasswordInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>access_password: int</code><br>
<code>update_password: int</code><br>
</span><br>

## DataStorePermission
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStorePermission` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>permission: int = 3</code><br>
<code>recipients: list[int] = []</code><br>
</span><br>

## DataStorePersistenceInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStorePersistenceInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>owner_id: int</code><br>
<code>slot_id: int</code><br>
<code>data_id: int</code><br>
</span><br>

## DataStorePersistenceInitParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStorePersistenceInitParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>persistence_id: int = 65535</code><br>
<code>delete_last_object: bool = True</code><br>
</span><br>

## DataStorePersistenceTarget
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStorePersistenceTarget` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>owner_id: int = 0</code><br>
<code>persistence_id: int = 65535</code><br>
</span><br>

## DataStorePrepareGetParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStorePrepareGetParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int = 0</code><br>
<code>lock_id: int = 0</code><br>
<code>persistence_target: [DataStorePersistenceTarget](#datastorepersistencetarget) = [DataStorePersistenceTarget](#datastorepersistencetarget)()</code><br>
<code>access_password: int = 0</code><br>
If `nex.version` >= 30500:<br>
<span class="docs">
<code>extra_data: list[str] = []</code><br>
</span><br>
</span><br>

## DataStorePrepareGetParamV1
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStorePrepareGetParamV1` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>lock_id: int = 0</code><br>
</span><br>

## DataStorePreparePostParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStorePreparePostParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>size: int</code><br>
<code>name: str</code><br>
<code>data_type: int</code><br>
<code>meta_binary: bytes</code><br>
<code>permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>delete_permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>flag: int</code><br>
<code>period: int</code><br>
<code>refer_data_id: int = 0</code><br>
<code>tags: list[str] = []</code><br>
<code>rating_init_param: list[[DataStoreRatingInitParamWithSlot](#datastoreratinginitparamwithslot)] = []</code><br>
<code>persistence_init_param: [DataStorePersistenceInitParam](#datastorepersistenceinitparam) = [DataStorePersistenceInitParam](#datastorepersistenceinitparam)()</code><br>
If `nex.version` >= 30500:<br>
<span class="docs">
<code>extra_data: list[str]</code><br>
</span><br>
</span><br>

## DataStorePreparePostParamV1
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStorePreparePostParamV1` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>size: int</code><br>
<code>name: str</code><br>
<code>data_type: int = 0</code><br>
<code>meta_binary: bytes = b""</code><br>
<code>permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>delete_permission: [DataStorePermission](#datastorepermission) = [DataStorePermission](#datastorepermission)()</code><br>
<code>flag: int</code><br>
<code>period: int</code><br>
<code>refer_data_id: int = 0</code><br>
<code>tags: list[str]</code><br>
<code>rating_init_param: list[[DataStoreRatingInitParamWithSlot](#datastoreratinginitparamwithslot)]</code><br>
</span><br>

## DataStorePrepareUpdateParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStorePrepareUpdateParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>size: int</code><br>
<code>update_password: int</code><br>
<code>extra_data: list[str]</code><br>
</span><br>

## DataStoreRateObjectParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreRateObjectParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>rating_value: int</code><br>
<code>access_password: int</code><br>
</span><br>

## DataStoreRatingInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreRatingInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>total_value: int</code><br>
<code>count: int</code><br>
<code>initial_value: int</code><br>
</span><br>

## DataStoreRatingInfoWithSlot
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreRatingInfoWithSlot` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>slot: int</code><br>
<code>info: [DataStoreRatingInfo](#datastoreratinginfo) = [DataStoreRatingInfo](#datastoreratinginfo)()</code><br>
</span><br>

## DataStoreRatingInitParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreRatingInitParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>flag: int</code><br>
<code>internal_flag: int</code><br>
<code>lock_type: int</code><br>
<code>initial_value: int</code><br>
<code>range_min: int</code><br>
<code>range_max: int</code><br>
<code>period_hour: int</code><br>
<code>period_duration: int</code><br>
</span><br>

## DataStoreRatingInitParamWithSlot
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreRatingInitParamWithSlot` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>slot: int</code><br>
<code>param: [DataStoreRatingInitParam](#datastoreratinginitparam) = [DataStoreRatingInitParam](#datastoreratinginitparam)()</code><br>
</span><br>

## DataStoreRatingLog
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreRatingLog` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>is_rated: bool</code><br>
<code>pid: int</code><br>
<code>rating_value: int</code><br>
<code>lock_expiration_time: [DateTime](../common#datetime)</code><br>
</span><br>

## DataStoreRatingTarget
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreRatingTarget` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>slot: int</code><br>
</span><br>

## DataStoreReqGetAdditionalMeta
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreReqGetAdditionalMeta` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>owner_id: int</code><br>
<code>data_type: int</code><br>
<code>version: int</code><br>
<code>meta_binary: bytes</code><br>
</span><br>

## DataStoreReqGetInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreReqGetInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>url: str</code><br>
<code>headers: list[[DataStoreKeyValue](#datastorekeyvalue)]</code><br>
<code>size: int</code><br>
<code>root_ca_cert: bytes</code><br>
If `nex.version` >= 30500:<br>
<span class="docs">
<code>data_id: int</code><br>
</span><br>
</span><br>

## DataStoreReqGetInfoV1
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreReqGetInfoV1` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>url: str</code><br>
<code>headers: list[[DataStoreKeyValue](#datastorekeyvalue)]</code><br>
<code>size: int</code><br>
<code>root_ca_cert: bytes</code><br>
</span><br>

## DataStoreReqGetNotificationUrlInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreReqGetNotificationUrlInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>url: str</code><br>
<code>key: str</code><br>
<code>query: str</code><br>
<code>root_ca_cert: bytes</code><br>
</span><br>

## DataStoreReqPostInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreReqPostInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>url: str</code><br>
<code>headers: list[[DataStoreKeyValue](#datastorekeyvalue)]</code><br>
<code>form: list[[DataStoreKeyValue](#datastorekeyvalue)]</code><br>
<code>root_ca_cert: bytes</code><br>
</span><br>

## DataStoreReqPostInfoV1
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreReqPostInfoV1` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>url: str</code><br>
<code>headers: list[[DataStoreKeyValue](#datastorekeyvalue)]</code><br>
<code>form: list[[DataStoreKeyValue](#datastorekeyvalue)]</code><br>
<code>root_ca_cert: bytes</code><br>
</span><br>

## DataStoreReqUpdateInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreReqUpdateInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>version: int</code><br>
<code>url: str</code><br>
<code>headers: list[[DataStoreKeyValue](#datastorekeyvalue)]</code><br>
<code>form: list[[DataStoreKeyValue](#datastorekeyvalue)]</code><br>
<code>root_ca_cert: bytes</code><br>
</span><br>

## DataStoreSearchParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreSearchParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>search_target: int</code><br>
<code>owner_ids: list[int]</code><br>
<code>owner_type: int</code><br>
<code>destination_ids: list[int]</code><br>
<code>data_type: int</code><br>
<code>created_after: [DateTime](../common#datetime)</code><br>
<code>created_before: [DateTime](../common#datetime)</code><br>
<code>updated_after: [DateTime](../common#datetime)</code><br>
<code>updated_before: [DateTime](../common#datetime)</code><br>
<code>refer_data_id: int</code><br>
<code>tags: list[str]</code><br>
<code>result_order_column: int</code><br>
<code>result_order: int</code><br>
<code>result_range: [ResultRange](../common#resultrange) = [ResultRange](../common#resultrange)</code><br>
<code>result_option: int</code><br>
<code>minimal_rating_frequency: int</code><br>
<code>use_cache: bool</code><br>
<code>total_count_enabled: bool</code><br>
<code>data_types: list[int]</code><br>
</span><br>

## DataStoreSearchResult
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreSearchResult` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>total_count: int</code><br>
<code>result: list[[DataStoreMetaInfo](#datastoremetainfo)]</code><br>
<code>total_count_type: int</code><br>
</span><br>

## DataStoreSpecificMetaInfo
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreSpecificMetaInfo` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>owner_id: int</code><br>
<code>size: int</code><br>
<code>data_type: int</code><br>
<code>version: int</code><br>
</span><br>

## DataStoreSpecificMetaInfoV1
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreSpecificMetaInfoV1` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>owner_id: int</code><br>
<code>size: int</code><br>
<code>data_type: int</code><br>
<code>version: int</code><br>
</span><br>

## DataStoreTouchObjectParam
<code>**def _\_init__**()</code><br>
<span class="docs">Creates a new `DataStoreTouchObjectParam` instance. Required fields must be filled in manually.</span>

The following fields are defined in this class:<br>
<span class="docs">
<code>data_id: int</code><br>
<code>lock_id: int</code><br>
<code>access_password: int</code><br>
</span><br>

