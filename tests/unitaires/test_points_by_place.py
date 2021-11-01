import pytest
from P11_Flask_Testing_Debugging import server


@pytest.mark.all_tests
@pytest.mark.points_by_place
class TestPointsByPlace:
    """ This test correspond to a new feature asked during the project testing
     Check that one place booked correspond to 3 points of the club balance"""

    club = [{"name": "Club_test", "email": "test@test.com", "points": "100"}]

    competition = [{"name": "Test_points_by_place", "date": "2022-03-27 10:00:00", "numberOfPlaces": "200"}]

    def test_club_points_by_place(self, client, mocker):
        """ check that with positive integers numbers, the balance od point of the club is updated
        after a reservation"""
        mocker.patch.object(server, 'clubs', self.club)
        mocker.patch.object(server, 'competitions', self.competition)
        compet = server.competitions[-1]
        club = server.clubs[-1]
        club_points_at_start = int(club['points'])
        data = {'competition': compet['name'], 'club': club['name'], 'places': '1'}
        resp = client.post('/purchasePlaces', data=data)
        welcome_message = "Welcome, " + club['email']
        points_updated = "Points available: " + club['points']
        assert resp.status_code == 200
        assert welcome_message in resp.data.decode()
        assert "Great-booking complete!" in resp.data.decode()
        assert points_updated in resp.data.decode()
        assert int(club['points']) == (int(club_points_at_start) - 3 * int(data['places']))
