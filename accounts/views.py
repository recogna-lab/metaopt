from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .forms import UserForm
from django.http import HttpResponseRedirect


def login(request):
    return render(request, 'accounts/pages/login.html')

def register(request):

    if request.method == 'POST':
        
        form = UserForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    else:

        print('Criando formulário')
        
        form = UserForm()

    return render(request, 'accounts/pages/register.html', {'form': form})

@require_POST
def user_registering(request):

    try:
        # Verifica se o e-mail que se está tentando cadastrar já não existe -> CASO: email seja único
        user = User.objects.get(email = request.POST['email'])

        if user:
            return render(request, 'caminho para index', {'msg': 'E-mail já cadastrado!'})
    
    except User.DoesNotExist:
        user_name = request.POST['user_name']
        email = request.POST['email']
        passwd = request.POST['password']

        newUser = User.objects.create_user(username=user_name, email=email, password=passwd)
        newUser.save()


