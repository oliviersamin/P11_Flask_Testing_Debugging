import pytest
from P11_Flask_Testing_Debugging import server
import time as t


def __is_in_future(competition):
    date_format = "%Y-%m-%d %H:%M:%S"
    result = t.strptime(competition['date'], date_format)
    result = t.mktime(result)
    diff = result - t.time()
    return diff > 0


@pytest.mark.past_competition
def test_past_competition(client, load_clubs, load_competitions):
    """ this test check the happy path (the competition takes place in the future)
    and the sad path (the competition is over) for the booking process """

    # préparation des données utilisées pour le test
    clubs = load_clubs
    competitions = load_competitions
    valid_competition = {}
    wrong_competition = {}
    for compet in competitions:
        if __is_in_future(compet) & (valid_competition == {}):
            valid_competition = compet
        elif (not __is_in_future(compet)) & (wrong_competition == {}):
            wrong_competition = compet
    club = clubs[-1]
    # connexion to site through the login page
    resp = client.post('/showSummary', data={'email': club['email']})
    expected_value = 'Welcome, ' + club['email']
    if expected_value in resp.data.decode():  # if login OK
        # test the happy_path
        resp = client.get('/book/{}/{}'.format(valid_competition['name'], club['name']))
        if 'How many places?' in resp.data.decode():  # if booking page reached
            data = {'competition': valid_competition['name'], 'club': club['name'], 'places': '1'}
            resp = client.post('/purchasePlaces', data=data)
            assert "Great-booking complete!" in resp.data.decode()
        # test the sad path
        resp = client.get('/book/{}/{}'.format(wrong_competition['name'], club['name']))
        assert "ERROR: This competition is over" in resp.data.decode()

    else:  # if login error by wrong credentials
        error_message = 'This is not a valid email, please try again'
        assert error_message in resp.data.decode()

