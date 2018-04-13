from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)


class Topic(models.Model):
    subject = models.CharField(max_length=255)

    # auto_now_add=True set the current date and time when a
    # Post object is created.
    last_update = models.DateTimeField(auto_now_add=True)

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
