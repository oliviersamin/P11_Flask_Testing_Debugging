from selenium.webdriver import Chrome
import pytest
import time


@pytest.mark.functional_tests
@pytest.mark.login_error
class TestWithSelenium:
    """ This test checks the happy path and the sad path of the login process. Here are the steps:
     Step 1: Happy path = Enter a valid email in the login page
     Step 2: Check that the welcome message contains the corresponding email
     Step 3: Sad path = Enter a non valid email in the login page
     Step 4: Check that an error message is displayed on the page"""


    def __open_site_with_chrome(self):
        self.browser = Chrome("chromedriver")
        self.browser.get("http://127.0.0.1:5000/")
        # time.sleep(5)
        # self.browser.close()

    def test_error_login_valid_email(self):
        """ Test the Happy path"""
        # Step 1
        self.__open_site_with_chrome()
        # enter valid data to get to the welcome page
        email = self.browser.find_element_by_name("email")
        secretary_email = "john@simplylift.co"
        email.send_keys(secretary_email)
        validate = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        validate.click()
        # Step 2
        # check that we are on the right page, that the welcome message contains the email entered and the logout link
        welcome_message = self.browser.find_element_by_tag_name("h2")
        expected_welcome = 'Welcome, ' + secretary_email
        logout_link = self.browser.find_element_by_tag_name("a")
        logout_text = 'Logout'
        assert expected_welcome == welcome_message.text
        assert logout_text in logout_link.text
        time.sleep(2)
        self.browser.close()

    def test_error_login_wrong_email(self):
        """ Test the sad path """
        # Step 3
        self.__open_site_with_chrome()
        # enter wrong data to get back to the index page
        email = self.browser.find_element_by_name("email")
        secretary_email = "toto@toto.com"
        email.send_keys(secretary_email)
        validate = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        validate.click()
        # Step 4
        # check that we are on the index page, that the welcome message contains the email entered and the logout link
        welcome_message = self.browser.find_element_by_tag_name("h2")
        expected_welcome = 'This is not a valid email, please try again'
        assert expected_welcome == welcome_message.text
        time.sleep(1)
        self.browser.close()
