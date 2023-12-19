from google.maps import places_v1
from google.maps import routing_v2
from google.api_core.client_options import ClientOptions
from dotenv import dotenv_values
from typing import List, Dict
from collections import defaultdict

class GMapClient:
    def __init__(self):
        config = dotenv_values(".env")
        # get API Key from .env
        self.my_key = config['GMAPS_API_KEY'] or 'CHECK YOUR ENV'
        # set a default home loc for testing
        self.home_loc = {'latitude': float(config['MY_LAT']), 'longitude': float(config['MY_LONG'])}
        self.home_id = {'placeId':config['MY_PLACE_ID']}

        self.fieldSet = {"id", "displayName", "formattedAddress", "location"}
        # initialize to place types dictionary (provide empty list if invalid key provided)
        self.ev_site_types: Dict(str, List[str]) = defaultdict(list)
        # build with all but existing EV Charging stations
        for key in ['automotive', 'entertainment', 'lodging', 'shopping', 'sports', 'transportation', 'other']:
            self.ev_site_types[key] = self.place_types(key)

    # defining a subset of types from https://developers.google.com/maps/documentation/places/web-service/place-types
    # where we expect it is reasonable to locate a new EV charger (includes existing infra if needed)
    def place_types(self, category):
        match category:
            case 'EVSE': # existing infrastructure
                return ['electric_vehicle_charging_station']
            case 'automotive':
                return ['car_dealer', 'gas_station', 'parking', 'rest_stop']
            case 'entertainment': # and Recreation
                return ['casino', 'community_center', 'convention_center', 'cultural_center', 'event_venue', 'marina', 'movie_theater', 'visitor_center']
            case 'lodging':
                return ['campground', 'extended_stay_hotel', 'hotel', 'lodging', 'motel', 'resort_hotel', 'rv_park']
            case 'shopping':
                return ['auto_parts_store', 'book_store', 'department_store', 'electronics_store', 'furniture_store', 'grocery_store', 'hardware_store', 'home_improvement_store', 'shopping_mall', 'sporting_goods_store', 'supermarket']
            case 'sports':
                return ['athletic_field', 'fitness_center', 'golf_course', 'gym', 'sports_club', 'sports_complex', 'stadium']
            case 'transportation':
                return ['airport', 'ferry_terminal', 'light_rail_station', 'park_and_ride', 'truck_stop']
            case 'other': # Government | Education | Health & Wellness | Places of Worship
                return ['city_hall', 'courthouse', 'library', 'hospital', 'church']

    def find_closest_station(self, radius, lat_lng_origin = None):
        if lat_lng_origin is None:
            # default from init
            lat_lng_origin = self.home_loc
        # init client with origin
        options = ClientOptions(api_key=self.my_key)
        client = routing_v2.RoutesClient(client_options=options)
        location_origin = {'location': {'lat_lng': lat_lng_origin}}
        # consider also waypoint by ID
        #waypoint_origin = routing_v2.types.Waypoint(location_origin)
        #waypoint_origin.place_id = home_id

        # go get closest EV Charging station
        search_response = self.search_nearby(radius, lat_lng_origin, 'EVSE')
        if len(search_response.places) < 1:
            raise Exception(f'No nearest station found at distance {str(radius)} from {lat_lng_origin}')

        else:
            # try the first one for starters (presume sorted by proximity)
            place = search_response.places[0]
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


    def search_nearby(self, rad, lat_lng = None, place_type = None):
        if lat_lng is None:
            # default from init
            lat_lng = self.home_loc
        # Create a client
        options = ClientOptions(api_key=self.my_key)
        client = places_v1.PlacesClient(client_options=options)

        # set up search location by lat/long and radius in meters (assumes km provided)
        search_km = 1000*rad # max 50000
        loc_restriction = places_v1.SearchNearbyRequest.LocationRestriction()
        loc_restriction.circle = places_v1.Circle(center=lat_lng, radius=search_km)

        loc_types = []
        if place_type == 'EVSE':
            # go direct to array of EV place types
            loc_types = self.place_types(place_type)
            # need the charge options (could be empty)
            self.fieldSet.add("evChargeOptions")
        elif place_type is None:
            # build an array from the built-in site types we are seeking
            for x in self.ev_site_types.values():
                loc_types.extend(x)
            # need to know what types we found
            self.fieldSet.add("types")
        #else:
            # build for all?
        request = places_v1.SearchNearbyRequest(
            location_restriction=loc_restriction,
            included_types=loc_types
        )
        # namespace scoping needed here
        fieldMask = "places." + ",places.".join(self.fieldSet) # no whitespace allowed
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
        fieldMask = ",".join(self.fieldSet) # no whitespace allowed

        # Make the request
        response = client.get_place(request=request, metadata=[("x-goog-fieldmask",fieldMask)])

        # Handle the response
        if 'electric_vehicle_charging_station' in response.types:
            print('EV Charging Station: ' + response.display_name.text + ': ' + response.formatted_address)
        return response
