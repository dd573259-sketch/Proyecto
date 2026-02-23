from dataclasses import field
from django.forms import ModelForm
from app.models import *
from django import forms 
from django.contrib.auth.hashers import make_password



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
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del menu'}),
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
        model = recetas
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de la receta'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion de la receta',
                    'rows': 3,
                    'cols': 3}),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio de la receta'}),
        }

class InsumosForm(ModelForm):
    class Meta:
        model = insumo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del insumo'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion del insumo',
                    'rows': 3,
                    'cols': 3}),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio del insumo'}),
        }
    def clean_nombre(self):
            nombre = self.cleaned_data.get('nombre')
            if len(nombre) < 3:
                raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
            return nombre 
    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        if len(descripcion) <10:
            raise forms.ValidationError('La descripcion debe tener al menos 10 caracteres')
        return descripcion
    
    def clean(self):
        cleaned_data  = super().clean()
        unidad = self.cleaned_data.get('unidad')
        valor = self.cleaned_data.get('valor')
        if int(unidad) < 0 or int(valor) < 0:
            raise forms.ValidationError("El valor y la unidad debe ser mayor a 0")
        return unidad
        
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
            'numero_documento': forms.TextInput(attrs={
                'placeholder': 'Ingrese el número de documento del usuario'
            }),
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del usuario'
            }),
            'apellido': forms.TextInput(attrs={
                'placeholder': 'Ingrese el apellido del usuario'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico del usuario'
            }),
            'rol': forms.Select(attrs={
                'placeholder': 'Seleccione el rol del usuario'
            }),
            'contraseña': forms.PasswordInput(attrs={
                'placeholder': 'Ingrese la contraseña'
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio")

        if len(nombre) < 3:
            raise forms.ValidationError(
                "El nombre debe tener al menos 3 caracteres"
            )

        if not nombre.isalpha():
            raise forms.ValidationError(
                "El nombre solo puede contener letras"
            )

        return nombre


    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')

        if not apellido:
            raise forms.ValidationError("El apellido es obligatorio")

        if len(apellido) < 2:
            raise forms.ValidationError(
                "El apellido debe tener al menos 2 caracteres"
            )

        if not apellido.isalpha():
            raise forms.ValidationError(
                "El apellido solo puede contener letras"
            )

        return apellido


    def clean_numero_documento(self):
        numero = self.cleaned_data.get("numero_documento")

        if not numero:
            raise forms.ValidationError(
                "El número de documento es obligatorio"
            )


        if len(str(numero)) < 10:
            raise forms.ValidationError(
                "El número de documento debe tener al menos 10 dígitos"
            )

        return numero


    def clean_contraseña(self):
        contraseña = self.cleaned_data.get('contraseña')
        errores = []

        if not contraseña:
            errores.append("La contraseña es obligatoria")
        else:
            if len(contraseña) < 8:
                errores.append("La contraseña debe tener al menos 8 caracteres")

            tiene_mayuscula = False
            tiene_minuscula = False
            tiene_numero = False

            for c in contraseña:
                if c.isupper():
                    tiene_mayuscula = True
                if c.islower():
                    tiene_minuscula = True
                if c.isdigit():
                    tiene_numero = True

            if not tiene_mayuscula:
                errores.append("Debe contener al menos una letra mayúscula en la contraseña")

            if not tiene_minuscula:
                errores.append("Debe contener al menos una letra minúscula en la contraseña")

            if not tiene_numero:
                errores.append("Debe contener al menos un número la contraseña")

        if errores:
            raise forms.ValidationError(errores)

        return make_password(contraseña)

    
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
