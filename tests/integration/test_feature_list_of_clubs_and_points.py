import pytest
from P11_Flask_Testing_Debugging import server
import time as t

@pytest.mark.all_tests
@pytest.mark.new_feature
class TestNewFeature:
    """ This test checks that anyone can access from the login page but without beeing logged in
    The list of all clubs with their actual balance points.
    Here are the steps used:
    Step 1: Connexion to page containing list of clubs
    Step 2: From there connect to the home page
    Step 3: From there login
    Step 4: Check the login is valid"""

    def test_new_feature(self, client):
        """ This test gathers all the steps described in the docstring of this class """

        club = server.clubs[0]
        # Step1
        # connexion to new feature of the site, the public page
        resp = client.get('/listOfClubPoints')
        if "List of all clubs and points" in resp.data.decode():
            # Step2
            resp = client.get('/')
            if resp.status_code == 200:
                # Step 3
                resp = client.post('/showSummary', data={'email': club['email']})
                # Step 4
                expected_value = 'Welcome, ' + club['email']
                assert expected_value in resp.data.decode()
