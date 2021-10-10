from selenium.webdriver import Chrome
import pytest
import time


@pytest.mark.login_error
class TestWithSelenium:
    def __open_site_with_Chrome(self):
        self.browser = Chrome("chromedriver")
        self.browser.get("http://127.0.0.1:5000/")
        # time.sleep(5)
        # self.browser.close()

    def test_error_login_valid_email(self):
        self.__open_site_with_Chrome()
        # enter valid data to get to the welcome page
        email = self.browser.find_element_by_name("email")
        secretary_email = "john@simplylift.co"
        email.send_keys(secretary_email)
        validate = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        validate.click()
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
        self.__open_site_with_Chrome()
        # enter wrong data to get back to the index page
        email = self.browser.find_element_by_name("email")
        secretary_email = "toto@toto.com"
        email.send_keys(secretary_email)
        validate = self.browser.find_element_by_tag_name("button")
        time.sleep(2)
        validate.click()
        # check that we are on the index page, that the welcome message contains the email entered and the logout link
        welcome_message = self.browser.find_element_by_tag_name("h2")
        expected_welcome = 'This is not a valid email, please try again'
        assert expected_welcome == welcome_message.text
        time.sleep(1)
        self.browser.close()
