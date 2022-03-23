from rest_framework import serializers

from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage

from FindARoomate.settings import EMAIL_HOST_USER
from .models import CustomUser, Waitlist
from .tokens import account_activation_token

class WaitlistSerializer(serializers.ModelSerializer):
    message = "email successfully submitted"

    class Meta:
        model = Waitlist
        fields = ['email']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["message"] = self.message
        return representation

    def save(self):
        data = self.validated_data
        email = data['email']
        subject = "Thanks for joining!"
        message = "You have successfully joined the find a roomate waitlist"
        send_mail(subject,
                  message,
                  EMAIL_HOST_USER,
                  [email],
                  fail_silently=False)
        value, created = Waitlist.objects.get_or_create(email=email)
        return value

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    #password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', ]#'password2']

        # def validate(self, attrs):
        #     if attrs['password'] != attrs['password2']:
        #         raise serializers.ValidationError({"message": "Password fields do no match"})
        #     return attrs

        def create(self, validated_data):
            user = CustomUser.objects.create(
                username = validated_data['username'],
                email = validated_data['email'],

            )

            user.set_password(validated_data['password'])
            user.save()

            return user 
