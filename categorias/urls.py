from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import  routers
from rest_framework.documentation import include_docs_urls

router=routers.DefaultRouter()


router.register(r'categorias', views.CategoriaView,'categorias')


urlpatterns = [

    path("api/",include(router.urls)),
    #path("/categorias/docs/",include_docs_urls(title="API categorias")),

    
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)