from locust import HttpUser, task
import pytest


class TestPerformance(HttpUser):

    @task(6)
    def access_to_welcome_page_happy_path(self):
        data = {'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '10'}
        self.client.post('http://127.0.0.1:5000/purchasePlaces', data)

    @task(6)
    def access_to_welcome_page_sad_path(self):
        data = {'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '13'}
        self.client.post('http://127.0.0.1:5000/purchasePlaces', data)
