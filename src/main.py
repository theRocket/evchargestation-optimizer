from gmaps.routing_places import GMapClient
from gcloud.storage import GCSClient
import pandas as pd
from io import BytesIO
# Examples to run as scripts
# search_result = search_nearby(my_home_loc, 2.0)
if __name__ == "__main__":
    # get csv data from Cloud Storage
    my_storage = GCSClient()
    # start with small test data file
    my_data_inmem = my_storage.download_blob_into_memory('wipeout.csv')
    csvStringIO = BytesIO(my_data_inmem)
    df = pd.read_csv(csvStringIO, sep=",")
    get_a_loc=df[['position_lat_degrees','position_long_degrees']].iloc[0]

    # do map stuff
    my_gmap_client = GMapClient()
    # search_loc = my_gmap_client.home_loc # default
    # search_loc = {'latitude': 33.1422946, 'longitude': -107.2596707} # downtown Truth or Consequences, NM
    search_loc = {'latitude': get_a_loc.position_lat_degrees, 'longitude': get_a_loc.position_long_degrees} # from above
    radius = 1.0
    print(f'Searching nearest EV charging stations in {str(radius)} km radius from {search_loc}')
    place = my_gmap_client.find_closest_station(radius, search_loc) # could accept default lat/lng from init
    print(f'Distance to nearest station (ID: {place['id']}): {str(place['distance']/1000)} km')
    ev_place = my_gmap_client.get_place_by_id(place['id'])
    # Check the response types
    print(f'Place Types: {ev_place.types}')
    if 'electric_vehicle_charging_station' in ev_place.types:
        print('EV Charging Station: ' + ev_place.display_name.text + ': ' + ev_place.formatted_address)
        print(ev_place.ev_charge_options)

    # parse out the JSON and count results
    # (optional) pass each Place ID to get more info
    # such as:
    # ev_place = my_gmap_client.get_place_by_id("ChIJWyLAeY-jhVQRJXqchdJTMio") #2200 Nevada (charging station)
    ev_place_ids = [
        'ChIJYzdF8JGjhVQRXpG9yDgUQuE', # 1100 Iowa St, Bellingham, WA (charging station)
        'ChIJ5bLfbpGjhVQRk2bIlAeIT2E',
        'ChIJXQZrS6OjhVQRsKV3tR-vU4g',
        'ChIJY5EsEnykhVQRp0lOuTLSjzY',
        'ChIJd6Y-x3ykhVQRJ1NWVupAffQ',
        'ChIJYzdF8JGjhVQRXpG9yDgUQuE',
        'ChIJWyLAeY-jhVQRJXqchdJTMio',
        'ChIJiyXeUYCjhVQRV8hiXFGZn3I'
        ]
    #for place in ev_place_ids:
        #ev_place = my_gmap_client.get_place_by_id(place)
        #print(ev_place)