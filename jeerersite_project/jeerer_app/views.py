from django.http import HttpRequest, HttpResponseRedirect
from .models import CardModel, BoardModel
from django.shortcuts import get_object_or_404, render
from django.urls import reverse


def index(request: HttpRequest):
    context = {
        'board_list': BoardModel.objects.all()
    }
    return render(request, 'jeerer_app/index.html', context)


def board_create(request: HttpRequest):
    new_board_name = request.POST['newBoard']
    if new_board_name != '':
        board = BoardModel.objects.create(name=new_board_name)
        return HttpResponseRedirect(reverse('jeerer_app:board', args=(board.id,)))
    return HttpResponseRedirect(reverse('jeerer_app:index'))


def board(request: HttpRequest, board_id: int):
    board = get_object_or_404(BoardModel, pk=board_id)
    context = {
        'board': board
    }
    return render(request, 'jeerer_app/board.html', context)


def card(request: HttpRequest, board_id: int, card_id: int):
    card = get_object_or_404(CardModel, pk=card_id)
    return render(request, 'jeerer_app/card.html', {'card': card})


def card_create(request: HttpRequest, board_id: int):
    board = get_object_or_404(BoardModel, pk=board_id)
    new_card_name = request.POST['newCard']
    if new_card_name != '':
        card = CardModel.objects.create(board=board, name=request.POST['newCard'])
        return HttpResponseRedirect(reverse('jeerer_app:card', args=(board_id, card.id,)))
    return render(request, 'jeerer_app/board.html', {'board': board})


def mark_done(request: HttpRequest, board_id: int, card_id: int):
    card = get_object_or_404(CardModel, pk=card_id)
    card.mark_done()
    return HttpResponseRedirect(reverse('jeerer_app:board', args=(board_id,)))


def children(request: HttpRequest, board_id: int, card_id: int):
    parent = get_object_or_404(CardModel, pk=card_id)
    if request.method == 'POST':
        new_card_name = request.POST['newCard']
        if new_card_name != '':
            parent.split([new_card_name])
        return HttpResponseRedirect(reverse('jeerer_app:card', args=(board_id, card_id,)))