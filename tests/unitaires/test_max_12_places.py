import pytest
from P11_Flask_Testing_Debugging import server
import json


@pytest.mark.max_12_places
class Test_max_12_places:

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
        clubs = self.load_clubs()

    def __setup_competition(self):
        compets = self.load_competitions()
        for c in self.competition:
            compets.append(c)
        compets = {'competitions': compets}
        with open('competitions.json', 'w') as comps:
                json.dump(compets, comps)
        compets = self.load_competitions()

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

    @pytest.mark.parametrize("data,expected_flash_message",
                             [({'places': '1'},
                               "Great-booking complete!"),
                              ({'places': '12'},
                               "Great-booking complete!"),
                              ({'places': '13'},
                               "ERROR: The maximum places to be reserved by club is 12"),
                              ({'places': '20'},
                               "ERROR: The maximum places to be reserved by club is 12"),
                              ({'places': '17'},
                               "ERROR: The maximum places to be reserved by club is 12")
                              ])
    def test_book_max_12_places(self, client, data, expected_flash_message):
        clubs = server.clubs
        competitions = server.competitions
        data = {'competition': competitions[-1]['name'], 'club': clubs[-1]['name'], 'places': data['places']}
        resp = client.post('/purchasePlaces', data=data)
        # assert resp.status_code == 200
        assert expected_flash_message in resp.data.decode()