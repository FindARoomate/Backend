from rest_framework.generics import CreateAPIView

from .models import Waitlist
from .serializers import WaitlistSerializer


class JoinWaitlist(CreateAPIView):
    """
    The View for the join_waitlist endpoint
    """

    queryset = Waitlist.objects.all()
    serializer_class = WaitlistSerializer
