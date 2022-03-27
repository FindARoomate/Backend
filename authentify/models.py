import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import SlugField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify

from rest_framework_simplejwt.tokens import RefreshToken

class CustomUser(AbstractUser):
    """
    custom user created with email as the username field
    """
    email = models.EmailField(_('email address'), unique=True)
    slug = SlugField(max_length=250, unique=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(CustomUser, self).save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        
    def __str__(self):
        return self.email


class BaseClass(models.Model):
    """
    Base class that contains fields other model classes will subclass from
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Waitlist(models.Model):
    """
    The waitlist model to add users that filled the waitlist form
    """
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
