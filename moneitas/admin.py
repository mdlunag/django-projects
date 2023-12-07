from django.contrib import admin

# Register your models here.

from .models import RegistroFinanciero,Label,Task

admin.site.register(RegistroFinanciero)
admin.site.register(Label)
admin.site.register(Task)

