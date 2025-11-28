from django.db import models
from datetime import datetime
from decimal import Decimal

# Create your models here.

class Usuario(models.Model):
    ROL_OPCIONES = (
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('proveedor', 'Proveedor'),
    )

    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo_electronico = models.CharField(max_length=150)
    contraseña = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROL_OPCIONES)
    fecha_registro = models.DateTimeField()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30)
    correo_electronico = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

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

    def __str__(self):
        return self.nombre



class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_insumo = models.IntegerField(null=True, blank=True)
    fecha_compra = models.DateTimeField()
    total_compra = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return f"Compra #{self.id_compra}"

