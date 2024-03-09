from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404


# Create your views here.
def post_list(request):
    post = post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'post': post})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id) 
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


