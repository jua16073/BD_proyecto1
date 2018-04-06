from django.http import HttpResponse
from .models import Vendedor, Cliente, Producto, Venta, LineaVenta, Proveedor
from django.template import loader
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.contrib import messages
import tweepy
import pymongo
import datetime
from chartit import DataPool, Chart, PivotChart, PivotDataPool
from django.db.models import *

#Se a;ade un CLIENTE a la base de datos
def anadirCliente(request):
    if request.method == 'GET':
        return render(request, 'bdrepuestos/anadirCliente.html', {'form': AnadirForm()})
    form = AnadirForm(request.POST)
    if form.is_valid():
        x=connection.cursor()
        x.execute("INSERT INTO bdrepuestos_cliente (nombre, telefono, dpi, correo, tipo, direccion, nit, twitter, fecha_de_comienzo) VALUES ('"+form.cleaned_data.get('nombre')+"', '"+form.cleaned_data.get('telefono')+"', '"+form.cleaned_data.get('dpi')+"', '"+form.cleaned_data.get('correo')+"', '"+form.cleaned_data.get('tipo')+"', '"+form.cleaned_data.get('direccion')+"', '"+form.cleaned_data.get('nit')+"', '"+form.cleaned_data.get('twitter')+"', '"+str(form.cleaned_data.get('fecha_de_comienzo'))+"'::date) RETURNING bdrepuestos_cliente.id")
    else:
        return render(request, 'bdrepuestos/anadirCliente.html', {'form': AnadirForm(request.POST)})
    return render(request, 'bdrepuestos/clientes.html', {'paso':0, 'form': ContactForm( modelo=0), 'things':Cliente.objects.all()})

#Se edita un CLIENTE que ya ha sido a;adido
def editarCliente(request, cliente_id):
    inst = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'GET':
        return render(request, 'bdrepuestos/editarCliente.html', {'form': AnadirForm(instance=inst)})
    form = AnadirForm(request.POST, instance=inst)
    if form.is_valid():
        x=connection.cursor()
        x.execute("UPDATE bdrepuestos_cliente SET nombre = '"+form.cleaned_data.get('nombre')+"', telefono = '"+form.cleaned_data.get('telefono')+"', dpi = '"+form.cleaned_data.get('dpi')+"', correo = '"+form.cleaned_data.get('correo')+"', tipo = '"+form.cleaned_data.get('tipo')+"', direccion = '"+form.cleaned_data.get('direccion')+"', nit = '"+form.cleaned_data.get('nit')+"', twitter = '"+form.cleaned_data.get('twitter')+"', fecha_de_comienzo = '"+str(form.cleaned_data.get('fecha_de_comienzo'))+"'::date WHERE bdrepuestos_cliente.id = "+str(cliente_id))
    else:
        return render(request, 'bdrepuestos/editarCliente.html', {'form': AnadirForm(request.POST, instance=inst)})
    return render(request, 'bdrepuestos/clientes.html', {'paso':0, 'form': ContactForm( modelo=0), 'things':Cliente.objects.all()})

#Se a;ade un PRODUCTO a la base de datos
def anadirProducto(request):
    if request.method == 'GET':
        return render(request, 'bdrepuestos/anadirProducto.html', {'form': anadirProductoForm()})
    form = anadirProductoForm(request.POST)
    if form.is_valid():
        x=connection.cursor()
        x.execute("SELECT id FROM bdrepuestos_proveedor WHERE nombre LIKE '"+ str(form.cleaned_data.get('proveedor'))+"'")
        prov = x.fetchone()[0]
        x.execute("INSERT INTO bdrepuestos_producto (nombre, categoria, precio1, precio2, precio3, disponibilidad, marca, proveedor_id) VALUES ('"+form.cleaned_data.get('nombre')+"', '"+form.cleaned_data.get('categoria')+"', "+str(form.cleaned_data.get('precio1'))+", "+str(form.cleaned_data.get('precio2'))+", "+str(form.cleaned_data.get('precio3'))+", "+str(form.cleaned_data.get('disponibilidad'))+", '"+form.cleaned_data.get('marca')+"', "+str(prov)+") RETURNING bdrepuestos_producto.id")
        print("El proveedor es ")
        print(str(form.cleaned_data.get('proveedor')))
    else:
        return render(request, 'bdrepuestos/anadirProducto.html', {'form': anadirProductoForm(request.POST)})
    return render(request, 'bdrepuestos/repuestos.html', {'paso':0, 'form': ContactForm(modelo=2), 'things': Producto.objects.all()})


