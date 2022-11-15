from django import forms

class UserForm(forms.Form):
    
    user_name = forms.CharField(label='Seu nome', max_length=100)
    email = forms.CharField(label='Seu email', max_length=50)
    password = forms.CharField(label='Sua senha', max_length=20)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
