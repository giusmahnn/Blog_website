from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Tag, Category, Comment
from .forms import PostCreateForm, PostEditForm, CommentForm
from django.urls import reverse
# Create your views here.


def post_list(request):
    '''
    This function shows the list of post in the db and orders them by the date created
    we also implemented a pagination function to help us section our post which we specified at 
    5 post per page
    '''
    post_list = Post.objects.all().order_by('-date_created')
    Pagin = Paginator(post_list, 5)
    page_num = request.GET.get('page', 1)
    page_obj = Pagin.get_page(page_num)
    return  render(request, 'post_list.html', {'page_obj': page_obj, 'is_paginated': page_obj.has_other_pages()})


def post_detail(request, slug):
    '''
    This function gets the full page of each post we want to read more on and if post doesn't,
    it shows a 404 page error
    '''
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)  # Fetch top-level comments
    comment_form = CommentForm
    context = {
        'post': post,
        'comments': comments,
        'comment_form': CommentForm
    }
    return render(request, 'post_detail.html', context)


@login_required
@require_POST
def post_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('post_detail', slug=post.slug)
    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'post_detail.html', context)


@login_required
def create_post(request):
    if request.method=='POST':
        form= PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostCreateForm()
    return render(request, 'create_post.html', {'form':form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method=='POST': 
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form= PostEditForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

@login_required
def delete_post(request,slug):
    post= get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post_list')


def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.liked.filter(id=request.user.id).exists():
        post.liked.remove(request.user)
        liked = False
    else:
        post.liked.add(request.user)
        liked=True
    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})

def search(request):

    query = request.GET.get('q')
    if query:
        result = Post.objects.filter(title__icontains = query) | Post.objects.filter(body__icontains = query)
    else:
        result=Post.objects.none
    return render(request, 'search.html', {'query':query, 'result':result})