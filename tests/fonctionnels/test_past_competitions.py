from selenium.webdriver import Chrome
import pytest
import time


@pytest.mark.past_competition
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
            if (l.text == "Book Places") & ("Fall" in l.get_attribute("href")):
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

