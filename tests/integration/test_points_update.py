import pytest
from P11_Flask_Testing_Debugging import server
import json


@pytest.mark.all_tests
@pytest.mark.points_updated
class TestPointsUpdated:
    """ This test  is made of the several steps:
    Step 1: Connexion to login page
    Step 2: When login successfull go to the booking page of a future competition
    Step 3: Book 1 place
    Step 4: Go back to the welcome page and check the value of the club balance points"""

    # SETUP THE TEST #####
    valid_number_of_places = 1
    wrong_number_of_places = -1
    future_competition = {"name": "Test_competition_in_future",
                          "date": "2022-03-27 10:00:00",
                          "numberOfPlaces": "200"}

    def load_clubs(self):
        """ load the data from 'clubs.json' and override the clubs variable from server.py """
        with open('clubs.json') as c:
            clubs = json.load(c)['clubs']
            return clubs

    def load_competitions(self):
        """ load the data from 'clubs.json' and override the competitions varable from server.py """
        with open('competitions.json') as comps:
            competitions = json.load(comps)
            return competitions

    def __setup_competitions_json_file(self):
        """ insert needed data for the tests and save the json """
        compets = self.load_competitions()
        compets['competitions'].append(self.future_competition)
        # compets = json.dumps(compets)
        with open('competitions.json', 'w') as comps:
            json.dump(compets, comps)

    def __teardown_competitions_json_file(self):
        compets = self.load_competitions()
        compets['competitions'] = compets['competitions'][:-1]
        with open('competitions.json', 'w') as comps:
            json.dump(compets, comps)

    def setup_method(self, method):
        self.__setup_competitions_json_file()
        server.competitions = self.load_competitions()

    def teardown_method(self, method):
        self.__teardown_competitions_json_file()
        server.competitions = self.load_competitions()

    # END OF THE SETUP #####

    def test_points_updated(self, client):
        """ This steps gather all the steps described in the docstring of this class """

        # Setup the test data
        competition = server.competitions['competitions'][-1]
        club = server.clubs[-1]
        # Step 1
        resp = client.post('/showSummary', data={'email': club['email']})
        expected_value = 'Welcome, ' + club['email']
        if expected_value in resp.data.decode():  # if login OK
            # Step 2
            resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
            if 'How many places?' in resp.data.decode():  # if booking page reached
                # Step 3
                # HAPPY PATH: book places with a valid positive integer as number of places
                data = {'competition': competition['name'], 'club': club['name'], 'places': self.valid_number_of_places}
                club['points'] = str(int(club['points']) - 3 * int(data['places']))
                resp = client.post('/purchasePlaces', data=data)
                # Step 4
                welcome_message = "Welcome, " + club['email']
                points_updated = "Points available: " + club['points']
                assert welcome_message in resp.data.decode()
                assert "Great-booking complete!" in resp.data.decode()
                assert points_updated in resp.data.decode()
                # SAD PATH: book places with a non positive integer as number of places
                # Step 3
                data = {'competition': competition['name'], 'club': club['name'], 'places': self.wrong_number_of_places}
                resp = client.post('/purchasePlaces', data=data)
                # Step 4
                error_message = 'ERROR: The number of places booked is not a positive integer'
                assert error_message in resp.data.decode()
                assert points_updated in resp.data.decode()
        else:  # if login error by wrong credentials
            error_message = 'This is not a valid email, please try again'
            assert error_message in resp.data.decode()
