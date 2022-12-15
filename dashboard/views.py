from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def index(request):
    return render(request, 'dashboard/pages/index.html')

@login_required
def new_optimization_task(request):
    return HttpResponse('New Optimization Task')

@login_required
def start_optimization_task(request):
    return HttpResponse('Start Optimization Task')

@login_required
def optimization_task(request, task_id):
    return HttpResponse('Optimization Task')