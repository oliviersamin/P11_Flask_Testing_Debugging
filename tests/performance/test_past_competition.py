from locust import HttpUser, task
import pytest


class TestPerformance(HttpUser):

    @task(6)
    def access_to_book_page(self):
        self.client.get('http://127.0.0.1:5000/book/Fall Classic/Simply Lift')

    @task(6)
    def denied_access_to_book_page_and_redirect_to_welcome_page(self):
        self.client.get('http://127.0.0.1:5000/book/Spring Festival/Simply Lift')
