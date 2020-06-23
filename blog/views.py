from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView

from .models import Post
from .forms import EmailPostForm


# Create your views here.
# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 1)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})

class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 1
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status='published', publish__year=year, publish__month=month, publish__day=day,
                             slug=post)
    return render(request, 'blog/post/detail.html', {'object': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data  # dictionary with keys - name field, values - values
            post_url = request.build_absolute_uri(post.get_absolute_url())  # create full post link for sending by email
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comment'])
            send_mail(subject, message, 'shopmanage7@gmail.com', [cd['to']], False)
            sent = True  # flag for complete message in template
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
