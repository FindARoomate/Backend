from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.core.mail import EmailMessage

from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Waitlist, CustomUser
from .serializers import WaitlistSerializer, RegisterSerializer
from .tokens import account_activation_token

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

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = self.queryset.get(email=user_data['email'])
        mail_subject = 'Activate your account.'
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
        message = "Hello {0},Kindly activate your account using this link\n {1}".format(user.username, 
        activation_link)
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

        return Response(serializer.data)


User = get_user_model()

class ActivateUser(ListCreateAPIView):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            return Response({"message": "You have been verified successfully"})
            
        else:
            return Response({"error":'Activation link is invalid!'})