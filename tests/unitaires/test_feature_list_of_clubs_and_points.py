import pytest
from P11_Flask_Testing_Debugging import server

@pytest.mark.all_tests
@pytest.mark.new_feature
class TestNewFeature:

    def test_new_feature(self, client):
        """ Test the connexion to the new feature's page """
        resp = client.get('/listOfClubPoints')
        assert resp.status_code == 200
        assert "List of all clubs and points" in resp.data.decode()

