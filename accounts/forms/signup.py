from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_attr, add_placeholder, strong_password


class SignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        add_placeholder(self.fields['first_name'], 'Digite seu nome')
        add_placeholder(self.fields['last_name'], 'Digite seu sobrenome')
        add_placeholder(self.fields['username'], 'Digite seu usuário')
        add_placeholder(self.fields['email'], 'Digite seu e-mail')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['confirm_password'], 'Confirme sua senha')
        
        for field in self.fields.values():
            add_attr(field, 'class', 'form-control')
            
            # Add tooltips
            add_attr(field, 'data-toggle', 'tooltip')
            add_attr(field, 'title', field.help_text)

    # Set an id for the form element
    id = 'signup-form'
    
    # Define the fields of the form
    first_name = forms.CharField(
        label='Nome',
        help_text=(
            'Preencha esse campo com o seu nome.'
        ),
        error_messages={'required': 'Digite seu nome.'}
    )

    last_name = forms.CharField(
        label='Sobrenome',
        help_text=(
            'Preencha esse campo com o seu sobrenome.'
        ),
        error_messages={'required': 'Digite seu sobrenome.'}
    )
    
    username = forms.CharField(
        label='Usuário',
        help_text=(
            'O nome de usuário pode conter letras, dígitos ou @.+-_.'
        ),
        error_messages={
            'required': 'Esse campo não pode ficar vazio.',
            'min_length': 'O usuário deve ter pelo menos 4 caracteres.',
            'max_length': 'O usuário pode ter no máximo 150 caracteres.' 
        },
        min_length=4,
        max_length=150
    )
                                
    email = forms.CharField(
        label='E-mail',
        help_text='O endereço de e-mail deve ser válido.',
        error_messages={'required': 'Esse campo não pode ficar vazio.'}
    )

    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(),
        min_length=8,
        max_length=20,
        help_text=(
            'A senha deve conter no mínimo 8 caracteres. Dentre esses, '
            'deve haver pelo menos uma letra maiúscula, uma minúscula e '
            'um dígito numérico.'
        ),
        error_messages={
            'required': 'Esse campo não pode ficar vazio.'
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
            'required': 'Por favor, digite sua senha novamente.'
        }
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        
        found = User.objects.filter(email=email).exists()

        if found:
            raise ValidationError(
                'O e-mail já está em uso.', 
                code='invalid'
            )

        return email
    
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