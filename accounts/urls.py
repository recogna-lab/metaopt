from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/perform/', views.perform_signup, name='perform_signup'),
    path('login/', views.login_view, name='login'),
    path('login/perform/', views.perform_login, name='perform_login'),
    path('logout/', views.logout_view, name='logout'),
]
