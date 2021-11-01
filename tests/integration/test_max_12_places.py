import pytest
from P11_Flask_Testing_Debugging import server
import time as t
import json


@pytest.mark.all_tests
@pytest.mark.max_12_places
class TestMax12Places:
    """ This test checks that no club can book more than 12 places for one competition.
    Here are the steps used:
    Step 1: Connexion to login page
    Step 2: When login successfull go to the booking page of a future competition
    Step 3: Book 10 place = Happy path
    Step 4: Go back to the welcome page and check the booking has been made
    Step 5: Use more points than 12 places = Sad path
    Step 6: Check that an error message is displayed on the page"""

    # SETUP THE TEST #####
    valid_number_of_places = 10
    wrong_number_of_places = 13

    club = [{"name": "Simply Lift", "email": "john@simplylift.co", "points": "200"}]

    competition = [{"name": "Spring Festival", "date": "2022-03-27 10:00:00", "numberOfPlaces": "50"}]

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

    def __setup_club(self):
        clubs = self.load_clubs()
        for c in self.club:
            clubs.append(c)
        clubs = {'clubs': clubs}
        with open('clubs.json', 'w') as comps:
            json.dump(clubs, comps)

    def __setup_competition(self):
        compets = self.load_competitions()
        for c in self.competition:
            compets.append(c)
        compets = {'competitions': compets}
        with open('competitions.json', 'w') as comps:
            json.dump(compets, comps)

    def __tear_down_club(self):
        clubs = self.load_clubs()
        clubs = clubs[:3]
        clubs = {'clubs': clubs}
        with open('clubs.json', 'w') as comps:
            json.dump(clubs, comps)

    def __tear_down_competitions(self):
        compet = self.load_competitions()
        compet = compet[:2]
        compet = {'competitions': compet}
        with open('competitions.json', 'w') as comps:
            json.dump(compet, comps)

    def setup_method(self, method):
        self.__setup_club()
        self.__setup_competition()

    def teardown_method(self, method):
        self.__tear_down_club()
        self.__tear_down_competitions()

    def __is_in_future(self, competition):
        date_format = "%Y-%m-%d %H:%M:%S"
        result = t.strptime(competition['date'], date_format)
        result = t.mktime(result)
        diff = result - t.time()
        return diff > 0

    # END OF THE SETUP #####

    def test_max_12_places(self, client):
        """ This test gathers all the steps described in the docstring of this class """

        club = server.clubs[-1]
        competition = server.competitions[-1]
        # Step 1
        resp = client.post('/showSummary', data={'email': club['email']})
        expected_value = 'Welcome, ' + club['email']
        if expected_value in resp.data.decode():  # if login OK
            # Step 2
            resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
            if 'How many places?' in resp.data.decode():  # if booking page reached
                # Step 3
                # HAPPY PATH: book number of places < 12
                data = {'competition': competition['name'], 'club': club['name'], 'places': self.valid_number_of_places}
                resp = client.post('/purchasePlaces', data=data)
                # Step 4
                welcome_message = "Welcome, " + club['email']
                assert welcome_message in resp.data.decode()
                assert "Great-booking complete!" in resp.data.decode()
                # Step 5
                # SAD PATH: book places with a non positive integer as number of places
                data = {'competition': competition['name'], 'club': club['name'], 'places': self.wrong_number_of_places}
                resp = client.post('/purchasePlaces', data=data)
                # Step 6
                error_message = 'ERROR: The maximum places to be reserved by club is 12'
                assert error_message in resp.data.decode()
        else:  # if login error by wrong credentials
            error_message = 'This is not a valid email, please try again'
            assert error_message in resp.data.decode()
