from django.urls import resolve
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from productos.models import Producto, ProductoUsuario, Categoria  # Add Favoritos if needed
from productos import views  # Replace 'myapp' with your actual app name

# Create your tests here.

class URLRoutingAndViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Users
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.staff_user = User.objects.create_user(username='staffuser', password='testpass', is_staff=True)
        self.superuser = User.objects.create_superuser(username='admin', password='testpass')

        # Categoria (required by Producto)
        self.category = Categoria.objects.create(nombre_categoria="Electrónica")  # Add any required fields

        # Producto
        self.product = Producto.objects.create(
            nombre="Test Producto",
            precio=100.00,
            cantidad_producto=5,
            estado_producto=True,
            categoria=self.category,
            descripcion="Producto de prueba"
        )

        # ProductoUsuario
        self.user_product = ProductoUsuario.objects.create(
            producto=self.product,
            usuario=self.user,
            cantidad_producto=2,
        )

    def test_router_urls(self):
        # Productos route
        res = self.client.get('/api/productos/')
        self.assertEqual(res.status_code, 200)

        # Favoritos route
        res = self.client.get('/api/favoritos/')
        self.assertIn(res.status_code, [200, 403]) 
        
    def test_search_products_valid(self):
        res = self.client.get('/api/filter_products/', {'criteria': 'nombre', 'value': 'Test'})
        self.assertEqual(res.status_code, 200)
        self.assertTrue('products' in res.data)

    def test_search_products_missing_params(self):
        res = self.client.get('/api/filter_products/')
        self.assertEqual(res.status_code, 400)
        
    def test_search_users_products_valid(self):
        res = self.client.get('/api/search_users_products/', {'criteria': 'usuario_id', 'value': self.user.id})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(isinstance(res.data, list))

    def test_search_users_products_missing_params(self):
        res = self.client.get('/api/search_users_products/', {'criteria': 'usuario_id'})
        self.assertEqual(res.status_code, 400)

    def test_delete_all_user_products(self):
        res = self.client.delete(f'/api/delete_all_userProducts/?user_id={self.user.id}')
        self.assertEqual(res.status_code, 204)
        self.assertEqual(ProductoUsuario.objects.filter(usuario=self.user).count(), 0)

    def test_url_resolves_correctly(self):
        self.assertEqual(resolve('/api/filter_products/').func, views.search_products)
        self.assertEqual(resolve('/api/search_users_products/').func, views.search_users_products)
        self.assertEqual(resolve('/api/delete_all_userProducts/').func, views.delete_all_user_products)