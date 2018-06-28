from django.conf.urls import include, url
from . import views 

urlpatterns = [
    url(r'^$', views.producto_list, name='main'),
    url(r'^register/$', views.register, name='register'),
    url(r'^consumir/(?P<pk>[0-9]+)/$', views.consumir_producto, name='consumir_producto'),
    url(r'^productos_usuario/(?P<pk>[0-9]+)/$', views.productos_usuario, name='productos_usuario'),

    url(r'^api/productos/list/$', views.produto_list_api),
    url(r'^api/productos/list/(?P<pk>[0-9]+)/$', views.producto_detail_api),
    
    url(r'^api/usuarios/list/$', views.User_list_api.as_view()),
    url(r'^api/usuarios/list/(?P<pk>[0-9]+)/$', views.User_detail_api.as_view()),
    url(r'^api/usuarios/update/(?P<pk>[0-9]+)/$', views.User_update_api.as_view()),

    url(r'^api/registros/list/$', views.Registro_list_api.as_view()),
    url(r'^api/registros/list/(?P<pk>[0-9]+)/$', views.Registro_detail_api.as_view()),
]