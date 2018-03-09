from django.db import models

# Create your models here.


class Proveedor(models.Model):
    nombre = models.TextField()

class Vendedor(models.Model):
    nombre = models.TextField()
    total_ventas = models.FloatField()
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria=models.TextField()
    precioA = models.FloatField(default = 0)
    precioB = models.FloatField(default = 0)
    precioC = models.FloatField(default = 0)
    disponibilidad = models.IntegerField(default = 0)
    marca = models.TextField()
    id_Proveedor = models.ForeignKey(Proveedor, on_delete = models.CASCADE)

class Cliente(models.Model):
    nombre = models.CharField(max_length = 200)
    telefono = models.CharField(max_length = 20)
    dpi = models.CharField(max_length = 15)
    correo = models.EmailField()
    tipo = models.CharField(max_length = 1)
    direccion = models.TextField()
    nit = models.CharField(max_length = 20)
    fecha_de_comienzo=models.DateField()

class Venta(models.Model):
    fecha_de_venta = models.DateField()
    id_Cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    total = models.FloatField(default = 0)
    id_Vendedor = models.ForeignKey(Vendedor, on_delete = models.CASCADE)

class LineaVenta(models.Model):
    id_Venta= models.ForeignKey(Venta, on_delete = models.CASCADE)
    cantidad = models.IntegerField(default = 1)
    precio = models.FloatField(default = 0)
    producto = models.ForeignKey(Producto, on_delete = models.CASCADE)



