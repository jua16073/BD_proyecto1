from django import forms
import psycopg2
from .models import Vendedor, Cliente, Producto, Venta, LineaVenta, Proveedor

def get_my_choices(mod):
    if mod == 0:
        modelo = Cliente
        i=2
    elif mod == 1:
        modelo = Vendedor
        i=2
    elif mod == 2:
        modelo = Producto
        i=2
    elif mod == 3:
        modelo = Proveedor
        i=2
    elif mod == 4:
        modelo = Venta
        i=2
    else:
        i=2
        modelo = Proveedor
    MY_CHOICES = []
    choices = modelo._meta.get_fields()
    for choice in choices:
        MY_CHOICES.append((choice.name, choice.name))
    MY_CHOICES.remove(MY_CHOICES[0])
    return MY_CHOICES


class ContactForm(forms.Form):
    query = forms.CharField(
        max_length=100
    )
    Por = forms.ChoiceField(choices=get_my_choices([('1', '1')]))
    def __init__(self, *args, **kwargs):
        modelo = kwargs.pop('modelo')
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['Por'] = forms.ChoiceField(choices=get_my_choices(modelo) )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        query = cleaned_data.get('query')
        
class AnadirForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
    def clean(self):
        cleaned_data = super(AnadirForm, self).clean()

class anadirProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
    def clean(self):
        cleaned_data = super(anadirProductoForm, self).clean()


class ContactForm2(forms.Form):
    name = forms.CharField(
        max_length=50
    )
    contraseña= forms.CharField( max_length=50, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(ContactForm2, self).clean()
        name = cleaned_data.get('name')
        contra = cleaned_data.get('contra')
