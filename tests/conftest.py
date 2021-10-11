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


@pytest.fixture
def is_a_positive_integer(string_to_check: str):
    """ check that the string_to_check is a positive integer and not another alphanumeric value
        param: input type = string
        param: ouput type = boolean
    """
    filter = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    check = ""
    for character in number_of_places:
        if character not in filter:
            check = character
            break
    return check == ""
