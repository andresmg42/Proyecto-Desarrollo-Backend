from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import  routers

router=routers.DefaultRouter()

router.register(r'usuarios',views.UsuarioView, 'usuarios')


urlpatterns = [

    path("api/",include(router.urls)),
    
  
    path('login/',views.login, name='login'),
    path('verify_email/',views.verify_email, name='verify_email'),
    path('register_user/',views.register_user, name='register_user'),
    
    
   
   
    
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)