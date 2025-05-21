from rest_framework import serializers
from .models import  Producto,ProductoUsuario,Favoritos
from django.contrib.auth.models import User

      
        
        
class UserProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductoUsuario
        fields= '__all__'

class FavoritosSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favoritos
        fields= '__all__'
        


      
class ProductoSerializer(serializers.ModelSerializer):
   
    foto_producto = serializers.ImageField(required=False)
    class Meta:
        model=Producto
        fields= ['id','nombre','foto_producto','categoria','precio','descripcion','cantidad_producto','estado_producto']
        
    def get_foto_producto(self,obj):
        return obj.foto_producto.url if obj.foto_producto else None