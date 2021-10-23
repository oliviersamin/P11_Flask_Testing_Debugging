from selenium.webdriver import Chrome
import pytest
import time
import json


# @pytest.mark.max_12_places
class TestWithSelenium:

    futur_competition = {"name": "Futur_competition", "date": "2022-03-27 10:00:00", "numberOfPlaces": "200"}
    club = [{"name": "Test_club", "email": "test_club@test.com", "points": "200"}]

    def __get_points_from_string(self, string_to_use):
        string_to_use = string_to_use[::-1]
        string_to_use = string_to_use[:string_to_use.find(':')]
        string_to_use = string_to_use[::-1]
        return(int(string_to_use))

    def load_competitions(self):
        """ load the data from 'clubs.json' and override the competitions varable from server.py """
        with open('competitions.json') as comps:
            competitions = json.load(comps)['competitions']
            return competitions

    def load_clubs(self):
        """ load the data from 'clubs.json' and override the clubs varable from server.py """
        with open('clubs.json') as c:
            clubs = json.load(c)['clubs']
            return clubs

    def __setup_competition(self):
        compets = self.load_competitions()
        compets.append(self.futur_competition)
        compets = {'competitions': compets}
        with open('competitions.json', 'w') as comps:
                json.dump(compets, comps)

    def __setup_club(self):
        clubs = self.load_clubs()
        for c in self.club:
            clubs.append(c)
        clubs = {'clubs': clubs}
        with open('clubs.json', 'w') as comps:
                json.dump(clubs, comps)
        clubs = self.load_clubs()


    def __tear_down_competitions(self):
        compet = self.load_competitions()
        compet = compet[:2]
        compet = {'competitions': compet}
        with open('competitions.json', 'w') as comps:
            json.dump(compet, comps)

    def __tear_down_club(self):
        clubs = self.load_clubs()
        clubs = clubs[:3]
        clubs = {'clubs': clubs}
        with open('clubs.json', 'w') as comps:
            json.dump(clubs, comps)


    def setup_method(self, method):
        self.__setup_competition()
        self.__setup_club()

    def teardown_method(self, method):
        self.__tear_down_competitions()
        self.__tear_down_club()

    def __open_site_with_Chrome(self):
        self.browser = Chrome("chromedriver")
        self.browser.get("http://127.0.0.1:5000/")

    def __login(self):
        self.__open_site_with_Chrome()
        # enter valid data to get to the welcome page
        email = self.browser.find_element_by_name("email")
        secretary_email = "test_club@test.com"
        email.send_keys(secretary_email)
        validate = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        validate.click()

    def __select_future_competition(self):
        links = self.browser.find_elements_by_tag_name("a")
        for l in links:
            if (l.text == "Book Places") & ("Futur_competition" in l.get_attribute("href")):
                time.sleep(2)
                l.click()
                break

    def __happy_booking_places(self):
        places = self.browser.find_element_by_name("places")
        places.send_keys("10")
        time.sleep(2)
        validate = self.browser.find_element_by_tag_name("button")
        validate.click()
        time.sleep(2)
        booking_message = "Great-booking complete!"
        body = self.browser.find_element_by_tag_name("body")
        assert booking_message in body.text
        self.browser.close()

    def __sad_booking_places(self):
        places = self.browser.find_element_by_name("places")
        places.send_keys("13")
        time.sleep(2)
        validate = self.browser.find_element_by_tag_name("button")
        validate.click()
        time.sleep(2)
        booking_message = "ERROR: The maximum places to be reserved by club is 12"
        body = self.browser.find_element_by_tag_name("body")
        assert booking_message in body.text
        self.browser.close()

    def test_sad_path(self):
        self.__login()
        self.__select_future_competition()
        self.__sad_booking_places()

    def test_happy_path(self):
        self.__login()
        self.__select_future_competition()
        self.__happy_booking_places()



