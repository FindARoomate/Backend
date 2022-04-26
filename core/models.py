import cloudinary
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    country = models.CharField(max_length=250, null=True)
    state = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=250, null=True)
    street_address = models.CharField(max_length=250, null=True)
    room_type = models.CharField(max_length=250, null=True)
    no_of_persons = models.IntegerField()
    no_of_current_roomies = models.IntegerField()
    amenities = ArrayField(
        models.CharField(max_length=250, null=True), size=12
    )
    date_to_move = models.DateTimeField(default=timezone.now)
    yearly_rent = models.DecimalField(max_digits=100, decimal_places=2)
    additional_cost = models.CharField(max_length=250, null=True)
    listing_title = models.CharField(max_length=250, null=True)
    additional_information = models.CharField(max_length=250, null=True)


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
