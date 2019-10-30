from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class Card:
    name: str
    parent: Card
    children: List[Card]
    _done: bool

    def __init__(self, name, parent=None, children=None):
        self.name = name
        self.parent = parent
        self.children = children if children is not None else []
        self._done = False

    def split(self, new_cards: List[str]) -> List[Card]:
        cards = [Card(name=name, parent=self) for name in new_cards]
        self.children.extend(cards)
        return cards

    def get_children(self) -> List[Card]:
        return self.children

    def get_all_children(self) -> List[Card]:
        all_children = []
        for child in self.get_children():
            all_children.append(child)
            all_children.extend(child.get_all_children())

        return all_children

    def get_parent(self) -> Card:
        return self.parent

    def is_done(self) -> bool:
        children = self.get_children()
        if children:
            return all(map(lambda child: child.is_done(), children))

        return self._done

    def mark_done(self):
        self._done = True
        for child in self.children:
            child.mark_done()
