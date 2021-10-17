from selenium.webdriver import Chrome
import pytest
import time


@pytest.mark.max_12_places
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

    def __select_future_competition(self):
        links = self.browser.find_elements_by_tag_name("a")
        for l in links:
            if (l.text == "Book Places") & ("Fall" in l.get_attribute("href")):
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


    def test_happy_path(self):
        self.__login()
        self.__select_future_competition()
        self.__happy_booking_places()

    def test_sad_path(self):
        self.__login()
        self.__select_future_competition()
        self.__sad_booking_places()


