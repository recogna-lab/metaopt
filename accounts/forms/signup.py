from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_attr, add_placeholder


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

    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome')
    username = forms.CharField(label='Usuário')
    email = forms.CharField(label='E-mail')
    
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput()
    )
    
    confirm_password = forms.CharField(
        label='Confirmar senha', 
        widget=forms.PasswordInput()
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
                'E-mail já está em uso.', 
                code='invalid'
            )

        return email