from selenium.webdriver import Chrome
from P11_Flask_Testing_Debugging import server
import pytest
import time


@pytest.mark.no_more_than_club_points
class TestWithSelenium:

    def __open_site_with_Chrome(self):
        self.browser = Chrome("chromedriver")
        self.browser.get("http://127.0.0.1:5000/")

    def __login(self, mocker):
        mocker.patch.object(server, 'clubs', [{"name": "Simply Lift",
                                               "email": "john@simplylift.co", "points": "3"}])
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
        places.send_keys("1")
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
        places.send_keys("10")
        time.sleep(2)
        validate = self.browser.find_element_by_tag_name("button")
        validate.click()
        time.sleep(2)
        booking_message = "ERROR: You cannot book more places than your total club's points"
        body = self.browser.find_element_by_tag_name("body")
        assert booking_message in body.text
        self.browser.close()


    def test_happy_path(self, mocker):
        self.__login(mocker)
        self.__select_future_competition()
        self.__happy_booking_places()

    def test_sad_path(self, mocker):
        self.__login(mocker)
        self.__select_future_competition()
        self.__sad_booking_places()


