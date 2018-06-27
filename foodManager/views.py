from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ConsumirForm
from .forms import CustomUserCreationUserForm

from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Producto, Registro

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .serializers import ProductoSerializer, UserSerializer, RegistroSerializer

from django_filters.rest_framework import DjangoFilterBackend

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

    cantidad_mas_vendida = cantidad('producto')
    cantidad_mas_usuario = cantidad('usuario')

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

class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def produto_list_api(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductoSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def producto_detail_api(request, pk):
    try:
        producto = Producto.objects.get(pk = pk)
    except Producto.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        return JSONResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProductoSerializer(producto, data = data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        serie.delete()
        return HttpResponse(status=204)

class User_list_api(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('username','email')
    search_fields = ('username','email','first_name')

class User_detail_api(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class User_update_api(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class User_delete_api(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Registro_list_api(generics.ListCreateAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

class Registro_detail_api(generics.RetrieveAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer