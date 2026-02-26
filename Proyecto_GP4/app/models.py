from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum
# Create your models here.

#Categorias Fuertes
class Usuario(models.Model):
    ROL_OPCIONES = (
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('proveedor', 'Proveedor'),
    )

    id_usuario = models.AutoField(primary_key=True)

    TIPO_DE_DOCUMENTO = [
        ("CC", "Cédula de Ciudadanía"),
        ("TI", "Tarjeta de Identidad"),
        ("CE", "Cédula de Extranjería"),
        ("Pasaporte", "Pasaporte"),
    ]

    tipo_de_documento = models.CharField(max_length=20, choices=TIPO_DE_DOCUMENTO, null=True)
    numero_documento = models.IntegerField(unique=True, null=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo_electronico = models.CharField(max_length=150)
    contraseña = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROL_OPCIONES)
    fecha_registro = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "usuario"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)

    TIPO_DE_DOCUMENTO = [
        ("CC", "Cédula de Ciudadanía"),
        ("TI", "Tarjeta de Identidad"),
        ("CE", "Cédula de Extranjería"),
        ("Pasaporte", "Pasaporte"),
    ]

    tipo_de_documento = models.CharField(max_length=20, choices=TIPO_DE_DOCUMENTO, null=True)
    numero_documento = models.IntegerField(unique=True, null=True)
    nombre_proveedor = models.CharField(max_length=150)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        db_table = "proveedor"

    def __str__(self):
        return self.nombre_proveedor

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    unidad = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = "producto"

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    ESTADO = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO, default="activo")
    fecha_creacion = models.DateTimeField(default=datetime.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        db_table = "categoria"

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)

    TIPO_DE_DOCUMENTO = [
        ("CC", "Cédula de Ciudadanía"),
        ("TI", "Tarjeta de Identidad"),
        ("CE", "Cédula de Extranjería"),
        ("Pasaporte", "Pasaporte"),
    ]
    
    TIPO_CLIENTE = [
        ("Regular", "Regular"),
        ("VIP", "VIP"),
        ("Frecuente", "Frecuente"),
    ]

    tipo_de_documento = models.CharField(max_length=20, choices=TIPO_DE_DOCUMENTO, null=True)
    numero_documento = models.IntegerField(unique=True, null=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)
    direccion = models.CharField(max_length=100)
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE, default="Regular")
    

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        db_table = 'cliente'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Factura(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        db_table = "factura"

    def __str__(self):
        return f"Factura {self.id} - Total: {self.valor_total}"
    
#modelos debiles
class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    insumo = models.IntegerField(null=True, blank=True)
    fecha_compra = models.DateTimeField(auto_now=True)
    total_compra = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        db_table = "compra"

    def __str__(self):
        return f"Compra #{self.id_compra} {self.proveedor}{self.usuario}{self.producto} {self.insumo}"
class Mesa(models.Model):
    id_mesa = models.AutoField(primary_key=True)
    numero_mesa = models.IntegerField(unique=True)
    estado = models.CharField(max_length=20)
    ESTADO = [
        ("Disponible", "Disponible"),
        ("No disponible", "No disponible"),
    ]

    estado = models.CharField(max_length=15, choices=ESTADO, default="Disponible")

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        db_table = 'mesa'

    def __str__(self):
        return f"Mesa {self.numero_mesa}"

class Plato(models.Model):
    id_plato = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, unique=True, null=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        db_table = "plato"
        
class Pedido(models.Model):

    ESTADO = [
        ("Preparación", "Preparación"),
        ("Entregado", "Entregado"),
    ]

    id_pedido = models.AutoField(primary_key=True)
    mesa = models.ForeignKey('Mesa', on_delete=models.CASCADE, verbose_name="Mesa")
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, verbose_name="Empleado")
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    estado = models.CharField(max_length=15, choices=ESTADO, default="Preparación", verbose_name="Estado")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        db_table = 'pedido' 
        ordering = ['fecha_hora']

    def __str__(self):
        return f"Pedido #{self.id_pedido} - Mesa {self.mesa.numero_mesa} - {self.estado}"

    @property
    def total_platos(self):
        """Suma el subtotal de todos los platos: cantidad × precio de la BD."""
        return sum(detalle.subtotal for detalle in self.detalle_platos.all())

    @property
    def total_productos(self):
        #Suma el subtotal de todos los productos: cantidad × precio de la BD.
        return sum(detalle.subtotal for detalle in self.detalle_productos.all())

    @property
    def total(self):
        #Total general del pedido = total platos + total productos.
        return self.total_platos + self.total_productos


