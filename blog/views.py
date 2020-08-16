from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import Count
from django.views.generic import ListView
from taggit.models import Tag

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm


# Create your views here.
def post_list(request, tag_slug=None):
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 1)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


# class PostListView(ListView):
#     queryset = Post.published.all()
#     paginate_by = 1
#     template_name = 'blog/post/list.html'
#     context_object_name = 'posts'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status='published', publish__year=year, publish__month=month, publish__day=day,
                             slug=post)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)  # create object, but not save into db
            new_comment.post = post
            new_comment.save()
    else:
        form = CommentForm()

    post_tags_ids = post.tags.all().values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html',
                  {'object': post, 'form': form, 'comments': comments, 'new_comment': new_comment,
                   'similar_posts': similar_posts})


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


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
    search_query = SearchQuery(query)
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        print('a')
    if form.is_valid():
        query = form.cleaned_data['query']
        print(query)
        results = Post.objects.annotate(similarity=TrigramSimilarity('title', query),).filter(
            similarity__gt=0.3).order_by('-similarity')

    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})
