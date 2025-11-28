from django.db import models

# Create your models here.











































































# Modelos de Comanda, pedido, mesa, cliente
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)
    direccion = models.CharField(max_length=100)
    tipo_cliente = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'cliente'
        
class Mesa(models.Model):
    id_mesa = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    numero_mesa = models.IntegerField(unique=True)
    estado = models.CharField(max_length=20)
    capacidad = models.IntegerField()
    
    def __str__(self):
        return self.numero_mesa

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        db_table = 'mesa'
        
class Comanda(models.Model):
    id_comanda = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20)
    
    def __str__(self):
        return self.id_comanda
    
    class Meta:
        verbose_name = 'Comanda'
        verbose_name_plural = 'Comandas'
        db_table = 'comanda'
        
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    id_comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20)
    
    def __str__(self):
        return self.id_pedido
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        db_table = 'pedido'