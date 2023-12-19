from gmaps.routing_places import GMapClient
from gcloud.storage import GCSClient
import pandas as pd
from io import BytesIO
# Examples to run as scripts
# search_result = search_nearby(my_home_loc, 2.0)
if __name__ == "__main__":
    # get csv data from Cloud Storage
    my_storage = GCSClient()
    # maybe too large?
    my_data_inmem = my_storage.download_blob_into_memory('strava.csv')
    csvStringIO = BytesIO(my_data_inmem)
    df = pd.read_csv(csvStringIO, sep=",")
    print(df.head())

    # do map stuff
    my_gmap_client = GMapClient()
    search_loc = my_gmap_client.home_loc
    # override with, ex: {'latitude':47.4281926, 'longitude':-120.3719613}
    radius = 1.0
    print(f'Searching nearest EV charging stations in {str(radius)} km radius from {search_loc}')
    distance = my_gmap_client.find_closest_station(radius, search_loc) # could accept default lat/lng from init
    print(f'Distance to nearest station: {str(distance/1000)} km')

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