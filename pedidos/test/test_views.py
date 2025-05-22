from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from pedidos.models import Pedido, PedidoProducto
from productos.models import Producto, Categoria
from django.contrib.auth.models import User
from datetime import datetime, time
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.core import mail

class PedidoViewSetTest(APITestCase):
    def setUp(self):
        test_password = make_password('testpass123!')
        self.user = User.objects.create_user(
            username='cliente', 
            password=test_password,
            email='cliente@test.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.pedido = Pedido.objects.create(
            usuarios=self.user,
            metodo_pago='Efectivo',
            direccion='Av. Central',
            hora=time(10, 0, 0),
            estado_pedido=False,
            fecha=datetime.today().date()
        )

    def test_list_pedidos(self):
        url = reverse('pedidos-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_pedido(self):
        url = reverse('pedidos-detail', kwargs={'pk': self.pedido.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.pedido.id)

    def test_create_pedido(self):
        url = reverse('pedidos-list')
        data = {
            'usuarios': self.user.id,
            'metodo_pago': 'Tarjeta',
            'direccion': 'Nueva Dirección',
            'estado_pedido': False,
            'hora': '10:00:00',
            'fecha': datetime.today().strftime('%Y-%m-%d')
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pedido.objects.count(), 2)

    def test_update_pedido(self):
        url = reverse('pedidos-detail', kwargs={'pk': self.pedido.id})
        data = {'direccion': 'Dirección Actualizada'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.direccion, 'Dirección Actualizada')

    def test_delete_pedido(self):
        url = reverse('pedidos-detail', kwargs={'pk': self.pedido.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pedido.objects.count(), 0)


class PedidoProductoViewSetTest(APITestCase):
    def setUp(self):
        test_password = make_password('testpass123!')
        self.user = User.objects.create_user(
            username='cliente', 
            password=test_password,
            email='cliente@test.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.categoria = Categoria()
        self.categoria.save()

        self.producto = Producto.objects.create(
            categoria=self.categoria,
            estado_producto=True,
            nombre='Hamburguesa',
            precio=25.0,
            descripcion='Hamburguesa doble carne',
            cantidad_producto=20
        )

        self.pedido = Pedido.objects.create(
            usuarios=self.user,
            metodo_pago='Tarjeta',
            direccion='Calle Luna',
            hora=time(13, 0, 0),
            estado_pedido=True,
            fecha=datetime.today().date()
        )

        self.pedido_producto = PedidoProducto.objects.create(
            pedido_ppid=self.pedido,
            producto_ppid=self.producto,
            cantidad_producto_carrito=2
        )

    def test_list_pedido_productos(self):
        url = reverse('pedidos_productos-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_pedido_producto(self):
        url = reverse('pedidos_productos-detail', kwargs={'pk': self.pedido_producto.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.pedido_producto.id)

    def test_update_pedido_producto(self):
        url = reverse('pedidos_productos-detail', kwargs={'pk': self.pedido_producto.id})
        data = {'cantidad_producto_carrito': 5}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pedido_producto.refresh_from_db()
        self.assertEqual(self.pedido_producto.cantidad_producto_carrito, 5)

    def test_delete_pedido_producto(self):
        url = reverse('pedidos_productos-detail', kwargs={'pk': self.pedido_producto.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PedidoProducto.objects.count(), 0)


class FuncionesAdicionalesViewTest(APITestCase):
    def setUp(self):
        test_password = make_password('testpass123!')
        self.user = User.objects.create_user(
            username='cliente', 
            password=test_password,
            email='cliente@test.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.categoria = Categoria()
        self.categoria.save()

        self.producto = Producto.objects.create(
            categoria=self.categoria,
            estado_producto=True,
            nombre='Hamburguesa',
            precio=25.0,
            descripcion='Hamburguesa doble carne',
            cantidad_producto=20
        )

        self.pedido = Pedido.objects.create(
            usuarios=self.user,
            metodo_pago='Tarjeta',
            direccion='Calle Luna',
            hora=time(13, 0, 0),
            estado_pedido=True,
            fecha=datetime.today().date()
        )

        self.pedido_producto = PedidoProducto.objects.create(
            pedido_ppid=self.pedido,
            producto_ppid=self.producto,
            cantidad_producto_carrito=2
        )

    def test_productos_mas_vendidos(self):
        url = '/api/productosMasVendidos'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], 'Hamburguesa')

    def test_indicadores_por_usuario(self):
        url = '/api/indicadores_por_usuario'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_pedidos_por_estado(self):
        url = '/api/pedidos_por_estado'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_ventas_diarias(self):
        url = '/api/ventas_diarias'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_metodos_pago_mas_utilizados(self):
        url = '/api/metodos_pago_mas_utilizados'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_clientes_mas_frecuentes(self):
        url = '/api/clientes_mas_frecuentes'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_valor_total_ventas(self):
        url = '/api/valor_total_ventas'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_ventas'], 50.0)  # 2 * 25

    def test_send_email_cancel(self):
        url = '/api/send_email_cancel/?dest=test@example.com&mensaje=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Pedido cancelado')

    def test_generar_factura(self):
        url = f'/api/generar_factura/?pedido_id={self.pedido.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'FACTURACION ELECTRONICA')


class ErrorCasesTest(APITestCase):
    def setUp(self):
        test_password = make_password('testpass123!')
        self.user = User.objects.create_user(
            username='cliente', 
            password=test_password,
            email='cliente@test.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_llenar_tabla_productos_pedidos_invalidos(self):
        url = '/api/llenarTablaProductosPedidos'
        data = [{
            'pedido_ppid': 999,  # ID inexistente
            'producto_ppid': 999,
            'cantidad_producto_carrito': 1
        }]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_send_email_cancel_fail(self):
        url = '/api/send_email_cancel/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generar_factura_fail(self):
        url = '/api/generar_factura/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)