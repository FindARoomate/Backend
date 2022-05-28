from django.urls import path

from .views import (
    AcceptConnection,
    ActivateRequest,
    CreateConnection,
    CreateProfile,
    CreateRoomateRequest,
    DeactivateRequest,
    GetOneRoomateRequest,
    GetProfile,
    GetRoomateRequests,
    GetUserActiveRoomateRequests,
    GetUserInactiveRoomateRequests,
    GetUserRoomateRequests,
    UpdateProfile,
    RejectConnection,
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
    # path(
    #     "profile/image-upload/", UploadImage.as_view(), name="upload-image"
    # ),
    path(
        "request/create/",
        CreateRoomateRequest.as_view(),
        name="create-roomate-request",
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
        "connections/create/", CreateConnection.as_view(), name="create-connection"
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
]

