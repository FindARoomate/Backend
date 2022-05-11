from authentify.models import CustomUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Profile, RequestImages, RoomateRequest


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

    def update(self, instance, validated_data):

        instance.fullname = validated_data["fullname"]
        instance.religion = validated_data["religion"]
        instance.gender = validated_data["gender"]
        instance.phone_number = validated_data["phone_number"]
        instance.personality = validated_data["personality"]
        # instance.date_of_birth = validated_data["date_of_birth"]
        instance.profession = validated_data["profession"]
        instance.bio = validated_data["bio"]
        instance.roomate_description = validated_data[
            "roomate_description"
        ]
        instance.age = validated_data["age"]

        instance.save()

        return instance


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

            for image_data in images_data.getlist("request_images"):
                RequestImages.objects.create(
                    request=roomate_request, image_file=image_data
                )
            return roomate_request

        except Profile.DoesNotExist:
            return serializers.ValidationError(
                detail="no profile created for the logged in user"
            )