#Se edita un PRODUCTO que ya este en la base de datos
def editarProducto(request, producto_id):
    inst = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'GET':
        return render(request, 'bdrepuestos/editarProducto.html', {'form': anadirProductoForm(instance=inst)})
    form = anadirProductoForm(request.POST, instance=inst)
    if form.is_valid():
        x=connection.cursor()
        x.execute("SELECT id FROM bdrepuestos_proveedor WHERE nombre LIKE '"+ str(form.cleaned_data.get('proveedor'))+"'")
        prov = x.fetchone()[0]
        x.execute("UPDATE bdrepuestos_producto SET nombre = '"+form.cleaned_data.get('nombre')+"', categoria = '"+form.cleaned_data.get('categoria')+"', precio1 = "+str(form.cleaned_data.get('precio1'))+", precio2 = "+str(form.cleaned_data.get('precio2'))+", precio3 = "+str(form.cleaned_data.get('precio3'))+", disponibilidad = "+str(form.cleaned_data.get('disponibilidad'))+", marca = '"+form.cleaned_data.get('marca')+"', proveedor_id = "+str(prov)+" WHERE bdrepuestos_producto.id = "+str(producto_id))
    else:
        return render(request, 'bdrepuestos/editarProducto.html', {'form': anadirProductoForm(request.POST, instance=inst)})
    return render(request, 'bdrepuestos/repuestos.html', {'paso':0, 'form': ContactForm(modelo=2), 'things': Producto.objects.all()})

#Se a;ade un PROVEEDOR a la base de datos
def anadirProveedor(request):
    if request.method == 'GET':
        return render(request, 'bdrepuestos/anadirProveedor.html', {'form': anadirProveedorForm()})
    form = anadirProveedorForm(request.POST)
    if form.is_valid():
        x=connection.cursor()
        x.execute("INSERT INTO bdrepuestos_proveedor (nombre) VALUES ('"+form.cleaned_data.get('nombre')+"') RETURNING bdrepuestos_proveedor.id")
    else:
        return render(request, 'bdrepuestos/anadirProveedor.html', {'form': anadirProveedorForm(request.POST)})
    return render(request, 'bdrepuestos/proveedores.html', {'form': ContactForm( modelo=5), 'things': Proveedor.objects.all()})

#Se edita un PROVEEDOR que ya ha sido a;adido
def editarProveedor(request, proveedor_id):
    inst = get_object_or_404(Proveedor, pk=proveedor_id)
    if request.method == 'GET':
        return render(request, 'bdrepuestos/editarCliente.html', {'form': anadirProveedorForm(instance=inst)})
    form = anadirProveedorForm(request.POST, instance=inst)
    if form.is_valid():
        x=connection.cursor()
        x.execute("UPDATE bdrepuestos_proveedor SET nombre = '"+form.cleaned_data.get('nombre')+"' WHERE bdrepuestos_proveedor.id = "+str(proveedor_id))
    else:
        return render(request, 'bdrepuestos/editarCliente.html', {'form': anadirProveedorForm(request.POST, instance=inst)})
    return render(request, 'bdrepuestos/proveedores.html', {'paso':0, 'form': ContactForm( modelo=5), 'things': Proveedor.objects.all()})


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    if request.method == 'GET':
        return render(request, 'bdrepuestos/home.html', {'form': anadirVentaForm()})
    form = anadirVentaForm(request.POST)
    if form.is_valid():
        x=connection.cursor()
        x.execute("SELECT id FROM bdrepuestos_cliente WHERE nombre LIKE '"+str(form.cleaned_data.get('cliente'))+"'")
        cl = x.fetchone()[0]
        x.execute("SELECT id FROM bdrepuestos_vendedor WHERE nombre LIKE '"+str(form.cleaned_data.get('vendedor'))+"'")
        vd = x.fetchone()[0]
        x.execute("INSERT INTO bdrepuestos_venta (fecha_de_venta, cliente_id, total, vendedor_id) VALUES ('"+str(form.cleaned_data.get('fecha_de_venta'))+"'::date, "+ str(cl) +", 0.0, "+ str(vd) +") RETURNING bdrepuestos_venta.id")
        x.execute("SELECT max(id) FROM bdrepuestos_venta")
        local = x.fetchone()[0]
    else:
        return render(request, 'bdrepuestos/home.html', {'form': anadirVentaForm(request.POST)})
    return redirect(editarVenta, pls = local)

