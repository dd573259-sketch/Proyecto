from dataclasses import field
from django.forms import ModelForm
from app.models import Categoria, Comanda, Mesa, Pedido, Cliente
from django import forms

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'cedula': forms.TextInput(attrs={
                'placeholder': 'Ingrese la cédula del cliente'}),
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del cliente'}),
            'apellido': forms.TextInput(attrs={
                'placeholder': 'Ingrese el apellido del cliente'}),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ingrese el teléfono del cliente'}),
            'correo_electronico': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico del cliente'}),
            'direccion': forms.TextInput(attrs={
                'placeholder': 'Ingrese la dirección del cliente'}),
            'tipo_cliente': forms.Select(attrs={
                'placeholder': 'Seleccione el tipo de cliente'}),
        }
class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={
                'placeholder': 'Ingrese la fecha y hora de la comanda'}),
            'valor': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el valor del pedido'}),
            'estado': forms.Select(attrs={
                'placeholder': 'Seleccione el estado del pedido'}),
            'comanda_id': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el ID de la comanda asociada al pedido'}),
            'mesa_id': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el ID de la mesa asociada al pedido'}),
        }
class MesaForm(ModelForm):
    class Meta:
        model = Mesa
        fields = '__all__'
        widgets = {
            'numero_mesa': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el número de la mesa'}),
            'estado': forms.Select(attrs={
                'placeholder': 'Seleccione el estado de la mesa'}),
            'capacidad': forms.NumberInput(attrs={
                'placeholder': 'Ingrese la capacidad de la mesa'}),
            'cliente_id': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el ID del cliente asignado a la mesa'}),
            'menu_id': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el ID del menú asignado a la mesa'}),
        }
class ComandaForm(ModelForm):
    class Meta:
        model = Comanda
        fields = '__all__'
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={
                'placeholder': 'Ingrese la fecha y hora de la comanda'}),
            'estado': forms.Select(attrs={
                'placeholder': 'Seleccione el estado de la comanda'}),
            'usuario_id': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el ID del usuario que realiza la comanda'}),
        }
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