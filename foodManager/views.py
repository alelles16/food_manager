from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Registro
from .forms import ConsumirForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def producto_list(request):
    productos = Producto.objects.order_by('-cantidad_actual')

    cantidad_mas_usuario = Registro.objects.all().values('usuario').annotate(total_consumido = Sum('cantidad_comprada')).order_by('-total_consumido').first()
    mas_usuario = User.objects.get(pk = cantidad_mas_usuario.get('usuario'))
    print(cantidad_mas_usuario)
    print(mas_usuario)

    cantidad_mas_vendida = Registro.objects.all().values('producto').annotate(total_vendido = Sum('cantidad_comprada')).order_by('-total_vendido').first()
    mas_vendido = Producto.objects.get(pk = cantidad_mas_vendida.get('producto'))

    return render(request, 'foodManager/producto_list.html',{'productos' : productos, 'mas_vendido' : mas_vendido, 'mas_usuario' : mas_usuario})

@login_required
def consumir_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = ConsumirForm(request.POST)

        if int(request.POST.get("cantidad_comprada")) > 0 :
            
            if form.is_valid() :
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

        else:
            error = 'warning'
                    
        return render(request, 'foodManager/consumir_producto.html', {'producto' : producto, 'form' : form, 'error': error})
        
    else:
        form = ConsumirForm()
        
    return render(request, 'foodManager/consumir_producto.html', {'producto' : producto, 'form' : form })