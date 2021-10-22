from selenium.webdriver import Chrome
import pytest
from P11_Flask_Testing_Debugging import server
import time
import json


@pytest.mark.past_competition
class TestWithSelenium:

    future_competition = {"name": "Test_competition_in_future",
                          "date": "2022-03-27 10:00:00",
                          "numberOfPlaces": "200"}

    def load_clubs(self):
        """ load the data from 'clubs.json' and override the clubs variable from server.py """
        with open('clubs.json') as c:
            clubs = json.load(c)['clubs']
            return clubs

    def load_competitions(self):
        """ load the data from 'clubs.json' and override the competitions varable from server.py """
        with open('competitions.json') as comps:
            competitions = json.load(comps)
            return competitions

    def __setup_competitions_json_file(self):
        """ insert needed data for the tests and save the json """
        compets = self.load_competitions()
        compets['competitions'].append(self.future_competition)
        # compets = json.dumps(compets)
        with open('competitions.json', 'w') as comps:
            json.dump(compets, comps)

    def __teardown_competitions_json_file(self):
        compets = self.load_competitions()
        compets['competitions'] = compets['competitions'][:-1]
        with open('competitions.json', 'w') as comps:
            json.dump(compets, comps)


    def setup_method(self, method):
        # server.clubs = self.load_clubs()
        self.__setup_competitions_json_file()
        server.competitions = self.load_competitions()

    def teardown_method(self, method):
        # server.clubs = self.load_clubs()
        self.__teardown_competitions_json_file()
        server.competitions = self.load_competitions()

    def __open_site_with_Chrome(self):
        self.browser = Chrome("chromedriver")
        self.browser.get("http://127.0.0.1:5000/")

    def __login(self):
        self.__open_site_with_Chrome()
        # enter valid data to get to the welcome page
        email = self.browser.find_element_by_name("email")
        secretary_email = "john@simplylift.co"
        email.send_keys(secretary_email)
        validate = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        validate.click()

    def __booking_places(self):
        places = self.browser.find_element_by_name("places")
        places.send_keys("1")
        time.sleep(2)
        validate = self.browser.find_element_by_tag_name("button")
        validate.click()
        time.sleep(2)

    def __sad_path(self):
        links = self.browser.find_elements_by_tag_name("a")
        for l in links:
            if (l.text == "Book Places") & ("Spring" in l.get_attribute("href")):
                print("selected = ", l.get_attribute("href"), flush=True)
                time.sleep(2)
                l.click()
                break
        booking_message = "ERROR: This competition is over"
        body = self.browser.find_element_by_tag_name("body")
        assert booking_message in body.text
        self.browser.close()

    def __happy_path(self):
        links = self.browser.find_elements_by_tag_name("a")
        for l in links:
            if (l.text == "Book Places") & ("Test_competition_in_future" in l.get_attribute("href")):
                time.sleep(2)
                l.click()
                break
        self.__booking_places()
        booking_message = "Great-booking complete!"
        body = self.browser.find_element_by_tag_name("body")
        assert booking_message in body.text
        self.browser.close()

    def test_sad_path(self):
        self.__login()
        self.__sad_path()

    def test_happy_path(self):
        self.__login()
        self.__happy_path()

