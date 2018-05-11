from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe

import math

from markdown import markdown


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(
            topic__board=self).order_by('-created_at').first()

    def get_last_ten_posts(self):
        return self.posts.order_by('created_at')[:10]


class Topic(models.Model):
    subject = models.CharField(max_length=255)

    # auto_now_add=True set the current date and time when a
    # Post object is created.
    last_updated = models.DateTimeField(auto_now_add=True)

    # The related_name parameter will be used to create a reverse
    # relationship where the Board instances will have access a list
    # of Topic instances that belong to it.
    # Django automatically creates this reverse relationship – the
    # related_name is optional. But if we don’t set a name for it,
    # Django will generate it with the name: (class_name)_set.
    board = models.ForeignKey(Board, related_name='topics',
                              on_delete=models.CASCADE)
    starter = models.ForeignKey(User, null=True, related_name='topics',
                                on_delete=models.SET_NULL)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts',
                              on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, null=True, related_name='posts',
                                   on_delete=models.SET_NULL)

    # related_name='+'. This instructs Django that we don’t need this reverse
    # relationship, so it will ignore it.
    updated_by = models.ForeignKey(User, null=True, related_name='+',
                                   on_delete=models.SET_NULL)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
