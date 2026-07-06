from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from .forms import LoginForm, RegistrationForm
from .models import User, Follow


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('posts:feed')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object
        context['posts'] = profile_user.posts.all()
        context['is_own_profile'] = profile_user == self.request.user
        return context

class UserSearchView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/search_results.html'
    context_object_name = 'found_users'

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return User.objects.none()
        return User.objects.filter(
            Q(username__icontains=query)
            | Q(email__icontains=query)
            | Q(first_name__icontains=query)
        ).exclude(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()
        return context

class FollowToggleView(LoginRequiredMixin, View):

    def post(self, request, username):
        target = get_object_or_404(User, username=username)
        if target != request.user:
            follow, created = Follow.objects.get_or_create(
                follower=request.user, following=target
            )
            if not created:
                follow.delete()
        return redirect('accounts:profile', username=username)