from django.contrib import admin

# Register your models here.

from .models import RegistroFinanciero,Etiqueta,Task

admin.site.register(RegistroFinanciero)
admin.site.register(Etiqueta)
admin.site.register(Task)

