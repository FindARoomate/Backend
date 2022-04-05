import email
from .models import CustomUser
from rest_framework.exceptions import ValidationError


def is_valid_email(value):
    try:
        CustomUser.objects.get(email__iexact=value.lower())
    except CustomUser.DoesNotExist:
        raise ValidationError(detail="No Account associated with this email")
