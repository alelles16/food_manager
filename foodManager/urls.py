from django.conf.urls import include, url
from . import views 

urlpatterns = [
    url(r'^$', views.producto_list, name='main'),
    url(r'^consumir/(?P<pk>[0-9]+)/$', views.consumir_producto, name='consumir_producto')
]