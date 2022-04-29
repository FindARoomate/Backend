from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, RoomateRequest
from .serializers import (
    ImageSerializer,
    ProfileSerializer,
    RoomateRequestSerializer,
)


class CreateProfile(CreateAPIView):

    serializer_class = ProfileSerializer
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
            instance, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProfile(APIView):
    def get(self, request):

        profile = Profile.objects.get(user=request.user)
        data = ProfileSerializer(profile).data

        return Response(data)


class UploadImage(CreateAPIView):

    permissionclasses = [IsAuthenticated]
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser,)


class CreateRoomateRequest(CreateAPIView):

    serializer_class = RoomateRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = RoomateRequest

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetRoomateRequests(APIView):
    def get(self, request):

        data = ProfileSerializer(many=True)

        return Response(data)
