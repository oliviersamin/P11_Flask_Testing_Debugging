from locust import HttpUser, task
import server
import json


class TestPerformance(HttpUser):
    """ This test check the performance to reach each page of the website.
     Therefore each method correspond to one page of the website"""

    futur_competition = {"name": "Test_competition_in_future", "date": "2022-03-27 10:00:00",
                         "numberOfPlaces": "200"}

    def __load_competitions(self):
        with open('competitions.json') as comps:
            competitions = json.load(comps)['competitions']
            return competitions

    def __setup_competition(self):
        compets = self.__load_competitions()
        if compets[-1]['name'] != self.futur_competition['name']:
            compets.append(self.futur_competition)
            compets = {'competitions': compets}
            with open('competitions.json', 'w') as comps:
                json.dump(compets, comps)

    def __tear_down_competitions(self):
        compet = self.__load_competitions()
        compet = compet[:2]
        compet = {'competitions': compet}
        with open('competitions.json', 'w') as comps:
            json.dump(compet, comps)

    def on_start(self):
        self.__setup_competition()
        print("/n###### ON START #########/n", flush=True)

    def on_stop(self):
        self.__tear_down_competitions()
        print("/n###### ON STOP #########/n", flush=True)

    @task(6)
    def access_index(self):
        self.client.get('http://127.0.0.1:5000/')

    @task(6)
    def access_show_summary(self):
        data = {'email': server.clubs[0]['email']}
        self.client.post('http://127.0.0.1:5000/showSummary', data)

    @task(6)
    def access_book(self):
        competitions = self.__load_competitions()
        url = 'http://127.0.0.1:5000/book/' + competitions[-1]['name'] + '/' + server.clubs[0]['name']
        self.client.get(url)

    @task(6)
    def access_purchase_places(self):
        competitions = self.__load_competitions()
        data = {'competition': competitions[-1]['name'], 'club': server.clubs[0]['name'],
                'places': "1"}
        self.client.post('http://127.0.0.1:5000/purchasePlaces', data)

    @task(6)
    def access_list_of_club_points(self):
        self.client.get('http://127.0.0.1:5000/listOfClubPoints')
