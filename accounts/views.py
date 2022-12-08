from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, PasswordResetForm, SetPasswordForm, SignupForm


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
    password_reset_url = reverse('accounts:send_password_reset')

    password_reset_data = request.session.get('password_reset_data', None)
    password_reset_form = PasswordResetForm(password_reset_data)
    
    return render(request, 'accounts/pages/password_reset.html', context={
        'form': password_reset_form,
        'form_action': password_reset_url,
        'has_password_fields': False
    })

def send_password_reset(request):
    login_url = reverse('accounts:login')

    if not request.POST:
        return redirect(reverse('accounts:password_reset'))

    password_reset_data = request.POST
    request.session['password_reset_data'] = password_reset_data

    password_reset_form = PasswordResetForm(password_reset_data)

    if password_reset_form.is_valid():
        if password_reset_form.email_exists():
            password_reset_form.send_email()

            message = 'E-mail de redefinição de senha enviado.'
            messages.success(request, message)   

            del request.session['password_reset_data'] 

            return redirect(login_url)

        messages.error(request, 'E-mail não encontrado.')
    else:
        messages.error(request, 'Por favor, digite seu e-mail.')
        
    return redirect('accounts:password_reset')

def confirm_password_reset(request, uidb64, token):
    set_password_form = SetPasswordForm()
    
    form_action = reverse(
        'accounts:complete_password_reset', args=(uidb64, token)
    )

    return render(request, 'accounts/pages/set_password.html', context={
        'form': set_password_form,
        'form_action': form_action,
        'has_password_fields': True
    })

def complete_password_reset(request, uidb64, token):
    confirm_password_reset_url = reverse(
        'accounts:confirm_password_reset', args=(uidb64, token)
    )

    if not request.POST:
        return redirect(confirm_password_reset)

    set_password_data = request.POST
    set_password_form = SetPasswordForm(set_password_data)

    if set_password_form.is_valid():
        set_password_form.set_password(uidb64)
        
        message = 'Senha alterada com sucesso.'
        messages.success(request, message)        

        return redirect(reverse('accounts:login'))
    
    messages.error(request, 'As senhas não são iguais.')
        
    return redirect(confirm_password_reset_url)