from django.contrib import admin
from .models import Pedido, PedidoProducto

class PedidoProductoInline(admin.TabularInline):
    model = PedidoProducto
    extra = 1

class PedidosAdmin(admin.ModelAdmin):
    list_display = (  "fecha", "mostrar_productos", "estado_pedido",)
    search_fields = ("usuarios_nombre", "mostrar_productos",)
    list_filter = ("fecha",)
    date_hierarchy = "fecha"
    inlines = [PedidoProductoInline]

    def mostrar_productos(self, obj):
        return ", ".join([producto.nombre for producto in obj.productos.all()])

    mostrar_productos.short_description = "Productos"

admin.site.register(Pedido, PedidosAdmin)