from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('home.html', views.home, name='home'),
	path('repuestos.html', views.catalogo, name='catalogo'),
	path('clientes.html', views.clientes, name='clientes'),
	path('compras.html', views.compras, name='compras'),
	path('proveedores.html', views.proveedores, name='proveedores'),
	path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
	path('repuestos/<int:producto_id>/', views.detalle_repuesto, name='detalle_repuesto'),
	path('proveedores/<int:proveedor_id>/', views.detalle_proveedor, name='detalle_proveedor')
]
