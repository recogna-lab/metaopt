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
            
    return render(request, 'accounts/pages/form_page.html', context={
        'page_title': 'Login',
        'form_title': 'Entre em sua conta',
        'form': LoginForm(),
        'form_action': reverse('accounts:perform_login'),
        'has_password_fields': True
    })

def perform_login(request):
    login_url = reverse('accounts:login')
    
    if not request.POST:
        return redirect(login_url)

    login_form = LoginForm(request.POST)
    
    if not login_form.is_valid():
        messages.error(request, 'Por favor, preencha os dois campos.')
        return redirect(login_url)
    
    authenticated_user = authenticate(
        username = login_form.cleaned_data.get('username', ''),
        password = login_form.cleaned_data.get('password', '')
    )
        
    if authenticated_user is None:
        messages.error(request, 'Usuário ou senha inválidos.')
        return redirect(login_url)
    
    login(request, authenticated_user)

    next_url = request.session.pop('next')
    return redirect(next_url)

def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))

def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard:index'))

    signup_data = request.session.get('signup_data', None)
    signup_form = SignupForm(signup_data)

    return render(request, 'accounts/pages/form_page.html', context={
        'page_title': 'Cadastro',
        'form_title': 'Crie uma conta',
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
    
    if not signup_form.is_valid():
        message = 'Por favor, preencha todos os campos corretamente.'
        messages.error(request, message) 
        return redirect(signup_url)

    signup_form.save_user()
    
    message = 'Usuário criado com sucesso.'
    messages.success(request, message)        
    
    del request.session['signup_data']

    return redirect(reverse('accounts:login'))

def password_reset(request):
    password_reset_data = request.session.get('password_reset_data', None)
    password_reset_form = PasswordResetForm(password_reset_data)
    
    return render(request, 'accounts/pages/form_page.html', context={
        'page_title': 'Pedido de Redefinição de Senha',
        'form_title': 'Peça uma nova senha',
        'form': password_reset_form,
        'form_action': reverse('accounts:send_password_reset'),
        'has_password_fields': False
    })

def send_password_reset(request):
    password_reset_url = reverse('accounts:password_reset')

    if not request.POST:
        return redirect(password_reset_url)

    password_reset_data = request.POST
    request.session['password_reset_data'] = password_reset_data

    password_reset_form = PasswordResetForm(password_reset_data)

    if not password_reset_form.is_valid():
        messages.error(request, 'Por favor, digite seu e-mail.')        
        return redirect(password_reset_url)
    
    if not password_reset_form.email_exists():
        messages.error(request, 'E-mail não encontrado.')
        return redirect(password_reset_url)
    
    password_reset_form.send_email()

    message = 'E-mail de redefinição de senha enviado.'
    messages.success(request, message)   

    del request.session['password_reset_data'] 

    return redirect(reverse('accounts:login'))

def confirm_password_reset(request, uidb64, token): 
    set_password_form = SetPasswordForm()
    
    if not set_password_form.check_user_and_token(uidb64, token):
        response = render(request, 'global/pages/error.html', context={
            'status_code': 498,
            'error_type': 'Token inválido.',
            'error_message': (
                'Parece que você já recuperou sua conta. '
                'Se preciso, solicite outra redefinição de senha.'
            )
        })
        response.status_code = 498
        return response

    request.session['uidb64'] = uidb64
    request.session['token'] = token

    return render(request, 'accounts/pages/form_page.html', context={
        'page_title': 'Redefinição de Senha',
        'form_title': 'Redefina sua senha',
        'form': set_password_form,
        'form_action': reverse('accounts:complete_reset'),
        'has_password_fields': True
    })

def complete_password_reset(request):
    uidb64 = request.session.get('uidb64')
    token = request.session.get('token')
    
    confirm_reset_url = reverse('accounts:confirm_reset', args=(uidb64, token))

    if not request.POST:
        return redirect(confirm_reset_url)

    set_password_data = request.POST
    set_password_form = SetPasswordForm(set_password_data)

    if not set_password_form.is_valid():
        messages.error(request, 'As senhas não são iguais.')        
        return redirect(confirm_reset_url)

    set_password_form.set_password(uidb64)
    
    message = 'Senha alterada com sucesso.'
    messages.success(request, message)        

    del request.session['uidb64'], request.session['token']

    return redirect(reverse('accounts:login'))