from rest_framework import viewsets
from .serializer import  CategoriaSerializer
from .models import Categoria


class CategoriaView(viewsets.ModelViewSet):
    serializer_class=CategoriaSerializer
    queryset=Categoria.objects.all()