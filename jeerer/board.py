from __future__ import annotations
from typing import List
from jeerer.card import Card


class Board:
    cards: List[Card]

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def get_all_cards(self):
        all_cards = []
        for card in self.cards:
            all_cards.append(card)
            all_cards.extend(card.get_all_children())
        return all_cards

    def get_done_cards(self):
        done_cards = [card for card in self.get_all_cards() if card.is_done()]
        return list(filter(lambda card: card.parent not in done_cards, done_cards))

    def get_unfinished_cards(self):
        unfinished_cards = [card for card in self.get_all_cards() if not card.is_done()]
        return list(filter(lambda card: not card.get_children(), unfinished_cards))
