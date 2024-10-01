from django.db import models
from picklefield.fields import PickledObjectField
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator

class registrationform(UserCreationForm):
    email = forms.EmailField(
        required = True,
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class Document(models.Model):
    #user = form.cleaned_data.get('username')
    name = models.CharField(max_length=255, default='Document name')
    myfile = models.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['csv', 'xlsx'])
    ])
    
    username = models.CharField(max_length=50, editable=False)

    def __str__(self):
        return self.name
    
class PickleModels(models.Model):
    pickle_model = models.FileField()
    username = models.CharField(max_length=50)