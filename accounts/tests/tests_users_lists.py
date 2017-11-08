from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from accounts.models import Account


def create_user(username, email, password, first_name, last_name):
    """
    This function creates a new Account object based on the provided information.
    :param username: The user's username
    :param email: The user's email address
    :param password: The user's password
    :param first_name: The user's first name
    :param last_name: The user's last name
    :return:
    """
    user = User.objects.create_user(
        username=username, email=email, password=password,
        first_name=first_name,
        last_name=last_name)
    account = Account.objects.create(user=user)
    account.save()


class UsersListTestCase(LiveServerTestCase):
    """
    This class serves as the home for functions related to displaying the list of users.
    """

    def setUp(self):
        """
        This function creates a mock user for performing actions.
        :return:
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.selenium = webdriver.Chrome(chrome_options=chrome_options)

        self.mocked_username = 'myuser'
        self.mocked_email = 'myemail@gmail.com'
        self.mocked_password = 'top_secret'
        self.mocked_first_name = "John"
        self.mocked_last_name = "K"

        create_user(
            username=self.mocked_username,
            email=self.mocked_email, password=self.mocked_password,
            first_name=self.mocked_first_name, last_name=self.mocked_last_name
        )

        self.mocked_user = User.objects.get(username=self.mocked_username)

        # set up other users too
        create_user(
            username='abc', email='myemail2@gmail.com', password='top_secret',
            first_name="AAA", last_name="BBB"
        )
        create_user(
            username='def', email='myemail3@gmail.com', password='top_secret',
            first_name="CCC", last_name="DDD"
        )
        create_user(
            username='ghi', email='myemail4@gmail.com', password='top_secret',
            first_name="EEE", last_name="FFF"
        )

        self.mocked_user_list = ["AAA BBB", "CCC DDD", "EEE FFF", "John K"]

        super(UsersListTestCase, self).setUp()

    def tearDown(self):
        """
        This function closes the web browser.
        :return:
        """
        self.selenium.quit()
        super(UsersListTestCase, self).tearDown()

    def selenium_login(self, username, password):
        """
        This function uses Selenium to log in to the application
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

    def tests_users_list_displaying(self):
        """
        This function tests that we can display all users
        :return:
        """
        # login and go to groups, then create group
        self.selenium.get(self.live_server_url)
        self.selenium_login(self.mocked_username, self.mocked_password)
        self.selenium.get('%s%s' % (self.live_server_url, '/users'))

        elems = self.selenium.find_elements_by_name("a_usernames")
        for elem in elems:
            print(elem)
        names = [elem.text for elem in elems]
        self.assertEqual(set(names), set(self.mocked_user_list))
