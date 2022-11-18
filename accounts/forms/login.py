from django import forms

from utils.django_forms import add_attr, add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        add_placeholder(self.fields['username'], 'Digite seu usuário')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        
        for field in self.fields.values():
            add_attr(field, 'class', 'input--style-4')

    # Set an id for the form element
    id = 'login-form'

    username = forms.CharField(label='Usuário')
    
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput()
    )
    
    remember_me = forms.BooleanField(
        label='Manter conectado',
        required=False
    )