def editarVenta(request, pls):
    try:
        inst = Venta.objects.get(id=pls)
    except Exception as e:
        inst = 0
    if inst:
        x=connection.cursor()
        x.execute("SELECT SUM(cantidad*precio) FROM bdrepuestos_lineaventa WHERE venta_id = '" + str(pls)+"'")
        tot = x.fetchone()[0]
        print(tot)
        x.execute("SELECT * FROM bdrepuestos_lineaventa WHERE venta_id = '"+str(pls)+"'")
        detalles = x.fetchall()
        if request.method == 'GET':
            return render(request, 'bdrepuestos/editarVenta.html', {'venta': pls, 'form': anadirVentaForm(instance=inst), 'detalles':detalles, 'total':tot})
        form = anadirVentaForm(request.POST, instance=inst)
        if form.is_valid():
            x=connection.cursor()
            x.execute("SELECT SUM(cantidad*precio) FROM bdrepuestos_lineaventa WHERE venta_id =" + str(pls))
            tot = x.fetchone()[0]
            x.execute("SELECT id FROM bdrepuestos_cliente WHERE nombre LIKE '"+str(form.cleaned_data.get('cliente'))+"'")
            cl = x.fetchone()[0]
            x.execute("SELECT id, total_ventas FROM bdrepuestos_vendedor WHERE nombre LIKE '"+str(form.cleaned_data.get('vendedor'))+"'")
            resultados = x.fetchone()
            vd = resultados[0]
            tventas = resultados[1]
            print("EL TOTAL DE VENTAS ES DE: " + str(tventas))
            x.execute("UPDATE bdrepuestos_venta SET fecha_de_venta = '"+str(form.cleaned_data.get('fecha_de_venta'))+"'::date, cliente_id = "+ str(cl) +", total = "+ str(tot) +" WHERE bdrepuestos_venta.id = "+str(pls))
            x.execute("UPDATE bdrepuestos_vendedor SET total_ventas = "+ str(tventas + tot) +" WHERE bdrepuestos_vendedor.id = "+ str(vd))
            return redirect(home)
        else:
            return render(request, 'bdrepuestos/editarVenta.html', {'venta': pls, 'form': anadirVentaForm(request.POST, instance=inst), 'detalles':detalles, 'total':tot})
    else:
        if request.method == 'GET':
            return render(request, 'bdrepuestos/home.html', {'form': anadirVentaForm()})
        form = anadirVentaForm(request.POST)
        if form.is_valid():
            x=connection.cursor()
            x.execute("SELECT id FROM bdrepuestos_cliente WHERE nombre LIKE '"+str(form.cleaned_data.get('cliente'))+"'")
            cl = x.fetchone()[0]
            x.execute("SELECT id FROM bdrepuestos_vendedor WHERE nombre LIKE '"+str(form.cleaned_data.get('vendedor'))+"'")
            vd = x.fetchone()[0]
            x.execute("INSERT INTO bdrepuestos_venta (fecha_de_venta, cliente_id, total, vendedor_id) VALUES ('"+str(form.cleaned_data.get('fecha_de_venta'))+"'::date, "+ str(cl) +", 0.0, "+ str(vd) +") RETURNING bdrepuestos_venta.id")
        else:
            return render(request, 'bdrepuestos/home.html', {'form': anadirVentaForm(request.POST)})

    return render(request, 'bdrepuestos/home.html', {'paso':0, 'form': anadirVentaForm()})

