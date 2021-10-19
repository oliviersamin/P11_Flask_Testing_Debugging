from selenium.webdriver import Chrome
import pytest
import time



@pytest.mark.points_updated
class TestWithSelenium:

    def __get_points_from_string(self, string):
        string = string[::-1]
        string = string[:string.find(':')]
        string = int(string[::-1])
        return string

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

    def __select_the_first_competition(self):
        # print(self.browser.find_element_by_tag_name("body").text, flush=True)
        self.initial_points = self.browser.find_element_by_tag_name("div").text
        print('self.initial_points = ', self.initial_points, flush=True)
        self.initial_points = self.__get_points_from_string(self.initial_points)
        links = self.browser.find_elements_by_tag_name("a")
        for l in links:
            if l.text == "Book Places":
                time.sleep(2)
                l.click()
                break

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
            self.final_points = self.__get_points_from_string(self.final_points)
            body = self.browser.find_element_by_tag_name("body")
            assert booking_message in body.text
            assert self.final_points == (self.initial_points - int(number_of_places))
        else:  # SAD PATH
            error_message = 'ERROR: The number of places booked is not a positive integer'
            body = self.browser.find_element_by_tag_name("body")
            assert error_message in body.text

        self.browser.close()

    def test_happy_path(self):
        self.__login()
        self.__select_the_first_competition()
        self.__choose_number_of_places_to_book("1", error=False)

    def test_sad_path(self):
        self.__login()
        self.__select_the_first_competition()
        self.__choose_number_of_places_to_book("-2", error=True)
