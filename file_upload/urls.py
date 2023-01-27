from django.urls import path
from file_upload.views import upload

urlpatterns = [
    path('',upload, name="fileupload"),
]