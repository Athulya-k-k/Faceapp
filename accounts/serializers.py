from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site




class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'mobile', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove 'confirm_password' from validated data
        user = CustomUser.objects.create_user(**validated_data)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Check if the provided email address exists in the database.
        """
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Account does not exist!")
        return value

    def create(self, validated_data):
        """
        Send the reset password email.
        """
        email = validated_data['email']
        user = CustomUser.objects.get(email=email)

        # Send reset password email
        current_site = get_current_site(self.context['request'])
        mail_subject = 'Reset your password'
        message = render_to_string('account_verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(mail_subject, message, 'from@example.com', [email])

        return user
    
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()