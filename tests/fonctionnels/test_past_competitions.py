from selenium.webdriver import Chrome
import pytest
import time
import json


@pytest.mark.functional_tests
@pytest.mark.past_competition
class TestWithSelenium:
    """ This test checks that no club can book places for a past competition.
    Here are the steps to do it:
    Step 1: Go to the login page
    Step 2: From this page login to access the home page
    Step 3: HAPPY PATH = from this page choose a competition in the future to book places
    Step 4: Check that the page confirm the booking
    Step 5: SAD PATH = from the home page choose a competition in the past to book places
    Step 6: Check that the page displays an error message"""

    # SETUP OF THE TESTS #####
    future_competition = {"name": "Test_competition_in_future",
                          "date": "2022-03-27 10:00:00",
                          "numberOfPlaces": "200"}
    club = [{"name": "Club_test", "email": "test@test.com", "points": "100"}]

    def load_clubs(self):
        with open('clubs.json') as c:
            clubs = json.load(c)['clubs']
            return clubs

    def load_competitions(self):
        with open('competitions.json') as comps:
            competitions = json.load(comps)
            return competitions

    def __setup_competitions_json_file(self):
        compets = self.load_competitions()
        compets['competitions'].append(self.future_competition)
        # compets = json.dumps(compets)
        with open('competitions.json', 'w') as comps:
            json.dump(compets, comps)

    def __setup_club(self):
        clubs = self.load_clubs()
        for c in self.club:
            clubs.append(c)
        clubs = {'clubs': clubs}
        with open('clubs.json', 'w') as comps:
            json.dump(clubs, comps)

    def __teardown_competitions_json_file(self):
        compets = self.load_competitions()
        compets['competitions'] = compets['competitions'][:-1]
        with open('competitions.json', 'w') as comps:
            json.dump(compets, comps)

    def __tear_down_club(self):
        clubs = self.load_clubs()
        clubs = clubs[:3]
        clubs = {'clubs': clubs}
        with open('clubs.json', 'w') as comps:
            json.dump(clubs, comps)

    def setup_method(self, method):
        self.__setup_competitions_json_file()
        self.__setup_club()

    def teardown_method(self, method):
        self.__teardown_competitions_json_file()
        self.__tear_down_club()

    # END OF SETUP #####
    # Step 1
    def __open_site_with_chrome(self):
        self.browser = Chrome("chromedriver")
        self.browser.get("http://127.0.0.1:5000/")

    # Step 2
    def __login(self):
        self.__open_site_with_chrome()
        # enter valid data to get to the welcome page
        email = self.browser.find_element_by_name("email")
        secretary_email = "john@simplylift.co"
        email.send_keys(secretary_email)
        validate = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        validate.click()

    # Step 3
    def __booking_places(self):
        places = self.browser.find_element_by_name("places")
        places.send_keys("1")
        time.sleep(2)
        validate = self.browser.find_element_by_tag_name("button")
        validate.click()
        time.sleep(2)

    # Step 6 & 7
    def __sad_path(self):
        links = self.browser.find_elements_by_tag_name("a")
        for link in links:
            if (link.text == "Book Places") & ("Spring" in link.get_attribute("href")):
                time.sleep(2)
                link.click()
                break
        booking_message = "ERROR: This competition is over"
        body = self.browser.find_element_by_tag_name("body")
        assert booking_message in body.text
        self.browser.close()

    # Step 4 & 5
    def __happy_path(self):
        links = self.browser.find_elements_by_tag_name("a")
        for link in links:
            if (link.text == "Book Places") & ("Test_competition_in_future" in link.get_attribute("href")):
                time.sleep(2)
                link.click()
                break
        self.__booking_places()
        booking_message = "Great-booking complete!"
        body = self.browser.find_element_by_tag_name("body")
        assert booking_message in body.text
        self.browser.close()

    # All Steps for sad path
    def test_sad_path(self):
        self.__login()
        self.__sad_path()

    # All Steps for happy path
    def test_happy_path(self):
        self.__login()
        self.__happy_path()
