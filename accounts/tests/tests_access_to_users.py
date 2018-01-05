from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from accounts.models import Account
from accounts.views import home


class AccessToUsersTest(TestCase):
    """
    This class contains tests to make sure that the user has access to the parts of the application concerning users.
    """
    def setUp(self):
        """
        This function creates a mock user for testing, as well as other users to test user page access.
        :return:
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='xyz', email='myemail@gmail.com', password='top_secret')
        Account.objects.create(user=self.user)

        # set up other users too
        user2 = User.objects.create_user(
            username='abc', email='myemail2@gmail.com', password='top_secret'
        )
        user3 = User.objects.create_user(
            username='def', email='myemail3@gmail.com', password='top_secret'
        )
        user4 = User.objects.create_user(
            username='ghi', email='myemail4@gmail.com', password='top_secret'
        )
        Account.objects.create(user=user2)
        Account.objects.create(user=user3)
        Account.objects.create(user=user4)

    def test_access_to_users_page(self):
        """
        This test checks that the user can access the page with the list of all users.
        :return:
        """
        request = self.factory.get('/users/')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_user_pages(self):
        """
        This test checks that the user can access the profile pages of all users.
        :return:
        """
        accounts = Account.objects.all()
        for a in accounts:
            request = self.factory.get('/users/' + str(a.user_id) + '/')
            request.user = self.user
            response = home(request)
            self.assertEqual(response.status_code, 200)

    def test_access_to_profile_page(self):
        """
        This test checks that the user can access their own profile page.
        :return:
        """
        request = self.factory.get('/profile/')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_friends_page(self):
        """
        This test checks that the user can access their list of friends.
        :return:
        """
        request = self.factory.get('/users/friends/')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)