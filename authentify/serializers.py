from django.contrib import auth
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .models import CustomUser, Waitlist
from .utils import is_valid_email


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


# class LoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         max_length=255, min_length=3, validators=[is_valid_email])
#     password = serializers.CharField(
#         max_length=68, min_length=6, write_only=True)
#     tokens = serializers.SerializerMethodField()

#     def get_tokens(self, obj):
#         user = CustomUser.objects.get(email=obj['email'])

#         return {
#             'refresh': user.tokens()['refresh'],
#             'access': user.tokens()['access']
#         }

#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password', 'tokens']

#     def validate(self, attrs):
#         email = attrs.get('email', '')
#         password = attrs.get('password', '')
#         user = auth.authenticate(email=email, password=password)

#         if not user:
#             raise AuthenticationFailed('Invalid credentials, try again')

#         if not user.is_active:
#             raise ValidationError(detail='Account disabled, contact admin')

#         return {
#             'email': user.email,
#             'tokens': user.tokens
#         }

#         return super().validate(attrs)


class ResendActivationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=225, min_length=3, validators=[is_valid_email])

    class Meta:
        model = CustomUser
        fields = ['email', ]

    def validate_email(self, value):
        user = CustomUser.objects.get(email__iexact=value.lower())

        if user.is_active:
            raise ValidationError(detail="user has been activated already")
        else:
            return value


class ResetPasswordSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(min_length=2, validators=[is_valid_email])

    class Meta:
        model = CustomUser
        fields = ['email', ]

    def save(self):
        email = self.validated_data['email']

        user = self.context['request'].user

        if user.email != email:
            raise ValidationError(
                {"authorize": "You dont have permission for this user."})
        else:
            return email


class ResetPasswordConfirmSerializer(serializers.ModelSerializer):

    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:

        model = CustomUser
        fields = ['new_password', ]

    def update(self, instance, validated_data):

        user = self.context['request'].user

        if user.id == instance.id:
            instance.set_password(validated_data['new_password'])

            instance.save()

            return instance
        else:
            raise ValidationError(
                {"authorize": "You dont have permission for this user."})

class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    email = serializers.EmailField(max_length=225)
    message = serializers.CharField(max_length=500)
