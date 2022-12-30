from celery_progress.views import get_progress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from metaopt.celery import app
from utils import load_json
from utils.plots import plot_bar, plot_convergence

from . import forms, models
from .tasks import feature_selection, optimization

# Dashboard page

@login_required
def index(request):
    tasks = models.get_all_tasks(user_id=request.user.id)
    
    return render(request, 'dashboard/pages/index.html', context={
        'title': 'Dashboard',
        'tasks': tasks
    })

@login_required
def search(request):
    search_term = request.GET.get('q')

    if not search_term or not search_term.strip():
        return redirect('dashboard:index')

    tasks = models.filter_tasks(
        user_id=request.user.id, 
        search_term=search_term
    )
    
    return render(request, 'dashboard/pages/index.html', context={
        'title': 'Dashboard',
        'search_term': search_term,
        'tasks': tasks
    })

# Optimization related views

@login_required
def new_optimization_task(request):
    optimization_form = forms.OptimizationForm()
    
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
    
    optimization_form = forms.OptimizationForm(request.POST)
    
    if not optimization_form.is_valid():
        error_message = (
            'Por favor, selecione todas as opções e insira valores válidos.'
        )
        messages.error(request, error_message)
        
        return redirect(new_opt_url)
    
    form_data = optimization_form.cleaned_data
    
    opt_task = optimization.delay(
        user_id=request.user.id,
        optimizer=form_data['optimizer'].acronym,
        function=form_data['function'].short_name,
        dimension=form_data['dimension'],
        bound=load_json(form_data['function'].bound),
        agents=form_data['agents'],
        iterations=form_data['iterations'],
        executions=form_data['executions']
    )
    
    return redirect('dashboard:task_detail', task_id=opt_task.task_id)

# Feature selection related views

@login_required
def new_feature_selection_task(request):
    feature_selection_form = forms.FeatureSelectionForm()
    
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
    
    feature_selection_form = forms.FeatureSelectionForm(request.POST)
    
    if not feature_selection_form.is_valid():
        error_message = (
            'Por favor, selecione todas as opções e insira valores válidos.'
        )
        messages.error(request, error_message)
        
        return redirect(new_fs_url)
    
    form_data = feature_selection_form.cleaned_data
    
    fs_task = feature_selection.delay(
        user_id=request.user.id,
        optimizer=form_data['optimizer'].acronym,
        function='Classificador OPF', # Only for saving in the db
        dataset=form_data['dataset'].name,
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
    task = models.get_task(request.user.id, task_id)
    
    if task is None:
        raise Http404()

    return render(request, 'dashboard/pages/task_detail.html', context={
        'title': 'Detalhes da Tarefa',
        'return_to': reverse('dashboard:index'),
        'task': task
    })

def revoke_task(request, task_id):
    task = models.get_task(request.user.id, task_id)
    
    # It task doensn't exist, raise page not found
    if task is None:
        raise Http404()
    
    # If task is in progress or pendent, revoke
    if task['status'] in 'Progresso Pendente':
        # Revoke
        app.control.revoke(task_id, terminate=True, signal='SIGKILL')
    
    # And redirect
    return redirect('dashboard:task_detail', task_id=task_id)

@login_required
def task_result(request, task_id):
    task = models.get_task(request.user.id, task_id)
    
    if task is None:
        raise Http404()
    
    if 'progress' in task['result']:
        redirect('dashboard:task_detail', task_id=task_id)
    
    # Get div with convergence plot
    conv_plot_div = plot_convergence(task)

    # Create variable to hold div with bar plot
    bar_plot_div = None

    # If task is a feature selection, get bar plot div
    if task['task_name'] == 'Seleção de Características':
        bar_plot_div = plot_bar(task)

    return render(request, 'dashboard/pages/task_result.html', context={
        'title': 'Resultado da Tarefa',
        'return_to': reverse('dashboard:task_detail', args=(task_id,)),
        'task': task,
        'conv_plot_div': conv_plot_div,
        'bar_plot_div': bar_plot_div
    })

# Endpoint for retrieving progress

@login_required
def task_progress(request, task_id):
    task = models.get_task(request.user.id, task_id)
    
    if task is None:
        raise Http404()
    
    return get_progress(request, task_id)