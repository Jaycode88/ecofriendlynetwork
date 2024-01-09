from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm

def blog_list(request):
    posts = Post.objects.all().order_by('-created_on')
    return render(request, 'blog/blog_list.html', {'posts': posts})

def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/blog_detail.html', {'post': post})

@login_required
def add_post(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user  # Set the author to the current user
                post.save()
                return redirect('blog_list')
        else:
            form = PostForm()
        return render(request, 'blog/add_post.html', {'form': form})
    else:
        return redirect('blog_list')

@login_required
def edit_post(request, pk):
    if request.user.is_superuser:
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('blog_detail', pk=pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/edit_post.html', {'form': form, 'post': post})
    else:
        return redirect('blog_list')

@login_required
def delete_post(request, pk):
    if request.user.is_superuser:
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('blog_list')
    else:
        return redirect('blog_list')
