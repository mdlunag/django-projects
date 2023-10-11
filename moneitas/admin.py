from django.contrib import admin

# Register your models here.

from .models import RegistroFinanciero,Etiqueta

admin.site.register(RegistroFinanciero)
admin.site.register(Etiqueta)

