from django.test import TestCase
from categorias.models import Categoria
from categorias.serializer import CategoriaSerializer
from rest_framework.exceptions import ValidationError

class CategoriaSerializerTests(TestCase):

    def test_serializar_categoria_valida(self):
        categoria = Categoria.objects.create(nombre_categoria="Deportes")
        serializer = CategoriaSerializer(categoria)
        self.assertEqual(serializer.data['nombre_categoria'], "Deportes")

    def test_deserializar_datos_validos(self):
        data = {'nombre_categoria': "Hogar"}
        serializer = CategoriaSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        categoria = serializer.save()
        self.assertEqual(categoria.nombre_categoria, "Hogar")

    def test_deserializar_nombre_categoria_vacio(self):
        data = {'nombre_categoria': ""}
        serializer = CategoriaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nombre_categoria', serializer.errors)

    def test_deserializar_nombre_categoria_demasiado_largo(self):
        data = {'nombre_categoria': 'X' * 31}  
        serializer = CategoriaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nombre_categoria', serializer.errors)