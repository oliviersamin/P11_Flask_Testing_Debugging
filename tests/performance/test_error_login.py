from locust import HttpUser, task
import pytest

@pytest.mark.login_error
class TestPerformance(HttpUser):

    @task(6)
    def home(self):
        self.client.get('http://127.0.0.1:5000/')

    @task(6)
    def login(self):
        self.client.post('http://127.0.0.1:5000/showSummary', {'email': 'john@simplylift.co'})

