from django.urls import path
from . import views

#app_name='bdrepuestos'

urlpatterns = [
	path('', views.index, name='index'),
	path('home.html', views.home, name='home'),
	path('repuestos.html', views.catalogo, name='catalogo'),
	path('clientes.html', views.clientes, name='clientes'),
	path('compras.html', views.compras, name='compras'),
	path('proveedores.html', views.proveedores, name='proveedores'),
	path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
	path('repuestos/<int:producto_id>/', views.detalle_repuesto, name='detalle_repuesto'),
	path('proveedores/<int:proveedor_id>/', views.detalle_proveedor, name='detalle_proveedor'),
	path('ventas/<int:venta_id>/', views.detalle_compra, name='detalle_compra'),
	path('anadirCliente.html', views.anadirCliente, name='anadirCliente'),
	path('editarCliente.html/<int:cliente_id>', views.editarCliente, name='editarCliente'),
	path('anadirProducto.html', views.anadirProducto, name='anadirProducto'),
	path('editarProducto.html/<int:producto_id>', views.editarProducto, name='editarProducto'),
	path('login.html',views.login, name='login'),
	path('ver',views.ver, name= 'ver'),
	path('chart', views.chart1, name='chart')
]
