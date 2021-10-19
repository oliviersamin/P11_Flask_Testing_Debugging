import pytest
from P11_Flask_Testing_Debugging import server
import time as t


def __is_in_future(competition):
    date_format = "%Y-%m-%d %H:%M:%S"
    result = t.strptime(competition['date'], date_format)
    result = t.mktime(result)
    diff = result - t.time()
    return diff > 0


@pytest.mark.no_more_than_club_points
def test_no_more_than_club_points(client, load_competitions, mocker):
    """ this test check the happy path (the number of places is <= 12)
    and the sad path (the number of places is > 12) for the booking process """

    # préparation des données utilisées pour le test
    mocker.patch.object(server, 'clubs', [{"name": "Simply Lift",
                                           "email": "john@simplylift.co", "points": "3"}])

    mocker.patch.object(server, 'competitions', [{"name": "Fall Classic",
                                                  "date": "2022-10-22 13:30:00",
                                                  "numberOfPlaces": "13"}])

    club = server.clubs[0]
    # choose a competition that takes place in the future
    competition = server.competitions[0]

    # connexion to site through the login page
    resp = client.post('/showSummary', data={'email': club['email']})
    expected_value = 'Welcome, ' + club['email']
    if expected_value in resp.data.decode():  # if login OK
        print('login OK...', flush=True)
        # go to the booking page for the selected competition
        resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
        if 'How many places?' in resp.data.decode():  # if booking page reached
            print('booking page reached...', flush=True)
            # HAPPY PATH: book number of places < number of club's points
            data = {'competition': competition['name'], 'club': club['name'], 'places': '1'}
            resp = client.post('/purchasePlaces', data=data)
            welcome_message = "Welcome, " + club['email']
            assert welcome_message in resp.data.decode()
            assert "Great-booking complete!" in resp.data.decode()
            # SAD PATH: book number of places > number of club's points
            data = {'competition': competition['name'], 'club': club['name'], 'places': '10'}
            resp = client.post('/purchasePlaces', data=data)
            error_message = "ERROR: You cannot book more places than your total club points"
            assert error_message in resp.data.decode()
    else:  # if login error by wrong credentials
        error_message = 'This is not a valid email, please try again'
        assert error_message in resp.data.decode()
