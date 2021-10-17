import pytest
from P11_Flask_Testing_Debugging import server


@pytest.mark.max_12_places
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
def test_book_max_12_places(client, load_clubs, load_competitions, data, expected_flash_message):
    clubs = load_clubs
    competitions = load_competitions
    data = {'competition': competitions[-1]['name'], 'club': clubs[0]['name'], 'places': data['places']}
    resp = client.post('/purchasePlaces', data=data)
    # assert resp.status_code == 200
    assert expected_flash_message in resp.data.decode()