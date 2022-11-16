from django import forms

from utils.django_forms import add_attr, add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        add_placeholder(self.fields['username'], 'Digite seu usuário')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        
        add_attr(self.fields['username'], 'class', 'input--style-4')
        add_attr(self.fields['password'], 'class', 'input--style-4')

    username = forms.CharField(label='Usuário')
    
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput()
    )
    
    remember_me = forms.BooleanField(
        label='Manter conectado',
        required=False
    )