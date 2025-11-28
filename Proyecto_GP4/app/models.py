from django.db import models

# Create your models here.














































































































































#---------------------------------------------------------------------------------
#notificacion, insumo,receta A CARGO DE ELKIN 

class insumo(models.Model):
    categoria = models.CharField(max_length=100)
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

class recetas(models.model):
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
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    insumo = models.ForeignKey(insumo, on_delete=models.CASCADE, null=True, blank=True)
    tipo_notificacion = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notificación {self.id} - {self.tipo_notificacion}"

    class Meta:
        verbose_name = "notificacion"
        verbose_name_plural = "notificaciones"
        db_table = "notificacion"
