from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, SignupForm


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard:index'))

    signup_form_data = request.session.get('signup_form_data', None)
    
    signup_form = SignupForm(signup_form_data)

    return render(request, 'accounts/pages/signup.html', context={
        'form': signup_form,
        'form_action': reverse('accounts:perform_signup')
    })

def perform_signup(request):
    signup_url = reverse('accounts:signup')

    if not request.POST:
        return redirect(signup_url)

    signup_form_data = request.POST
    request.session['signup_form_data'] = signup_form_data
    
    signup_form = SignupForm(signup_form_data)
    
    if signup_form.is_valid():
        user = signup_form.save(commit=False)
        user.set_password(user.password)
        user.save()
        
        message = 'Usuário criado com sucesso. '
        message += 'Por favor, logue.'
        
        messages.success(request, message)        
      
        del request.session['signup_form_data']

        return redirect(reverse('accounts:login'))

    messages.success(request, 'Erro de validação.')
            
    return redirect(signup_url)

def login_view(request):
    dashboard_url = reverse('dashboard:index')
    
    if request.user.is_authenticated:
        return redirect(dashboard_url)
    
    next = request.GET.get('next', '')
    request.session['next'] = next or dashboard_url
    
    login_form = LoginForm()

    return render(request, 'accounts/pages/login.html', context={
        'form': login_form,
        'form_action': reverse('accounts:perform_login')
    })

def perform_login(request):
    login_url = reverse('accounts:login')
    
    if not request.POST:
        return redirect(login_url)
    
    login_form = LoginForm(request.POST)
    
    if login_form.is_valid():
        authenticated_user = authenticate(
            username=login_form.cleaned_data.get('username', ''),
            password=login_form.cleaned_data.get('password', '')
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
