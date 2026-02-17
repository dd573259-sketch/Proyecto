from django.db import models
from datetime import datetime



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
    telefono = models.CharField(max_length=30)
    correo_electronico = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200)

    class Meta:
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

    tipo_de_documento = models.CharField(max_length=20, choices=TIPO_DE_DOCUMENTO, null=True)
    numero_documento = models.IntegerField(unique=True, null=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)
    direccion = models.CharField(max_length=100)
    tipo_cliente = models.CharField(max_length=20)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"



class Comanda(models.Model):
    id_comanda = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    ESTADO = [
        ("En preparación", "En preparación"),
        ("Listo", "Listo"),
        ("Entregado", "Entregado"),
    ]

    estado = models.CharField(max_length=15, choices=ESTADO, default="En preparación")

    class Meta:
        db_table = 'comanda'

    def __str__(self):
        return f"Comanda {self.id_comanda}"


class Mesa(models.Model):
    id_mesa = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero_mesa = models.IntegerField(unique=True)
    estado = models.CharField(max_length=20)
    capacidad = models.IntegerField()
    ESTADO = [
        ("En preparación", "En preparación"),
        ("Listo", "Listo"),
        ("Entregado", "Entregado"),
    ]

    estado = models.CharField(max_length=15, choices=ESTADO, default="En preparación")

    class Meta:
        db_table = 'mesa'

    def __str__(self):
        return f"Mesa {self.numero_mesa}"


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    ESTADO = [
        ("En preparación", "En preparación"),
        ("Listo", "Listo"),
        ("Entregado", "Entregado"),
    ]

    estado = models.CharField(max_length=15, choices=ESTADO, default="En preparación")

    class Meta:
        db_table = 'pedido'

    def __str__(self):
        return f"Pedido {self.id_pedido}"


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "venta"

    def __str__(self):
        return f"Venta {self.id_venta} - {self.usuario.nombre} - ${self.total_venta}"


class Factura(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)

    class Meta:
        db_table = "factura"

    def __str__(self):
        return f"Factura {self.id} - Total ${self.valor_total}"


class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "pago"

    def __str__(self):
        return f"Pago {self.id_pago} - ${self.monto}"
