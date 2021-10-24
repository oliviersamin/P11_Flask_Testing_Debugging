import pytest
from P11_Flask_Testing_Debugging import server
from flask import url_for

@pytest.mark.all_tests
@pytest.mark.login_error
def test_error_login_valid_email_used(client, load_clubs):
    """ test using an email existing in the clubs.json file (mocked)"""
    clubs = load_clubs
    data = {'email': clubs[-1]['email']}
    resp = client.post('/showSummary', data=data)
    expected_status_code = 200
    expected_value = 'Welcome, ' + data['email']
    assert resp.status_code == expected_status_code
    assert expected_value in resp.data.decode()


@pytest.mark.login_error
def test_error_login_invalid_email_used(client):
    """ test using an email not existing in the clubs.json file"""
    data = {'email': 'invalid_email@test.com'}
    resp = client.post('/showSummary', data=data)
    assert resp.status_code == 200
    expected_value = 'This is not a valid email, please try again'
    assert expected_value in resp.data.decode()

