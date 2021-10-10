import pytest
import json
from P11_Flask_Testing_Debugging import server


@pytest.fixture
def client():
    """ client to be able to use flask app """
    server.app.config.update({'TESTING': True})
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def load_clubs():
    """ load the data from 'clubs.json' and override the clubs varable from server.py """
    with open('clubs.json') as c:
         clubs = json.load(c)['clubs']
         return clubs


@pytest.fixture
def load_competitions():
    """ load the data from 'clubs.json' and override the competitions varable from server.py """
    with open('competitions.json') as comps:
         competitions = json.load(comps)['competitions']
         return competitions
