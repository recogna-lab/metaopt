from django import forms

from utils.django_forms import add_attr, add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        add_placeholder(self.fields['username'], 'Digite seu usuário')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        
        add_attr(self.fields['username'], 'class', 'form-control')
        add_attr(self.fields['password'], 'class', 'form-control')

    username = forms.CharField(label='Usuário')
    
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput()
    )