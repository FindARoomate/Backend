from django.forms import ValidationError
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser, Waitlist

class WaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = ['email']

    def save(self):
        email = self.validated_data['email']
        Waitlist.objects.create(email=email)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', ]  # 'password2']

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],

        )

        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise ValidationError(detail='Account disabled, contact admin')

        try:
            user = CustomUser.objects.get(email__iexact=email.lower())
        except CustomUser.DoesNotExist:
            raise ValidationError(
                detail="No Account associated with this email")

        return {
            'email': user.email,
            'tokens': user.tokens
        }

        return super().validate(attrs)
