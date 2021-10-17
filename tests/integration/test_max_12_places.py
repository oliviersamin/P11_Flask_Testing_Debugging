import pytest
from P11_Flask_Testing_Debugging import server
import time as t

valid_number_of_places = 10
wrong_number_of_places = 13

def __is_in_future(competition):
    date_format = "%Y-%m-%d %H:%M:%S"
    result = t.strptime(competition['date'], date_format)
    result = t.mktime(result)
    diff = result - t.time()
    return diff > 0


@pytest.mark.max_12_places
def test_max_12_places(client, load_clubs, load_competitions):
    """ this test check the happy path (the number of places is <= 12)
    and the sad path (the number of places is > 12) for the booking process """

    # préparation des données utilisées pour le test
    clubs = load_clubs
    competitions = load_competitions
    club = clubs[-1]
    # choose a competition that takes place in the future
    competition = {}
    for c in competitions:
        if __is_in_future(c):
            competition = c
            break

    # connexion to site through the login page
    resp = client.post('/showSummary', data={'email': club['email']})
    expected_value = 'Welcome, ' + club['email']
    if expected_value in resp.data.decode():  # if login OK
        # go to the booking page for the selected competition
        resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
        if 'How many places?' in resp.data.decode():  # if booking page reached
            # HAPPY PATH: book number of places < 12
            data = {'competition': competition['name'], 'club': club['name'], 'places': valid_number_of_places}
            resp = client.post('/purchasePlaces', data=data)
            welcome_message = "Welcome, " + club['email']
            assert welcome_message in resp.data.decode()
            assert "Great-booking complete!" in resp.data.decode()
            # SAD PATH: book places with a non positive integer as number of places
            data = {'competition': competition['name'], 'club': club['name'], 'places': wrong_number_of_places}
            resp = client.post('/purchasePlaces', data=data)
            error_message = 'ERROR: The maximum places to be reserved by club is 12'
            assert error_message in resp.data.decode()
    else:  # if login error by wrong credentials
        error_message = 'This is not a valid email, please try again'
        assert error_message in resp.data.decode()
