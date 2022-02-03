import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import SlugField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify


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