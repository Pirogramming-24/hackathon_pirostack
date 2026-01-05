from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signUp, name='signUp'),
    path('login/',views.login, name='login')
]
