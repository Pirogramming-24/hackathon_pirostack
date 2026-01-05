from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('superadmin/',views.superadmin,name='superadmin'),
    path('signup/', views.signUp, name='signUp'),
    path('',views.login, name='login')
]
