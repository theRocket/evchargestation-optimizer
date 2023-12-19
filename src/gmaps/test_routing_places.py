from routing_places import GMapClient

def test_search_nearby():
    # need a mock here to prevent API call (Google Cloud bill plus time in CI/CD)
    test_client = GMapClient()
    test_loc = {'latitude':48.7649179, 'longitude':-122.4602791}
    # verify initialized to correct site locator
    assert('rv_park' in test_client.ev_site_types['lodging'])
    # verify evChargeOptions field mask returned for EVSE
    result = test_client.search_nearby(2.0, test_loc, 'EVSE')
    assert(len(result.places) > 0)
    place_closest = result.places[0]
    assert(place_closest.location.latitude > 48.0)
    assert(place_closest.location.longitude < -66.0)
    if place_closest.ev_charge_options: # could be empty for some locations
        assert(place_closest.ev_charge_options.connector_count>0) 