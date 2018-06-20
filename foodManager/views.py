from django.shortcuts import render
from django.utils import timezone
from .models import Producto

def producto_list(request):
    productos = Producto.objects.order_by('cantidad_actual')
    return render(request, 'foodManager/producto_list.html',{'productos' : productos})