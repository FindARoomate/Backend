from django.urls import path

from .views import (
    ActivateRequest,
    CreateProfile,
    CreateRoomateRequest,
    GetOneRoomateRequest,
    GetProfile,
    GetRoomateRequests,
    UpdateProfile,
    UploadImage,
    DeactivateRequest,
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
        "profile/image-upload/", UploadImage.as_view(), name="upload-image"
    ),
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
]
