from django.contrib import admin
from blog import models


# Register your models here.

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'author', 'publish', 'status',)
    list_filter = ('status', 'created', 'publish', 'author')  # Filter right
    list_display_links = ('pk', 'title',)  # add links
    search_fields = ('title', 'body',)  # add search field? which work only with 'title' and 'body'
    prepopulated_fields = {'slug': ('title',)}  # auto generate slug on title field
    raw_id_fields = ('author',)  # add help-window to search authors
    date_hierarchy = 'publish'  # add links for navigating by 'publish'(date)
    ordering = ('status', 'publish',)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active',)
    list_filter = ('active', 'created', 'updated',)  # Filter right\
    search_fields = ('name', 'email', 'body',)
