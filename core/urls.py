from django.urls import path

from .views import (
    AcceptConnection,
    ActivateRequest,
    CancelConnection,
    ConnectionRequestStatistics,
    CreateConnection,
    CreateProfile,
    CreateRoomateRequest,
    DeactivateRequest,
    GetAllNotification,
    GetAProfile,
    GetOneRoomateRequest,
    GetProfile,
    GetReceivedRequests,
    GetRoomateRequests,
    GetSentRequests,
    GetUserActiveRoomateRequests,
    GetUserInactiveRoomateRequests,
    GetUserRoomateRequests,
    RejectConnection,
    RequestStatistics,
    UpdateNotification,
    UpdateProfile,
    UpdateRoomateRequest,
    UploadImage,
    DeleteImage,
)

urlpatterns = [
    path(
        "profile/create/", CreateProfile.as_view(), name="create-profile"
    ),
    path(
        "profile/<str:pk>/update/",
        UpdateProfile.as_view(),
        name="update-profile",
    ),
    path("profile/get/", GetProfile.as_view(), name="get-profile"),
    path(
        "profile/<str:pk>/",
        GetAProfile.as_view(),
        name="get-a-profile",
    ),
    path(
        "request/create/",
        CreateRoomateRequest.as_view(),
        name="create-roomate-request",
    ),
    path(
        "request/<str:pk>/update/",
        UpdateRoomateRequest.as_view(),
        name="update-roomate-request",
    ),
    path(
        "request/get/",
        GetRoomateRequests.as_view(),
        name="get-roomate-requests",
    ),
    path(
        "request/get/<str:pk>/",
        GetOneRoomateRequest.as_view(),
        name="get-one-roomate-request",
    ),
    path(
        "request/activate/<str:pk>/",
        ActivateRequest.as_view(),
        name="activate-a-request",
    ),
    path(
        "request/deactivate/<str:pk>/",
        DeactivateRequest.as_view(),
        name="deactivate-a-request",
    ),
    path(
        "request/users/",
        GetUserRoomateRequests.as_view(),
        name="get-user-requests",
    ),
    path(
        "request/users/active/",
        GetUserActiveRoomateRequests.as_view(),
        name="get-user-active-requests",
    ),
    path(
        "request/users/inactive/",
        GetUserInactiveRoomateRequests.as_view(),
        name="get-user-inactive-requests",
    ),
    path(
        "connections/create/",
        CreateConnection.as_view(),
        name="create-connection",
    ),
    path(
        "connections/accept/<str:pk>/",
        AcceptConnection.as_view(),
        name="accept-connection",
    ),
    path(
        "connections/reject/<str:pk>/",
        RejectConnection.as_view(),
        name="accept-connection",
    ),
    path(
        "connections/<str:pk>/delete/",
        CancelConnection.as_view(),
        name="delete-connection",
    ),
    path(
        "connections/sent/",
        GetSentRequests.as_view(),
        name="sent-connections",
    ),
    path(
        "connections/recieved/",
        GetReceivedRequests.as_view(),
        name="sent-connections",
    ),
    path(
        "statistics/",
        RequestStatistics.as_view(),
        name="request-statistics",
    ),
    path(
        "notifications/",
        GetAllNotification.as_view(),
        name="notifications",
    ),
    path(
        "notifications/<str:pk>/",
        UpdateNotification.as_view(),
    ),
    path(
        "connections/<str:pk>/requests/",
        ConnectionRequestStatistics.as_view(),
    ),
    path("image/request/", UploadImage.as_view()),
    path("image/request/<str:pk>/", DeleteImage.as_view())

]
