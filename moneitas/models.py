from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django
from django.utils.translation import gettext_lazy as _



STATE_CHOICES = (
        ('incomplete', 'TO DO'),
        ('complete', 'Done'),
    )

METHOD_CHOICES = (
    ('cash', _('Cash')),
    ('credit_card', _('Card')),
    )

class Type(models.TextChoices):
        INCOME = 'income', _('Income')
        EXPENSE = 'expense', _('Expense')

class Label(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=7, choices=Type.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el registro con el usuario

    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
         constraints = [
              models.UniqueConstraint(fields=['name', 'user'], name='unique_label_per_user')
         ]

class FinancialRecord(models.Model):
    type = models.CharField(max_length=7, choices=Type.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el registro con el usuario
    method = models.CharField(max_length=12, choices=METHOD_CHOICES, default='credit_card')
    income_paid = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username}: {self.get_type_display()}: {self.amount} - {self.date}"


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES)

    def __str__(self):
        return f"{self.name}"
