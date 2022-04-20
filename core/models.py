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


class ProfileImage(BaseClass):

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    image = CloudinaryField("image")

class RoomateRequest(BaseClass):

    state = models.CharField()
    city = models.CharField()
    street_address = models.CharField()
    room_type = models.CharField()
    no_of_persons = models.CharField()
    no_of_current_roomies = models.CharField()
    no_of_roomies_needed = models.CharField()
    amenities = models.CharField()
    date_to_move = models.CharField()
    yearly_rent = models.CharField()
    listing_title = models.CharField()
    additional_information = models.CharField()

class ListingImage(BaseClass):
    pass
