from selenium.webdriver import Chrome
from P11_Flask_Testing_Debugging import server
import pytest
import time
import json


@pytest.mark.functional_tests
@pytest.mark.points_by_place
class TestWithSelenium:
    """ Test the change in number of points needed to book a place
     Step 1: Login
     Step 2: Choose a competition in the futur
     Step 3: Book a place in this competition
     Step 4: Check that the correct amount of point has been removed to the club balance points
     """

    ##### Steup the data and the test ########
    futur_competition = {"name": "Test_competition_in_future",
                          "date": "2022-03-27 10:00:00",
                          "numberOfPlaces": "200"}

    club = [{"name": "Club_test", "email": "test@test.com", "points": "100"}]

    amount_of_places = '1'

    def __get_points_from_string(self, string_to_use):
        string_to_use = string_to_use[::-1]
        string_to_use = string_to_use[:string_to_use.find(':')]
        string_to_use = string_to_use[::-1]
        return(int(string_to_use))

    def load_clubs(self):
        """ load the data from 'clubs.json' and override the clubs varable from server.py """
        with open('clubs.json') as c:
            clubs = json.load(c)['clubs']
            return clubs

    def load_competitions(self):
        """ load the data from 'clubs.json' and override the competitions varable from server.py """
        with open('competitions.json') as comps:
            competitions = json.load(comps)['competitions']
            return competitions

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

    #######  end of setup #########


    def __open_site_with_chrome(self):
        self.browser = Chrome("chromedriver")
        self.browser.get("http://127.0.0.1:5000/")

    # Step 1
    def __login(self):
        self.__open_site_with_chrome()
        # enter valid data to get to the welcome page
        email = self.browser.find_element_by_name("email")
        secretary_email = "test@test.com"
        email.send_keys(secretary_email)
        validate = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        validate.click()

    # Step 2
    def __select_future_competition(self):
        links = self.browser.find_elements_by_tag_name("a")
        for l in links:
            if (l.text == "Book Places") & ("Test" in l.get_attribute("href")):
                time.sleep(2)
                l.click()
                break

    # Step 3
    def __booking_places(self):
        time.sleep(2)
        places = self.browser.find_element_by_name("places")
        places.send_keys(self.amount_of_places)
        time.sleep(2)
        validate = self.browser.find_element_by_tag_name("button")
        validate.click()
        time.sleep(2)

    # Step 4
    def __check_amount_of_points_in_balance_club(self):
        booking_message = "Great-booking complete!"
        amount_of_points_expected = str(int(self.club[0]['points']) - 3 * int(self.amount_of_places))
        expected_message = "Points available: " + amount_of_points_expected
        body = self.browser.find_element_by_tag_name("body")
        assert booking_message in body.text
        assert expected_message in body.text
        self.browser.close()

    # Test with all previous steps
    def test_happy_path(self):
        self.__login()
        self.__select_future_competition()
        self.__booking_places()
        self.__check_amount_of_points_in_balance_club()


