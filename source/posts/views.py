from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, DetailView

from posts.forms import PostForm, CommentForm
from posts.models import Like, Post


class PostCreateView(LoginRequiredMixin, CreateView):

    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.object.pk})

class PostLikeView(LoginRequiredMixin, View):

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        Like.objects.get_or_create(user=request.user, post=post)
        return redirect('posts:detail', pk=post.pk)

class FeedView(LoginRequiredMixin, TemplateView):
    template_name = 'posts/feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        followed_ids = user.following.values_list('following_id', flat=True)
        posts = list(
            Post.objects.filter(author_id__in=list(followed_ids) + [user.id])
            .select_related('author')
            .order_by('-created_at')
        )
        for post in posts:
            post.liked_by_user = post.is_liked_by(user)
        context['posts'] = posts
        return context

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.liked_by_user = self.object.is_liked_by(self.request.user)
        context['comments'] = self.object.comments.select_related('author')
        context['comment_form'] = CommentForm()
        return context

class CommentCreateView(LoginRequiredMixin, View):

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        return redirect('posts:detail', pk=post.pk)