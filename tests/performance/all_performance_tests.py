from locust import HttpUser, task
import server


class TestPerformance(HttpUser):

    @task(6)
    def access_index(self):
        self.client.get('http://127.0.0.1:5000/')

    @task(6)
    def access_show_summary(self):
        data = {'email': server.clubs[0]['email']}
        self.client.post('http://127.0.0.1:5000/showSummary', data)

    @task(6)
    def access_book(self):
        url = 'http://127.0.0.1:5000/book/' + server.competitions[0]['name'] + '/' + server.clubs[0]['name']
        self.client.get(url)

    @task(6)
    def access_purchase_places(self):
        data = {'competition': server.competitions[0]['name'], 'club': server.clubs[0]['name'],
                'places': "1"}
        self.client.post('http://127.0.0.1:5000/purchasePlaces', data)

    @task(6)
    def access_list_of_club_points(self):
        self.client.get('http://127.0.0.1:5000/listOfClubPoints')
