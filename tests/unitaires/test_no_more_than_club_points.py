import pytest
from P11_Flask_Testing_Debugging import server
import time as t


@pytest.mark.all_tests
@pytest.mark.no_more_than_club_points
class TestNoMoreThanClubPoints:
    """ This test check that no club can book more than its balance points
     An error message shall be written otherwise"""

    def __is_in_future(self, competition):
        date_format = "%Y-%m-%d %H:%M:%S"
        result = t.strptime(competition['date'], date_format)
        result = t.mktime(result)
        diff = result - t.time()
        return diff > 0

    @pytest.mark.parametrize("data,expected_flash_message",
                             [({'places': '1'},
                               "Great-booking complete!"),
                              ({'places': '14'},
                               "ERROR: You cannot book more places than your total club points"),
                              ({'places': '10'},
                               "ERROR: You cannot book more places than your total club points"),
                              ])
    def test_book_no_more_than_clubs_points(self, client, data, expected_flash_message, mocker):
        mocker.patch.object(server, 'clubs', [{"name": "Test_club",
                                               "email": "test_club@test.com", "points": "8"}])
        mocker.patch.object(server, 'competitions', [{"name": "Test_competition",
                                                      "date": "2022-10-22 13:30:00",
                                                      "numberOfPlaces": "200"}])

        data = {'competition': server.competitions[0]['name'],
                'club': server.clubs[0]['name'],
                'places': data['places']}
        resp = client.post('/purchasePlaces', data=data)
        # assert resp.status_code == 200
        assert expected_flash_message in resp.data.decode()
