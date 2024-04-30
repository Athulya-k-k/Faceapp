from django.urls import path
from .views import register_user, user_login, user_logout,forgot_password,reset_password
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<str:uidb64>/<str:token>/', reset_password, name='reset_password'),
    
]