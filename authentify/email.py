from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


def send_activation_email(request, value):
    mail_subject = 'Activate your account.'
    uid = urlsafe_base64_encode(force_bytes(value.pk))
    token = account_activation_token.make_token(value)
    activation_link = settings.FRONTEND_URL+'/auth/activate/'+uid+'/'+token
    message = "Hello {0},Kindly activate your account using this link\n {1}".format(value.username,
                                                                                    activation_link)
    email = EmailMessage(mail_subject, message, to=[value.email])
    email.send()


def send_password_reset_email(request, value):
    mail_subject = 'Password Change Request'
    current_site = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(value.pk))
    token = account_activation_token.make_token(value)
    activation_link = "http://"+current_site + \
        '/auth/reset-password-confirm/'+uid+'/'+token
    message = "Hello {0},You requested for a password change on this account,\n \
Click on the link to reset your password or disregard if you didn't request\nCheers!\n{1}".format(value.username, activation_link)
    email = EmailMessage(mail_subject, message, to=[value.email])
    email.send()
