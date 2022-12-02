from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/perform/', views.perform_signup, name='perform_signup'),
    path('login/', views.login_view, name='login'),
    path('login/perform/', views.perform_login, name='perform_login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset-password', views.reset_password, name='reset_password'),
    path('reset-password/perform/', views.perform_reset_password, name='perform_reset_password'),
    path('new_password/<uidb64>/<token>/', views.new_password, name='new_password'),
    path('new_password_confirm/<uidb64>/<token>/', views.perform_new_password, name='perform_new_password'),
]