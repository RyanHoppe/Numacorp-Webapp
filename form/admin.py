from django.contrib import admin

# Register your models here.
from .models import MaterialsModel, ClockInModel, ClockOutModel

admin.site.register(MaterialsModel)
admin.site.register(ClockInModel)
admin.site.register(ClockOutModel)