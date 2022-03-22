from django.urls import path
from .views import JoinWaitlist



urlpatterns = [
    path("join-waitlist/", JoinWaitlist.as_view(), name="join_waitlist"),
]
