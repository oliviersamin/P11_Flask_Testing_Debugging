import pytest
from P11_Flask_Testing_Debugging import server
import json

@pytest.mark.points_updated
class Test_points_updated:

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

    @pytest.mark.parametrize("data,expected_flash_message",
                             [({"name": "Simply Lift", "email": "john@simplylift.co", "points": "-13"},
                               "ERROR: The number of points for the club is not a positive integer"),
                              ({"name": "Simply Lift", "email": "john@simplylift.co", "points": "AA/13"},
                               "ERROR: The number of points for the club is not a positive integer"),
                              ({"name": "Simply Lift", "email": "john@simplylift.co", "points": "3.1"},
                               "ERROR: The number of points for the club is not a positive integer")
                              ])
    def test_club_points_is_not_positive_integer(self, client, data, expected_flash_message, mocker):
        mocker.patch.object(server, 'clubs', [data])
        print('server.clubs = ', server.clubs, flush=True)
        """ check that the points in the club input are positive integer """
        resp = client.post('/showSummary', data=data)
        assert expected_flash_message in resp.data.decode()


    @pytest.mark.parametrize("compet,expected_message",
                             [({"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "-25"},
                               "ERROR: The number of places is not a positive integer"),
                              ({"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "2.3"},
                              "ERROR: The number of places is not a positive integer"),
                              ({"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "A4"},
                               "ERROR: The number of places is not a positive integer"),
                              ])
    def test_competition_number_of_places_is_not_positive_integer(self, client, compet, expected_message, mocker):
        """ check that the number of places in the competition input is positive integer """
        mocker.patch.object(server, 'competitions', [compet])
        clubs = server.clubs
        data = {'email': clubs[0]['email']}
        resp = client.post('/showSummary', data=data)
        assert expected_message in resp.data.decode()


    @pytest.mark.parametrize("data,expected_flash_message",
                             [({'places': '-3'},
                               "ERROR: The number of places booked is not a positive integer"),
                              ({'places': "3.7"},
                              "ERROR: The number of places booked is not a positive integer"),
                              ({'places': "AE/"},
                               "ERROR: The number of places booked is not a positive integer"),
                              ])
    def test_booking_places_is_not_positive_integer(self, client, data, expected_flash_message):
        """ check that the number of places asked is a positive integer"""
        clubs = server.clubs
        competitions = server.competitions
        data = {'competition': competitions[-1]['name'], 'club': clubs[0]['name'], 'places': data['places']}
        resp = client.post('/purchasePlaces', data=data)
        assert expected_flash_message in resp.data.decode()


    def test_club_points_updated(self, client, load_clubs):
        """ check that with positive integers numbers, the balance od point of the club is updated
        after a reservation"""
        clubs = load_clubs
        competitions = server.competitions
        club = {}
        compet = {}
        # selection of a club with a positive integer as number of points
        for c in clubs:
            if int(c['points']) & int(c['points']) > 0:
                club = c
                break

        # selection of a competition with a positive integer as number of places
        for c in competitions:
            if int(c['numberOfPlaces']) & int(c['numberOfPlaces']) >0:
                compet = c
                break

        data = {'competition': compet['name'],
                'club': club['name'],
                'places': '1'}
        print('club points avant = ', club['points'], flush=True)
        club['points'] = str(int(club['points']) - int(data['places']))
        resp = client.post('/purchasePlaces', data=data)
        welcome_message = "Welcome, " + club['email']
        points_updated = "Points available: " + club['points']
        print('points updated = ', points_updated, flush=True)
        assert resp.status_code == 200
        assert welcome_message in resp.data.decode()
        assert "Great-booking complete!" in resp.data.decode()
        assert points_updated in resp.data.decode()
