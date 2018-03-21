from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('home.html', views.home, name='home'),
	path('repuestos.html', views.catalogo, name='catalogo'),
	path('clientes.html', views.clientes, name='clientes'),
	path('compras.html', views.compras, name='compras'),
	path('proveedores.html', views.proveedores, name='proveedores')
]


