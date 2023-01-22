from django.urls import path 
from registration.views import register

urlpatterns = [
    path('',register, name="register"),
]