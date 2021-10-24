import pytest
from P11_Flask_Testing_Debugging import server
import time as t


@pytest.mark.new_feature
class TestNewFeature:

    def test_new_feature(self, client):
        """ this test check the new feature and its integration to login page
         Step 1: Go to the new feature's page
         Step2: From there go back to the home page
         Step3: Login from the home page"""

        club = server.clubs[0]
        # Step1
        # connexion to new feature of the site, the public page
        resp = client.get('/listOfClubPoints')
        if "List of all clubs and points" in resp.data.decode():
            # if Step1 OK --> Step2
            resp = client.get('/')
            if resp.status_code == 200:
                # if Step 2 OK --> Step 3
                resp = client.post('/showSummary', data={'email': club['email']})
                expected_value = 'Welcome, ' + club['email']
                assert expected_value in resp.data.decode()
