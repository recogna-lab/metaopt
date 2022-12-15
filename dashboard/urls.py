from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'opt/new/', 
         views.new_optimization_task, 
         name='new_optimization_task'
    ),
    path(
        'opt/new/start/', 
        views.start_optimization_task, 
        name='start_optimization_task'
    ),
    path(
        'opt/<task_id>/', 
        views.optimization_task, 
        name='optimization_task'
    )
]
