from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.question_list, name='list'),
    path('category/<int:category_id>/', views.question_list_by_category, name='list_by_category'),
    path('<int:pk>/', views.question_detail, name='detail'),
    path('create/', views.question_create, name='create'),
    path('<int:pk>/answer/', views.answer_create, name='answer_create'),
    path('<int:pk>/resolve/', views.question_resolve, name='resolve'),
    path('staff/', views.staff_unanswered, name='staff_unanswered'),
]
