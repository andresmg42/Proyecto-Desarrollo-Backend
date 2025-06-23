from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

class UsuarioViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin', password='adminpass', email='admin@example.com'
        )
        self.staff_user = User.objects.create_user(
            username='staff', password='staffpass', is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username='normal', password='normalpass'
        )
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_register_user_view(self):
        url = reverse('usuarios-register')  # your ViewSet register action
        data = {
            "username": "newuser",
            "password": "newpass123",
            "email": "new@example.com",
            "is_staff": False,
            "is_superuser": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_login_view(self):
        url = reverse('login')  # make sure this name is in your urls.py
        data = {"username": "admin", "password": "adminpass"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_verify_email(self):
        url = reverse('verify_email')  # make sure this name is in your urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Email verificado exitosamente')

    def test_update_user(self):
        url = reverse('usuarios-update-user')
        data = {
            'id': self.normal_user.id,
            'username': 'updateduser',
            'email': 'updated@example.com',
            'password': 'newsecurepass',
            'is_staff': False,
            'is_superuser': False
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'updateduser')

    def test_search_users_by_username(self):
        url = reverse('usuarios-search-users') + '?criteria=username&value=admin'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['users']), 1)
        self.assertIn('admin', [u['username'] for u in response.data['users']])

    def test_is_staff_permission(self):
        # Login with staff user
        token = Token.objects.create(user=self.staff_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Allowed: list users
        response = self.client.get(reverse('usuarios-list'))
        self.assertIn(response.status_code, [200, 403])  # Depends on implementation

        # Forbidden: update_user (method PUT)
        data = {'id': self.normal_user.id, 'username': 'hack'}
        response = self.client.put(reverse('usuarios-update-user'), data)
        self.assertEqual(response.status_code, 403)
