from dataclasses import field
from django.forms import ModelForm
from app.models import *
from django import forms 
from django.forms import inlineformset_factory


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

class PlatoForm(ModelForm):
    class Meta:
        model = Plato
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del plato'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion del plato',
                    'rows': 3,
                    'cols': 3}),
        }
        
class NotificacionForm(ModelForm):
    class Meta:
        model = Notificacion
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de la notificación'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion de la notificación',
                    'rows': 3,
                    'cols': 3}),
        }
class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        widgets = {
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion del menu',
                    'rows': 3,
                    'cols': 3}),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio del menu'}),
        }
        

class RecetaForm(ModelForm):
    class Meta:
        model = Receta
        fields = ['plato']   # solo el plato si así lo tienes
        widgets = {
            'plato': forms.Select(attrs={
                'class': 'form-control'
            })
        }

class DetalleRecetaForm(ModelForm):
    class Meta:
        model = DetalleReceta
        fields = ['insumo', 'cantidad']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'})
        }

DetalleFormSet = inlineformset_factory(
    Receta,
    DetalleReceta,
    form=DetalleRecetaForm,
    extra=1,
    can_delete=True
)

class InsumosForm(ModelForm):
    class Meta:
        model = insumo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del insumo'}),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la descripcion del insumo',
                'rows': 3,
                'cols': 3}),
            'valor': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el valor del insumo'}),
        }

    # 🔹 Validaciones de NOMBRE
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if len(nombre) < 3:
            raise forms.ValidationError(
                'El nombre debe tener al menos 3 caracteres'
            )

        if nombre.isdigit():
            raise forms.ValidationError(
                'El nombre no puede ser solo números'
            )

        if nombre.startswith(' '):
            raise forms.ValidationError(
                'El nombre no puede iniciar con espacio'
            )
        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')

        if len(descripcion) < 10:
            raise forms.ValidationError(
                'La descripcion debe tener al menos 10 caracteres'
            )

        if descripcion.isdigit():
            raise forms.ValidationError(
                'La descripcion no puede ser solo números'
            )

        return descripcion

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')

        if valor is not None and valor > 10000000:
            raise forms.ValidationError(
                'El valor es demasiado alto'
            )

        return valor


    # 🔹 Validación individual de STOCK
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')

        if stock is not None and stock > 10000:
            raise forms.ValidationError(
                'El stock es demasiado alto'
            )

        return stock

    def clean(self):
        cleaned_data = super().clean()

        valor = cleaned_data.get('valor')
        stock = cleaned_data.get('stock')

        if valor is not None and valor < 0:
            self.add_error('valor', 'El valor debe ser mayor a 0')

        if stock is not None and stock < 0:
            self.add_error('stock', 'El stock no puede ser negativo')

        return cleaned_data    
    
        
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
