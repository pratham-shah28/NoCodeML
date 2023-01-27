from django.db import models

from django.core.validators import FileExtensionValidator
class Document(models.Model):
    name = models.CharField(max_length=255, default='Document_name')
    myfile = models.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['csv', 'xlsx'])
    ])

    def __str__(self):
        return self.name