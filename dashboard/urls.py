from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/search/', views.search, name='search'),
    path('tasks/compare/', views.compare, name='compare'),
    path(
        'opt/new/', 
         views.new_optimization_task, 
         name='new_opt_task'
    ),
    path(
        'opt/new/start/', 
        views.start_optimization_task, 
        name='start_opt_task'
    ),
    path(
        'fs/new/',
        views.new_feature_selection_task,
        name='new_fs_task'
    ),
    path(
        'fs/new/start',
        views.start_feature_selection_task,
        name='start_fs_task'
    ),
    path(
        'detail/<uuid:task_id>/', 
        views.task_detail, 
        name='task_detail'
    ),
    path(
        'result/<uuid:task_id>/',
        views.task_result,
        name='task_result'
    ),
    path(
        'progress/<uuid:task_id>/', 
        views.task_progress, 
        name='task_progress'
    )
]