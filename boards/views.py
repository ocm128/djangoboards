from django.contrib.auth.models import User
from django.db.models import Count

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# from django.http import Http404
# from django.http import HttpResponse

from .forms import NewTopicForm, PostForm
from .models import Board, Topic, Post


def home(request):
    """
    Home view.
    """
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    """
    List board topics view.

    pk is used to identify board's id
    """
    board = get_object_or_404(Board, pk=pk)

    # Get the number of posts (replies) that a given topic has
    # The replies should not consider the starter topic (-1)
    topics = board.topics.order_by('-last_updated').annotate(
        replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    # Get the currently logged in user
    # user = User.objects.first()

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            # redirect to the created topic page
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        # The request is GET
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    """
    List topic posts view.

    pk is used to identify the Board.
    topic_pk which is used to identify which topic to retrieve
    from the database.
    """
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    """
    Reply post view (Vista de mensaje de respuesta)

    pk is used to identify the Board.
    topic_pk which is used to identify which topic to retrieve
    from the database.
    """
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
