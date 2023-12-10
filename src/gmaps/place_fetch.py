from google.maps import places_v1
from google.maps import routing_v2
from google.api_core.client_options import ClientOptions
from dotenv import load_dotenv
import os


# get API Key from .env
def get_api_key():
    load_dotenv()
    return os.environ['GMAPS_API_KEY']

# default to 2618 Moore St, Bellingham WA for testing
my_home_loc = {'latitude':48.7649179, 'longitude':-122.4602791}
my_home_id = {'placeId':'ChIJX68rroajhVQREP_2FtfamJM'}

def find_closest_station(lat_lng_origin = my_home_loc, rad = 2.0, my_key: str = 'CHECK YOUR ENV'):
    # init client with origin
    options = ClientOptions(api_key=my_key)
    client = routing_v2.RoutesClient(client_options=options)
    location_origin = {'location': {'lat_lng': lat_lng_origin}}
    # consider also waypoint by ID
    #waypoint_origin = routing_v2.types.Waypoint(location_origin)
    #waypoint_origin.place_id = my_home_id

    # go get closest station
    search_response = search_nearby(my_home_loc, rad, my_key)
    print('Nearest stations: ')
    print(search_response)
    if len(search_response.places) < 1:
        raise Exception(f'No nearest station found at distance {str(rad)} from {my_home_loc}')

    for place in search_response.places:
        # try the first one for starters (presume sorted by proximity)
        location_destin = {
            'location': {
                'lat_lng': {
                    'latitude': place.location.latitude,
                    'longitude': place.location.longitude
                    }
                }
            }
        request = routing_v2.ComputeRoutesRequest(
            origin=location_origin, #waypoint_origin
            destination=location_destin
        )
        # choose which fields to return (no whitespace, comma separator)
        fieldMask = "routes.distanceMeters" # may need these later: routes.duration, routes.polyline.encodedPolyline
        response = client.compute_routes(request=request ,metadata=[("x-goog-fieldmask",fieldMask)])
        return response.routes[0].distance_meters


def search_nearby(lat_lng = my_home_loc, rad=15.0, my_key: str = 'CHECK YOUR ENV'):
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
    # print(response.places)
    return response

def get_place_by_id(place_id: str, api_key: str = 'CHECK YOUR ENV'):
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

    # Handle the response
    if 'electric_vehicle_charging_station' in response.types:
        print('EV Charging Station: ' + response.display_name.text + ': ' + response.formatted_address)
    return response

# Examples
# search_result = search_nearby(my_home_loc, 2.0)
if __name__ == "__main__":
    my_key = get_api_key()
    distance = find_closest_station(my_home_loc, 1.0, my_key) # accept global defaults
    print(f'Distance to nearest station: {str(distance/1000)} km')

# parse out the JSON and count results
# (optional) pass each Place ID to get more info

# get_place_by_id("ChIJX68rroajhVQREP_2FtfamJM") #2618 Moore
# get_place_by_id("ChIJWyLAeY-jhVQRJXqchdJTMio") #2200 Nevada (charging station)
# get_place_by_id("ChIJ5bLfbpGjhVQRk2bIlAeIT2E")
# get_place_by_id("ChIJXQZrS6OjhVQRsKV3tR-vU4g")
# get_place_by_id("ChIJY5EsEnykhVQRp0lOuTLSjzY")
# get_place_by_id("ChIJd6Y-x3ykhVQRJ1NWVupAffQ")
# get_place_by_id("ChIJYzdF8JGjhVQRXpG9yDgUQuE")
# get_place_by_id("ChIJWyLAeY-jhVQRJXqchdJTMio")
# get_place_by_id("ChIJiyXeUYCjhVQRV8hiXFGZn3I")