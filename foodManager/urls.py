from django.conf.urls import include, url
from . import views 

urlpatterns = [
    url(r'^$', views.producto_list, name='main'),
    url(r'^register/$', views.register, name='register'),
    url(r'^consumir/(?P<pk>[0-9]+)/$', views.consumir_producto, name='consumir_producto'),

    url(r'^api/productos/$', views.produto_list_api),
    url(r'^api/productos/(?P<pk>[0-9]+)/$', views.producto_detail_api),
    
    url(r'^api/usuarios/$', views.User_list_api.as_view()),
    url(r'^api/usuarios/(?P<pk>[0-9]+)/$', views.User_detail_api.as_view())
]