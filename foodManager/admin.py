from django.contrib import admin
from .models import Producto, Registro

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'marca', 'cantidad_actual']
    list_filter = ('nombre', 'marca')
    fields = ('nombre', 'marca')

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ['producto', 'usuario', 'cantidad_comprada']
    list_filter = ('producto', 'usuario')