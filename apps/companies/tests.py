from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from .models import User, Company
from rest_framework_simplejwt.tokens import RefreshToken

class CompanyAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpass',
            date_of_birth='2000-01-01'
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_register(self):
        url = reverse('company_register')
        data = {
            'name': 'Test Company',
            'email': 'test@example.com',
            'phone': '1234567890'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, 'Test Company')

    def test_update(self):
        company = Company.objects.create(
            name='Test Company',
            email='test@example.com',
            phone='1234567890',
            user=self.user
        )
        url = reverse('company_update')
        data = {'id': company.id, 'name': 'Updated Company'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 202)
        company.refresh_from_db()
        self.assertEqual(company.name, 'Updated Company')
