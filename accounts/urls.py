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
        'password_reset/send/', 
        views.send_password_reset, 
        name='send_password_reset'
    ),
    path(
        'reset/<uidb64>/<token>/', 
        views.confirm_password_reset, 
        name='confirm_reset'
    ),
    path(
        'reset/complete/', 
        views.complete_password_reset, 
        name='complete_reset'
    ),
]