from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm


def login_view(request):
    loginForm = LoginForm()
    
    return render(request, 'accounts/login.html', context={
        'form': loginForm,
        'form_action': reverse('accounts:perform_login')
    })

def perform_login(request):
    if not request.POST:
        return redirect('accounts:login')
    
    loginForm = LoginForm(request.POST)
    
    if loginForm.is_valid():
        authenticated_user = authenticate(
            username=loginForm.cleaned_data.get('username', ''),
            password=loginForm.cleaned_data.get('password', '')
        )
        
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('dashboard:index')
        
        messages.error(request, 'Credenciais inválidas.')
    else:
        messages.error(request, 'Erro de validação.')
    
    return redirect('accounts:login')