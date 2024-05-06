from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def user_logout(request):
   return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)

User = get_user_model()

@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        token = PasswordResetTokenGenerator().make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f'http://127.0.0.1:5501/frontend/html/ResetPass.html?uidb64={uidb64}&token={token}'
        send_mail(
    'Reset your password',
    f'Click the link to reset your password: {reset_link}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)


        return Response({'message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and PasswordResetTokenGenerator().check_token(user, token):
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid password reset link.'}, status=status.HTTP_400_BAD_REQUEST)
