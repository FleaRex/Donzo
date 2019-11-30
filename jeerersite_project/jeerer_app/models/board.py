from __future__ import annotations
from django.db import models


class BoardModel(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    def get_all_cards(self):
        return list(self.cardmodel_set.all())

    def get_done_cards(self):
        done_cards = [card for card in self.cardmodel_set.all() if card.is_done()]
        # If Task A is made of subtask 1 and 2 then we don't care that 1 is done if A is done
        return list(filter(lambda card: card.parent not in done_cards, done_cards))

    def get_unfinished_cards(self):
        unfinished_cards = [card for card in self.cardmodel_set.all() if not card.is_done()]

        # We only want to see things that can be worked on (the smallest unfinished subtasks)
        return list(filter(lambda card: not card.get_children(), unfinished_cards))
