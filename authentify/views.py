from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Waitlist, CustomUser
from .serializers import WaitlistSerializer, RegisterSerializer, LoginSerializer, ResendActivationSerializer, ChangePasswordSerializer
from .tokens import account_activation_token
from FindARoomate.settings import EMAIL_HOST_USER
from .email import send_activation_email


class JoinWaitlist(CreateAPIView):
    """
    The View for the join_waitlist endpoint
    """
    queryset = Waitlist.objects.all()
    serializer_class = WaitlistSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        if Waitlist.objects.filter(email=email).exists():
            return Response({
                "email": email,
                "message": "email already joined waitlist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            subject = "Thanks for joining!"
            message = "You have successfully joined the find a roomate waitlist"
            send_mail(subject,
                      message,
                      EMAIL_HOST_USER,
                      [email],
                      fail_silently=False)

            return Response({
                "email": email,
                "message": "email successfully submitted"
            }, status=status.HTTP_201_CREATED)


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

        send_activation_email(request, user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActivateUser(APIView):
    """
    The view to activate users 
    """

    def get(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "You have been verified successfully"},
                            status=status.HTTP_200_OK)

        else:
            return Response({"error": 'Activation link is invalid!'},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(CreateAPIView):
    """
    This endpoint logins users
    """
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data['tokens'], status=status.HTTP_200_OK)


class ResendActivationView(CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = ResendActivationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = self.queryset.get(email=user_data['email'])

        send_activation_email(request, user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        user = CustomUser.objects.get(id=pk)
        serializer = ChangePasswordSerializer(
            user, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your password has been successfully changed"})
