from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token



def send_activation_email(request, value):
        mail_subject = 'Activate your account.'
        current_site = get_current_site(request).domain
        uid = urlsafe_base64_encode(force_bytes(value.pk))
        token = account_activation_token.make_token(value)
        activation_link = "http://"+current_site+'/auth/activate/'+uid+'/'+token
        message = "Hello {0},Kindly activate your account using this link\n {1}".format(value.username,
                                                                                        activation_link)
        email = EmailMessage(mail_subject, message, to=[value.email])
        email.send()

def send_password_reset_email(self, value):
        pass
