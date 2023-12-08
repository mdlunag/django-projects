from django.contrib import admin

# Register your models here.

from .models import FinancialRecord,Label,Task

admin.site.register(FinancialRecord)
admin.site.register(Label)
admin.site.register(Task)

