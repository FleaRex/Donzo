from django.db import models
from typing import Iterable
from .board import BoardModel


class CardModel(models.Model):
    board = models.ForeignKey(BoardModel, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=256)
    done = models.BooleanField(default=False)

    def __str__(self):
        family_history = []
        current_generation = self
        while current_generation is not None:
            family_history.insert(0, current_generation.name)
            current_generation = current_generation.parent

        return '~>'.join(family_history)

    def split(self, new_cards: Iterable[str]):
        for name in new_cards:
            CardModel.objects.create(board=self.board, name=name, parent=self)

    def get_children(self) -> Iterable[CardModel]:
        return list(CardModel.objects.filter(parent=self))

    def get_all_children(self) -> Iterable[CardModel]:
        all_children = []
        for child in self.get_children():
            all_children.append(child)
            all_children.extend(child.get_all_children())

        return all_children

    def get_parent(self) -> CardModel:
        return self.parent

    def is_done(self) -> bool:
        children = self.get_children()
        if children:
            return all(map(lambda child: child.is_done(), children))

        return self.done

    def mark_done(self):
        self.done = True
        self.save()
        for child in self.get_children():
            child.mark_done()

