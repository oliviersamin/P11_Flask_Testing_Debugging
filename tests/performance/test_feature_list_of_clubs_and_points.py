from locust import HttpUser, task
import pytest


class TestPerformance(HttpUser):

    @task(6)
    def access_to_new_feature_page(self):
        self.client.get('http://127.0.0.1:5000/listOfClubPoints')
