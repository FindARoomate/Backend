from cloudinary.models import CloudinaryField

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import SlugField
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    custom user created with email as the username field
    """

    email = models.EmailField(_("email address"), unique=True)
    slug = SlugField(max_length=250, unique=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

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

    class Meta:
        abstract = True
        get_latest_by = "updated_at"
        ordering = ("-updated_at", "-created_at")


class Waitlist(BaseClass):
    """
    The waitlist model to add users that filled the waitlist form
    """

    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.email


class Profile(BaseClass):

    GENDER = (
        ("male", "male"),
        ("female", "female"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=250, blank=True)
    image = CloudinaryField("image")
    religion = models.CharField(max_length=250, blank=True)
    gender = models.CharField(max_length=250, blank=True, choices=GENDER)
    phone_number = models.IntegerField()
    personality = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.user.username} Profile"

