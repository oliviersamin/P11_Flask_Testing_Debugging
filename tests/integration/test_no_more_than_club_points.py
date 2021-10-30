import pytest
from P11_Flask_Testing_Debugging import server
import time as t


@pytest.mark.all_tests
@pytest.mark.no_more_than_club_points
class TestNoMoreThanClubPoints:
    """ This test checks that no club can use more than its club balance points. Here are the steps used:
    Step 1: Connexion to login page
    Step 2: When login successfull go to the booking page of a future competition
    Step 3: Book 1 place = Happy path
    Step 4: Go back to the welcome page and check the booking has been made
    Step 5: Use more points than its club balance to book places = Sad path
    Step 6: Check that an error message is displayed on the page"""


    def test_no_more_than_club_points(self, client, load_competitions, mocker):
        """ This test gathers all the steps described in the docstring of this class """

        ####### SETUP OF THE TEST ##########
        mocker.patch.object(server, 'clubs', [{"name": "Test_club",
                                               "email": "test_club@test.com", "points": "8"}])
        mocker.patch.object(server, 'competitions', [{"name": "Test_competition",
                                                      "date": "2022-10-22 13:30:00",
                                                      "numberOfPlaces": "200"}])
        club = server.clubs[0]
        # choose a competition that takes place in the future
        competition = server.competitions[0]
        ####### END OF THE SETUP ########
        # Step 1
        resp = client.post('/showSummary', data={'email': club['email']})
        expected_value = 'Welcome, ' + club['email']
        if expected_value in resp.data.decode():  # if login OK
            # Step 2
            resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
            if 'How many places?' in resp.data.decode():  # if booking page reached
                # Step 3
                # HAPPY PATH: book number of places < number of club's points
                data = {'competition': competition['name'], 'club': club['name'], 'places': '1'}
                resp = client.post('/purchasePlaces', data=data)
                # Step 4
                welcome_message = "Welcome, " + club['email']
                assert welcome_message in resp.data.decode()
                assert "Great-booking complete!" in resp.data.decode()
                # Step 5
                # SAD PATH: book number of places > number of club's points
                data = {'competition': competition['name'], 'club': club['name'], 'places': '10'}
                resp = client.post('/purchasePlaces', data=data)
                # Step 6
                error_message = "ERROR: You cannot book more places than your total club points"
                assert error_message in resp.data.decode()
        else:  # if login error by wrong credentials
            error_message = 'This is not a valid email, please try again'
            assert error_message in resp.data.decode()
