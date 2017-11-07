from django.contrib.auth.models import User, Group
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from accounts.models import Account


def create_user(username, email, password):
    user = User.objects.create_user(
        username=username, email=email, password=password)
    Account.objects.create(user=user)


# TODO 1. Adding users to groups
# TODO 2. Adding transactions to groups
# TODO 3. Groups with the same name

class GroupCreatingTestCase(LiveServerTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.selenium = webdriver.Chrome(chrome_options=chrome_options)

        self.mocked_username = 'myuser'
        self.mocked_email = 'myemail@gmail.com'
        self.mocked_password = 'top_secret'

        create_user(
            username=self.mocked_username,
            email=self.mocked_email, password=self.mocked_password)

        self.mocked_user = User.objects.get(username=self.mocked_username)
        super(GroupCreatingTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(GroupCreatingTestCase, self).tearDown()

    def selenium_login(self, username, password):
        self.assertEqual(self.selenium.title, 'Login Page')
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(password)
        self.selenium.find_element_by_name("login").click()

    def selenium_create_group(self, group_name):
        # click create group button
        self.selenium.find_element_by_name("create_group_button").click()
        self.assertEqual(self.selenium.title, 'Create Group form')
        # filling the form and creating a group of the name "Example group"
        group_name_input = self.selenium.find_element_by_name("group_name")
        group_name_input.send_keys(group_name)
        self.selenium.find_element_by_name("save_button").click()

    def test_add_new_group(self):
        # login
        self.selenium.get(self.live_server_url)
        self.selenium_login(self.mocked_username, self.mocked_password)
        self.assertEqual(self.selenium.title, 'Dashboard')
        # go to groups
        self.selenium.get('%s%s' % (self.live_server_url, '/groups'))
        self.assertEqual(self.selenium.title, 'Groups')
        # calculate total number of groups
        total_number_of_groups = self.mocked_user.groups.count()
        # creating group
        self.selenium_create_group("Example group")
        # checking if the total_number_of_groups is ok
        current_number_of_groups = self.mocked_user.groups.count()
        self.assertEqual(current_number_of_groups, total_number_of_groups + 1)
