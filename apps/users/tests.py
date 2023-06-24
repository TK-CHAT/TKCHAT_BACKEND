from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from .models import User

class UserAPITests(APITestCase):
    def test_register(self):
        url = reverse('user_regiter')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpass',
            'password2': 'testpass',
            'date_of_birth': '2000-01-01'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_login(self):
        user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpass',
            date_of_birth='2000-01-01'
        )
        url = reverse('user_login')
        data = {'email': 'test@example.com', 'password': 'testpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 202)
        self.assertIn('access', response.data)

    def test_user_info(self):
        user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpass',
            date_of_birth='2000-01-01'
        )
        self.client.force_authenticate(user=user)
        url = reverse('user_info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data[0]['email'], 'test@example.com')
