from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, NewPasswordForm, PasswordResetForm, SignupForm


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
        'has_password_fields': True
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

            next_url = request.session.pop('next')
            return redirect(next_url)
        
        messages.error(request, 'Usuário ou senha inválidos.')
    else:
        messages.error(request, 'Por favor, preencha os dois campos.')
    
    return redirect(login_url)

def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))

def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard:index'))

    signup_data = request.session.get('signup_data', None)
    signup_form = SignupForm(signup_data)

    return render(request, 'accounts/pages/signup.html', context={
        'form': signup_form,
        'form_action': reverse('accounts:perform_signup'),
        'has_password_fields': True
    })

def perform_signup(request):
    signup_url = reverse('accounts:signup')

    if not request.POST:
        return redirect(signup_url)

    signup_data = request.POST
    request.session['signup_data'] = signup_data
    
    signup_form = SignupForm(signup_data)
    
    if signup_form.is_valid():
        user = signup_form.save(commit=False)
        user.set_password(user.password)
        user.save()
        
        message = 'Usuário criado com sucesso.'
        messages.success(request, message)        
      
        del request.session['signup_data']

        return redirect(reverse('accounts:login'))

    message = 'Por favor, preencha todos os campos corretamente.'
    messages.error(request, message)  
    
    return redirect(signup_url)

def password_reset(request):
    password_reset_url = reverse('accounts:perform_password_reset')

    password_reset_data = request.session.get('password_reset_data', None)
    password_reset_form = PasswordResetForm(password_reset_data)
    
    return render(request, 'accounts/pages/password_reset.html', context={
        'form': password_reset_form,
        'form_action': password_reset_url,
        'has_password_fields': False
    })

def perform_password_reset(request):
    login_url = reverse('accounts:login')

    if not request.POST:
        return redirect(reverse('accounts:password_reset'))

    password_reset_data = request.POST
    request.session['password_reset_data'] = password_reset_data

    password_reset_form = PasswordResetForm(password_reset_data)

    if password_reset_form.is_valid():
        if password_reset_form.email_exists():
            password_reset_form.send_email(password_reset_data['email'])

            message = 'E-mail de redefinição de senha enviado.'
            messages.success(request, message)   

            del request.session['password_reset_data'] 

            return redirect(login_url)

        messages.error(request, 'E-mail não encontrado.')
    else:
        messages.error(request, 'Por favor, digite seu e-mail.')
        
    return redirect('accounts:password_reset')

def new_password(request, uidb64, token):
    new_password_form = NewPasswordForm()
    
    form_action = reverse('accounts:perform_new_password', args=(uidb64, token))

    return render(request, 'accounts/pages/new_password.html', context={
        'form': new_password_form,
        'form_action': form_action,
        'has_password_fields': True
    })

def perform_new_password(request, uidb64, token):
    new_password_url = reverse('accounts:new_password', args=(uidb64, token))

    if not request.POST:
        return redirect(new_password_url)

    new_password_data = request.POST
    new_password_form = NewPasswordForm(new_password_data)

    if new_password_form.is_valid():
        new_password_form.change_password(uidb64, new_password_data)
        
        message = 'Senha alterada com sucesso.'
        messages.success(request, message)        

        return redirect(reverse('accounts:login'))
    
    messages.error(request, 'As senhas não são iguais.')
        
    return redirect(new_password_url)