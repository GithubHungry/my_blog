from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')  # template that we use for  creating HTML
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}  # always return context-dict


@register.simple_tag
def total_comments(count=5):
    print(Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count])
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
