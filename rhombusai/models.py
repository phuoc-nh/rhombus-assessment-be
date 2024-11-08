from django.db import models

class ExampleModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class FileTypeModel(models.Model):
    file = models.CharField(max_length=255)
    type = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.file