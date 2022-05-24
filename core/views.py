import django_filters
from authentify.models import CustomUser
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, RoomateRequest
from .serializers import ProfileSerializer, RoomateRequestSerializer


class CreateProfile(CreateAPIView):

    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated]
    queryset = Profile

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateProfile(UpdateAPIView):

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def put(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProfile(APIView):
    def get(self, request):
        email = request.user.email
        profile = Profile.objects.get(user=request.user)
        data = ProfileSerializer(profile).data

        return Response({"email":email, "data": data})


class CreateRoomateRequest(CreateAPIView):

    serializer_class = RoomateRequestSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)
    queryset = RoomateRequest.objects.all()


class RoomateRequestFilter(django_filters.FilterSet):
    religion = django_filters.CharFilter(field_name="profile__religion")
    gender = django_filters.CharFilter(field_name="profile__gender")

    class Meta:
        model = RoomateRequest
        fields = [
            "city",
            "country",
            "state",
            "gender",
            "religion",
            "room_type",
            "listing_title",
            "is_active",
        ]


class GetRoomateRequests(ListAPIView):
    serializer_class = RoomateRequestSerializer
    queryset = RoomateRequest.objects.all()
    filter_class = RoomateRequestFilter


class GetOneRoomateRequest(RetrieveAPIView):

    serializer_class = RoomateRequestSerializer
    queryset = RoomateRequest.objects.all()


class DeactivateRequest(UpdateAPIView):

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = RoomateRequestSerializer
    queryset = RoomateRequest.objects.all()

    def patch(self, request, pk, *args, **kwargs):
        roomate_request = RoomateRequest.objects.get(id=pk)

        serializer = self.get_serializer(
            roomate_request,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "detail": "request deactivated successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ActivateRequest(UpdateAPIView):

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = RoomateRequestSerializer
    queryset = RoomateRequest.objects.all()

    def patch(self, request, pk, *args, **kwargs):
        roomate_request = RoomateRequest.objects.get(id=pk)

        serializer = self.get_serializer(
            roomate_request,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "detail": "request activated successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class GetUserRoomateRequests(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = RoomateRequestSerializer
    queryset = RoomateRequest.objects.all()

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        roomate_request = RoomateRequest.objects.filter(profile=profile)
        serializer = RoomateRequestSerializer(roomate_request, many=True)

        return Response(serializer.data)

class GetUserActiveRoomateRequests(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = RoomateRequestSerializer
    queryset = RoomateRequest.objects.all()

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        roomate_request = RoomateRequest.objects.filter(profile=profile, is_active=True)
        serializer = RoomateRequestSerializer(roomate_request, many=True)

        return Response(serializer.data)

class GetUserInactiveRoomateRequests(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = RoomateRequestSerializer
    queryset = RoomateRequest.objects.all()

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        roomate_request = RoomateRequest.objects.filter(profile=profile, is_active=False)
        serializer = RoomateRequestSerializer(roomate_request, many=True)

        return Response(serializer.data)
