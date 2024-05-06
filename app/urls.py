from django.urls import path
from .views import upload_and_recognize

urlpatterns = [
    path('upload_and_recognize/', upload_and_recognize, name='upload_and_recognize'),
]
