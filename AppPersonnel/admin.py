from django.contrib import admin
from .import models


admin.site.register(models.Fonction)
admin.site.register(models.Grade)
admin.site.register(models.Service)

