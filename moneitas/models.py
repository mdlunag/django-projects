from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django
from django.utils.translation import gettext_lazy as _


TYPE_CHOICES = (
        (_('income'), _('Income')),
        (_('expense'), _('Expense')),
    )

STATE_CHOICES = (
        ('incomplete', 'TO DO'),
        ('complete', 'Done'),
    )

METHOD_CHOICES = (
    ('cash', _('Cash')),
    ('credit_card', _('Card')),
    )

class Label(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el registro con el usuario

    def __str__(self):
        return f"{self.name} ({self.type})"

class RegistroFinanciero(models.Model):
    tipo = models.CharField(max_length=7, choices=TYPE_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    label = models.ForeignKey(Label, on_delete=models.CASCADE, blank=True, null=True)
    nota = models.TextField(blank=True, null=True)
    eliminar = models.BooleanField(default=False)  # Campo para identificar registros a eliminar
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el registro con el usuario
    metodo = models.CharField(max_length=12, choices=METHOD_CHOICES, default='cash')


    def __str__(self):
        return f"{self.user.username}: {self.get_tipo_display()}: {self.monto} - {self.fecha}"


class Task(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES)

    def __str__(self):
        return f"{self.nombre}"