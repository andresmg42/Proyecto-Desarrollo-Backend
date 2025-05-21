from django.db import models

class Categoria(models.Model):
    
    nombre_categoria=models.CharField(max_length=30, verbose_name="Nombre de la categoría")
    class Meta:
        verbose_name='categoria'
        verbose_name_plural='categorias'
    

    def __str__(self):
        return self.nombre_categoria
