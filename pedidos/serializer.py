from rest_framework import serializers
from .models import Pedido, PedidoProducto
from productos.models import Producto

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pedido
        fields= '__all__'

class PedidoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model=PedidoProducto
        fields= '__all__'
        

class ProductosMasVendidosSerializer(serializers.Serializer):
    total_vendidos=serializers.IntegerField()
    class Meta:
        model=Producto
        fields='__all__'
  