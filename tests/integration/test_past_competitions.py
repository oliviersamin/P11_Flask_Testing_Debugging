import pytest
from P11_Flask_Testing_Debugging import server
import time as t
import json


@pytest.mark.all_tests
@pytest.mark.past_competition
class TestPastCompetition:
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
        """ this test check the happy path (the competition takes place in the future)
        and the sad path (the competition is over) for the booking process """

        club = server.clubs[-1]
        # connexion to site through the login page
        resp = client.post('/showSummary', data={'email': club['email']})
        expected_value = 'Welcome, ' + club['email']
        if expected_value in resp.data.decode():  # if login OK
            # test the happy_paths
            for competition in server.competitions:
                if self.__is_in_future(competition):
                    resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
                    if 'How many places?' in resp.data.decode():  # if booking page reached
                        data = {'competition': competition['name'], 'club': club['name'], 'places': '1'}
                        resp = client.post('/purchasePlaces', data=data)
                        assert "Great-booking complete!" in resp.data.decode()
            # test the sad paths
            for competition in server.competitions:
                if not self.__is_in_future(competition):
                    resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
                    assert "ERROR: This competition is over" in resp.data.decode()

        else:  # if login error by wrong credentials
            error_message = 'This is not a valid email, please try again'
            assert error_message in resp.data.decode()

