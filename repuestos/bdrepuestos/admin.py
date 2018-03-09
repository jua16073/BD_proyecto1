from django.contrib import admin
from .models import Vendedor, Producto, Cliente, Venta, LineaVenta, Proveedor

# Register your models here.



admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Vendedor)
admin.site.register(Venta)
admin.site.register(LineaVenta)
admin.site.register(Proveedor)
