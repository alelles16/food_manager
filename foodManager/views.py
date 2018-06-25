from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Registro
from .forms import ConsumirForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationUserForm

def register(request):
    if request.method == "POST":
        f = CustomUserCreationUserForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('main')
    else: 
        f = CustomUserCreationUserForm()

    return render(request, 'registration/register.html', {'form': f})

def producto_list(request):
    productos = Producto.objects.order_by('-cantidad_actual')

    def cantidad(consult):
        return Registro.objects.all().values(consult).annotate(total = Sum('cantidad_comprada')).order_by('-total').first()

    cantidad_mas_usuario = cantidad('usuario')
    print(cantidad_mas_usuario)
    cantidad_mas_vendida = cantidad('producto')    
    print(cantidad_mas_vendida)

    try:
        mas_usuario = User.objects.get(pk = cantidad_mas_usuario.get('usuario'))
    except Exception as e:
        print(e)
        mas_usuario = None

    try:
        mas_vendido = Producto.objects.get(pk = cantidad_mas_vendida.get('producto'))
    except Exception as e:
        print(e)
        mas_vendido = None

    return render(request, 'foodManager/producto_list.html',{'productos' : productos, 'mas_vendido' : mas_vendido, 'mas_usuario' : mas_usuario, 'cantidad_mas_usuario' : cantidad_mas_usuario})

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