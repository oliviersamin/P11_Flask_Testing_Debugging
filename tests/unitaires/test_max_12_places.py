import pytest
from P11_Flask_Testing_Debugging import server
import json



@pytest.mark.all_tests
@pytest.mark.max_12_places
class Test_max_12_places:

    club = [{"name": "Simply Lift", "email": "john@simplylift.co", "points": "200"}]

    competition = [{"name": "Spring Festival", "date": "2022-03-27 10:00:00", "numberOfPlaces": "50"}]

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
    def test_book_max_12_places(self, client, data, expected_flash_message, mocker):
        mocker.patch.object(server, 'clubs', self.club)
        mocker.patch.object(server, 'competitions', self.competition)
        data = {'competition': server.competitions[-1]['name'], 'club': server.clubs[-1]['name'], 'places': data['places']}
        resp = client.post('/purchasePlaces', data=data)
        # assert resp.status_code == 200
        assert expected_flash_message in resp.data.decode()

