from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm


def login_view(request):
    dashboard_url = reverse('dashboard:index')
    
    if request.user.is_authenticated:
        return redirect(dashboard_url)
    
    next = request.GET.get('next', '')
    request.session['next'] = next or dashboard_url
    
    loginForm = LoginForm()

    return render(request, 'accounts/login.html', context={
        'form': loginForm,
        'form_action': reverse('accounts:perform_login')
    })

def perform_login(request):
    login_url = reverse('accounts:login')
    
    if not request.POST:
        return redirect(login_url)
    
    loginForm = LoginForm(request.POST)
    
    if loginForm.is_valid():
        authenticated_user = authenticate(
            username=loginForm.cleaned_data.get('username', ''),
            password=loginForm.cleaned_data.get('password', '')
        )
        
        if authenticated_user is not None:
            login(request, authenticated_user)

            next_url = request.session.pop('next')
            return redirect(next_url)
        
        messages.error(request, 'Credenciais inválidas.')
    else:
        messages.error(request, 'Erro de validação.')
    
    return redirect(login_url)

def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))