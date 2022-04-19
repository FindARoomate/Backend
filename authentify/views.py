from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .email import send_activation_email, send_password_reset_email
from .models import CustomUser, Waitlist
from .serializers import (
    ContactFormSerializer,
    RegisterSerializer,
    ResendActivationSerializer,
    ResetPasswordConfirmSerializer,
    ResetPasswordSerializer,
    WaitlistSerializer,
)
from .tokens import account_activation_token


class JoinWaitlist(APIView):
    """
    The View for the join_waitlist endpoint
    """

    queryset = Waitlist.objects.all()
    serializer_class = WaitlistSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        name = serializer.data["name"]
        if Waitlist.objects.filter(email=email).exists():
            return Response(
                {
                    "email": email,
                    "name": name,
                    "message": "email already joined waitlist",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            serializer.save()
            subject = "Thanks for joining!"
            message = f"Dear{name}, You have successfully joined the find a roomate waitlist"
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return Response(
                {
                    "email": email,
                    "message": "email successfully submitted",
                },
                status=status.HTTP_201_CREATED,
            )


class Register(APIView):

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
        user = self.queryset.get(email=user_data["email"])

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
        except (
            TypeError,
            ValueError,
            OverflowError,
            CustomUser.DoesNotExist,
        ):
            user = None
        if user is not None and account_activation_token.check_token(
            user, token
        ):
            user.is_active = True
            user.save()
            return Response(
                {"message": "You have been verified successfully"},
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"error": "Activation link is invalid!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendActivation(APIView):

    queryset = CustomUser.objects.all()
    serializer_class = ResendActivationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = self.queryset.get(email=user_data["email"])

        send_activation_email(request, user)

        return Response(
            {"message": "An activation link has been sent to your email"},
            status=status.HTTP_201_CREATED,
        )


class ResetPassword(APIView):

    serializer_class = ResetPasswordSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = self.queryset.get(email=user_data["email"])

        send_password_reset_email(request, user)

        return Response(
            {"detail": "You have been sent an email for password change"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirm(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            CustomUser.DoesNotExist,
        ):
            user = None
        if user is not None and account_activation_token.check_token(
            user, token
        ):
            serializer = self.serializer_class(
                user, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)

            return Response(
                {"detail": "Your password has been successfully changed"}
            )

        else:
            return Response(
                {"error": "Activation link is invalid!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ContactForm(APIView):

    serializer_class = ContactFormSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            name = serializer.data["name"]
            subject = "Contact form message from " + name
            body = {
                "name": serializer.data["name"],
                "email": serializer.data["email"],
                "message": serializer.data["message"],
            }
            message = "\n".join(body.values())
            send_mail(
                subject,
                message,
                email,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response(
                {"success": "email successfully sent"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "An error occured, try again"},
                status=status.HTTP_400_BAD_REQUEST,
            )
