from selenium.webdriver import Chrome
import pytest
import time


@pytest.mark.points_updated
class TestWithSelenium:
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
        links = self.browser.find_elements_by_tag_name("a")
        for l in links:
            if l.text == "Book Places":
                time.sleep(2)
                l.click()
                break

    def __choose_number_of_places_to_book(self, number_of_places):
        places = self.browser.find_element_by_name("places")
        places.send_keys(number_of_places)
        time.sleep(2)
        validate = self.browser.find_element_by_tag_name("button")
        validate.click()
        time.sleep(3)
        logout = self.browser.find_element_by_tag_name("a")
        logout.click()
        self.browser.close()

    def test_happy_path(self):
        self.__login()
        self.__select_the_first_competition()
        self.__choose_number_of_places_to_book("1")

    def test_sad_path(self):
        self.__login()
        self.__select_the_first_competition()
        self.__choose_number_of_places_to_book("-2")

