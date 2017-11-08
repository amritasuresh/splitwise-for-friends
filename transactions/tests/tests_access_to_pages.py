from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from accounts.models import Account
from accounts.views import home
from transactions.models import Transaction


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
    This class tests that the current user can access the transaction pages.
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

    def test_access_to_transactions_page(self):
        """
        This function tests that the user can view the page that lists all of their transactions.
        :return:
        """
        request = self.factory.get('/transactions')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_pending_page(self):
        """
        This function tests that the user can view the page that lists all of their pending transactions.
        :return:
        """
        request = self.factory.get('/transactions/pending')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_completed_page(self):
        """
        This function tests that the user can view the page that lists all of their completed transactions.
        :return:
        """
        request = self.factory.get('/transactions/completed')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_resolution_page(self):
        """
        This function tests that the user can view the page that lists all of the proposed balance resolutions.
        :return:
        """
        request = self.factory.get('/transactions/resolution')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_transactions(self):
        """
        This function tests that the user can view all of the transactions in the application.
        :return:
        """
        ts = Transaction.objects.all()
        for t in ts:
            request = self.factory.get('/transactions/' + str(t.id) + '/')
            request.user = self.user
            response = home(request)
            self.assertEqual(response.status_code, 200)