from authentify.models import CustomUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (
    Connection,
    Notification,
    Profile,
    RequestImages,
    RoomateRequest,
)

# class ImageSerializer(serializers.ModelSerializer):
#     image_url = serializers.ReadOnlyField()

#     class Meta:
#         model = ProfileImage
#         fields = ["image_url"]


class ProfileSerializer(serializers.ModelSerializer):

    image_url = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "fullname",
            "religion",
            "gender",
            "phone_number",
            "personality",
            "date_of_birth",
            "profession",
            "bio",
            "profile_picture",
            "age_range",
            "image_url",
            "roomie_gender",
            "roomie_personality",
            "roomie_age",
            "roomie_religion",
            "roomate_description",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"created_at": {"read_only": True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("profile_picture")

        return representation

    def create(self, validated_data):
        current_user = self.context["request"].user
        user = CustomUser.objects.get(email__iexact=current_user.email)

        if Profile.objects.filter(user=user).exists():
            raise ValidationError(
                {"detail": "Profile with this user already exists"}
            )
        else:

            profile = Profile.objects.create(user=user, **validated_data)

            return profile


class RequestImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = RequestImages
        fields = ["image_url"]


class RoomateRequestSerializer(serializers.ModelSerializer):

    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    request_images = RequestImageSerializer(
        many=True, read_only=True, source="images"
    )
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = RoomateRequest
        fields = [
            "id",
            "profile",
            "country",
            "state",
            "city",
            "street_address",
            "latitude",
            "longitude",
            "room_type",
            "date_to_move",
            "no_of_persons",
            "no_of_current_roomies",
            "amenities",
            "rent_per_person",
            "additional_cost",
            "request_images",
            "listing_title",
            "additional_information",
            "is_active",
            "profile",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "profile": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.context["request"].user
        images_data = self.context.get("request").FILES

        try:

            profile = Profile.objects.select_related("user").get(user=user)

            roomate_request = RoomateRequest.objects.create(
                profile=profile, **validated_data
            )
            roomate_request.is_active = True
            roomate_request.save()

            for image_data in images_data.getlist("request_images"):
                RequestImages.objects.create(
                    request=roomate_request, image_file=image_data
                )
            return roomate_request

        except Profile.DoesNotExist:
            return serializers.ValidationError(
                detail="no profile created for the logged in user"
            )


class ConnectionSerializer(serializers.ModelSerializer):
    roomate_request = RoomateRequestSerializer(read_only=True)
    request_id = serializers.IntegerField(write_only=True)
    sender_data = serializers.SerializerMethodField()

    def get_sender_data(self, obj):
        sender_data = Profile.objects.filter(user=obj.sender)
        data = ProfileSerializer(sender_data, many=True).data
        return data

    class Meta:
        model = Connection
        fields = [
            "id",
            "sender",
            "reciever",
            "roomate_request",
            "request_id",
            "sender_data",
            "status",
            "created_at",
        ]
        extra_kwargs = {
            "sender": {"read_only": True},
            "reciever": {"read_only": True},
        }

    def create(self, validated_data):

        sender = self.context["request"].user
        request_id = validated_data["request_id"]
        roomate_request = RoomateRequest.objects.get(id=request_id)
        reciever = CustomUser.objects.get(
            id=roomate_request.profile.user.id
        )

        if Connection.objects.filter(
            sender=sender, roomate_request=roomate_request
        ).exists():
            raise ValidationError(
                {
                    "detail": "You have sent a connection to this request already"
                }
            )

        if sender.id == reciever.id:
            raise ValidationError(
                {"error": "You can't send connection to yourself"}
            )
        else:
            connection = Connection.objects.create(
                sender=sender,
                reciever=reciever,
                roomate_request=roomate_request,
            )
        return connection


class NotificationSerializer(serializers.ModelSerializer):

    connection = ConnectionSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "connection",
            "title",
            "content",
            "is_read",
            "created_at",
        ]
