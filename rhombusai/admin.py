from django.contrib import admin
from .models import ExampleModel, FileTypeModel
# Register your models here.
admin.site.register(ExampleModel)
admin.site.register(FileTypeModel)