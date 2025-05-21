from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto


class Pedido(models.Model):
    
    usuarios = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cliente_pid', verbose_name="Id del usuario")
    metodo_pago=models.CharField(max_length=30, verbose_name="Método de pago")
    direccion=models.CharField(max_length=30, verbose_name="direccion" ,default='sin Direccion')
    productos=models.ManyToManyField(Producto,through='PedidoProducto')
    hora=models.TimeField(auto_now_add=True)
    estado_pedido=models.BooleanField(verbose_name="Envíado")
    fecha =models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name='pedido'
        verbose_name_plural='pedidos'
       
    
    
    
class PedidoProducto(models.Model):
    pedido_ppid = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto_ppid = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto_carrito=models.IntegerField()
    
    class Meta:
        unique_together=('pedido_ppid','producto_ppid')
        constraints=[
            models.UniqueConstraint(
                fields=['pedido_ppid','producto_ppid'],
                name='unique_pedido_producto'
            )
        ]