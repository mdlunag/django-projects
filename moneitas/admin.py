from django.contrib import admin

# Register your models here.

from .models import FinancialRecord,Label,Task, RecurrentRecord

admin.site.register(FinancialRecord)
admin.site.register(Label)
admin.site.register(Task)
admin.site.register(RecurrentRecord)

