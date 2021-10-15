from locust import HttpUser, task
import pytest


class TestPerformance(HttpUser):

    @task(6)
    def access_to_book_page(self):
        self.client.get('http://127.0.0.1:5000/book/Spring Festival/Simply Lift')

    @task(6)
    def book_places_for_a_competition(self):
        self.client.post('http://127.0.0.1:5000/purchasePlaces', {'competition': 'Spring Festival',
                                                                  'club': 'Simply Lift',
                                                                  'places': '1'})

