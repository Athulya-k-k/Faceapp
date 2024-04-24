from django.urls import path
from .views import register_user, user_login, user_logout,forgot_password
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
     path('forgotpassword/', forgot_password, name='forgot_password'),
     path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
      path('activate/<uidb64>/<token>/', views.activate, name='activate'),
       path('resetpassword/<str:uidb64>/<str:token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/', views.resetPassword, name='resetPassword'),
]