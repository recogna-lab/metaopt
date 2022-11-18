from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, SignupForm, ResetPasswordForm


def reset_password(request):
    forgot_password_url = reverse('accounts:perform_reset_password')

    forgot_form = ResetPasswordForm()

    return render(request, 'accounts/pages/reset_password.html', context={
        'form': forgot_form,
        'form_action': forgot_password_url,
    })

def perform_reset_password(request):
    login_url = reverse('accounts:login')

    if not request.POST:
        return redirect(reverse('accounts:reset_password'))

    password_data = request.POST

    request.session['password_data'] = password_data

    forgot_password_form = ResetPasswordForm(password_data)

    if forgot_password_form.is_valid():

        if forgot_password_form.email_exists():

            message = "E-mail para redefinição enviado. Por favor, verifique."
            messages.success(request, message)   

            forgot_password_form.send_email(password_data['email'])

            del request.session['password_data'] 

            return redirect(login_url)
        
        messages.error(request, 'E-mail não cadastrado.')
    
    messages.error(request, 'Endereço de e-mail inválido.')
        
    return redirect('accounts:reset_password')

def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard:index'))

    signup_form_data = request.session.get('signup_form_data', None)
    
    signup_form = SignupForm(signup_form_data)

    return render(request, 'accounts/pages/signup.html', context={
        'form': signup_form,
        'form_action': reverse('accounts:perform_signup'),
    })

def perform_signup(request):
    signup_url = reverse('accounts:signup')

    if not request.POST:
        return redirect(signup_url)

    signup_form_data = request.POST

    print(signup_form_data)

    request.session['signup_form_data'] = signup_form_data
    
    signup_form = SignupForm(signup_form_data)
    
    if signup_form.is_valid():
        user = signup_form.save(commit=False)
        user.set_password(user.password)
        user.save()
        
        message = 'Usuário criado com sucesso.'
        messages.success(request, message)        
      
        del request.session['signup_form_data']

        return redirect(reverse('accounts:login'))

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
        'form_action': reverse('accounts:perform_login'),
    })

def perform_login(request):
    login_url = reverse('accounts:login')
    
    if not request.POST:
        return redirect(login_url)
    
    login_form = LoginForm(request.POST)
    
    if login_form.is_valid():
        authenticated_user = authenticate(
            username = login_form.cleaned_data.get('username', ''),
            password = login_form.cleaned_data.get('password', '')
        )
        
        if authenticated_user is not None:
            login(request, authenticated_user)

            if not login_form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
                    
            next_url = request.session.pop('next')
            return redirect(next_url)
        
        messages.error(request, 'Credenciais inválidas.')
    else:
        messages.error(request, 'Erro de validação.')
    
    return redirect(login_url)

def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))