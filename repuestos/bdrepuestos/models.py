from django.db import models

# Create your models here.


class Proveedor(models.Model):
    nombre = models.TextField()
    def __str__(self):
        return self.nombre

class Vendedor(models.Model):
    nombre = models.CharField(max_length = 200)
    contrasena=models.CharField(max_length = 200)
    total_ventas = models.FloatField()
    contraseña = models.TextField()
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre=models.CharField(max_length = 200)
    categoria=models.CharField(max_length = 200)
    precio1 = models.FloatField(default = 0)
    precio2 = models.FloatField(default = 0)
    precio3 = models.FloatField(default = 0)
    disponibilidad = models.IntegerField(default = 0)
    marca = models.TextField()
    proveedor = models.ForeignKey(Proveedor, on_delete = models.CASCADE)
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length = 200)
    telefono = models.CharField(max_length = 20)
    dpi = models.CharField(max_length = 15)
    correo = models.EmailField()
    tipo = models.CharField(max_length = 1)
    direccion = models.TextField()
    nit = models.CharField(max_length = 20)
    twitter=models.CharField(max_length = 40)
    fecha_de_comienzo=models.DateField()
    def __str__(self):
        return self.nombre

class Venta(models.Model):
    fecha_de_venta = models.DateField()
    id_Cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    total = models.FloatField(default = 0)
    vendedor = models.ForeignKey(Vendedor, on_delete = models.CASCADE)

class LineaVenta(models.Model):
    venta= models.ForeignKey(Venta, on_delete = models.CASCADE)
    cantidad = models.IntegerField(default = 1)
    precio = models.FloatField(default = 0)
    producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
