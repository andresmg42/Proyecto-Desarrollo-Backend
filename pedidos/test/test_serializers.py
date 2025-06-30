from rest_framework.test import APITestCase
from pedidos.models import Pedido, PedidoProducto
from productos.models import Producto, Categoria
from django.contrib.auth.models import User
from pedidos.serializer import PedidoSerializer, PedidoProductoSerializer
from datetime import datetime, time
from django.contrib.auth.hashers import make_password

class PedidoSerializerTest(APITestCase):
    def setUp(self):
        test_password = make_password('testpass123!')
        self.user = User.objects.create_user(username='cliente', password=test_password)
        self.pedido = Pedido.objects.create(
            usuarios=self.user,
            metodo_pago='Tarjeta',
            direccion='Calle 123',
            hora=time(14, 0, 0),
            estado_pedido=True,
            fecha=datetime.today().date()
        )

    def test_pedido_serializer_output(self):
        serializer = PedidoSerializer(self.pedido)
        data = serializer.data
        self.assertEqual(data['usuarios'], self.user.id)
        self.assertEqual(data['metodo_pago'], 'Tarjeta')
        self.assertEqual(data['direccion'], 'Calle 123')
        self.assertEqual(data['estado_pedido'], True)
        self.assertEqual(data['fecha'], self.pedido.fecha.strftime('%Y-%m-%d'))
    
    def tearDown(self):
        User.objects.all().delete()
        Pedido.objects.all().delete()
        Producto.objects.all().delete()
        Categoria.objects.all().delete()

class PedidoProductoSerializerTest(APITestCase):
    def setUp(self):
        test_password = make_password('testpass123!')
        self.user = User.objects.create_user(username='cliente', password=test_password)
        

        self.categoria = Categoria()
        self.categoria.save()
        

        self.producto = Producto.objects.create(
            categoria=self.categoria,
            estado_producto=True,
            nombre='Pizza',
            precio=20.0,
            descripcion='Pizza familiar',
            cantidad_producto=15
        )
        
        self.pedido = Pedido.objects.create(
            usuarios=self.user,
            metodo_pago='Efectivo',
            direccion='Av. Siempre Viva',
            hora=time(12, 0, 0),
            estado_pedido=False,
            fecha=datetime.today().date()
        )
        self.pedido_producto = PedidoProducto.objects.create(
            pedido_ppid=self.pedido,
            producto_ppid=self.producto,
            cantidad_producto_carrito=3
        )

    def test_pedido_producto_serializer_output(self):
        serializer = PedidoProductoSerializer(self.pedido_producto)
        data = serializer.data
        self.assertEqual(data['pedido_ppid'], self.pedido.id)
        self.assertEqual(data['producto_ppid'], self.producto.id)
        self.assertEqual(data['cantidad_producto_carrito'], 3)

    def tearDown(self):
        User.objects.all().delete()
        Pedido.objects.all().delete()
        Producto.objects.all().delete()
        Categoria.objects.all().delete()