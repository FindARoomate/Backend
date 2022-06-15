import django_filters
from authentify.models import CustomUser
from rest_framework import filters, status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .enums import ConnectionStatus
from .models import Connection, Notification, Profile, RoomateRequest
from .serializers import (
    ConnectionSerializer,
    NotificationSerializer,
    ProfileSerializer,
    RoomateRequestSerializer,
)
from .utils import create_notification


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

    def patch(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProfile(APIView):
    def get(self, request):
        email = request.user.email
        profile = Profile.objects.get(user=request.user)
        data = ProfileSerializer(profile).data

        return Response({"email": email, "data": data})


class GetAProfile(RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class CreateRoomateRequest(CreateAPIView):

    serializer_class = RoomateRequestSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)
    queryset = RoomateRequest.objects.all()


class UpdateRoomateRequest(UpdateAPIView):

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = RoomateRequestSerializer
    queryset = RoomateRequest.objects.all()

    def patch(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


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
    queryset = RoomateRequest.objects.filter(is_active=True)
    filter_class = RoomateRequestFilter
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    search_fields = ["listing_title"]


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
        profile = Profile.objects.get(user=request.user)
        try:
            roomate_request = RoomateRequest.objects.get(
                id=pk, profile=profile
            )

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
        except Exception as e:
            print(e)
            return Response(
                {"detail": "You do not have permission to edit request"}
            )


class ActivateRequest(UpdateAPIView):

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = RoomateRequestSerializer
    queryset = RoomateRequest.objects.all()

    def patch(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        try:
            roomate_request = RoomateRequest.objects.get(
                id=pk, profile=profile
            )

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
        except Exception as e:
            print(e)
            return Response(
                {"detail": "You do not have permission to edit request"}
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
        roomate_request = RoomateRequest.objects.filter(
            profile=profile, is_active=True
        )
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
        roomate_request = RoomateRequest.objects.filter(
            profile=profile, is_active=False
        )
        serializer = RoomateRequestSerializer(roomate_request, many=True)

        return Response(serializer.data)


class CreateConnection(CreateAPIView):

    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Connection

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        sender_fullname = serializer.data["sender_data"][0]["fullname"]
        reciever = serializer.data["reciever"]
        connection_id = serializer.data["id"]
        content = f"{sender_fullname} just sent you a connection request"
        user = CustomUser.objects.get(
            id=reciever,
        )
        connection_type = "recieved"
        connection = Connection.objects.get(id=connection_id)
        create_notification(user, content, connection_type, connection)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AcceptConnection(UpdateAPIView):

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ConnectionSerializer
    queryset = Connection.objects.all()

    def patch(self, request, pk, *args, **kwargs):
        connection = Connection.objects.get(id=pk)

        serializer = self.get_serializer(
            connection,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        sender = serializer.data["sender"]
        reciever_fullname = serializer.data["roomate_request"]["profile"][
            "fullname"
        ]
        connection_id = serializer.data["id"]
        content = (
            f"{reciever_fullname} just accepted your connection request"
        )
        user = CustomUser.objects.get(
            id=sender,
        )
        connection_type = "accepted"
        connection = Connection.objects.get(id=connection_id)
        create_notification(user, content, connection_type, connection)

        return Response(
            {
                "detail": "connection accepted successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class RejectConnection(UpdateAPIView):

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ConnectionSerializer
    queryset = Connection.objects.all()

    def patch(self, request, pk, *args, **kwargs):
        connection = Connection.objects.get(id=pk)

        serializer = self.get_serializer(
            connection,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        sender = serializer.data["sender"]
        reciever_fullname = serializer.data["roomate_request"]["profile"][
            "fullname"
        ]
        connection_id = serializer.data["id"]
        content = (
            f"{reciever_fullname} just declined your connection request"
        )
        user = CustomUser.objects.get(
            id=sender,
        )
        connection_type = "declined"
        connection = Connection.objects.get(id=connection_id)
        create_notification(user, content, connection_type, connection)

        return Response(
            {
                "detail": "connection rejected successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CancelConnection(DestroyAPIView):

    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Connection.objects.all()

    def delete(self, request, pk):
        try:
            connection = Connection.objects.filter(
                id=pk, sender=request.user
            )
            connection.delete()
            return Response(
                {"message": "Connection deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception as e:
            return Response(
                {"detail": "An error occured"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetSentRequests(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ConnectionSerializer
    queryset = Connection.objects.all()

    def get(self, request):
        user = request.user
        pending = Connection.objects.filter(
            sender=user, status=ConnectionStatus.PENDING
        )
        accepted = Connection.objects.filter(
            sender=user, status=ConnectionStatus.ACCEPTED
        )
        rejected = Connection.objects.filter(
            sender=user, status=ConnectionStatus.REJECTED
        )

        pending_data = self.serializer_class(pending, many=True)
        accepted_data = self.serializer_class(accepted, many=True)
        rejected_data = self.serializer_class(rejected, many=True)

        return Response(
            {
                "pending_requests": pending_data.data,
                "accepted_requests": accepted_data.data,
                "rejected_request": rejected_data.data,
            }
        )


class GetReceivedRequests(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ConnectionSerializer
    queryset = Connection.objects.all()

    def get(self, request):
        user = request.user
        pending = Connection.objects.filter(
            reciever=user, status=ConnectionStatus.PENDING
        )
        accepted = Connection.objects.filter(
            reciever=user, status=ConnectionStatus.ACCEPTED
        )
        rejected = Connection.objects.filter(
            reciever=user, status=ConnectionStatus.REJECTED
        )

        pending_data = self.serializer_class(pending, many=True)
        accepted_data = self.serializer_class(accepted, many=True)
        rejected_data = self.serializer_class(rejected, many=True)

        return Response(
            {
                "pending_requests": pending_data.data,
                "accepted_requests": accepted_data.data,
                "rejected_request": rejected_data.data,
            }
        )


class RequestStatistics(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        active_request = RoomateRequest.objects.filter(
            profile=profile, is_active=True
        ).count()
        inactive_request = RoomateRequest.objects.filter(
            profile=profile, is_active=False
        ).count()
        connection_sent = Connection.objects.filter(sender=user).count()
        connection_recieved = Connection.objects.filter(
            reciever=user
        ).count()

        response = {
            "active_requests": active_request,
            "inactive_requests": inactive_request,
            "connections_sent": connection_sent,
            "connections_recieved": connection_recieved,
        }

        return Response(response)


class GetAllNotification(ListAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get(self, request):
        notification = Notification.objects.filter(user=request.user)
        serializer = self.serializer_class(notification, many=True)

        return Response(serializer.data)


class UpdateNotification(UpdateAPIView):

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
