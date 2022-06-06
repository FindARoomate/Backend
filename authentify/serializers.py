from core.models import Profile
from core.serializers import ProfileSerializer
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser, Waitlist
from .utils import is_valid_email


class WaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = ["email", "name"]

    def save(self):
        email = self.validated_data["email"]
        name = self.validated_data["name"]
        Waitlist.objects.create(email=email, name=name)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = CustomUser.objects.get(id=self.user.id)
        try:
            profile = Profile.objects.get(user=user)
            profile_serializer = ProfileSerializer(profile)
            profile_data = profile_serializer.data
        except Profile.DoesNotExist:
            profile_data = []
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["request_lifetime"] = "20 minutes"
        data["data"] = {
            "id": self.user.id,
            "email": self.user.email,
            "last_login": self.user.last_login,
            "profile_data": profile_data,
        }
        user.last_login = timezone.now()
        user.save()
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    confirm_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "confirm_password",
            "last_login",
        ]

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError(
                "Those passwords don't match."
            )
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()

        return user


class ResendActivationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=225, min_length=3, validators=[is_valid_email]
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
        ]

    def validate_email(self, value):
        user = CustomUser.objects.get(email__iexact=value.lower())

        if user.is_active:
            raise ValidationError(detail="user has been activated already")
        else:
            return value


class ResetPasswordSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        min_length=2, validators=[is_valid_email]
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
        ]

    def save(self):
        email = self.validated_data["email"]

        user = self.context["request"].user

        if user.email != email:
            raise ValidationError(
                {"authorize": "You dont have permission for this user."}
            )
        else:
            return email


class ResetPasswordConfirmSerializer(serializers.ModelSerializer):

    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:

        model = CustomUser
        fields = [
            "new_password",
        ]

    def update(self, instance, validated_data):

        user = self.context["request"].user

        if user.id == instance.id:
            instance.set_password(validated_data["new_password"])

            instance.save()

            return instance
        else:
            raise ValidationError(
                {"authorize": "You dont have permission for this user."}
            )


class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    email = serializers.EmailField(max_length=225)
    message = serializers.CharField(max_length=500)
