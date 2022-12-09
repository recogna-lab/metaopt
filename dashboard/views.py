from django.contrib.auth.decorators import login_required
from django.shortcuts import render

redirect_to = 'accounts:login'
next_redirect_field = 'next'

@login_required(redirect_to, next_redirect_field)
def index(request):
    return render(request, 'dashboard/pages/index.html')