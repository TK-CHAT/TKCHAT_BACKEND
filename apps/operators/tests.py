
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from .models import User, Company, Operator
from rest_framework_simplejwt.tokens import RefreshToken

class OperatorAPITests(APITestCase):
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
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.company = Company.objects.create(
            name='Test Company',
            email='test@example.com',
            phone='1234567890',
            user=self.user
        )

    def test_register(self):
        url = reverse('operator_register')
        data = {
            'first_name': 'Test',
            'last_name': 'Operator',
            'email': 'operator@example.com',
            'password': 'testpass',
            'phone': '233345674',
            'date_of_birth': '2000-01-01',
            'work_company': self.company.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Operator.objects.count(), 1)
        self.assertEqual(Operator.objects.get().email, 'operator@example.com')

    def test_update(self):
        operator = Operator.objects.create(
            first_name='Test',
            last_name='Operator',
            email='operator@example.com',
            password='testpass',
            date_of_birth='2000-01-01',
            work_company=self.company,
        )
        url = reverse('operator_update')
        data = {
          'id': operator.id, 
          'first_name': 'Updated',
          'work_company': self.company.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        operator.refresh_from_db()
        self.assertEqual(operator.first_name, 'Updated')
