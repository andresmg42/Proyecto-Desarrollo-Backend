from django.test import TestCase
from django.contrib.auth.models import User
from productos.models import Producto, ProductoUsuario, Favoritos
from categorias.models import Categoria  
from cloudinary.models import CloudinaryField

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.categoria = Categoria.objects.create(nombre_categoria='Electrónica')  # assuming Categoria has a 'nombre' field
        self.producto = Producto.objects.create(
            categoria=self.categoria,
            estado_producto=True,
            nombre='Smartphone',
            precio=599.99,
            descripcion='Último modelo',
            cantidad_producto=10,
            foto_producto=None
        )

    def test_producto_creation(self):
        self.assertEqual(self.producto.nombre, 'Smartphone')
        self.assertEqual(self.producto.precio, 599.99)
        self.assertTrue(self.producto.estado_producto)
        self.assertEqual(str(self.producto), 'Smartphone')

    def test_producto_usuario_creation(self):
        prod_user = ProductoUsuario.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_producto=2
        )
        self.assertEqual(prod_user.usuario.username, 'testuser')
        self.assertEqual(prod_user.cantidad_producto, 2)

    def test_favoritos_creation(self):
        favorito = Favoritos.objects.create(
            usuario=self.user,
            producto=self.producto
        )
        self.assertEqual(favorito.usuario, self.user)
        self.assertEqual(favorito.producto, self.producto)