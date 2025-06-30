from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from categorias.models import Categoria

class CategoriaViewSetTests(APITestCase):

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre_categoria="Tecnología")
        self.base_url = '/api/categorias/'

    def test_listar_categorias(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_crear_categoria_valida(self):
        data = {'nombre_categoria': 'Juguetes'}
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categoria.objects.last().nombre_categoria, 'Juguetes')

    def test_crear_categoria_nombre_vacio(self):
        data = {'nombre_categoria': ''}
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nombre_categoria', response.data)

    def test_crear_categoria_nombre_largo(self):
        data = {'nombre_categoria': 'X' * 31}
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nombre_categoria', response.data)

    def test_obtener_categoria(self):
        url = f"{self.base_url}{self.categoria.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre_categoria'], self.categoria.nombre_categoria)

    def test_actualizar_categoria(self):
        url = f"{self.base_url}{self.categoria.id}/"
        data = {'nombre_categoria': 'Electrodomésticos'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre_categoria'], 'Electrodomésticos')

    def test_eliminar_categoria(self):
        url = f"{self.base_url}{self.categoria.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Categoria.objects.filter(id=self.categoria.id).exists())