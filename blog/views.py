from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Favorite
from .forms import PostForm

def blog_list(request):
    """
    Render a page that lists all blog posts, including the user's favorite posts if authenticated.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered template displaying a list of blog posts.
    """

    # Retrieve all blog posts, ordered by creation date
    posts = Post.objects.all().order_by('-created_on')

    # Initialize an empty list to store favorite post IDs
    favorite_post_ids = []

    # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            # Retrieve the user's favorite posts and store their IDs in favorite_post_ids
            favorite_posts = Favorite.objects.get(user=request.user).posts.all()
            favorite_post_ids = [post.id for post in favorite_posts]
        except Favorite.DoesNotExist:
            favorite_post_ids = []

    # Render the blog list template with the posts and favorite_post_ids
    return render(request, 'blog/blog_list.html', {'posts': posts, 'favorite_post_ids': favorite_post_ids})


def blog_detail(request, pk):
    """
    Render a page that displays the details of a specific blog post, including favorite status.

    Args:
        request: The HTTP request object.
        pk: The primary key of the blog post to display.

    Returns:
        A rendered template displaying the blog post details.
    """

    # Get the blog post with the given primary key (pk) or return a 404 page if not found
    post = get_object_or_404(Post, pk=pk)
    # Initialize is_favourite as false
    is_favorite = False

     # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            favorite = Favorite.objects.get(user=request.user)
            # Check if the current post is in the user's favorite posts
            is_favorite = post in favorite.posts.all()
        except Favorite.DoesNotExist:
            is_favorite = False

    # Render the blog detail template with the post and is_favorite status
    return render(request, 'blog/blog_detail.html', {'post': post, 'is_favorite': is_favorite})

@login_required
def add_post(request):
    """
    Render a page to add a new blog post (restricted to superusers).

    Args:
        request: The HTTP request object.

    Returns:
        A rendered template for adding a new blog post.
    """

    # Check if the user is a superuser
    if request.user.is_superuser:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                # Set the author of the post to the current user
                post.author = request.user
                post.save()
                # Redirect to the blog list page & display message after successful post creation
                messages.success(request, 'Blog post added successfully')
                return redirect('blog_list')
        else:
            form = PostForm()
    # Render the add_post template with the form
    return render(request, 'blog/add_post.html', {'form': form})

@login_required
def edit_post(request, pk):
    """
    Render a page to edit an existing blog post (restricted to superusers).

    Args:
        request: The HTTP request object.
        pk: The primary key of the blog post to edit.

    Returns:
        A rendered template for editing an existing blog post.
    """

    # Check if the user is a superuser
    if request.user.is_superuser:
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                # Redirect to the updated blog post's detail page with toast 
                messages.success(request, 'Blog post updated successfully')
                return redirect('blog_detail', pk=pk)
        else:
            form = PostForm(instance=post)
    # Render the edit_post template with the form and the post being edited
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    """
    Delete a blog post (restricted to superusers).

    Args:
        request: The HTTP request object.
        pk: The primary key of the blog post to delete.

    Returns:
        Redirects to the blog list page after successful deletion.
    """

    # Check if the user is a superuser
    if request.user.is_superuser:
        # Get post or show 404 error
        post = get_object_or_404(Post, pk=pk)
        # Delete Post
        post.delete()
    # Redirect to the blog list page after successful deletion with toast
    messages.success(request, 'Blog post deleted successfully')
    return redirect('blog_list')

@login_required
def add_to_favorite_posts(request, pk):
    """
    Add a blog post to the user's list of favorite posts.

    Args:
        request: The HTTP request object.
        pk: The primary key of the blog post to add to favorites.

    Returns:
        Redirects to the blog post's detail page after adding to favorites.
    """
    # Get post or show 404 error
    post = get_object_or_404(Post, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user)
    # Add the post to the user's favorite posts
    favorite.posts.add(post)
    # Redirect to the blog post's detail page with toast
    messages.success(request, 'Added to favorites')
    return redirect('blog_detail', pk=pk)

@login_required
def favorite_posts_list(request):
    """
    Render a page that lists the user's favorite blog posts.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered template displaying the user's favorite posts.
    """
    # Initialise posts and favorite posts lists
    favorite_post_ids = []
    posts = []

    # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            favorite = Favorite.objects.get(user=request.user)
            # Retrieve the user's favorite posts and store them in the 'posts' list
            posts = favorite.posts.all()
            favorite_post_ids = [post.id for post in posts]
        except Favorite.DoesNotExist:
            posts = []
            favorite_post_ids = []
    # Render the favorite_posts_list template with the user's favorite posts and favorite_post_ids
    return render(request, 'blog/favorite_posts_list.html', {'posts': posts, 'favorite_post_ids': favorite_post_ids})
    


@login_required
def remove_from_favorite_posts(request, pk):
    """
    Remove a blog post from the user's list of favorite posts.

    Args:
        request: The HTTP request object.
        pk: The primary key of the blog post to remove from favorites.

    Returns:
        Redirects to the blog list page after removing from favorites.
    """

    # Get Post or display 404 error
    post = get_object_or_404(Post, pk=pk)
    try:
        favorite = Favorite.objects.get(user=request.user)

        # Check if the post is in the user's favorite posts and remove it
        if post in favorite.posts.all():
            favorite.posts.remove(post)
    except Favorite.DoesNotExist:
        pass  # User doesn't have a favorites object, do nothing

    # Redirect to the blog list page after removing from favorites
    messages.success(request, 'Blog post removed from favourites')
    return redirect('blog_list')