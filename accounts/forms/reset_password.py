from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from metaopt.settings.mail import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from utils.django_forms import add_attr, add_placeholder


class ResetPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        add_placeholder(self.fields['email'], 'Digite seu-email')
        
        for field in self.fields.values():
            add_attr(field, 'class', 'input--style-4')

    # Set an id for the form element
    id = 'password-form'

    email = forms.CharField(
        label = "E-mail",
        help_text = 'O endereço de e-mail deve ser válido.',
        error_messages={'required': 'Esse campo não pode ficar vazio.'}
    )

    def email_exists(self):
        email = self.cleaned_data.get('email', '')

        found = User.objects.filter(email=email).exists()

        return found

    def send_email(self, email):

        user = User.objects.filter(email=email).first()

        subject = "Pedido de Redefinição de Senha"
        email_template = "accounts/password_reset_email.txt"
        c = {
            "email" : user.email,
            'domain' : '127.0.0.1:8000',
            'site_name': "MetaOPT",
            "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
            "user" : user.first_name,
            "token" : default_token_generator.make_token(user),
            'protocol' : 'http',
        }

        email = render_to_string(email_template, c)
        try:
            send_mail(subject=subject, message=email, from_email="", recipient_list=[user.email], auth_user=EMAIL_HOST_USER,
            auth_password=EMAIL_HOST_PASSWORD, fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