class DetallePlato(models.Model):

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalle_platos", verbose_name="Pedido")
    plato = models.ForeignKey('Plato', on_delete=models.CASCADE, verbose_name="Plato")
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Cantidad")

    class Meta:
        verbose_name = "Detalle de Plato"
        verbose_name_plural = "Detalles de Platos"
        unique_together = ('pedido', 'plato')

    def __str__(self):
        return f"{self.plato.nombre} x {self.cantidad}"

    @property
    def subtotal(self):
        """Toma el precio directamente de la BD y multiplica por la cantidad."""
        return self.cantidad * self.plato.precio

class DetallePedido(models.Model):

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalle_productos", verbose_name="Pedido")
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Cantidad")

    class Meta:
        verbose_name = "Detalle de Producto"
        verbose_name_plural = "Detalles de Productos"
        db_table = "detalle_pedido" 
        unique_together = ('pedido', 'producto')

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio
            
class Comanda(models.Model):
    id_comanda = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    ESTADO = [
        ("Preparación", "Preparación"),
        ("Entregado", "Entregado"),
    ]

    estado = models.CharField(max_length=15, choices=ESTADO, default="Preparación")

    class Meta:
        verbose_name = "Comanda"
        verbose_name_plural = "Comandas"
        db_table = 'comanda'

    def __str__(self):
        return f"Comanda {self.id_comanda}"


        
class Menu(models.Model):
    id_menu = models.AutoField(primary_key=True)

    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        if self.plato:
            return self.plato.nombre
        elif self.producto:
            return self.producto.nombre
        return "Menu vacío"

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
        db_table = "menu"



class insumo(models.Model):

    UNIDAD_OPCIONES = [
        ("kg", "Kilogramo (kg)"),
        ("g", "Gramo (g)"),
        ("l", "Litro (L)"),
        ("ml", "Mililitro (ml)"),
        ("m", "Metro (m)"),
        ("cm", "Centímetro (cm)"),
        ("unidad", "Unidad"),
    ]

    id_insumo = models.AutoField(primary_key=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=100)
    unidad = models.CharField( max_length=20, choices=UNIDAD_OPCIONES, default="unidad")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'insumo'
        verbose_name_plural = 'insumos'
        db_table = 'insumo'

class Receta(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name='recetas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receta de {self.plato.nombre}"
        @property
        def costo_total(self):
            return sum(
                detalle.cantidad * detalle.insumo.valor
                for detalle in self.detalles.all()
            )

    class Meta:
        db_table = 'receta'
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'

class DetalleReceta(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='detalles')
    insumo = models.ForeignKey(insumo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.insumo.nombre} - {self.cantidad}"

    class Meta:
        db_table = 'detalle_receta'
        unique_together = ('receta', 'insumo')
        verbose_name = 'Detalle Receta'
        verbose_name_plural = 'Detalles Recetas'

class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    insumo = models.ForeignKey(insumo, on_delete=models.CASCADE, null=True, blank=True)
    tipo_notificacion = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notificacion {self.id} - {self.tipo_notificacion}"

    class Meta:
        verbose_name = "notificacion"
        verbose_name_plural = "notificaciones"
        db_table = "notificacion"

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        db_table = "venta"

    def __str__(self):
        return f"Venta {self.id_venta} - {self.usuario.nombre} - ${self.total_venta}"

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"   
        db_table = "pago"

    def __str__(self):
        return f"Pago {self.id_pago} - ${self.monto}"
