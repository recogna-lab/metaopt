from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode

from utils.django_forms import add_attr, add_placeholder, strong_password


class NewPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.name = 'new_password_form'
        
        add_placeholder(self.fields['password'], 'Digite a nova senha')
        add_placeholder(self.fields['confirm_password'], 'Repita sua senha')
        
        for field in self.fields.values():
            add_attr(field, 'class', 'form-control')
            
            # Add tooltips
            add_attr(field, 'data-toggle', 'tooltip')
            add_attr(field, 'title', field.help_text)

    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(),
        min_length=8,
        max_length=20,
        help_text=(
            'Digite uma combinação de pelo menos 8 caracteres como letras ' 'maiúsculas e minúsculas, e dígitos.'
        ),
        error_messages={
            'required': 'Por favor, digite sua senha.'
        },
        validators=[strong_password]
    )
    
    confirm_password = forms.CharField(
        label='Confirmar senha', 
        widget=forms.PasswordInput(),
        min_length=8,
        max_length=20,
        help_text=(
            'Repita sua senha.'
        ),
        error_messages={
            'required': 'Por favor, repita sua senha.'
        }
    )

    def change_password(self, uidb64, password):
        id = urlsafe_base64_decode(uidb64)
        
        user = User.objects.filter(id = id).first() 

        user.set_password(password.get('password'))

        user.save()

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            password_confirmation_error = ValidationError(
                'O campo "Confirmar senha" deve ser igual ao "Senha".',
                code='invalid'
            )
            
            raise ValidationError({
                'confirm_password': [
                    password_confirmation_error
                ]
            })