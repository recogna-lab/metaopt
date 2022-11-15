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
        
        add_attr(self.fields['first_name'], 'class', 'form-control')
        add_attr(self.fields['last_name'], 'class', 'form-control')
        add_attr(self.fields['username'], 'class', 'form-control')
        add_attr(self.fields['email'], 'class', 'form-control')
        add_attr(self.fields['password'], 'class', 'form-control')
        add_attr(self.fields['confirm_password'], 'class', 'form-control')

    first_name = forms.CharField(
        label='Nome',
        error_messages={'required': 'Digite seu nome.'}
    )

    last_name = forms.CharField(
        label='Sobrenome',
        error_messages={'required': 'Digite seu sobrenome.'}
    )
    
    username = forms.CharField(
        label='Usuário',
        help_text=(
            'O usuário pode conter letras, dígitos ou os símbolos @.+-_. '
            'Esse campo deve ter entre 4 e 150 caracteres.'
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
        error_messages={'required': 'Esse campo não pode ficar vazio.'},
        help_text='O e-mail deve ser válido.'
    )

    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Esse campo não pode ficar vazio.'
        },
        help_text=(
            'A senha deve conter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um dígito numérico. No mais, a senha '
            'deve conter pelo menos 8 caracteres.'
        ),
        validators=[strong_password]
    )
    
    confirm_password = forms.CharField(
        label='Confirmar senha', 
        widget=forms.PasswordInput(),
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
                'password': password_confirmation_error,
                'confirm_password': [
                    password_confirmation_error
                ]
            })