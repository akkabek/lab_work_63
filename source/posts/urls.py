from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.FeedView.as_view(), name='feed'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('posts/<int:pk>/like/', views.PostLikeView.as_view(), name='like'),
    path('posts/<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),


]
