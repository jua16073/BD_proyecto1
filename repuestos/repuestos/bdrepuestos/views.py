from django.http import HttpResponse
from .models import Vendedor, Cliente, Producto, Venta, LineaVenta, Proveedor
from django.template import loader
from .forms import ContactForm
from django.shortcuts import render
from django.db import connection


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data.get('query'))
        x=connection.cursor()
        try:
            x.execute(form.cleaned_data.get('query'))
            row=x.fetchone()
            for p in  row:
                print (p)
        except:
            print("wrong query")
        #for p in 
        #Choice.objects.raw(form.cleaned_data.get('query')):
            #print(p)


    return render(request, 'bdrepuestos/home.html', {'form': form})
