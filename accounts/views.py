from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .models import CustomUser
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .utils import CustomJWTAuthentication

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

@api_view(['POST'])
def forgot_password(request):
    if request.method == 'POST':
        serializer = ForgotPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset email has been sent to your email address"})
      
        return Response({"message": "There is no account with this email id"})

User = get_user_model()

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')  
    else:
       
        return HttpResponse('Activation link is invalid or expired.')

def resetpassword_validate(request, uidb64, token):
    try:
       
        uid = urlsafe_base64_decode(uidb64).decode()
       
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('login')

@api_view(['POST'])
def resetPassword(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data['password']
        confirm_password = serializer.validated_data['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            try:
                user = User.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successfully')
                return JsonResponse({'message': 'Password reset successfully', 'success': True})
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return JsonResponse({'error': 'User does not exist.', 'success': False}, status=400)
        else:
            messages.error(request, 'Passwords do not match!')
            return JsonResponse({'error': 'Passwords do not match.', 'success': False}, status=400)
    else:
        return JsonResponse(serializer.errors, status=400) 


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
def homepage(request):

    return Response({'message': 'Welcome to the homepage'})
