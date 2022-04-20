from django.urls import path

from .views import CreateProfile, GetProfile, UpdateProfile

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
]