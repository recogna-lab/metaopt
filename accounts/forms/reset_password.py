from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
        
        print(f'email: {email}')

        user = User.objects.filter(email=email).first()

        print(user.first_name)

