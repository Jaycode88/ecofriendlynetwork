from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Favorite
from .forms import PostForm

def blog_list(request):
    posts = Post.objects.all().order_by('-created_on')
    favorite_post_ids = []
    if request.user.is_authenticated:
        try:
            favorite_posts = Favorite.objects.get(user=request.user).posts.all()
            favorite_post_ids = [post.id for post in favorite_posts]
        except Favorite.DoesNotExist:
            favorite_post_ids = []

    return render(request, 'blog/blog_list.html', {'posts': posts, 'favorite_post_ids': favorite_post_ids})


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        try:
            favorite = Favorite.objects.get(user=request.user)
            is_favorite = post in favorite.posts.all()
        except Favorite.DoesNotExist:
            is_favorite = False

    return render(request, 'blog/blog_detail.html', {'post': post, 'is_favorite': is_favorite})

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

@login_required
def add_to_favorite_posts(request, pk):
    post = get_object_or_404(Post, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user)
    favorite.posts.add(post)
    return redirect('blog_detail', pk=pk)

@login_required
def favorite_posts_list(request):
    favorite_post_ids = []
    posts = []
    if request.user.is_authenticated:
        try:
            favorite = Favorite.objects.get(user=request.user)
            posts = favorite.posts.all()
            favorite_post_ids = [post.id for post in posts]
        except Favorite.DoesNotExist:
            posts = []
            favorite_post_ids = []

    return render(request, 'blog/favorite_posts_list.html', {'posts': posts, 'favorite_post_ids': favorite_post_ids})


@login_required
def remove_from_favorite_posts(request, pk):
    post = get_object_or_404(Post, pk=pk)
    try:
        favorite = Favorite.objects.get(user=request.user)
        if post in favorite.posts.all():
            favorite.posts.remove(post)
    except Favorite.DoesNotExist:
        pass  # User doesn't have a favorites object, do nothing
    return redirect('blog_list')  # Redirect to the blog