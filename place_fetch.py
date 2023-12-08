from google.maps import places_v1
from google.api_core.client_options import ClientOptions
from dotenv import load_dotenv
import os

# get API Key from .env
load_dotenv()
GMAPS_API_KEY = os.environ['GMAPS_API_KEY']
my_home_loc = {'latitude':48.7649179, 'longitude':-122.4602791}

def get_place_by_id(place_id: str, api_key: str = GMAPS_API_KEY):
    # Create a client
    options = ClientOptions(api_key=api_key)
    client = places_v1.PlacesClient(
        client_options=options,
    )

    # Initialize request argument(s)
    request = places_v1.GetPlaceRequest(
        name="places/" + place_id
    )
    fieldMask = "formattedAddress,displayName,types,primaryType,location"

    # Make the request
    response = client.get_place(request=request, metadata=[("x-goog-fieldmask",fieldMask)])
    print(response)
    # Handle the response
    if 'electric_vehicle_charging_station' in response.types:
        print('EV Charging Station: ' + response.display_name.text + ': ' + response.formatted_address)

def search_nearby(lat_lng = my_home_loc, rad=15.0, my_key: str = GMAPS_API_KEY):
    # Create a client
    options = ClientOptions(api_key=my_key)
    client = places_v1.PlacesClient(client_options=options)

    # Initialize request argument(s)
    search_km = 1000*rad # convert from km to meters, max 50000
    loc_restriction = places_v1.SearchNearbyRequest.LocationRestriction()
    loc_restriction.circle = places_v1.Circle(center=lat_lng, radius=search_km)
    request = places_v1.SearchNearbyRequest(
        location_restriction=loc_restriction,
        included_types=['electric_vehicle_charging_station']
    )
    # no whitespace here!
    fieldMask = "places.id,places.displayName,places.formattedAddress,places.location,places.evChargeOptions"
    # Make the request
    response = client.search_nearby(request=request, metadata=[("x-goog-fieldmask",fieldMask)])

    # Handle the response
    print(response.places)

search_result = search_nearby(my_home_loc, 2.0)
# parse out the JSON and count results
# (optional) pass each Place ID to get more info

get_place_by_id("ChIJX68rroajhVQREP_2FtfamJM") #2618 Moore
get_place_by_id("ChIJWyLAeY-jhVQRJXqchdJTMio") #2200 Nevada (charging station)
# get_place_by_id("ChIJ5bLfbpGjhVQRk2bIlAeIT2E")
# get_place_by_id("ChIJXQZrS6OjhVQRsKV3tR-vU4g")
# get_place_by_id("ChIJY5EsEnykhVQRp0lOuTLSjzY")
# get_place_by_id("ChIJd6Y-x3ykhVQRJ1NWVupAffQ")
# get_place_by_id("ChIJYzdF8JGjhVQRXpG9yDgUQuE")
# get_place_by_id("ChIJWyLAeY-jhVQRJXqchdJTMio")
# get_place_by_id("ChIJiyXeUYCjhVQRV8hiXFGZn3I")