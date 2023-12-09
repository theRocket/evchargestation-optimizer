from place_fetch import search_nearby

def test_search_nearby():
    # need a mock here
    my_home_loc = {'latitude':48.7649179, 'longitude':-122.4602791}
    result = search_nearby(my_home_loc, 2.0)
    assert(len(result.places) > 0)