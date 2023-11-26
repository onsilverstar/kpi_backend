from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.KPI_Measure)
admin.site.register(models.KPI_Metric)
admin.site.register(models.Reporting_Lead)
admin.site.register(models.Manager)
admin.site.register(models.Senior_Manager)
admin.site.register(models.External)
admin.site.register(models.Director)
admin.site.register(models.Department)



