from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from accounts.models import Account


class UserLoginTestCase(LiveServerTestCase):
    """
    This class tests that the user is able to log in to the application.
    """
    def setUp(self):
        """
        This function sets up the Account object for a mock login.
        :return:
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.selenium = webdriver.Chrome(chrome_options=chrome_options)

        self.mocked_username = 'myuser'
        self.mocked_email = 'myemail@gmail.com'
        self.mocked_password = 'top_secret'

        self.mocked_user = User.objects.create_user(
            username=self.mocked_username,
            email=self.mocked_email, password=self.mocked_password)

        self.mocked_user.save()
        Account.objects.create(user=self.mocked_user)
        super(UserLoginTestCase, self).setUp()

    def tearDown(self):
        """
        This function ends the browser session.
        :return:
        """
        self.selenium.quit()
        super(UserLoginTestCase, self).tearDown()

    def selenium_login(self, username, password):
        """
        This function logs in to the application.
        :param username: The user's username
        :param password: The user's password
        :return:
        """
        self.assertEqual(self.selenium.title, 'Login Page')
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(password)
        self.selenium.find_element_by_name("login").click()

    def test_correct_login(self):
        """
        This function tests that the user can log in to the application with the correct username and password.
        :return:
        """
        self.selenium.get(self.live_server_url)
        self.selenium_login(self.mocked_username, self.mocked_password)
        self.assertNotEquals(self.selenium.title, 'Login Page')

    def test_incorrect_login(self):
        """
        This function verifies that the user cannot log in to the application with an incorrect password.
        :return:
        """
        print(self.mocked_user.password)
        self.selenium.get(self.live_server_url)
        self.selenium_login(self.mocked_username, self.mocked_password + '123')
        self.assertEquals(self.selenium.title, 'Login Page')
