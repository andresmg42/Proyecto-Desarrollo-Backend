from django.db import models
from categorias.models import Categoria
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

    
class Producto(models.Model):
    
    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='categoria_cid', verbose_name="Categoría")
    estado_producto=models.BooleanField(verbose_name="Disponible")
    nombre=models.CharField(max_length=30)
    precio= models.DecimalField(max_digits=10, decimal_places=2)
    descripcion=models.CharField(max_length=50, verbose_name="Descripción")
    cantidad_producto=models.IntegerField(verbose_name="Cantidad")
    foto_producto=CloudinaryField('image', blank=True, null=True)
    
    class Meta:
        verbose_name='producto'
        verbose_name_plural='productos'
        
    def __str__(self):
        return self.nombre
    
class ProductoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete= models.CASCADE)
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto=models.IntegerField()

class Favoritos(models.Model):
    usuario = models.ForeignKey(User, on_delete= models.CASCADE)
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE)
    class Meta:
        verbose_name='Favorito'
        verbose_name_plural='Favoritos'
    
    
    

    
 

