import pytest
from P11_Flask_Testing_Debugging import server
import time as t


def __from_date_to_epoch_time(date):
    date_format = "%Y-%m-%d %H:%M:%S"
    result = t.strptime(date, date_format)
    return t.mktime(result)


@pytest.mark.past_competition
@pytest.mark.parametrize("competition,expected_flash_message",
                         [({"name": "Test1", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
                           "ERROR: This competition is over"),
                          ({"name": "Test2", "date": "2019-04-02 12:00:00", "numberOfPlaces": "25"},
                           "ERROR: This competition is over"),
                          ({"name": "Test3", "date": "2020-09-27 14:00:00", "numberOfPlaces": "25"},
                           "ERROR: This competition is over")
                          ])
def test_past_competition_access(client, load_clubs, competition, expected_flash_message, mocker):
    mocker.patch.object(server, 'competitions', [competition])
    clubs = load_clubs
    club = clubs[0]
    resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
    # difference between actual dae and competition date
    # competition_date = __from_date_to_epoch_time(competition['date'])
    # difference = competition_date - t.time()
    # assert difference >= 0
    assert expected_flash_message in resp.data.decode()


@pytest.mark.past_competition
@pytest.mark.parametrize("competition,expected_message",
                         [({"name": "Test1", "date": "2022-03-27 10:00:00", "numberOfPlaces": "25"},
                           "How many places?"),
                          ({"name": "Test2", "date": "2023-04-02 12:00:00", "numberOfPlaces": "25"},
                           "How many places?"),
                          ({"name": "Test3", "date": "2022-09-27 14:00:00", "numberOfPlaces": "25"},
                           "How many places?")
                          ])
def test_future_competition_access(client, load_clubs, competition, expected_message, mocker):
    mocker.patch.object(server, 'competitions', [competition])
    clubs = load_clubs
    club = clubs[0]
    resp = client.get('/book/{}/{}'.format(competition['name'], club['name']))
    assert expected_message in resp.data.decode()
