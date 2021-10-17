from locust import HttpUser, task
import pytest


class TestPerformance(HttpUser):

    @classmethod
    def setup_class(cls, mocker):
        mocker.patch.object(server, 'clubs', [{"name": "Simply Lift",
                                               "email": "john@simplylift.co", "points": "3"}])

    @task(6)
    def access_to_welcome_page_happy_path(self):
        data = {'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '1'}
        self.client.post('http://127.0.0.1:5000/purchasePlaces', data)

    @task(6)
    def access_to_welcome_page_sad_path(self):
        data = {'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '10'}
        self.client.post('http://127.0.0.1:5000/purchasePlaces', data)
