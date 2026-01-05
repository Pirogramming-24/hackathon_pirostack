from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path('', views.post_list, name='post_list'),
]