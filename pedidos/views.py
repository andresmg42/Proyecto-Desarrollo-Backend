from rest_framework import viewsets
from .serializer import  PedidoSerializer, PedidoProductoSerializer, ProductosMasVendidosSerializer
from .models import  Pedido, PedidoProducto
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes,api_view
from rest_framework.response import Response
from django.db.models import Count,Sum
from productos.models import Producto
from productos.serializer import ProductoSerializer
from django.http import JsonResponse
from django.db.models import F,Sum
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from usuarios.serializer import UsuarioSerializer





class PedidoView(viewsets.ModelViewSet):
    serializer_class=PedidoSerializer
    queryset=Pedido.objects.all()
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    


class PedidoProductoView(viewsets.ModelViewSet):
    serializer_class=PedidoProductoSerializer
    queryset=PedidoProducto.objects.all()
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def llenarTablaProductosPedidos(request):
    
    data=request.data
    print(data)
    for element in data:
        serializer= PedidoProductoSerializer(data=element)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            actualizarCantidadProductos(serializer)
            
    return Response({'los datos fueron guardados con exito'},status=200)

def actualizarCantidadProductos(serializer):
    try:
        producto=Producto.objects.get(id=serializer.data['producto_ppid'])
        producto.cantidad_producto=producto.cantidad_producto-serializer.data['cantidad_producto_carrito']
        producto.save()
        print('el producto se actualizo con exito')
    except Producto.DoesNotExist:
        print('el producto no existe')
    except KeyError:
        print('la clave producto_PPid no esta en serializer.data')




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def productosMasVendidos(request):
   
    resultados = (
        Producto.objects
        .annotate(total_vendidos=Sum('pedidoproducto__cantidad_producto_carrito'))
        .values('nombre', 'precio', 'total_vendidos','estado_producto','cantidad_producto')
        .order_by('-total_vendidos')
    )
      
    
    for resultado in resultados:
        resultado['ingresos']=resultado['precio']*resultado['total_vendidos']
    
    
    return Response(resultados,status=200)    
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def indicadores_por_usuario(request):
    
    resultado=(Pedido.objects.values('usuarios__username').annotate(
        total_productos_vendidos=Sum('pedidoproducto__cantidad_producto_carrito'), 
        total_pedidos=Count('id'),
        ingresos_por_usuario=Sum(F('pedidoproducto__cantidad_producto_carrito')*F('pedidoproducto__producto_ppid__precio')
        ) 
        ))

    return Response(resultado,status=200)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated]) 
@api_view(['GET'])   
def pedidos_por_estado(request):
    
    resultado=(Pedido.objects.values('estado_pedido').annotate(
      total_pedidos=Count('id')  
    ))
    
    return Response(resultado,status=200)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def ventas_diarias(request):
    resultado=(Pedido.objects.values('fecha').annotate(
        total_pedidos=Count('id'),
        total_ventas=Sum(F('pedidoproducto__cantidad_producto_carrito')*F('pedidoproducto__producto_ppid__precio'))
    ))
    
    return Response(resultado,status=200)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def metodos_pago_mas_utilizados(request):
    resultado=(Pedido.objects.values('metodo_pago').annotate(
        frecuencia=Count('id')
    )).order_by('-frecuencia')
    
    return Response(resultado,status=200)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def clientes_mas_frecuentes(request):
    
    resultado=(Pedido.objects.values('usuarios__username').annotate(
        total_pedidos=Count('id')
    )).order_by('-total_pedidos')
    
    return Response(resultado,status=200)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def valor_total_ventas(request):
    resultado=(Pedido.objects.aggregate(
        total_ventas=Sum(F('pedidoproducto__cantidad_producto_carrito') * F('pedidoproducto__producto_ppid__precio'))
    ))
    return Response(resultado,status=200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def productos_mas_vendidos(request):
    resultado=(Producto.objects.values('nombre').annotate(
        total_vendidos=Sum('pedidoproducto__cantidad_producto_carrito')
    ))
    
    return Response(resultado,status=200)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def send_email_cancel(request):
    dest = request.GET.get('dest')
    mensaje = request.GET.get('mensaje')
    
    if not dest or not mensaje:
        return Response({'error': 'Missing dest or mensaje parameter'}, status=400)
    
    try:
        send_mail(
            'Pedido cancelado',
            mensaje, 
            'tiendaonlinedesarrollo@gmail.com',
            [dest],
            fail_silently=False,
        )
        return Response({'success': 'Email sent successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def generar_factura(request):
    pedido_id = request.GET.get('pedido_id')
    
   
    
    if not pedido_id:
        return Response({'error': 'Falta el ID del pedido'}, status=400)
    
    try:
        
        pedido = Pedido.objects.get(id=pedido_id)
        productos_ids = pedido.productos.values_list('id', flat=True)
        
        
        usuario = pedido.usuarios
        
        usuario_serializado = UsuarioSerializer(usuario).data
        
        
        productos = PedidoProducto.objects.filter(pedido_ppid=pedido_id)
        productos_serializados = PedidoProductoSerializer(productos, many=True).data
        
        
        
       
        productos_info = Producto.objects.filter(id__in=productos_ids)
        productos_info_serializados = ProductoSerializer(productos_info, many=True).data
        
        cantidades_carrito = {}
        for producto in productos_serializados:
            cantidades_carrito[producto['producto_ppid']] = producto.get('cantidad_producto_carrito', 0)
        
        
        total = 0
        total_por_producto = {}
        
        for producto in productos_info_serializados:
            pid = producto['id']
            print('pedido_id:',pedido_id)
            cant = float(cantidades_carrito.get(pid, 0))
            precio = float(producto['precio'])
            print('precio:',precio)
            print('cantidad:',cant)
            total_por_producto[pid] = cant * precio
            print(total_por_producto)
            total += cant * precio
        
    
        serializer = PedidoSerializer(pedido)
        
        
        mensaje = f"""
        FACTURA ELECTRONICA
            CLASSMART
        --------------------
        Pedido ID: {pedido_id}
        Fecha: {serializer.data['fecha']}
        Hora: {serializer.data['hora']}
        Estado pedido: Aceptado
        Metodo de pago: {serializer.data['metodo_pago']}
        Direccion de envio: {serializer.data['direccion']}
        
        INFORMACION CLIENTE:
        
        Nombre: {usuario_serializado['username']}
        Email: {usuario_serializado['email']}
        
        Productos:
        """
        
        for producto in productos_info_serializados:
            cantidad_carrito = cantidades_carrito.get(producto['id'], 0)
            total_producto = total_por_producto.get(producto['id'], 0)
            
            
            mensaje += f"""
            - Producto: {producto['nombre']}
              Precio: {producto['precio']}
              Cantidad en carrito: {cantidad_carrito}
              Total por producto: {total_producto}
            """
        
        mensaje += f"""
        
        --------------------------------
        Total:  {total}
        ¡GRACIAS POR CONFIAR EN NOSOTROS!
        """
    
        
        
        send_mail(
            'FACTURACION ELECTRONICA',
            mensaje, 
            'tiendaonlinedesarrollo@gmail.com',
            [usuario_serializado['email'],'victoria.volveras@correounivalle.edu.co'],
            fail_silently=False,
        )
        
        return Response({'mensaje':{mensaje}}, status=200)
    
    except Pedido.DoesNotExist:
        return Response({'error': 'Pedido no encontrado'}, status=404)

