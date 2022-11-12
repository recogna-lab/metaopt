from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='accounts:login', redirect_field_name='next')
def index(request):
    return render(request, 'dashboard/index.html')