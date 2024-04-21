from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import date

STATE_CHOICES = (
        ('incomplete', 'TO DO'),
        ('complete', 'Done'),
    )

METHOD_CHOICES = (
    ('cash', _('Cash')),
    ('credit_card', _('Card')),
    )

CADENCE_CHOICES = (
     ('monthly', _('Monthly')),
     ('weekly', _('Weekly')),
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
              models.UniqueConstraint(fields=['name', 'user', 'type'], name='unique_label_per_user')
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

class RecurrentRecord(models.Model):
    type = models.CharField(max_length=7, choices=Type.choices, default=Type.EXPENSE)
    date_from = models.DateField(default=now)
    date_to = models.DateField(null=True, blank=True)
    amount = models.DecimalField(decimal_places=2,  max_digits=10)
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el registro con el usuario
    method = models.CharField(max_length=12, choices=METHOD_CHOICES, default='credit_card')

    cadence_type = models.CharField(choices=CADENCE_CHOICES, default='monthly')
    cadence_position = models.IntegerField(default=1)

    last_created_date = models.DateField(null=True)
    next_create_date = models.DateField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['comment', 'user', 'type'], name='unique_recurrent_record_per_user')
        ]
