from django.db import models
from django.utils import timezone

class Producto (models.Model):
    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    cantidad_actual = models.PositiveIntegerField(default=0)

    def __str__ (self):
        return '{} - {}'.format(self.nombre, self.cantidad_actual)

class Registro (models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha = models.DateTimeField(blank=True, null=True, editable=False)
    cantidad_comprada = models.PositiveIntegerField(default=0, verbose_name='Cantidad')

    def nuevo_registro (self):
        self.fecha = timezone.now()
        self.producto.cantidad_actual -= self.cantidad_comprada
        self.producto.save()
    
    def save (self, *args, **kwargs):
        self.nuevo_registro()
        super(Registro, self).save(*args, **kwargs)

    def __str__ (self):
        return '{} - {}'.format(self.producto.nombre, self.cantidad_comprada)
