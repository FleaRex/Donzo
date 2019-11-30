from django.http import HttpRequest, HttpResponseRedirect
from .models import CardModel
from django.shortcuts import get_object_or_404, render
from django.urls import reverse


def index(request: HttpRequest):
    card_list = CardModel.objects.all()
    context = {
        'card_list': card_list
    }
    return render(request, 'jeerer_app/index.html', context)


def card(request: HttpRequest, card_id: int):
    card = get_object_or_404(CardModel, pk=card_id)
    return render(request, 'jeerer_app/card_info.html', {'card': card})


def card_create(request: HttpRequest):
    card = CardModel(name=request.POST['newCard'])
    card.save()
    return HttpResponseRedirect(reverse('jeerer_app:card', args=(card.id,)))


def mark_done(request: HttpRequest, card_id: int):
    card = get_object_or_404(CardModel, pk=card_id)
    card.mark_done()
    return HttpResponseRedirect(reverse('jeerer_app:index'))


def children(request: HttpRequest, card_id: int):
    parent = get_object_or_404(CardModel, pk=card_id)
    if request.method == 'POST':
        parent.split([request.POST['newCard']])
        return HttpResponseRedirect(reverse('jeerer_app:card', args=(card_id,)))
