from django.test import TestCase
from categorias.models import Categoria
from django.core.exceptions import ValidationError

class CategoriaModelTests(TestCase):

    def test_creacion_categoria_valida(self):
        categoria = Categoria.objects.create(nombre_categoria="Electrónica")
        self.assertEqual(categoria.nombre_categoria, "Electrónica")
        self.assertEqual(str(categoria), "Electrónica")
        self.assertEqual(Categoria.objects.count(), 1)

    def test_str_method(self):
        categoria = Categoria(nombre_categoria="Ropa")
        self.assertEqual(str(categoria), "Ropa")

    def test_nombre_categoria_longitud_maxima(self):
        nombre_largo = "X" * 30  
        categoria = Categoria(nombre_categoria=nombre_largo)
        categoria.full_clean()  
        categoria.save()
        self.assertEqual(categoria.nombre_categoria, nombre_largo)

    def test_nombre_categoria_longitud_excedida(self):
        nombre_largo = "X" * 31 
        categoria = Categoria(nombre_categoria=nombre_largo)
        with self.assertRaises(ValidationError):
            categoria.full_clean()  