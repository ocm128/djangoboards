from django.shortcuts import render, get_object_or_404
# from django.http import Http404
# from django.http import HttpResponse

# from boards import views
from .models import Board


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
