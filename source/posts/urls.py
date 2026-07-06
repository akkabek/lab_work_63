from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('posts/create/', views.PostCreateView.as_view(), name='create')
]
