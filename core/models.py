import http.client
import json
import urllib.parse

import cloudinary
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone

from .enums import ConnectionStatus, Gender, Personality, Religion
from .managers import SoftDeletionManager


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

class SoftDeleteBaseModel(models.Model):

    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, hard=False):
        if hard:
            super(SoftDeleteBaseModel, self).delete()
        else:
            self.deleted_at = timezone.now()
            self.save()

    def restore(self):
        self.deleted_at = None
        self.save()



class Profile(BaseClass):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    profile_picture = CloudinaryField(
        "image",
    )
    fullname = models.CharField(
        max_length=250,
        blank=True,
    )
    religion = models.CharField(
        max_length=250,
        blank=True,
        choices=Religion.choices,
    )
    gender = models.CharField(
        max_length=250,
        blank=True,
        choices=Gender.choices,
    )
    phone_number = models.CharField(
        max_length=23,
    )
    personality = models.CharField(
        max_length=250,
        choices=Personality.choices,
    )
    profession = models.CharField(
        max_length=250,
    )
    bio = models.TextField(
        max_length=250,
    )
    age_range = models.CharField(
        max_length=250,
    )
    roomie_gender = models.CharField(
        max_length=250,
        choices=Gender.choices,
    )
    roomie_religion = models.CharField(
        max_length=250,
        choices=Religion.choices,
    )
    roomie_personality = models.CharField(
        max_length=250,
        choices=Personality.choices,
    )
    roomie_age = models.CharField(max_length=200)
    roomate_description = models.TextField(
        max_length=250,
    )

    def __str__(self):
        return f"{self.user} Profile"

    @property
    def image_url(self):
        return (
            f"https://res.cloudinary.com/dczoldewu/{self.profile_picture}"
        )


class RoomateRequest(BaseClass):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="roomate_request"
    )
    country = models.CharField(
        max_length=250,
    )
    state = models.CharField(
        max_length=250,
    )
    city = models.CharField(
        max_length=250,
    )
    street_address = models.CharField(
        max_length=250,
    )
    room_type = models.CharField(
        max_length=250,
    )
    no_of_persons = models.IntegerField()
    no_of_current_roomies = models.IntegerField()
    amenities = ArrayField(
        models.CharField(max_length=250),
        size=12,
    )
    date_to_move = models.DateField(
        default=timezone.now,
    )
    rent_per_person = models.DecimalField(
        max_digits=100,
        decimal_places=2,
    )
    additional_cost = models.CharField(max_length=250)
    listing_title = models.CharField(max_length=250)
    additional_information = models.CharField(max_length=250)
    latitude = models.DecimalField(
        max_digits=200,
        decimal_places=10,
    )
    longitude = models.DecimalField(
        max_digits=200,
        decimal_places=10,
    )
    is_active = models.BooleanField()

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

        return latitude, longitude

    def save(self, *args, **kwarg):
        latitude, longitude = self.get_lat_and_long()
        self.latitude = latitude
        self.longitude = longitude
        super(RoomateRequest, self).save(*args, **kwarg)


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
    cloudinary.uploader.destroy(instance.image_file.public_id)


class Connection(BaseClass, SoftDeleteBaseModel):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sender",
        default=None,
    )
    reciever = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reciever",
        default=None,
    )
    roomate_request = models.ForeignKey(
        RoomateRequest,
        on_delete=models.CASCADE,
        related_name="connections",
    )
    status = models.CharField(
        max_length=100,
        choices=ConnectionStatus.choices,
        default=ConnectionStatus.PENDING,
    )

class Notification(BaseClass, SoftDeleteBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, related_name="connections")
    title = models.CharField(max_length=250)
    content = models.CharField(max_length=250)
    is_read = models.BooleanField(default=False)
