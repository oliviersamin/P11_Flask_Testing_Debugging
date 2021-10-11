import pytest
from P11_Flask_Testing_Debugging import server


@pytest.mark.points_updated
@pytest.mark.parametrize("data,expected_flash_message",
                         [({"name": "Simply Lift", "email": "john@simplylift.co", "points": "-13"},
                           "ERROR: The number of points for the club is not a positive integer"),
                          ({"name": "Simply Lift", "email": "john@simplylift.co", "points": "AA/13"},
                           "ERROR: The number of points for the club is not a positive integer"),
                          ({"name": "Simply Lift", "email": "john@simplylift.co", "points": ""},
                           "ERROR: The number of points for the club is not a positive integer")
                          ])
def test_club_points_is_not_positive_integer(client, data, expected_flash_message):
    """ check that the points in the club input are positive integer """
    resp = client.post('/showSummary', data=data)
    assert expected_flash_message in resp.data.decode()
    client.close()

@pytest.mark.points_updated
@pytest.mark.parametrize("data,expected_flash_message",
                         [({"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "-25"},
                           "ERROR: The number of places for one competition is not a positive integer"),
                          ({"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "2.3"},
                          "ERROR: The number of places for one competition is not a positive integer"),
                          ({"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "A4"},
                           "ERROR: The number of places for one competition is not a positive integer"),
                          ])
def test_competition_number_of_places_is_not_positive_integer(client, data, expected_flash_message):
    """ check that the number of places in the competition input is positive integer """
    clubs = server.clubs
    data = {'email': clubs[0]['email']}
    resp = client.post('/showSummary', data=data)
    assert expected_flash_message in resp.data.decode()
    client.close()


@pytest.mark.points_updated
@pytest.mark.parametrize("data,expected_flash_message",
                         [({'places': '-3'},
                           "ERROR: The number of places booked is not a positive integer"),
                          ({'places': "3.7"},
                          "ERROR: The number of places booked is not a positive integer"),
                          ({'places': "AE/"},
                           "ERROR: The number of places booked is not a positive integer"),
                          ])
def test_booking_places_is_not_positive_integer(client, data, expected_flash_message):
    """ check that the number of places asked is a positive integer"""
    clubs = server.clubs
    competitions = server.competitions
    data = {'competition': competitions[-1]['name'], 'club': clubs[0]['name'], 'places': data['places']}
    resp = client.post('/purchasePlaces', data=data)
    # assert resp.status_code == 200
    assert expected_flash_message in resp.data.decode()
    client.close()


@pytest.mark.points_updated
def test_club_points_updated(client):
    """ check that with positive integers numbers, the balance od point of the club is updated
    after a reservation"""
    clubs = server.clubs
    competitions = server.competitions
    club = {}
    compet = {}
    for c in clubs:
        if int(c['points']) & int(c['points']) > 0:
            club = c
            break

    for c in competitions:
        if int(c['numberOfPlaces']) & int(c['numberOfPlaces']) >0:
            compet = c
            break

    data = {'competition': compet['name'],
            'club': club['name'],
            'places': '1'}
    club['points'] = str(int(club['points']) - int(data['places']))
    resp = client.post('/purchasePlaces', data=data)
    welcome_message = "Welcome, " + club['email']
    points_updated = "Points available: " + club['points']
    assert resp.status_code == 200
    assert welcome_message in resp.data.decode()
    assert "Great-booking complete!" in resp.data.decode()
    assert points_updated in resp.data.decode()
