from dataclasses import field
from django.forms import ModelForm
from app.models import *
from django import forms 
import re
from django import forms
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError



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
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del usuario'}),
            'apellido': forms.TextInput(attrs={
                'placeholder': 'Ingrese el apellido del usuario'}),
            'correo_electronico': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico del usuario'}),
            'rol': forms.Select(attrs={
                'placeholder': 'Seleccione el rol del usuario'}),
            'contrasena': forms.PasswordInput(attrs={
                'placeholder': 'Ingrese la contraseña del usuario'}),
            'numero_documento': forms.TextInput(attrs={
                'placeholder': 'Ingrese el número de documento del usuario'}),
            'contrasena_actual': forms.PasswordInput(attrs={
                'placeholder': 'Ingrese la contraseña actual del usuario'}),
    
        }
    def clean_nombre(self): 
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios')
        return nombre
    
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if len(apellido) < 3:
            raise forms.ValidationError('El apellido debe tener al menos 3 caracteres')
        if not re.match(r'^[a-zA-Z\s]+$', apellido):
            raise forms.ValidationError('El apellido solo puede contener letras y espacios')   
        return apellido

    def clean_correo_electronico(self):
        correo = self.cleaned_data.get('correo_electronico')

        if not correo:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
        correo = correo.lower().strip()
        usuarios = Usuario.objects.filter(correo_electronico__iexact=correo)
        if self.instance.pk:
            usuarios = usuarios.exclude(pk=self.instance.pk)
        if usuarios.exists():
            raise forms.ValidationError("El correo electrónico ya está registrado.")
        return correo
    
    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        if len(contrasena) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', contrasena):
            raise forms.ValidationError('La contraseña debe contener al menos una letra mayúscula')

        if not re.search(r'[a-z]', contrasena):
            raise forms.ValidationError('La contraseña debe contener al menos una letra minúscula')

        if not re.search(r'[0-9]', contrasena):
            raise forms.ValidationError('La contraseña debe contener al menos un número')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contrasena):
            raise forms.ValidationError('La contraseña debe contener al menos un carácter especial')

        if re.search(r'(.)\1{3,}', contrasena):
            raise forms.ValidationError('La contraseña no puede contener caracteres repetidos más de 3 veces')

        if contrasena in ['123456', 'password', 'qwerty', 'admin123']:
            raise forms.ValidationError('La contraseña es demasiado común')
        
        return contrasena
    
    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get('numero_documento')
        if not re.match(r'^[0-9]+$', numero_documento):
            raise forms.ValidationError('El número de documento solo puede contener números')
        if len(numero_documento) < 10:
            raise forms.ValidationError('El número de documento debe tener al menos 10 caracteres') 
        return numero_documento

    
    
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
            'numero_documento': forms.TextInput(attrs={
                'placeholder': 'Ingrese el número de documento del proveedor'}),
        }

    def clean_nombre_proveedor(self):
        nombre = (self.cleaned_data.get('nombre_proveedor') or "").strip()

        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')

        if len(nombre) < 3:
            raise forms.ValidationError('El nombre del proveedor debe tener al menos 3 caracteres')
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\.\-&]+$', nombre):
            raise forms.ValidationError('El nombre contiene caracteres no permitidos')

        return nombre

    def clean_telefono(self):
        telefono = (self.cleaned_data.get('telefono') or "").strip()

        if not telefono:
            raise forms.ValidationError('El teléfono es obligatorio.')

        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono solo puede contener números')

        if len(telefono) < 10:
            raise forms.ValidationError('El teléfono debe tener al menos 10 caracteres')

        return telefono

    def clean_correo_electronico(self):
        correo = (self.cleaned_data.get('correo_electronico') or "").strip().lower()

        if not correo:
            raise forms.ValidationError('El correo electrónico es obligatorio.')

        proveedores = Proveedor.objects.filter(correo_electronico__iexact=correo)
        if self.instance.pk:
            proveedores = proveedores.exclude(pk=self.instance.pk)

        if proveedores.exists():
            raise forms.ValidationError('El correo electrónico ya está registrado.')

        return correo

    def clean_direccion(self):
        direccion = (self.cleaned_data.get('direccion') or "").strip()

        if len(direccion) < 10:
            raise forms.ValidationError('La dirección debe tener al menos 10 caracteres')

        return direccion

    def clean_numero_documento(self):
        numero = (self.cleaned_data.get('numero_documento') or "").strip()

        if not numero.isdigit():
            raise forms.ValidationError('El número de documento debe contener solo números.')

        return numero

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
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio del producto'}),
            'stock': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el stock del producto'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date',}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date',
                'placeholder': 'Ingrese la fecha de vencimiento del producto'}),
        }

    def clean_nombre(self):
        nombre = (self.cleaned_data.get('nombre') or "").strip()
        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')

        if len(nombre) < 3:
            raise forms.ValidationError('El nombre del producto debe tener al menos 3 caracteres')

        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\.\-&]+$', nombre):
            raise forms.ValidationError('El nombre contiene caracteres no permitidos')
        return nombre

    def clean_descripcion(self):
        descripcion = (self.cleaned_data.get('descripcion') or "").strip()

        if not descripcion:
            raise forms.ValidationError('La descripción es obligatoria.')

        if len(descripcion) < 5:
            raise forms.ValidationError('La descripción debe tener al menos 5 caracteres')
        return descripcion



    def clean_precio(self):
        precio = self.cleaned_data.get('precio')

        if precio is None:
            raise forms.ValidationError('El precio es obligatorio.')

        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')
        return precio

    def clean(self):
        cleaned_data = super().clean()

        fecha_ingreso = cleaned_data.get('fecha_ingreso')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')

        if fecha_vencimiento and fecha_ingreso:
            if fecha_vencimiento <= fecha_ingreso:
                self.add_error('fecha_vencimiento', 'La fecha de vencimiento debe ser posterior a la fecha de ingreso.')
        return cleaned_data

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
