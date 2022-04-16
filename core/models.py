from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models
from django.utils import timezone

from .enums import Gender, Personality, Religion


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


class Profile(BaseClass):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    fullname = models.CharField(max_length=250, blank=True)
    image = CloudinaryField("image")
    religion = models.CharField(
        max_length=250, blank=True, choices=Religion.choices
    )
    gender = models.CharField(
        max_length=250, blank=True, choices=Gender.choices
    )
    phone_number = models.IntegerField(null=True)
    date_of_birth = models.DateTimeField(default=timezone.now)
    personality = models.CharField(
        max_length=250, choices=Personality.choices
    )
    profession = models.CharField(max_length=250)
    bio = models.TextField(max_length=250)
    age = models.IntegerField()
    roomate_description = models.TextField(max_length=250)

    def __str__(self):
        return f"{self.user} Profile"
