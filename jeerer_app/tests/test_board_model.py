from django.test import TestCase

from jeerer_app.models import CardModel, BoardModel


class BoardModelTests(TestCase):

    def test_board_has_cards(self):
        board = BoardModel.objects.create(name="Test Board")
        card = CardModel.objects.create(board=board, name="Test Card")
        self.assertEqual(board.get_all_cards(), [card])

    def test_board_get_done_cards(self):
        board = BoardModel.objects.create(name="Test Board")
        not_done = CardModel.objects.create(board=board, name="Not Done")
        done = CardModel.objects.create(board=board, name="Done")
        done.mark_done()

        self.assertEqual(board.get_done_cards(), [done])

    def test_board_get_unfinished_cards(self):
        board = BoardModel.objects.create(name="Test Board")
        not_done = CardModel.objects.create(board=board, name="Not Done")
        done = CardModel.objects.create(board=board, name="Done")
        done.mark_done()

        self.assertEqual(board.get_unfinished_cards(), [not_done])

    def test_board_get_done_includes_children(self):
        board = BoardModel.objects.create(name="Test Board")
        grandparent = CardModel.objects.create(board=board, name="Grandparent")
        grandparent.split(["Parent A", "Parent B"])
        parents = grandparent.get_children()
        parent_a, parent_b = parents[0], parents[1]

        parent_a.mark_done()
        self.assertEqual(board.get_done_cards(), [parent_a])

    def test_board_unfinished_includes_children(self):
        board = BoardModel.objects.create(name="Test Board")
        grandparent = CardModel.objects.create(board=board, name="Grandparent")
        grandparent.split(["Parent A", "Parent B"])
        parents = grandparent.get_children()
        parent_a, parent_b = parents[0], parents[1]

        parent_a.mark_done()
        self.assertEqual(board.get_unfinished_cards(), [parent_b])

    def test_board_get_done_gets_highest_done_part(self):
        board = BoardModel.objects.create(name="Test Board")
        grandparent = CardModel.objects.create(board=board, name="Grandparent")
        grandparent.split(["Parent A", "Parent B"])
        parents = grandparent.get_children()
        parent_a, parent_b = parents[0], parents[1]
        parent_a.split(["Child A 0", "Child A 1"])
        children_a = parent_a.get_children()
        parent_b.split(["Child B 0", "Child B 1"])
        children_b = parent_b.get_children()
        child_a_0, child_a_1 = children_a[0], children_a[1]
        child_b_0, child_b_1 = children_b[0], children_b[1]

        child_a_0.mark_done()
        child_a_1.mark_done()
        child_b_0.mark_done()

        self.assertEqual(board.get_done_cards(), [parent_a, child_b_0])

    def test_board_get_unfinished_gets_lowest_unfinished_part(self):
        board = BoardModel.objects.create(name="Test Board")
        grandparent = CardModel.objects.create(board=board, name="Grandparent")
        grandparent.split(["Parent A", "Parent B"])
        parents = grandparent.get_children()
        parent_a, parent_b = parents[0], parents[1]
        parent_a.split(["Child A 0", "Child A 1"])
        children_a = parent_a.get_children()
        parent_b.split(["Child B 0", "Child B 1"])
        children_b = parent_b.get_children()
        child_a_0, child_a_1 = children_a[0], children_a[1]
        child_b_0, child_b_1 = children_b[0], children_b[1]

        child_a_0.mark_done()

        self.assertEqual(board.get_unfinished_cards(), [child_a_1, child_b_0, child_b_1])

    def test_board_add_card(self):
        board = BoardModel.objects.create(name="Test Board")
        card = CardModel.objects.create(board=board, name="Test")

        self.assertEqual(board.get_all_cards(), [card])
