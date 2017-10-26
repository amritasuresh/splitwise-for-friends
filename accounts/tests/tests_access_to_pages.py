from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from accounts.models import Account
from accounts.views import home


class AccessToPagesTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='xyz', email='myemail@gmail.com', password='top_secret')
        Account.objects.create(user=self.user)


    def test_access_to_home_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_register_page(self):
        request = self.factory.get('/register')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_login_page(self):
        request = self.factory.get('/login')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_to_forget_password_page(self):
        request = self.factory.get('/forgotpassword')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)


