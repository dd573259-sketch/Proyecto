from dataclasses import field
from django.forms import ModelForm
from app.models import Categoria
from django import forms
from django import forms


from app.models import Usuario
from app.models import Proveedor
from app.models import Producto
from app.models import Compra



class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de la categoria'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion de la categoria',
                    'rows': 3,
                    'cols': 3}),
        }

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del usuario'}),
            'apellido': forms.TextInput(attrs={
                'placeholder': 'Ingrese el apellido del usuario'}),
            'correo_electronico': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico del usuario'}),
            'rol': forms.Select(attrs={
                'placeholder': 'Seleccione el rol del usuario'}),
                

        }

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre_proveedor': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del proveedor'}),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ingrese el teléfono del proveedor'}),
            'correo_electronico': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico del proveedor'}),
            'direccion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la dirección del proveedor',
                'rows': 3,
                'cols': 3}),
        }

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del producto'}),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la descripción del producto',
                'rows': 3,
                'cols': 3}),
            'unidad': forms.TextInput(attrs={
                'placeholder': 'Ingrese la unidad del producto'}),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio del producto'}),
            'stock': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el stock del producto'}),
        }
class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'producto': forms.Select(attrs={
                'placeholder': 'Seleccione el producto'}),
            'proveedor': forms.Select(attrs={
                'placeholder': 'Seleccione el proveedor'}),
            'cantidad': forms.NumberInput(attrs={
                'placeholder': 'Ingrese la cantidad de la compra'}),
            'fecha_compra': forms.DateInput(attrs={
                'placeholder': 'Ingrese la fecha de la compra',
                'type': 'date'}),
        }