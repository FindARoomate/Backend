from django.urls import path
from .views import JoinWaitlist, Register, ActivateUser
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns = [
    path("join-waitlist/", JoinWaitlist.as_view(), name="join_waitlist"),
    path("register/", Register.as_view(), name="register"),
    path('activate/<str:uid>/<str:token>', ActivateUser.as_view(), name='activate'),
]
