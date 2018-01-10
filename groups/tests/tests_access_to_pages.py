from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from accounts.models import Account
from accounts.views import home

from events.models import Event


def create_user(username, email, password):
    """
    This function creates a new user for the application based on the provided information.
    :param username: The user's username
    :param email: The user's email address
    :param password: The user's password
    :return:
    """
    user = User.objects.create_user(
        username=username, email=email, password=password)
    Account.objects.create(user=user)


class AccessToPagesTest(TestCase):
    """
    This class tests that the current user can access the group pages.
    """
    def setUp(self):
        """
        This function sets up a user for testing.
        :return:
        """
        self.factory = RequestFactory()

        self.mocked_username = 'xyz'
        self.mocked_email = 'email@email.com'
        self.mocked_password = 'abcd1234'

        create_user(self.mocked_username, self.mocked_email,
                    self.mocked_password)

        self.user = User.objects.get(username='xyz')

    def test_access_to_group_page(self):
        """
        This function tests that the user can view the page that lists their current groups.
        :return:
        """
        request = self.factory.get('/groups')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_groups(self):
        """
        This function tests that the user can access all pages of their current groups.
        :return:
        """
        groups = self.user.groups.all()
        for g in groups:
            request = self.factory.get('/groups/' + str(g.id) + '/')
            response = home(request)
            self.assertEqual(response.status_cdo)

    def test_access_to_events(self):
        """
        This function tests that the user can access all pages of the events in each of their groups.
        :return:
        """
        groups = self.user.groups.all()
        for g in groups:
            events = Event.objects.filter(group_id=g.id)
            for e in events:
                request = self.factory.get('/groups/' + str(g.id) + '/events/' + str(e.id) + '/')
                response = home(request)
                self.assertEqual(response.status_cdo)