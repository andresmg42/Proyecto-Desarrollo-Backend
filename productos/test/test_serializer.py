from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from productos.models import Producto, ProductoUsuario, Favoritos
from productos.serializer import ProductoSerializer, UserProductoSerializer, FavoritosSerializer
from categorias.models import Categoria  # Replace with your actual app name

class SerializersTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.categoria = Categoria.objects.create(nombre_categoria='Electrónica')
        self.producto = Producto.objects.create(
            categoria=self.categoria,
            estado_producto=True,
            nombre='Laptop',
            precio=1200.00,
            descripcion='Portátil potente',
            cantidad_producto=5,
            foto_producto=None
        )
        self.producto_usuario = ProductoUsuario.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_producto=3
        )
        self.favorito = Favoritos.objects.create(
            usuario=self.user,
            producto=self.producto
        )

    def test_producto_serializer_output(self):
        serializer = ProductoSerializer(instance=self.producto)
        data = serializer.data
        self.assertEqual(data['nombre'], 'Laptop')
        self.assertEqual(data['precio'], '1200.00')
        self.assertEqual(data['estado_producto'], True)
        self.assertIn('foto_producto', data)

    def test_producto_serializer_input_valid(self):
        data = {
            'categoria': self.categoria.id,
            'estado_producto': True,
            'nombre': 'Tablet',
            'precio': '300.00',
            'descripcion': 'Buena tablet',
            'cantidad_producto': 4
        }
        serializer = ProductoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_user_producto_serializer(self):
        serializer = UserProductoSerializer(instance=self.producto_usuario)
        data = serializer.data
        self.assertEqual(data['usuario'], self.user.id)
        self.assertEqual(data['producto'], self.producto.id)
        self.assertEqual(data['cantidad_producto'], 3)

    def test_favoritos_serializer(self):
        serializer = FavoritosSerializer(instance=self.favorito)
        data = serializer.data
        self.assertEqual(data['usuario'], self.user.id)
        self.assertEqual(data['producto'], self.producto.id)
