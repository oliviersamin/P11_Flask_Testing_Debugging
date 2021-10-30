import pytest
from P11_Flask_Testing_Debugging import server
import time as t
import json


@pytest.mark.all_tests
@pytest.mark.past_competition
class TestPastCompetition:
    """ This test checks that if a club try to book a place in a past competition,
     an error message is displayed and if it clicks on a future competition link
      the booking page appear. To do so here are the steps:
    Step 1: Connexion to login page
    For the happy path:
    Step 2: When login successfull go to the booking page of a future competition
    Step 3: Book 1 place
    Step 4: Go back to the welcome page and check the booking message appear
    For the sad path:
    Step 5: When login successfull, click on the booking link of a past competition
    and check an error message appears.
    """

    future_competition = {"name": "Test_competition_in_future",
                          "date": "2022-03-27 10:00:00",
                          "numberOfPlaces": "200"}

    def load_clubs(self):
        """ load the data from 'clubs.json' and override the clubs varable from server.py """
        with open('clubs.json') as c:
            clubs = json.load(c)['clubs']
            return clubs

    def load_competitions(self):
        """ load the data from 'clubs.json' and override the competitions varable from server.py """
        with open('competitions.json') as comps:
            competitions = json.load(comps)['competitions']
            return competitions

    def setup_method(self, method):
        server.clubs = self.load_clubs()
        server.competitions = self.load_competitions()
        server.competitions.append(self.future_competition)

    def teardown_method(self, method):
        server.clubs = self.load_clubs()
        server.competitions = self.load_competitions()

    def __is_in_future(self, competition):
        date_format = "%Y-%m-%d %H:%M:%S"
        result = t.strptime(competition['date'], date_format)
        result = t.mktime(result)
        diff = result - t.time()
        return diff > 0

    def test_past_competition(self, client):
        """ this test gather all the steps described in the docstring of this class """

        club = server.clubs[-1]
        # Step 1
        resp = client.post('/showSummary', data={'email': club['email']})
        expected_value = 'Welcome, ' + club['email']
        if expected_value in resp.data.decode():  # if login OK
            for competition in server.competitions:
                if self.__is_in_future(competition):
                    # Step 2
                    resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
                    if 'How many places?' in resp.data.decode():  # if booking page reached
                        # Step 3
                        data = {'competition': competition['name'], 'club': club['name'], 'places': '1'}
                        resp = client.post('/purchasePlaces', data=data)
                        # Step 4
                        assert "Great-booking complete!" in resp.data.decode()
            # Step 5
            for competition in server.competitions:
                if not self.__is_in_future(competition):
                    resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
                    assert "ERROR: This competition is over" in resp.data.decode()

        else:  # if login error by wrong credentials
            error_message = 'This is not a valid email, please try again'
            assert error_message in resp.data.decode()

