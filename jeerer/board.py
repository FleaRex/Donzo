from __future__ import annotations
from typing import List
from jeerer.card import Card


class Board:
    cards: List[Card]

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __str__(self) -> str:
        return "Not Done:" + \
               self._get_numbered_list(self.get_unfinished_cards()) + \
               "\nDone:" + \
               self._get_numbered_list(self.get_done_cards())

    def _get_numbered_list(self, cards: List[Card]) -> str:
        return "".join([f"\n    {index}. " + str(card) for index, card in enumerate(cards)])

    def get_all_cards(self):
        all_cards = []
        for card in self.cards:
            all_cards.append(card)
            all_cards.extend(card.get_all_children())
        return all_cards

    def get_done_cards(self):
        done_cards = [card for card in self.get_all_cards() if card.is_done()]

        # If Task A is made of subtask 1 and 2 then we don't care that 1 is done if A is done
        return list(filter(lambda card: card.parent not in done_cards, done_cards))

    def get_unfinished_cards(self):
        unfinished_cards = [card for card in self.get_all_cards() if not card.is_done()]

        # We only want to see things that can be worked on (the smallest unfinished subtasks)
        return list(filter(lambda card: not card.get_children(), unfinished_cards))

    def add_card(self, card: Card):
        self.cards.append(card)