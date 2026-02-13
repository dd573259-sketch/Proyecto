from dataclasses import field
from django.forms import ModelForm
from app.models import Categoria
from app.models import Factura
from app.models import Venta
from app.models import Pago
from django import forms 


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
        
class FacturaForm(ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        widgets = {
            'valor_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el valor total'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('Efectivo', 'Efectivo'),
                ('Tarjeta', 'Tarjeta'),
                ('Transferencia', 'Transferencia'),
            ])
        }

class VentaForm(ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'
        
        widgets = {
            'usuario': forms.Select(attrs={
                'class': 'form-control'
            }),
            'pedido': forms.Select(attrs={
                'class': 'form-control'
            }),
            'total_venta': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }
        
class PagoForm(ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'
        widgets = {
            'venta': forms.Select(attrs={
                'class': 'form-control'
            }),
            'factura': forms.Select(attrs={
                'class': 'form-control'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }
