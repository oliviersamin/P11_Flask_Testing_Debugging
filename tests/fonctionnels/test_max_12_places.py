from selenium.webdriver import Chrome
import pytest
import time
import json


@pytest.mark.functional_tests
@pytest.mark.max_12_places
class TestWithSelenium:
    """ This test checks that no club can book more than 12 places in a single competition.
    Here are the steps to do it:
    Step 1: Go to the login page
    Step 2: From this page login to access the home page
    Step 3: From this page choose a competition (in the future) to book places
    Step 4: HAPPY PATH = From there book less than 12 places
    Step 5: Check that the page confirm the booking
    Step 6: SAD PATH = once clicked on the booking link book more than 12 places
    Step 7: Check that the page displays an error message"""

    ##### SETUP THE TESTS #####
    futur_competition = {"name": "Futur_competition", "date": "2022-03-27 10:00:00", "numberOfPlaces": "200"}
    club = [{"name": "Test_club", "email": "test_club@test.com", "points": "200"}]

    def __get_points_from_string(self, string_to_use):
        string_to_use = string_to_use[::-1]
        string_to_use = string_to_use[:string_to_use.find(':')]
        string_to_use = string_to_use[::-1]
        return int(string_to_use)

    def load_competitions(self):
        with open('competitions.json') as comps:
            competitions = json.load(comps)['competitions']
            return competitions

    def load_clubs(self):
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

    ##### END OF THE SETUP #####

    # Step 1
    def __open_site_with_chrome(self):
        self.browser = Chrome("chromedriver")
        self.browser.get("http://127.0.0.1:5000/")

    # Step 2
    def __login(self):
        self.__open_site_with_chrome()
        # enter valid data to get to the welcome page
        email = self.browser.find_element_by_name("email")
        secretary_email = "test_club@test.com"
        email.send_keys(secretary_email)
        validate = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        validate.click()

    # Step 3
    def __select_future_competition(self):
        links = self.browser.find_elements_by_tag_name("a")
        for link in links:
            if (link.text == "Book Places") & ("Futur_competition" in link.get_attribute("href")):
                time.sleep(2)
                link.click()
                break

    # Step 4 & 5
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

    # Step 6 & 7
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

    # All steps for happy path
    def test_sad_path(self):
        self.__login()
        self.__select_future_competition()
        self.__sad_booking_places()

    # All steps for sad path
    def test_happy_path(self):
        self.__login()
        self.__select_future_competition()
        self.__happy_booking_places()
