from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.question_list, name='list'),
    path('category/<int:category_id>/', views.question_list_by_category, name='list_by_category'),
    path('<int:pk>/', views.question_detail, name='detail'),
    path('create/', views.question_create, name='create'),
    path('<int:pk>/answer/', views.answer_create, name='answer_create'),
    path('<int:pk>/answer/<int:answer_pk>/reply/', views.reply_create, name='reply_create'),
    path('<int:pk>/resolve/', views.question_resolve, name='resolve'),
    path('<int:pk>/scrap/', views.question_scrap, name='scrap'),
    path('<int:pk>/update/', views.question_update, name='update'),
    path('<int:pk>/delete/', views.question_delete, name='delete'),
    path('staff/', views.staff_unanswered, name='staff_unanswered'),
]
