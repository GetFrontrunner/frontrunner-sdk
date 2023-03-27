# Market

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**injective_id** | **str** | The marketId on Injective | 
**created** | **datetime** |  | [optional] 
**updated** | **datetime** |  | [optional] 
**long_entity_id** | **str** | The ID of the SportEntity on the long side of the market; if this side wins the market will go to 1 | [optional] 
**short_entity_id** | **str** | The ID of the SportEntity, if it exists, on the short side of the market; if this side wins the market will go to 0. If this is null, then the short side of the market is the \\&#x27;not\\&#x27; of the &#x60;longEntity&#x60; | [optional] 
**status** | [**MarketStatus**](MarketStatus.md) |  | 
**prop_id** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

