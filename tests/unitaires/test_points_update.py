import pytest
from P11_Flask_Testing_Debugging import server
import json


@pytest.mark.all_tests
@pytest.mark.points_updated
class TestPointsUpdated:
    """ This test needs several steps as this is the first one implemented after the login error.
     In order to validate that the points have been updated properly one first need to be sure that:
     Step 1: The club balance points is a positive integer
     Step 2: The competition number of places is a positive integer
     Step 3: The number of places booked is a positive integer
     Step 4: At last that the club balance points has been properly updated
     For each of these step an error message needs to be displayed if needed"""

    # SETUP OF THE TEST  ###########
    club = [{"name": "Simply Lift", "email": "john@simplylift.co", "points": "-13"},
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "AA/13"},
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "3.1"}]

    competition = [{"name": "Spring Festival", "date": "2022-03-27 10:00:00", "numberOfPlaces": "-25"},
                   {"name": "Spring Festival", "date": "2022-03-27 10:00:00", "numberOfPlaces": "2.3"},
                   {"name": "Spring Festival", "date": "2022-03-27 10:00:00", "numberOfPlaces": "A4"},
                   {"name": "Spring Festival", "date": "2022-03-27 10:00:00", "numberOfPlaces": "200"}]

    def load_clubs(self):
        """ load the data from 'clubs.json' and override the clubs variable from server.py """
        with open('clubs.json') as c:
            clubs = json.load(c)['clubs']
            return clubs

    def load_competitions(self):
        """ load the data from 'clubs.json' and override the competitions variable from server.py """
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

    # END OF SETUP ###########

    # Step 1
    def test_club_points_is_not_positive_integer(self, client):
        """ check that the points in the club input are positive integer """
        for club in server.clubs[3:]:
            resp = client.post('/showSummary', data=club)
            print('club = ', club, flush=True)
            print(resp.data.decode(), flush=True)
            expected_flash_message = "ERROR: The number of points for the club is not a positive integer"
            assert expected_flash_message in resp.data.decode()

    # Step 2
    def test_competition_number_of_places_is_not_positive_integer(self, client):
        """ check that the number of places in the competition input is positive integer """
        data = {'email': server.clubs[0]['email']}
        resp = client.post('/showSummary', data=data)
        expected_message = "ERROR: The number of places is not a positive integer"
        assert expected_message in resp.data.decode()

    # Step 3
    def test_booking_places_is_not_positive_integer(self, client):
        """ check that the number of places asked is a positive integer"""
        competition_in_futur = server.competitions[-1]
        data = {'competition': competition_in_futur['name'], 'club': server.clubs[0]['name'], 'places': '-3'}
        resp = client.post('/purchasePlaces', data=data)
        expected_flash_message = "ERROR: The number of places booked is not a positive integer"
        assert expected_flash_message in resp.data.decode()

    # Step 4
    def test_club_points_updated(self, client, load_clubs):
        """ check that with positive integers numbers, the balance od point of the club is updated
        after a reservation"""
        compet = server.competitions[-1]
        club = server.clubs[0]
        starting_points = club['points']
        data = {'competition': compet['name'],
                'club': club['name'],
                'places': '1'}
        expected_points_updated = str(int(starting_points) - int(data['places']) * 3)
        resp = client.post('/purchasePlaces', data=data)
        welcome_message = "Welcome, " + club['email']
        points_updated = "Points available: " + expected_points_updated
        assert resp.status_code == 200
        assert welcome_message in resp.data.decode()
        assert "Great-booking complete!" in resp.data.decode()
        assert points_updated in resp.data.decode()
