from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import (Paginator, EmptyPage,
                                   PageNotAnInteger)
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# Create your views here.
# def post_list(request):
#     post = Post.published.all()
#     paginator = Paginator(post, 3)
#     page_number = request.GET.get('page', 1)

#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     return render(request,
#                   'blog/post/list.html',
#                   {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day) 
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed as validation
            cd = form.cleaned_data
            #TODO send email
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommend you read {post.title}"
            message = f"Read {post.title} as {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
           
            send_mail(subject, message, 'kelanidarasimi9@gmail.com',
                    [cd['to']], fail_silently=True)
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request,
                   'blog/post/share.html',
                   {'post': post,
                    'form': form,
                    'sent': sent})