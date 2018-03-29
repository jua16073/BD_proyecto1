from django.http import HttpResponse
from .models import Vendedor, Cliente, Producto, Venta, LineaVenta, Proveedor
from django.template import loader
from .forms import ContactForm
from django.shortcuts import render, get_object_or_404
from django.db import connection


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    #INGRESO DE Compras
    if request.method == 'GET':
        return render(request, 'bdrepuestos/home.html', {'form': ContactForm(modelo=0) })
    form = ContactForm(request.POST, modelo=0)
    if form.is_valid():
        print(form.cleaned_data.get('query'))
        x=connection.cursor()
        x.execute(form.cleaned_data.get('query'))
        row=x.fetchone()
    return render(request, 'bdrepuestos/home.html', {'form': form})

#CATALOGO DE Repuestos
def catalogo(request):
    if request.method == 'GET':
        paso = 0
        things = Producto.objects.all()
        return render(request, 'bdrepuestos/repuestos.html', {'paso':paso, 'form': ContactForm(modelo=2), 'things': things})
    form = ContactForm(request.POST, modelo=2)
    if form.is_valid():
        print(form.cleaned_data.get('query'))
        x=connection.cursor()
        try:
            x.execute("SELECT * FROM bdrepuestos_producto WHERE CAST("+form.cleaned_data.get('Por') + " AS TEXT) LIKE '%"+form.cleaned_data.get('query')+"%'")
            if(form.cleaned_data.get('query')!=''):
                things=x.fetchall()
                paso = 1
        except ValueError:
            things = Producto.objects.all()

    else:
        paso = 0
        things = Producto.objects.all()
    return render(request, 'bdrepuestos/repuestos.html', {
        'things': things, 'form': form, 'paso':paso
    })

#LISTA DE Clientes
def clientes(request):
    if request.method == 'GET':
        paso = 0
        things = Cliente.objects.all()
        return render(request, 'bdrepuestos/clientes.html', {'paso':paso, 'form': ContactForm(modelo=0), 'things': things})
    form = ContactForm(request.POST, modelo=0)
    if form.is_valid():
        print(form.cleaned_data.get('query'))
        x=connection.cursor()
        try:
            x.execute("SELECT * FROM bdrepuestos_cliente WHERE CAST("+form.cleaned_data.get('Por') + " AS TEXT) LIKE '%"+form.cleaned_data.get('query')+"%'")
            if(form.cleaned_data.get('query')!=''):
                things=x.fetchall()
                paso = 1
        except ValueError:
            things = Cliente.objects.all()

    else:
        paso = 0
        things = Cliente.objects.all()
    return render(request, 'bdrepuestos/clientes.html', {
        'things': things, 'form': form, 'paso':paso
    })

#LISTA DE Proveedores
def proveedores(request):
    if request.method == 'GET':
        paso = 0
        things = Proveedor.objects.all()
        return render(request, 'bdrepuestos/proveedores.html', {'paso':paso, 'form': ContactForm(modelo=3), 'things': things})
    form = ContactForm(request.POST, modelo=3)
    if form.is_valid():
        print(form.cleaned_data.get('query'))
        x=connection.cursor()
        try:
            x.execute("SELECT * FROM bdrepuestos_proveedor WHERE CAST("+form.cleaned_data.get('Por') + " AS TEXT) LIKE '%"+form.cleaned_data.get('query')+"%'")
            if(form.cleaned_data.get('query')!=''):
                things=x.fetchall()
                paso = 1
        except ValueError:
            things = Proveedor.objects.all()

    else:
        paso = 0
        things = Proveedor.objects.all()
    return render(request, 'bdrepuestos/proveedores.html', {
        'things': things, 'form': form, 'paso':paso
    })

#LISTA DE Compras
def compras(request):
    if request.method == 'GET':
        paso = 0
        things = Venta.objects.all()
        return render(request, 'bdrepuestos/compras.html', {'paso':paso, 'form': ContactForm(modelo=4), 'things': things})
    form = ContactForm(request.POST, modelo=4)
    if form.is_valid():
        print(form.cleaned_data.get('query'))
        x=connection.cursor()
        try:
            x.execute("SELECT * FROM bdrepuestos_venta WHERE CAST(" + form.cleaned_data.get('Por') + " AS TEXT) LIKE '"+form.cleaned_data.get('query')+"'")
            if(form.cleaned_data.get('query')!=''):
                things=x.fetchall()
                paso = 1
        except ValueError:
            things = Venta.objects.all()

    else:
        paso = 0
        things = Venta.objects.all()
    return render(request, 'bdrepuestos/compras.html', {
        'things': things, 'form': form, 'paso':paso
    })


def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    return render(request, 'bdrepuestos/detalles_cliente.html', {'cliente':cliente})

def detalle_repuesto(request, producto_id):
    repuesto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'bdrepuestos/detalles_repuesto.html', {'repuesto':repuesto})

def detalle_proveedor(request, proveedor_id):
    cliente = get_object_or_404(Proveedor, pk=cliente_id)
    return render(request, 'bdrepuestos/detalles_cliente.html', {'cliente':cliente})

def detalle_compra(request, venta_id):
    compra = get_object_or_404(Venta, pk=venta_id)
    x=connection.cursor()
    x.execute("SELECT * FROM bdrepuestos_lineaventa WHERE venta_id = '"+str(compra.id)+"'")
    detalles = x.fetchall()
    return render(request, 'bdrepuestos/detalles_compra.html', {'compra':compra, 'detalles':detalles})
