from django.urls import path
from . import views

urlpatterns = [
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/<slug:topic_slug>/', views.article_list, name='article_list'),
    path('topics/<slug:topic_slug>/<slug:article_slug>/', views.article_detail, name='article_detail'),
]
