from django.test import TestCase
from django.urls import reverse
from jeerer_app.models import CardModel, BoardModel
from django.contrib.auth.models import User


class ViewTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test", password="password")
        self.client.force_login(self.user)
        other_user = User.objects.create(username="Other")
        self.board = BoardModel.objects.create(name="Test Board")
        self.board.users.add(self.user)
        self.other_board = BoardModel.objects.create(name="Other Board")
        self.other_board.users.add(other_user)
        self.other_card = CardModel.objects.create(board=self.other_board, name="X")

    def test_mark_done(self):
        card = CardModel.objects.create(board=self.board, name="X")
        self.client.post(reverse('jeerer_app:mark_done', args=(self.board.id, card.id,)))
        card.refresh_from_db()
        self.assertTrue(card.is_done())

    def test_create_card(self):
        self.client.post(reverse('jeerer_app:card_create', args=(self.board.id,)), data={"newCard": "Test"})
        self.assertEqual(
            2,
            len(CardModel.objects.all())
        )

    def test_do_not_create_empty_child(self):
        card = CardModel.objects.create(board=self.board, name="X")
        self.client.post(reverse('jeerer_app:children', args=(self.board.id, card.id,)), data={"newCard": "Child"})
        self.assertEqual(
            1,
            len(CardModel.objects.filter(parent=card))
        )

    def test_create_board(self):
        self.client.post(reverse('jeerer_app:board_create'), data={"newBoard": "Test"})
        self.assertEqual(
            3,
            len(BoardModel.objects.all())
        )

    def test_do_not_create_empty_card(self):
        self.client.post(reverse('jeerer_app:card_create', args=(self.board.id,)), data={"newCard": ""})
        self.assertEqual(
            0,
            len(CardModel.objects.filter(name=""))
        )

    def test_do_not_create_empty_child(self):
        card = CardModel.objects.create(board=self.board, name="X")
        self.client.post(reverse('jeerer_app:children', args=(self.board.id, card.id,)), data={"newCard": ""})
        self.assertEqual(
            0,
            len(CardModel.objects.filter(parent=card))
        )

    def test_delete_card(self):
        card = CardModel.objects.create(board=self.board, name="X")
        self.client.post(reverse('jeerer_app:card_delete', args=(self.board.id, card.id,)), data={})
        self.assertEqual(
            1,
            len(CardModel.objects.all())
        )

    def test_do_not_have_access_to_not_your_boards(self):
        response = self.client.get(reverse('jeerer_app:index'))
        self.assertNotContains(response, "Other Board")
        self.assertContains(response, "Test Board")

    def test_do_not_have_access_to_not_your_board(self):
        response = self.client.get(reverse('jeerer_app:board', args=(self.other_board.id,)))
        self.assertEqual(response.status_code, 403)

    def test_do_not_have_access_to_not_your_cards(self):
        response = self.client.get(reverse('jeerer_app:card', args=(self.other_board.id, self.other_card.id)))
        self.assertEqual(response.status_code, 403)

    def test_do_not_have_access_if_card_not_in_board(self):
        response = self.client.get(reverse('jeerer_app:card', args=(self.board.id, self.other_card.id)))
        self.assertEqual(response.status_code, 403)

    def test_cannot_delete_not_your_cards(self):
        response = self.client.get(reverse('jeerer_app:card_delete', args=(self.other_board.id, self.other_card.id)))
        self.assertEqual(response.status_code, 403)

    def test_cannot_delete_if_card_not_in_board(self):
        response = self.client.get(reverse('jeerer_app:card_delete', args=(self.board.id, self.other_card.id)))
        self.assertEqual(response.status_code, 403)

    def test_cannot_mark_done_not_your_cards(self):
        response = self.client.get(reverse('jeerer_app:mark_done', args=(self.other_board.id, self.other_card.id)))
        self.assertEqual(response.status_code, 403)

    def test_cannot_mark_done_if_card_not_in_board(self):
        response = self.client.get(reverse('jeerer_app:mark_done', args=(self.board.id, self.other_card.id)))
        self.assertEqual(response.status_code, 403)

    def test_cannot_create_card_if_no_access_to_board(self):
        response = self.client.post(reverse('jeerer_app:card_create', args=(self.other_board.id,)), data={"newCard": "Test"})
        self.assertEqual(response.status_code, 403)
