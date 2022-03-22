from rest_framework import serializers
from django.core.mail import send_mail
from FindARoomate.settings import EMAIL_HOST_USER
from .models import CustomUser, Waitlist


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

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']