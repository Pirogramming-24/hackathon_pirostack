from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:post_id>/',views.post_detail,name='post_detail'),
    path('create/',views.post_create,name='post_create'),
    path('<int:post_id>/comments/create/',views.comment_create,name='comment_create'),
    path('<int:post_id>/edit/',views.post_edit,name='post_edit'),
]