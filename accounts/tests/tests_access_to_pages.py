from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from accounts.models import Account
from accounts.views import home


class AccessToPagesTest(TestCase):
    """
    This class tests that the user has access to all web pages relating to the login process.
    """
    def setUp(self):
        """
        This function creates a mock user for testing.
        :return:
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='xyz', email='myemail@gmail.com', password='top_secret')
        Account.objects.create(user=self.user)

    def test_access_to_home_page(self):
        """
        This test checks that the user can access the home page.
        :return: Asserts that the HTTP response was successful.
        """
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_register_page(self):
        """
        This test checks that the user can access the registration page.
        :return: Asserts that the HTTP response was successful.
        """
        request = self.factory.get('/register')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_login_page(self):
        """
        This test checks that the user can access the login page.
        :return: Asserts that the HTTP response was successful.
        """
        request = self.factory.get('/login')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_forget_password_page(self):
        """
        This test checks that the user can access the forgotten password page.
        :return: Asserts that the HTTP response was successful.
        """
        request = self.factory.get('/forgotpassword')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)
