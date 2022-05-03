import http.client
import json
import urllib.parse

import cloudinary
import requests
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
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
    fullname = models.CharField(max_length=250, blank=True, null=True)
    religion = models.CharField(
        max_length=250, blank=True, choices=Religion.choices, null=True
    )
    gender = models.CharField(
        max_length=250, blank=True, choices=Gender.choices, null=True
    )
    phone_number = models.CharField(max_length=23, null=True)
    date_of_birth = models.DateTimeField(default=timezone.now)
    personality = models.CharField(
        max_length=250, choices=Personality.choices, null=True
    )
    profession = models.CharField(max_length=250, null=True)
    bio = models.TextField(max_length=250, null=True)
    age = models.IntegerField(null=True)
    roomie_gender = models.CharField(
        max_length=250, choices=Gender.choices, null=True
    )
    roomie_religion = models.CharField(
        max_length=250, choices=Religion.choices, null=True
    )
    roomie_personality = models.CharField(
        max_length=250, choices=Personality.choices, null=True
    )
    roomie_age = models.IntegerField(null=True)
    roomate_description = models.TextField(max_length=250, null=True)

    def __str__(self):
        return f"{self.user} Profile"


class ProfileImage(BaseClass):

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    image = CloudinaryField("image")


class RoomateRequest(BaseClass):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE
    )
    country = models.CharField(max_length=250, null=True)
    state = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=250, null=True)
    street_address = models.CharField(max_length=250, null=True)
    room_type = models.CharField(max_length=250, null=True)
    no_of_persons = models.IntegerField(null=True)
    no_of_current_roomies = models.IntegerField(null=True)
    amenities = ArrayField(
        models.CharField(max_length=250, null=True), size=12
    )
    date_to_move = models.DateTimeField(default=timezone.now, null=True)
    rent_per_person = models.DecimalField(
        max_digits=100, decimal_places=2, null=True
    )
    additional_cost = models.CharField(max_length=250, null=True)
    listing_title = models.CharField(max_length=250, null=True)
    additional_information = models.CharField(max_length=250, null=True)
    is_active = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"{self.profile} Request"

    def get_lat_and_long(self):
        ACCESS_KEY = settings.POSITION_ACCESS_KEY
        conn = http.client.HTTPConnection("api.positionstack.com")
        params = urllib.parse.urlencode(
            {
                "query": str(self.street_address)
                + str(self.city)
                + str(self.state)
                + str(self.country),
                "access_key": ACCESS_KEY,
                "limit": 1,
            }
        )
        conn.request("GET", "/v1/forward?{}".format(params))
        res = conn.getresponse()
        data = res.read()
        result = data.decode("utf-8")
        result = json.loads(result)
        latitude = result["data"][0]["latitude"]
        longitude = result["data"][0]["longitude"]
        result = [latitude, longitude]

        return result

    @property
    def latitude(self):

        response = self.get_lat_and_long()

        return response[0]

    @property
    def longitude(self):

        response = self.get_lat_and_long()

        return response[1]


class RequestImages(BaseClass):
    request = models.ForeignKey(
        RoomateRequest,
        on_delete=models.CASCADE,
        related_name="images",
        null=False,
    )
    image_file = CloudinaryField("image")

    @property
    def image_url(self):
        return f"https://res.cloudinary.com/dczoldewu/{self.image_file}"


# delete image(s) from cloudinary on model's deletion
@receiver(pre_delete, sender=RequestImages)
def photo_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.image_field.public_id)
