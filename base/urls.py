
from django.urls import path 
from base.views import register,upload

urlpatterns = [
    path('',register, name="register"),
    #path('',upload,name='upload')
]