from django.db import models
from datetime import datetime
from decimal import Decimal
from django.core.validators import MinValueValidator
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


class Pedido(models.Model):
    
    ESTADO = [
        ("Preparación", "Preparación"),
        ("Entregado", "Entregado"),
    ]
    
    id_pedido = models.AutoField(primary_key=True)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidades = models.IntegerField(validators=[MinValueValidator(1)])
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADO, default="Preparación")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        db_table = 'pedido'

    def __str__(self):
        return f"Pedido {self.id_pedido}"

    @property
    def total(self):
        return self.producto.precio * self.cantidades
    
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
        
class Menu(models.Model):
    id_menu = models.AutoField(primary_key=True)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
        db_table = "menu"


class insumo(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    unidad=models.CharField(max_length=100)
    valor=models.CharField(max_length=100)
    stock=models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    class Meta:

        verbose_name = 'insumo'
        verbose_name_plural = 'insumos'
        db_table = 'insumo'

class recetas(models.Model):
    id_receta = models.AutoField(primary_key=True)
    plato= models.CharField(max_length=100)
    nombre= models.CharField(max_length=100)
    descripcion= models.CharField(max_length=100)
    unidad= models.CharField(max_length=100)
    valor= models.CharField(max_length=100)
    stock= models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nombre}' - {self.insumo}
    
    class Meta:
        verbose_name = 'receta'
        verbose_name_plural = 'recetas'
        db_table = 'receta'

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
