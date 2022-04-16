from authentify.models import CustomUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:

        model = Profile
        fields = [
            "id",
            "fullname",
            "religion",
            "gender",
            "image",
            "image_url",
            "phone_number",
            "personality",
            "date_of_birth",
            "profession",
            "bio",
            "age",
            "roomate_description",
            "created_at",
        ]
        extra_kwargs = {"created_at": {"read_only": True}}

    def get_image_url(self, obj):

        return f"https://res.cloudinary.com/dczoldewu/{obj.image}"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("image")
        return representation

    def create(self, validated_data):
        current_user = self.context["request"].user
        user = CustomUser.objects.get(email__iexact=current_user.email)

        profile = Profile.objects.create(user=user, **validated_data)

        return profile

    def update(self, instance, validated_data):

        instance.fullname = validated_data["fullname"]
        instance.religion = validated_data["religion"]
        instance.gender = validated_data["gender"]
        instance.phone_number = validated_data["phone_number"]
        # instance.image = validated_data["image"]
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
