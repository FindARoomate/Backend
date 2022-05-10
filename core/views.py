import django_filters
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import modify_input_for_multiple_files
from .models import Profile, RequestImages, RoomateRequest
from .serializers import (
    ImageSerializer,
    ProfileSerializer,
    RoomateRequestSerializer,
    RequestImageSerializer
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
    queryset = RoomateRequest.objects.all()

    def post(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        profile = ProfileSerializer(profile)
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "request_data": serializer.data,
                "profile_data": profile.data,
            },
            status=status.HTTP_201_CREATED,
        )


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

class RequestImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        all_images = RequestImages.objects.all()
        serializer = RequestImageSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        request = request.data.get('request')

        # converts querydict to original dict
        images = dict((request.data).lists())['image_file']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(request,
                                                            img_name)
            file_serializer = RequestImageSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)