import pytest
from P11_Flask_Testing_Debugging import server


valid_number_of_places = 1
wrong_number_of_places = -1

@pytest.mark.points_updated
def test_points_updated(client, load_clubs, load_competitions):
    """ this test check the happy path (the number of places is a positive integer)
    and the sad path (the number of places is not a positive integer) for the booking process """

    # préparation des données utilisées pour le test
    clubs = load_clubs
    competitions = load_competitions
    competition = competitions[-1]
    club = clubs[-1]
    # connexion to site through the login page
    resp = client.post('/showSummary', data={'email': club['email']})
    expected_value = 'Welcome, ' + club['email']
    if expected_value in resp.data.decode():  # if login OK
        # go to the booking page for one competition
        resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
        if 'How many places?' in resp.data.decode():  # if booking page reached
            print('page de réservation atteinte...')
            # HAPPY PATH: book places with a valid positive integer as number of places
            print('booking with correct data....', flush=True)
            data = {'competition': competition['name'], 'club': club['name'], 'places': valid_number_of_places}
            club['points'] = str(int(club['points']) - int(data['places']))
            resp = client.post('/purchasePlaces', data=data)
            welcome_message = "Welcome, " + club['email']
            points_updated = "Points available: " + club['points']
            assert welcome_message in resp.data.decode()
            assert "Great-booking complete!" in resp.data.decode()
            assert points_updated in resp.data.decode()
            print('booking with correct data.... OK!', flush=True)
            # SAD PATH: book places with a non positive integer as number of places
            print('booking with wrong data....', flush=True)
            data = {'competition': competition['name'], 'club': club['name'], 'places': wrong_number_of_places}
            resp = client.post('/purchasePlaces', data=data)
            error_message = 'ERROR: The number of places booked is not a positive integer'
            assert error_message in resp.data.decode()
            assert points_updated in resp.data.decode()
            print('booking with wrong data....OK!', flush=True)
    else:  # if login error by wrong credentials
        error_message = 'This is not a valid email, please try again'
        assert error_message in resp.data.decode()