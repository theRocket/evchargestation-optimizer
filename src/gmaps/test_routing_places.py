from routing_places import GMapClient

def test_search_nearby():
    # need a mock here
    my_home_loc = GMapClient()
    result = my_home_loc.search_nearby(2.0)
    assert(len(result.places) > 0)
    place_closest = result.places[0]
    assert(place_closest.location.latitude > 48.0)
    assert(place_closest.location.longitude < -66.0)