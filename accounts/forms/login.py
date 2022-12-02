from django import forms

from utils.django_forms import add_attr, add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.name = 'login_form'
        
        add_placeholder(self.fields['username'], 'Digite seu usuário')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        
        for field in self.fields.values():
            if 'BooleanField' not in str(type(field)):
                add_attr(field, 'class', 'form-control')

    username = forms.CharField(label='Usuário')
    
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput()
    )