from django.contrib.auth.models import User, Group
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import uuid

from accounts.models import Account
from events.models import Event


def create_user(username, email, password):
    """
    This function creates a new Account object based on the provided information.
    :param username: The user's username
    :param email: The user's email address
    :param password: The user's password
    :return:
    """
    user = User.objects.create_user(
        username=username, email=email, password=password)
    Account.objects.create(user=user)


# TODO 2. Adding transactions to groups
# TODO 3. Groups with the same name

class GroupCreatingTestCase(LiveServerTestCase):
    """
    This class serves as the home for functions related to testing the creation of groups.
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

        create_user(
            username=self.mocked_username,
            email=self.mocked_email, password=self.mocked_password)

        self.mocked_user = User.objects.get(username=self.mocked_username)
        super(GroupCreatingTestCase, self).setUp()

    def tearDown(self):
        """
        This function closes the web browser.
        :return:
        """
        self.selenium.quit()
        super(GroupCreatingTestCase, self).tearDown()

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

    def selenium_create_group(self, group_name):
        """
        This function uses Selenium to create a new group.
        :param group_name: The name of the new group to be created
        :return:
        """
        # click create group button
        self.selenium.find_element_by_name("create_group_button").click()
        # filling the form and creating a group of the name "Example group"
        group_name_input = self.selenium.find_element_by_name("group_name")
        group_name_input.send_keys(group_name)
        self.selenium.find_element_by_name("save_button").click()

    def test_add_new_group(self):
        """
        This function tests that the current user can create a new group.
        :return:
        """
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

    def tests_groups_displaying(self):
        """
        This function tests that we can display all groups
        :return:
        """
        # login and go to groups, then create group
        self.selenium.get(self.live_server_url)
        self.selenium_login(self.mocked_username, self.mocked_password)
        self.selenium.get('%s%s' % (self.live_server_url, '/groups'))

        # adding example groups
        group_names = ["Group1", "Group2", "Group3"]
        for group_name in group_names:
            self.selenium_create_group(group_name)

        # complecting group names and checking if they are equal
        elems = self.selenium.find_elements_by_name("group_access_link")
        names = [elem.text for elem in elems]
        self.assertEqual(set(names), set(group_names))

    def selenium_add_user_to_group(self, username):
            """
            This function uses Selenium to add user to group.
            :return:
            """
            #self.selenium.find_element_by_name("add-user-to-group").click()
            #self.assertEqual(self.selenium.title, 'Add user to group form')
            # filling the form and creating a user with the name "Example group"
            select_username = Select(self.selenium.find_element_by_name("username"))
            select_username.select_by_visible_text(username)
            self.selenium.find_element_by_name("save-button").click()

    def selenium_add_transactions(self, transaction, payer, details, eventname):
        """
        This function uses Selenium to add transaction within the group
        :return:
        """
        #filling in the form with required information
        self.selenium.find_element_by_name("add-transaction").click()
        select_payer = Select(self.selenium.find_element_by_name("payer"))
        select_payer.select_by_visible_text(payer)
        select_event = Select(self.selenium.find_element_by_name("event"))
        select_event.select_by_visible_text(eventname)
        group_transaction = self.selenium.find_element_by_name("transaction")
        group_transaction.send_keys(transaction)
        group_details = self.selenium.find_element_by_name("details")
        group_details.send_keys(details)
        self.selenium.find_element_by_name("save_button_transaction").click()


    def tests_adding_users(self):
        """
        This function tests that we can add users to groups
        :return:
        """
        #create mock users
        create_user(username='testuser', email='test+test@gmail.com', password='password123')
        create_user(username='testuser2', email='test+test@gmail.com', password='password123')
        #login and go to groups, then create a group
        self.selenium.get(self.live_server_url)
        self.selenium_login(self.mocked_username, self.mocked_password)
        self.selenium.get('%s%s' % (self.live_server_url, '/groups'))
        self.selenium_create_group("TestGroup")

        #go into the group and add users
        self.selenium.find_element_by_name("group_access_link").click()
        user_names = ["testuser", "testuser2"]
        for user_name in user_names:
            self.selenium.find_element_by_name("add-user").click()
            self.selenium_add_user_to_group(user_name)

        #check if they are successfully added and makes sure the number of members are the same
        self.selenium.find_element_by_name("group_members").click()
        elems = self.selenium.find_elements_by_name("group-members")
        for elem in elems:
            print(elem)
        self.assertEqual(set(elems).__len__(), set(user_names).__len__()+1)

    def selenium_add_event_to_group(self, event):
        """
        This function uses Selenium to add events within the group
        :return:
        """
        self.selenium.find_element_by_name("add-event").click()
        event_name = self.selenium.find_element_by_name("event_name")
        event_name.send_keys(event)
        self.selenium.find_element_by_name("save_button_event").click()


    def test_adding_events(self):
        """
                This functions tests if we can add events to groups
                :return:
                """
        # create mock users
        create_user(username='testuser', email='test+test@gmail.com', password='password123')
        create_user(username='testuser2', email='test+test@gmail.com', password='password123')
        # login and go to groups, then create a group
        self.selenium.get(self.live_server_url)
        self.selenium_login(self.mocked_username, self.mocked_password)
        self.selenium.get('%s%s' % (self.live_server_url, '/groups'))
        self.selenium_create_group("TestGroup")

        # go into the group and add users
        self.selenium.find_element_by_name("group_access_link").click()
        user_names = ["testuser", "testuser2"]
        for user_name in user_names:
            self.selenium.find_element_by_name("add-user").click()
            self.selenium_add_user_to_group(user_name)
        event_name="default"
        self.selenium_add_event_to_group(event_name)
        self.selenium.find_element_by_name("events-list").click()
        elems = self.selenium.find_elements_by_name("event_elt")
        for elem in elems:
            print(elem)
            self.assertEqual(elem.text, event_name)
        self.assertEqual(set(elems).__len__(), 1)



    def test_adding_transactions(self):
        """
        This functions tests if we can add transactions to groups
        :return:
        """
        # create mock users
        create_user(username='testuser', email='test+test@gmail.com', password='password123')
        create_user(username='testuser2', email='test+test@gmail.com', password='password123')
        # login and go to groups, then create a group
        self.selenium.get(self.live_server_url)
        self.selenium_login(self.mocked_username, self.mocked_password)
        self.selenium.get('%s%s' % (self.live_server_url, '/groups'))
        self.selenium_create_group("TestGroup")

        # go into the group and add users
        self.selenium.find_element_by_name("group_access_link").click()
        user_names = ["testuser", "testuser2"]
        for user_name in user_names:
            self.selenium.find_element_by_name("add-user").click()
            self.selenium_add_user_to_group(user_name)

        #add default event
        self.selenium_add_event_to_group("default")

        #add transactions
        self.selenium_add_transactions("30", "testuser", "lunch", "default")
        self.selenium_add_transactions("30", "testuser", "dinner", "default")

        #check in resolutions
        #self.selenium.find_element_by_name("transaction-lists").click()
        elems = self.selenium.find_elements_by_name("transaction-name")
        for elem in elems:
            print(elem)
            self.assertIn(elem.text, {"lunch", "dinner"})
            #self.assertEqual(elem.text, "lunch")
        self.assertEqual(set(elems).__len__(), 4)

    def test_resolution_opt_transaction(self):
        """
        This is the test for the resolution by optimising users
        :return:
        """
        # create mock users
        create_user(username='testuser', email='test+test@gmail.com', password='password123')
        create_user(username='testuser2', email='test+test@gmail.com', password='password123')
        # login and go to groups, then create a group
        self.selenium.get(self.live_server_url)
        self.selenium_login(self.mocked_username, self.mocked_password)
        self.selenium.get('%s%s' % (self.live_server_url, '/groups'))
        self.selenium_create_group("TestGroup")

        # go into the group and add users
        self.selenium.find_element_by_name("group_access_link").click()
        user_names = ["testuser", "testuser2"]
        for user_name in user_names:
            self.selenium.find_element_by_name("add-user").click()
            self.selenium_add_user_to_group(user_name)

        # add default event
        self.selenium_add_event_to_group("default")

        # add transactions
        self.selenium_add_transactions("30", "testuser", "lunch", "default")
        self.selenium_add_transactions("15", "testuser2", "dinner", "default")

        #checking that all transactions were successfully added
        elems = self.selenium.find_elements_by_name("transaction-name")
        for elem in elems:
            print(elem)
        self.assertEqual(set(elems).__len__(), 4)

        #resolve by optimising transactions
        self.selenium.find_element_by_name("resolve-all").click()
        self.selenium.find_element_by_id("tran").click()
        self.selenium.find_element_by_name("save_button_resolve").click()

        #checking that new transactions are added
        elems = self.selenium.find_elements_by_name("transaction-name")
        self.assertEqual(set(elems).__len__(), 5)

        #checking that they are right

        payers = self.selenium.find_elements_by_name("payer-name")
        payees = self.selenium.find_elements_by_name("payee-name")
        statuses = self.selenium.find_elements_by_name("status")
        amount = self.selenium.find_elements_by_name("amount")
        count_pending=0
        count_completed=0

        for status in statuses:
            if status.text == 'Pending':
                count_pending += 1
            else:
                count_completed += 1

        #total number of pending transactions is 1
        self.assertEqual(count_completed, 4)
        self.assertEqual(count_pending, 1)

        #only resolution transactions are marked pending
        for i in range(5):
            if(statuses[i].text=='Pending'):
                self.assertEqual(elems[i].text, 'resolution')


    def test_resolution_opt_user(self):
        """
        This is the test for the resolution by optimising users
        :return:
        """
        # create mock users
        create_user(username='testuser', email='test+test@gmail.com', password='password123')
        create_user(username='testuser2', email='test+test@gmail.com', password='password123')
        # login and go to groups, then create a group
        self.selenium.get(self.live_server_url)
        self.selenium_login(self.mocked_username, self.mocked_password)
        self.selenium.get('%s%s' % (self.live_server_url, '/groups'))
        self.selenium_create_group("TestGroup")

        # go into the group and add users
        self.selenium.find_element_by_name("group_access_link").click()
        user_names = ["testuser", "testuser2"]
        for user_name in user_names:
            self.selenium.find_element_by_name("add-user").click()
            self.selenium_add_user_to_group(user_name)

        # add default event
        self.selenium_add_event_to_group("default")

        # add transactions
        self.selenium_add_transactions("30", "testuser", "lunch", "default")
        self.selenium_add_transactions("15", "testuser2", "dinner", "default")

        #checking that all transactions were successfully added
        elems = self.selenium.find_elements_by_name("transaction-name")
        for elem in elems:
            print(elem)
        self.assertEqual(set(elems).__len__(), 4)

        #resolve by optimising transactions
        self.selenium.find_element_by_name("resolve-all").click()
        self.selenium.find_element_by_id("user").click()
        self.selenium.find_element_by_name("save_button_resolve").click()

        #checking that new transactions are added
        elems = self.selenium.find_elements_by_name("transaction-name")
        self.assertEqual(set(elems).__len__(), 6)

        #checking that they are right

        payers = self.selenium.find_elements_by_name("payer-name")
        payees = self.selenium.find_elements_by_name("payee-name")
        statuses = self.selenium.find_elements_by_name("status")
        amount = self.selenium.find_elements_by_name("amount")
        count_pending=0
        count_completed=0

        for status in statuses:
            if status.text == 'Pending':
                count_pending += 1
            else:
                count_completed += 1

        #total number of pending transactions is 1
        self.assertEqual(count_completed, 4)
        self.assertEqual(count_pending, 2)

        #only resolution transactions are marked pending
        for i in range(5):
            if(statuses[i].text=='Pending'):
                self.assertEqual(elems[i].text, 'resolution')








