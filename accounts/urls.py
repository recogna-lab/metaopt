from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/perform/', views.perform_login, name='perform_login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signup/perform/', views.perform_signup, name='perform_signup'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path(
        'password_reset/perform/', 
        views.perform_password_reset, 
        name='perform_password_reset'
    ),
    path(
        'new_password/<uidb64>/<token>/', 
        views.new_password, 
        name='new_password'
    ),
    path(
        'new_password_confirm/<uidb64>/<token>/', 
        views.perform_new_password, 
        name='perform_new_password'
    ),
]