from django.contrib import admin
from .models import Categoria

class CategoriasAdmin(admin.ModelAdmin):
    list_display = ("nombre_categoria",)
    search_fields = ("nombre_categoria",)

admin.site.register(Categoria, CategoriasAdmin)
