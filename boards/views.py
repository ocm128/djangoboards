from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
# from django.http import Http404
# from django.http import HttpResponse

from .forms import NewTopicForm
from .models import Board, Topic, Post


def home(request):
    boards = Board.objects.all()
    """
    boards_name = list()

    for board in boards:
        boards_name.append(board.name)

    response_html = '<br>'.join(boards_name)
    """
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    # Get the currently logged in user
    user = User.objects.first()

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            # redirect to the created topic page
            return redirect('board_topics', pk=board.pk)
    else:
            # The request is GET
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
