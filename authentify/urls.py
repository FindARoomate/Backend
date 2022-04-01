from django.urls import path
from .views import JoinWaitlist, Register, ActivateUser, LoginAPIView, ResendActivationView




urlpatterns = [
    path("join-waitlist/", JoinWaitlist.as_view(), name="join_waitlist"),
    path("register/", Register.as_view(), name="register"),
    path('activate/<str:uid>/<str:token>', ActivateUser.as_view(), name='activate'),
    path('resend-activation/', ResendActivationView.as_view(), name="resend_activate"),
    path('login/', LoginAPIView.as_view(), name="login")
]
