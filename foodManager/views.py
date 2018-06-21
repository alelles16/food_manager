from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ConsumirForm

def producto_list(request):
    productos = Producto.objects.order_by('-cantidad_actual')
    return render(request, 'foodManager/producto_list.html',{'productos' : productos})

def consumir_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ConsumirForm(request.POST)
        
        if form.is_valid() and int(request.POST.get("cantidad_comprada")) > 0 :
            registro_consumo = form.save(commit=False)
            total = producto.cantidad_actual - registro_consumo.cantidad_comprada
            error = ''

            if total >= 0 and producto.cantidad_actual > 0:
                registro_consumo.producto = producto
                registro_consumo.usuario = request.user
                registro_consumo.save()
                error = 'free'

            else:
                error = 'problem'
                
            return render(request, 'foodManager/consumir_producto.html', {'producto' : producto, 'form' : form, 'error': error})
    
    else:
        form = ConsumirForm()
        
    return render(request, 'foodManager/consumir_producto.html', {'producto' : producto, 'form' : form})