def anadirLineaVenta(request, venta):
    if request.method == 'GET':
        return render(request, 'bdrepuestos/anadirLineaVenta.html', {'form': anadirLineaForm(), 'venta':venta})
    print("1")
    form = anadirLineaForm(request.POST)
    if form.is_valid():
        print("2")
        x=connection.cursor()
        x.execute("SELECT max(id) FROM bdrepuestos_venta")
        local = x.fetchone()[0]
        print("lOCAL = " + str(local))
        x.execute("SELECT id FROM bdrepuestos_producto WHERE nombre LIKE '"+str(form.cleaned_data.get('producto'))+"'")
        prod = x.fetchone()[0]
        x.execute("INSERT INTO bdrepuestos_lineaventa (cantidad, precio, venta_id, producto_id) VALUES ("+str(form.cleaned_data.get('cantidad'))+", "+str(form.cleaned_data.get('precio'))+", "+str(venta)+", "+str(prod)+" ) RETURNING bdrepuestos_lineaventa.id")
    else:
        return render(request, 'bdrepuestos/anadirLineaVenta.html', {'form': anadirLineaForm(request.POST), 'venta':venta})
    return redirect(editarVenta, pls = local)

def eliminarCliente(request, id):
    x=connection.cursor()
    x.execute("SELECT nombre FROM bdrepuestos_cliente WHERE id = "+str(id))
    nombre = str(x.fetchone()[0])
    if request.method == 'GET':
        return render(request, 'bdrepuestos/eliminarCliente.html', {'form': eliminarForm(), 'cliente_id':id, 'nombre': nombre})
    form = eliminarForm(request.POST)
    if form.is_valid():
        if form.cleaned_data.get('eliminar'):
            x.execute("SELECT id FROM bdrepuestos_venta WHERE cliente_id = "+ str(id))
            ventas = x.fetchall()
            for venta in ventas:
                x.execute("DELETE FROM bdrepuestos_lineaventa WHERE venta_id = "+ str(venta[0]))
            x.execute("DELETE FROM bdrepuestos_venta WHERE cliente_id = "+ str(id))
            x.execute("DELETE FROM bdrepuestos_cliente WHERE bdrepuestos_cliente.id = "+ str(id))
            return redirect(clientes)
        else:
            return redirect(detalle_cliente, cliente_id=id)

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

#Tweets de los clientes
def cliente_twitter(nombre_screen):
    a = []
    client = pymongo.MongoClient("localhost",27017)
    db = client.twitter

    consumer_key = 'tVXKlrYZ0XtJRhhvMKTIxvuxZ'
    consumer_secret = 'ag5HztuW6fwaHpObEQYw6NXu8dM5J8uwClqonwWX3WnzJnLeJw'
    access_token = '711807286079913985-ugwPIWrPiUCsoWq1DhGGz0PitJ2KeBl'
    access_token_secret = 'KnYNsaiwc5Ow4rk5BE0Pem05RGp7DKXMJPMV68qmHG0EW'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    try:
        i = 0
        statuses = api.user_timeline(screen_name = nombre_screen, count = 10, include_rts = True, exclude_replies = True )
        for s in statuses:
            if db.twitterinos.find_one({'text':s.text})==None:
                twitterinos = {'tweet': s.text, 'user': s.author.screen_name}
                a.append(twitterinos)
                db.twitterinos.save(twitterinos)
                print(str(i)+s.text)
                i+=1
    except:
        return (a)
    return(a)


def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    return render(request, 'bdrepuestos/detalles_cliente.html', {'cliente':cliente, 'twitter':cliente_twitter(cliente.twitter)})

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


def login(request):
    if request.method == 'GET':
        return render(request, 'bdrepuestos/login.html', {'form':ContactForm2()})
    form= ContactForm2(request.POST)
    return render(request,'./bdrepuestos/login.html', {'form': form})


