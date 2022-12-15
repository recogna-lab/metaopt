from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import OptimizationForm
from .tasks import optimization


@login_required
def index(request):
    return render(request, 'dashboard/pages/index.html')

@login_required
def new_optimization_task(request):
    optimization_form = OptimizationForm()
    
    return render(request, 'dashboard/pages/form_page.html', context={
        'task_type': 'Otimização',
        'form': optimization_form
    })

@login_required
def start_optimization_task(request):
    new_opt_url = 'dashboard:new_opt_task'
    
    if not request.POST:
        return redirect(new_opt_url)
    
    optimization_form = OptimizationForm(request.POST)
    
    if not optimization_form.is_valid():
        messages.error(request, 'Por favor, selecione as opções desejadas.')
        return redirect(new_opt_url)
    
    form_data = optimization_form.cleaned_data
    
    opt_task = optimization.delay(
        user_id=request.user.id,
        optimizer=form_data['optimizer'].acronym, 
        function=form_data['function'].short_name, 
        agents=form_data['agents'], 
        iterations=form_data['iterations']
    )

    return redirect('dashboard:opt_task', task_id=opt_task.task_id)

@login_required
def optimization_task(request, task_id):
    return HttpResponse('Optimization Task')