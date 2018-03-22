from django.http import HttpResponse
from .models import Vendedor, Cliente, Producto, Venta, LineaVenta, Proveedor
from django.template import loader
from .forms import ContactForm
from django.shortcuts import render, get_object_or_404
from django.db import connection


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data.get('query'))
        x=connection.cursor()
        x.execute(form.cleaned_data.get('query'))
        row=x.fetchone()
        for p in  row:
            print (p.nombre)
        #for p in
        #Choice.objects.raw(form.cleaned_data.get('query')):
            #print(p)


    return render(request, 'bdrepuestos/home.html', {'form': form})

def catalogo(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data.get('query'))
        x=connection.cursor()
        try:
            x.execute("SELECT * FROM bdrepuestos_producto WHERE categoria LIKE '"+form.cleaned_data.get('query')+"'")
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

def clientes(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data.get('query'))
        x=connection.cursor()
        try:
            x.execute("SELECT * FROM bdrepuestos_cliente WHERE nombre LIKE '"+form.cleaned_data.get('query')+"'")
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

def proveedores(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data.get('query'))
        x=connection.cursor()
        try:
            x.execute("SELECT * FROM Proveedor WHERE nombre LIKE '"+form.cleaned_data.get('query')+"'")
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

def compras(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data.get('query'))
        x=connection.cursor()
        try:
            x.execute("SELECT * FROM bdrepuestos_venta WHERE vendedor LIKE '"+form.cleaned_data.get('query')+"'")
            if(form.cleaned_data.get('query')!=''):
                things=x.fetchall()
                paso = 1
        except ValueError:
            things = Venta.objects.all()

    else:
        paso = 0
        things = Cliente.objects.all()
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
