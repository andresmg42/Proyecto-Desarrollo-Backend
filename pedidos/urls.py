from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import  routers
from rest_framework.documentation import include_docs_urls

router=routers.DefaultRouter()

router.register(r'pedidos',views.PedidoView,'pedidos')
router.register(r'pedidos_productos',views.PedidoProductoView,'pedidos_productos')

#router.register(r'llenarTablaProductosPedidos',views.llenarTablaProductosPedidos,'llenarTablaProductosPedidos')


urlpatterns = [

    path("api/",include(router.urls)),
    path("api/llenarTablaProductosPedidos",views.llenarTablaProductosPedidos, name='llenarTablaProductosPedidos'),
    path("api/productosMasVendidos",views.productosMasVendidos, name='productosMasVendidos'),
    path("api/indicadores_por_usuario",views.indicadores_por_usuario, name='ventas_totales_metodo_pago'),
    path("api/pedidos_por_estado",views.pedidos_por_estado, name='pedidos_por_estado'),
    path("api/ventas_diarias",views.ventas_diarias, name='ventas_diarias'),
    path("api/metodos_pago_mas_utilizados",views.metodos_pago_mas_utilizados, name='metodos_pago_mas_utilizados'),
    path("api/clientes_mas_frecuentes",views.clientes_mas_frecuentes, name='clientes_mas_frecuentes'),
    path("api/valor_total_ventas",views.valor_total_ventas, name='valor_total_ventas'),
    path("api/productos_mas_vendidos",views.productos_mas_vendidos, name='productos_mas_vendidos'),
    
    path("api/send_email_cancel/", views.send_email_cancel,name='send_email_cancel'),
    path("api/generar_factura/", views.generar_factura),
    #path("pedidos/docs/",include_docs_urls(title="API Pedidos")),
    

    
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)