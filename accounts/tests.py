from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from accounts.views import home


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')

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