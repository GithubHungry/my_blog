from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class PublishedManager(models.Manager):
    """New manager for filtering published posts."""

    def get_queryset(self):
        """Method will be executed every Post.published.all() [example]"""
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    """Model for posts."""
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'),)
    title = models.CharField(max_length=225)
    slug = models.SlugField(max_length=225, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()  # Save objects manager by default
    published = PublishedManager()  # Add custom manager

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug, self.publish.year, self.publish.month, self.publish.day])

    def __str__(self):
        return self.title
