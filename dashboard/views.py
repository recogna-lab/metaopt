from celery_progress.views import get_progress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from utils import load_json
from utils.plots import plot_convergence

from .forms import FeatureSelectionForm, OptimizationForm
from .models import get_all_tasks, get_task
from .tasks import feature_selection, optimization

# Dashboard page

@login_required
def index(request):
    tasks = get_all_tasks(user_id=request.user.id)
    
    return render(request, 'dashboard/pages/index.html', context={
        'title': 'Dashboard',
        'tasks': tasks
    })

# Optimization related views

@login_required
def new_optimization_task(request):
    optimization_form = OptimizationForm()
    
    return render(request, 'dashboard/pages/new_task.html', context={
        'title': 'Otimização',
        'return_to': reverse('dashboard:index'),
        'form': optimization_form,
        'form_action': reverse('dashboard:start_opt_task')
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
        space=load_json(form_data['function'].search_space),
        agents=form_data['agents'],
        iterations=form_data['iterations'],
        executions=form_data['executions']
    )
    
    return redirect('dashboard:task_detail', task_id=opt_task.task_id)

# Feature selection related views

@login_required
def new_feature_selection_task(request):
    feature_selection_form = FeatureSelectionForm()
    
    return render(request, 'dashboard/pages/new_task.html', context={
        'title': 'Seleção de Características',
        'return_to': reverse('dashboard:index'),
        'form': feature_selection_form,
        'form_action': reverse('dashboard:start_fs_task')
    })

@login_required
def start_feature_selection_task(request):
    new_fs_url = 'dashboard:new_fs_task'
    
    if not request.POST:
        return redirect(new_fs_url)
    
    feature_selection_form = FeatureSelectionForm(request.POST)
    
    if not feature_selection_form.is_valid():
        messages.error(request, 'Por favor, selecione as opções desejadas.')
        return redirect(new_fs_url)
    
    form_data = feature_selection_form.cleaned_data
    
    fs_task = feature_selection.delay(
        user_id=request.user.id,
        optimizer=form_data['optimizer'].acronym, 
        dataset=form_data['dataset'].file_name,
        transfer_function=form_data['transfer_function'].name.lower(),
        dimension=form_data['dataset'].features,
        agents=form_data['agents'], 
        iterations=form_data['iterations'],
        executions=form_data['executions']
    )

    return redirect('dashboard:task_detail', task_id=fs_task.task_id)

# Task related views

@login_required
def task_detail(request, task_id):
    task = get_task(request.user.id, task_id)
    
    if task is None:
        raise Http404()

    return render(request, 'dashboard/pages/task_detail.html', context={
        'title': 'Detalhes da Tarefa',
        'return_to': reverse('dashboard:index'),
        'task': task
    })

@login_required
def task_result(request, task_id):
    task = get_task(request.user.id, task_id)
    
    if task is None:
        raise Http404()
    
    if 'progress' in task.result:
        redirect('dashboard:task_detail', task_id=task_id)
    
    fitness_values = task.result['fitness_values']
    conv_plot_div = plot_convergence(fitness_values)

    return render(request, 'dashboard/pages/task_result.html', context={
        'title': 'Resultado da Tarefa',
        'return_to': reverse('dashboard:task_detail', args=(task_id,)),
        'task': task,
        'conv_plot_div': conv_plot_div
    })

# Endpoint for retrieving progress

@login_required
def task_progress(request, task_id):
    task = get_task(request.user.id, task_id)
    
    if task is None:
        raise Http404()
    
    return get_progress(request, task_id)