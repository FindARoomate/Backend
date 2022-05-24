from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import SlugField
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    custom user created with email as the username field
    """

    username = None
    email = models.EmailField(_("email address"), unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Waitlist(models.Model):
    """
    The waitlist model to add users that filled the waitlist form
    """

    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=250, null=True)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.email
