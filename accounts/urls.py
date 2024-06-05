from django.urls import path
from .views import register_user, register_staff
from . import views

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('register-staff/', register_staff, name='register_staff_user'),
     path('register-vendor/', views.register_vendor, name='register_vendor'),
    path('login/', views.user_login, name='user_login'),
     path('registered-users/', views.registered_users_list, name='registered_users_list'), 
    path('create-user/', views.create_user, name='create_user'),
  
    path('get-user/<int:user_id>/', views.get_user, name='get_user'),
    path('update-user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    
    
]
