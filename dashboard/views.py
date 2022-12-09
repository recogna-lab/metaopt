from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .tasks import dummy_task


@login_required(login_url='accounts:login', redirect_field_name='next')
def index(request):
    task = dummy_task.delay(message='And I say Hi!')
    return render(request, 'dashboard/pages/index.html')