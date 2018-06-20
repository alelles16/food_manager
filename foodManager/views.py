from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import Producto

def producto_list(request):
    productos = Producto.objects.order_by('-cantidad_actual')
    return render(request, 'foodManager/producto_list.html',{'productos' : productos})

def consumir_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'foodManager/consumir_producto.html', {'producto' : producto})