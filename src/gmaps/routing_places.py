from google.maps import places_v1
from google.maps import routing_v2
from google.api_core.client_options import ClientOptions
from dotenv import dotenv_values

class GMapClient:
    def __init__(self):
        config = dotenv_values(".env")
        # get API Key from .env
        self.my_key = config['GMAPS_API_KEY'] or 'CHECK YOUR ENV'
        # default to 2618 Moore St, Bellingham WA for testing
        self.my_home_loc = {'latitude':48.7649179, 'longitude':-122.4602791}
        self.my_home_id = {'placeId':'ChIJX68rroajhVQREP_2FtfamJM'} 

    def find_closest_station(self, radius, lat_lng_origin = None):
        if lat_lng_origin is None:
            # default from init
            lat_lng_origin = self.my_home_loc
        # init client with origin
        options = ClientOptions(api_key=self.my_key)
        client = routing_v2.RoutesClient(client_options=options)
        location_origin = {'location': {'lat_lng': lat_lng_origin}}
        # consider also waypoint by ID
        #waypoint_origin = routing_v2.types.Waypoint(location_origin)
        #waypoint_origin.place_id = my_home_id

        # go get closest station
        search_response = self.search_nearby(radius, lat_lng_origin)
        print(f'Nearest stations in {str(radius)} km radius: ')
        print(search_response)
        if len(search_response.places) < 1:
            raise Exception(f'No nearest station found at distance {str(radius)} from {lat_lng_origin}')

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


    def search_nearby(self, rad, lat_lng = None):
        if lat_lng is None:
            # default from init
            lat_lng = self.my_home_loc
        # Create a client
        options = ClientOptions(api_key=self.my_key)
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

    def get_place_by_id(self, place_id: str):
        # Create a client
        options = ClientOptions(api_key=self.my_key)
        client = places_v1.PlacesClient(
            client_options=options,
        )

        # Initialize request argument(s)
        request = places_v1.GetPlaceRequest(
            name="places/" + place_id
        )
        # evChargeOptions not always returning data
        fieldMask = "formattedAddress,displayName,types,primaryType,location,evChargeOptions"

        # Make the request
        response = client.get_place(request=request, metadata=[("x-goog-fieldmask",fieldMask)])

        # Handle the response
        if 'electric_vehicle_charging_station' in response.types:
            print('EV Charging Station: ' + response.display_name.text + ': ' + response.formatted_address)
        return response
