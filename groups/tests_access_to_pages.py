from django.contrib.auth.models import User, Group
from django.test import TestCase, RequestFactory

from accounts.models import Account
from groups.models import UserGroup
from accounts.views import home


def create_user(username, email, password):
    user = User.objects.create_user(
        username=username, email=email, password=password)
    Account.objects.create(user=user)


class AccessToPagesTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.mocked_username = 'xyz'
        self.mocked_email = 'email@email.com'
        self.mocked_password = 'abcd1234'

        create_user(self.mocked_username, self.mocked_email,
                    self.mocked_password)

        self.user = User.objects.get(username='xyz')

    def test_access_to_groups(self):
        request = self.factory.get('/groups')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)
