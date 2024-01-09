from django.shortcuts import render, get_object_or_404
from .models import Post

def blog_list(request):
    posts = Post.objects.all().order_by('-created_on')
    return render(request, 'blog/blog_list.html', {'posts': posts})

def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/blog_detail.html', {'post': post})
