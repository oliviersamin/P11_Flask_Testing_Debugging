from selenium.webdriver import Chrome
from P11_Flask_Testing_Debugging import server
import pytest
import time


@pytest.mark.functional_tests
@pytest.mark.new_feature
class TestWithSelenium:
    """ This test checks that every user can see a list with clubs names and their related balance points without
    need to be connected to the site. Here are the steps to do it:
    Step 1: From home page go to the new feature's page
    Step 2: From this page go back to home page
    Step 3: From this page login"""

    def __open_site_with_chrome(self):
        self.browser = Chrome("chromedriver")
        self.browser.get("http://127.0.0.1:5000/")

    def __go_to_new_feature_page(self):
        """ Step 1"""
        self.__open_site_with_chrome()
        links = self.browser.find_elements_by_tag_name("a")
        for link in links:
            if link.text == "Click here":
                time.sleep(2)
                link.click()
                break

    def __go_back_from_new_feature_page_to_home_page(self):
        """ Step 2"""
        links = self.browser.find_elements_by_tag_name("a")
        for link in links:
            if link.text == "Click here":
                time.sleep(2)
                link.click()
                break

    def __login(self):
        """ Step 3"""
        email = self.browser.find_element_by_name("email")
        secretary_email = server.clubs[0]['email']
        email.send_keys(secretary_email)
        validate = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        validate.click()

    def test_happy_path(self):
        """ Whole scenario"""
        self.__go_to_new_feature_page()
        self.__go_back_from_new_feature_page_to_home_page()
        self.__login()
        time.sleep(2)
        self.browser.close()
