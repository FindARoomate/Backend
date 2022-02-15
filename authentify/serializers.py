from rest_framework import serializers

from .models import Waitlist


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
        value, created = Waitlist.objects.get_or_create(email=email)
        return value