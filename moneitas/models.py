from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django

TIPO_CHOICES = (
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    )

STATE_CHOICES = (
        ('incomplete', 'TO DO'),
        ('complete', 'Done'),
    )

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el registro con el usuario

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class RegistroFinanciero(models.Model):
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE, blank=True, null=True)
    nota = models.TextField(blank=True, null=True)
    eliminar = models.BooleanField(default=False)  # Campo para identificar registros a eliminar
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el registro con el usuario


    def __str__(self):
        return f"{self.user.username}: {self.get_tipo_display()}: {self.monto} - {self.fecha}"


class Task(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES)

    def __str__(self):
        return f"{self.nombre}"