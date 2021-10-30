from selenium.webdriver import Chrome
import pytest
import time
import json


@pytest.mark.functional_tests
@pytest.mark.points_updated
class TestWithSelenium:
    """ This test checks that the balance points of a club is updated after a valid booking.
    Here are the steps used:
    Step 1: Login
    Step 2: Select a futur competition to book places
    Step 3: Happy path = Book a valid number of places
    Step 4: Check that the booking message is displayed
    Step 5: Sad path = Book a non valid number of places
    Step 6: Check that an error message is displayed"""

    #### SET UP THE TESTS #####
    futur_competition = {"name": "Futur_competition", "date": "2022-03-27 10:00:00", "numberOfPlaces": "200"}

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

    def __setup_competition(self):
        compets = self.load_competitions()
        compets.append(self.futur_competition)
        compets = {'competitions': compets}
        with open('competitions.json', 'w') as comps:
                json.dump(compets, comps)

    def __tear_down_competitions(self):
        compet = self.load_competitions()
        compet = compet[:2]
        compet = {'competitions': compet}
        with open('competitions.json', 'w') as comps:
            json.dump(compet, comps)

    def setup_method(self, method):
        self.__setup_competition()

    def teardown_method(self, method):
        self.__tear_down_competitions()

    #### ENF OF THE SET UP #####

    #### METHODS USED FOR THE TESTS ####
    def __open_site_with_chrome(self):
        self.browser = Chrome("chromedriver")
        self.browser.get("http://127.0.0.1:5000/")

    def __login(self):
        self.__open_site_with_chrome()
        # enter valid data to get to the welcome page
        email = self.browser.find_element_by_name("email")
        secretary_email = "john@simplylift.co"
        email.send_keys(secretary_email)
        validate = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        validate.click()

    def __select_the_futur_competition(self):
        self.initial_points = self.browser.find_element_by_tag_name("div").text
        self.initial_points = self.__get_points_from_string(self.initial_points)
        links = self.browser.find_elements_by_tag_name("a")
        compets = []
        for l in links:
            if l.text == "Book Places":
                compets.append(l)
        time.sleep(2)
        compets[-1].click()

    def __choose_number_of_places_to_book(self, number_of_places, error):
        places = self.browser.find_element_by_name("places")
        places.send_keys(number_of_places)
        time.sleep(2)
        validate = self.browser.find_element_by_tag_name("button")
        validate.click()
        time.sleep(3)
        if not error:  # HAPPY PATH
            booking_message = "Great-booking complete!"
            self.final_points = self.browser.find_element_by_tag_name("div").text
            print("\n######## DANS CHOOSE ###########\n", self.final_points, flush=True)
            self.final_points = self.__get_points_from_string(self.final_points)
            print("self.final_points = ", self.final_points)
            body = self.browser.find_element_by_tag_name("body")
            assert booking_message in body.text
            assert self.final_points == (self.initial_points - 3 * int(number_of_places))
        else:  # SAD PATH
            error_message = 'ERROR: The number of places booked is not a positive integer'
            body = self.browser.find_element_by_tag_name("body")
            assert error_message in body.text

        self.browser.close()

    #### TESTS ####
    def test_happy_path(self):
        self.__login()
        self.__select_the_futur_competition()
        self.__choose_number_of_places_to_book("1", error=False)

    def test_sad_path(self):
        self.__login()
        self.__select_the_futur_competition()
        self.__choose_number_of_places_to_book("-2", error=True)
