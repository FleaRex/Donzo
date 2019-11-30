from django.test import TestCase
from django.urls import reverse
from jeerer_app.models import CardModel, BoardModel

class ViewTests(TestCase):
    def setUp(self) -> None:
        self.board = BoardModel.objects.create(name="Test Board")

    def test_mark_done(self):
        card = CardModel.objects.create(board=self.board, name="X")
        self.client.post(reverse('jeerer_app:mark_done', args=(self.board.id, card.id,)))
        card.refresh_from_db()
        self.assertTrue(card.is_done())

    def test_create_card(self):
        self.client.post(reverse('jeerer_app:card_create', args=(self.board.id,)), data={"newCard": "Test"})
        self.assertEqual(
            1,
            len(CardModel.objects.filter(name="Test"))
        )

    def test_create_child(self):
        card = CardModel.objects.create(board=self.board, name="X")
        self.client.post(reverse('jeerer_app:children', args=(self.board.id, card.id,)), data={"newCard": "Test"})
        self.assertEqual(
            1,
            len(CardModel.objects.filter(parent=card))
        )