def ver(request):
    if request.method == 'GET':
        return render(request, 'bdrepuestos/login.html', {'form':ContactForm2()})
    form = ContactForm2(request.POST)
    if form.is_valid():
        print(form.cleaned_data.get('contraseña'))
        x=connection.cursor()
        try:
            x.execute("SELECT * FROM bdrepuestos_vendedor WHERE  nombre LIKE '"+form.cleaned_data.get('name')+"'AND contraseña LIKE '"+form.cleaned_data.get('contraseña')+"'")
            if(form.cleaned_data.get('name')!=''):
                things=x.fetchall()
                print (len(things))
                if (len(things)!=0):
                    return render (request, 'bdrepuestos/home.html')
                else:
                    return render(request, 'bdrepuestos/login.html', {'form':form})
                paso = 1
        except ValueError:
            things = Producto.objects.all()
        return HttpResponse("wow")
    else:
        return render(request, 'bdrepuestos/login.html', {'form':form})


def chart1(request):
    x=connection.cursor()
    vend_data= DataPool(series=[{
    'options':{
    'source': Vendedor.objects.raw('SELECT * FROM bdrepuestos_vendedor')
    },
    'terms':[
    'nombre',
    #'contrasena',
    'total_ventas',
    'contraseña']}
    ])

    ventas_data=PivotDataPool(series=[{
        'options':{'source': Venta.objects.all(),
        'categories':['fecha_de_venta']},
        'terms':{
        'tot': Sum('total')}
        }])

    producto_data=DataPool(series=[{
        'options':{'source': Producto.objects.raw('SELECT * FROM bdrepuestos_producto'),
        },
        'terms':['nombre',
        'categoria',
        'precio1',
        'precio2',
        'precio3',
        'disponibilidad',
        'marca',
        'proveedor']
        }])

    cliente_data=PivotDataPool(series=[{
        'options':{'source': Cliente.objects.all(),
        'categories':['tipo']},
        'terms':{
        'nums': Count('nombre')
        }
        }])

    clientes_best= DataPool(series=[{
        'options':{'source': Cliente.objects.raw('SELECT * FROM bdrepuestos_cliente')},
        'terms':['nombre',
        'id']
        },
        {
        'options':{'source': Venta.objects.raw('SELECT * FROM bdrepuestos_venta')},
        'terms':[
        'id_Cliente',
        'total'
        ]
        }])

    clientes_10= PivotDataPool(series=[{
        'options':{'source':Venta.objects.all(),
        'categories':['id_Cliente'],
        'top_n_per_cat':10},
        'terms':{
        'tot': Sum('total')
        }
        }])

    productos_10=PivotDataPool(series=[{
        'options':{'source':LineaVenta.objects.all(),
        'categories':['producto'],
        'top_n_per_cat':10},
        'terms':{
        'cont': Count('cantidad')
        }
        }])


    cht= Chart(
    datasource= vend_data,
    series_options=[{
    'options':{
    'type':'pie',
    'stacking': False},
    'terms':{
    'nombre':[
    'total_ventas']}
    }],
    chart_options =
    {'title':{
    'text':'Ventas por vendedor'},
    'xAxis':{'text': 'Ventas'}
    }
    )

    cht1=PivotChart(
        datasource=ventas_data,
        series_options=[{
        'options':{ 'type': 'column',
        'stacking': True},

        'terms':['tot']
        }],
        chart_options= {
        'title':{
        'text':'Venta por dia'
        },
        'xAxis':{'text':'Ventas'}
        })

    cht2=PivotChart(
        datasource=cliente_data,
        series_options=[{ 'options':{ 'type': 'column'},
        'terms':['nums']
        }],
        chart_options={
        'title':{
        'text': 'Tipos de cliente'
        },
        'xAxis':{'text': 'Tipos de Clientes'}
        })

    cht3=PivotChart(
        datasource=clientes_10,
        series_options=[{
        'options':{'type': 'column', 'stacking': True},
        'terms':
        ['tot']
        }],
        chart_options={
        'title':{
        'text':'Mejores Clientes'
        }
        })
    cht4=PivotChart(
        datasource=productos_10,
        series_options=[{
        'options':{'type':'column'},
        'terms':
        ['cont']
        }],
        chart_options={
        'title':{
        'text':'Productos mas Vendidos'
        }
        })
    return render(request, 'bdrepuestos/cuadros.html',{'charts':[cht,cht1,cht2,cht3,cht4]})
