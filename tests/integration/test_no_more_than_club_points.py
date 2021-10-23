import pytest
from P11_Flask_Testing_Debugging import server
import time as t


@pytest.mark.no_more_than_club_points
class Test_points_updated:

    def test_no_more_than_club_points(self, client, load_competitions, mocker):
        """ this test check the happy path (the number of places is <= 12)
        and the sad path (the number of places is > 12) for the booking process """

        # préparation des données utilisées pour le test
        mocker.patch.object(server, 'clubs', [{"name": "Test_club",
                                               "email": "test_club@test.com", "points": "8"}])
        mocker.patch.object(server, 'competitions', [{"name": "Test_competition",
                                                      "date": "2022-10-22 13:30:00",
                                                      "numberOfPlaces": "200"}])

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
