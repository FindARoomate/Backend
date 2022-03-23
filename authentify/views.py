from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .models import Waitlist, CustomUser
from .serializers import WaitlistSerializer, RegisterSerializer


class JoinWaitlist(CreateAPIView):
    """
    The View for the join_waitlist endpoint
    """

    queryset = Waitlist.objects.all()
    serializer_class = WaitlistSerializer

class Register(CreateAPIView):
    
    """
    The view to register users
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)