from gmaps.routing_places import GMaps
# Examples to run as scripts
# search_result = search_nearby(my_home_loc, 2.0)
if __name__ == "__main__":
    my_gmap_client = GMaps()
    distance = my_gmap_client.find_closest_station(1.0) # accept defaults from init
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