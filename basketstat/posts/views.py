from django.shortcuts import render, get_object_or_404

# Create your views here.
#from . import views
from .models import Post



from django.contrib.auth.models import User


# Login required for Class based views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# import all Class based views
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView, 
                                  UpdateView,
                                  DeleteView)

# PostListView


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    # by default, it renders post_list.html
    context_object_name = 'posts'

    
    # query for all posts created by user    
    def get_queryset(self):
        # kwargs: get username from url
        user = self.request.user
        return Post.objects.filter(account=user).order_by('-date')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post





class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['author', 'title', 'content']

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)
    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)

    # UserPassesTestMixin runs test_func to check if the user is the post author
    def test_func(self):
        post = self.get_object()    # get the post we are currently trying to update
        if self.request.user == post.account:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/posts/'

    def test_func(self):
        post = self.get_object()    # get the post we are currently trying to update
        if self.request.user == post.account:
            return True
        return False



