from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    ActivateUser,
    ContactForm,
    JoinWaitlist,
    MyTokenObtainPairView,
    Register,
    ResendActivation,
    ResetPassword,
    ResetPasswordConfirm,
)

urlpatterns = [
    path("join-waitlist/", JoinWaitlist.as_view(), name="join_waitlist"),
    path("register/", Register.as_view(), name="register"),
    path(
        "activate/<str:uid>/<str:token>",
        ActivateUser.as_view(),
        name="activate",
    ),
    path(
        "resend-activation/",
        ResendActivation.as_view(),
        name="resend_activate",
    ),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path(
        "reset-password/", ResetPassword.as_view(), name="reset-password"
    ),
    path(
        "reset-password-confirm/<str:uid>/<str:token>",
        ResetPasswordConfirm.as_view(),
        name="reset-password-confirm",
    ),
    path("contact-us/", ContactForm.as_view(), name="contact-us"),
]
