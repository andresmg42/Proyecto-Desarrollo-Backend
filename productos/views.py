from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ProductoSerializer,UserProductoSerializer,FavoritosSerializer
from .models import  Producto,ProductoUsuario,Favoritos
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication


        
class IsStaffOrSuperuserWriteOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

class ProductosUsuariosView(viewsets.ModelViewSet):
    serializer_class= UserProductoSerializer
    queryset = ProductoUsuario.objects.all()

class FavoritosView(viewsets.ModelViewSet):
    serializer_class= FavoritosSerializer
    queryset = Favoritos.objects.all()

class ProductoView(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()
    
    
    def get_authenticators(self):
        return super().get_authenticators()
    authentication_classes = [TokenAuthentication]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve','partial_update']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsStaffOrSuperuserWriteOnly]
            
        return [permission() for permission in permission_classes]
    


@api_view(['GET'])
def search_products(request):
    
    criteria = request.GET.get('criteria')
    value = request.GET.get('value')
    
    print("criteria= ",criteria)
    print("value= ",value)
    
    if not criteria or not value:
        return Response({"error": "Missing criteria or value"}, status=400)

    # Mapea los criterios a los campos del modelo
  
    
    match criteria:
        case 'categoria_id':
            value=int(value)
        case 'cantidad_producto':
            value=int(value)
            
        case 'estado_producto':
            
            value = value.lower()=='activo'
            
            
        case 'precio':
            value=float(value)
        
        case 'nombre':
            criteria='nombre__icontains'
            
        
        case _:
            value=value
    


    filter_args = {criteria: value}
    products = Producto.objects.filter(**filter_args)
    serializer = ProductoSerializer(instance=products, many=True)  
    # for product in serializer.data:
    #     product['foto_producto'] = request.build_absolute_uri(product['foto_producto'])
    return Response({"products": serializer.data}, status=status.HTTP_200_OK)
    
    
    
@api_view(['GET'])
def search_users_products(request):
    
    criteria = request.GET.get('criteria')
    value=request.GET.get('value')
    if value is not None:
        value = int(value)
    
    
    
    if not criteria or not value:
        return Response({"error": "Missing criteria or value"}, status=400)

    filter_args = {criteria: value}
    t_pu = ProductoUsuario.objects.filter(**filter_args)

    return Response(find_user_product(t_pu,request), status=status.HTTP_200_OK)


def find_user_product(user_products,request):
    
    productos = []
    
    for product in user_products:
         id_product = product.producto_id
         id_user_product=product.id
         product_filter = Producto.objects.filter(id=id_product)
         serializer = ProductoSerializer(instance=product_filter, many=True)
         producto=serializer.data[0]
         producto['foto_producto'] = request.build_absolute_uri(producto['foto_producto'])
         producto['id_user_product']=id_user_product
         producto['cantidad_user_producto']=product.cantidad_producto
         productos.append(producto)
         
    return productos
    
@api_view(['DELETE'])    
def delete_all_user_products(request):
    id_user=request.GET.get('user_id')
    num,dic=ProductoUsuario.objects.filter(usuario_id=id_user).delete()
    return Response({'nuemro de objetos eliminados':num},status=204)
    
    
    