# swagger_client.FrontrunnerApi

All URIs are relative to *https://partner-api.getfrontrunner.com/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_leagues**](FrontrunnerApi.md#get_leagues) | **GET** /leagues | Get Frontrunner Sports Leagues
[**get_markets**](FrontrunnerApi.md#get_markets) | **GET** /markets | Get Frontrunner Markets
[**get_props**](FrontrunnerApi.md#get_props) | **GET** /props | Get Frontrunner Props
[**get_sport_entities**](FrontrunnerApi.md#get_sport_entities) | **GET** /sportEntities | Get list of Frontrunner SportEntity
[**get_sport_events**](FrontrunnerApi.md#get_sport_events) | **GET** /sportEvents | Get list of Frontrunner SportEvent

# **get_leagues**
> list[League] get_leagues(id=id, sport=sport)

Get Frontrunner Sports Leagues

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKeyAuth
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FrontrunnerApi(swagger_client.ApiClient(configuration))
id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Frontrunner League id (optional)
sport = 'sport_example' # str |  (optional)

try:
    # Get Frontrunner Sports Leagues
    api_response = api_instance.get_leagues(id=id, sport=sport)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FrontrunnerApi->get_leagues: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**str**](.md)| Frontrunner League id | [optional] 
 **sport** | **str**|  | [optional] 

### Return type

[**list[League]**](League.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_markets**
> list[Market] get_markets(id=id, injective_id=injective_id, prop_id=prop_id, event_id=event_id, league_id=league_id, status=status)

Get Frontrunner Markets

`status` default is `active` if not provided. If `status` is provided as not `active`, one of `id`, `injectiveId`, `propId`, or `eventId` must be provided as well

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKeyAuth
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FrontrunnerApi(swagger_client.ApiClient(configuration))
id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Frontrunner Market id (optional)
injective_id = 'injective_id_example' # str | Injective market id (optional)
prop_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Frontrunner Prop id (optional)
event_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Frontrunner SportEvent id (optional)
league_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Frontrunner League id (optional)
status = swagger_client.MarketStatus() # MarketStatus | Frontrunner Market status (optional)

try:
    # Get Frontrunner Markets
    api_response = api_instance.get_markets(id=id, injective_id=injective_id, prop_id=prop_id, event_id=event_id, league_id=league_id, status=status)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FrontrunnerApi->get_markets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**str**](.md)| Frontrunner Market id | [optional] 
 **injective_id** | **str**| Injective market id | [optional] 
 **prop_id** | [**str**](.md)| Frontrunner Prop id | [optional] 
 **event_id** | [**str**](.md)| Frontrunner SportEvent id | [optional] 
 **league_id** | [**str**](.md)| Frontrunner League id | [optional] 
 **status** | [**MarketStatus**](.md)| Frontrunner Market status | [optional] 

### Return type

[**list[Market]**](Market.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_props**
> list[Prop] get_props(id=id, league_id=league_id)

Get Frontrunner Props

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKeyAuth
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FrontrunnerApi(swagger_client.ApiClient(configuration))
id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Frontrunner Prop id (optional)
league_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Frontrunner League id (optional)

try:
    # Get Frontrunner Props
    api_response = api_instance.get_props(id=id, league_id=league_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FrontrunnerApi->get_props: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**str**](.md)| Frontrunner Prop id | [optional] 
 **league_id** | [**str**](.md)| Frontrunner League id | [optional] 

### Return type

[**list[Prop]**](Prop.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sport_entities**
> list[SportEntity] get_sport_entities(id=id, sport=sport, league_id=league_id)

Get list of Frontrunner SportEntity

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKeyAuth
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FrontrunnerApi(swagger_client.ApiClient(configuration))
id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Frontrunner SportEntity id (optional)
sport = 'sport_example' # str |  (optional)
league_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str |  (optional)

try:
    # Get list of Frontrunner SportEntity
    api_response = api_instance.get_sport_entities(id=id, sport=sport, league_id=league_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FrontrunnerApi->get_sport_entities: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**str**](.md)| Frontrunner SportEntity id | [optional] 
 **sport** | **str**|  | [optional] 
 **league_id** | [**str**](.md)|  | [optional] 

### Return type

[**list[SportEntity]**](SportEntity.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sport_events**
> list[SportEvent] get_sport_events(id=id, sport=sport, league_id=league_id, starts_since=starts_since)

Get list of Frontrunner SportEvent

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKeyAuth
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.FrontrunnerApi(swagger_client.ApiClient(configuration))
id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str | Frontrunner SportEvent id (optional)
sport = 'sport_example' # str |  (optional)
league_id = '38400000-8cf0-11bd-b23e-10b96e4ef00d' # str |  (optional)
starts_since = '2013-10-20T19:20:30+01:00' # datetime | The minimum start time to return (optional)

try:
    # Get list of Frontrunner SportEvent
    api_response = api_instance.get_sport_events(id=id, sport=sport, league_id=league_id, starts_since=starts_since)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FrontrunnerApi->get_sport_events: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**str**](.md)| Frontrunner SportEvent id | [optional] 
 **sport** | **str**|  | [optional] 
 **league_id** | [**str**](.md)|  | [optional] 
 **starts_since** | **datetime**| The minimum start time to return | [optional] 

### Return type

[**list[SportEvent]**](SportEvent.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

