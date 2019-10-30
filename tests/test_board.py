from jeerer.card import Card
from jeerer.board import Board


def test_board_has_cards():
    board = Board([Card(name="Test")])
    assert board.get_all_cards() == [Card(name="Test")]


def test_board_get_done_cards():
    not_done = Card(name="Not Done")
    done = Card(name="Done")
    done.mark_done()

    board = Board([done, not_done])
    assert board.get_done_cards() == [done]


def test_board_get_unfinished_cards():
    not_done = Card(name="Not Done")
    done = Card(name="Done")
    done.mark_done()

    board = Board([done, not_done])
    assert board.get_unfinished_cards() == [not_done]


def test_board_get_done_includes_children():
    grandparent = Card(name="Grandparent")
    parents = grandparent.split(["Parent A", "Parent B"])
    parent_a, parent_b = parents[0], parents[1]

    board = Board([grandparent])
    parent_a.mark_done()
    assert board.get_done_cards() == [parent_a]


def test_board_unfinished_includes_children():
    grandparent = Card(name="Grandparent")
    parents = grandparent.split(["Parent A", "Parent B"])
    parent_a, parent_b = parents[0], parents[1]

    board = Board([grandparent])
    parent_a.mark_done()
    assert board.get_unfinished_cards() == [parent_b]


def test_board_get_done_gets_highest_done_part():
    grandparent = Card(name="Grandparent")
    parents = grandparent.split(["Parent A", "Parent B"])
    parent_a, parent_b = parents[0], parents[1]
    children_a = parent_a.split(["Child A 0", "Child A 1"])
    children_b = parent_b.split(["Child B 0", "Child B 1"])
    child_a_0, child_a_1 = children_a[0], children_a[1]
    child_b_0, child_b_1 = children_b[0], children_b[1]

    board = Board([grandparent])
    child_a_0.mark_done()
    child_a_1.mark_done()
    child_b_0.mark_done()

    assert board.get_done_cards() == [parent_a, child_b_0]


def test_board_get_unfinished_gets_lowest_unfinished_part():
    grandparent = Card(name="Grandparent")
    parents = grandparent.split(["Parent A", "Parent B"])
    parent_a, parent_b = parents[0], parents[1]
    children_a = parent_a.split(["Child A 0", "Child A 1"])
    children_b = parent_b.split(["Child B 0", "Child B 1"])
    child_a_0, child_a_1 = children_a[0], children_a[1]
    child_b_0, child_b_1 = children_b[0], children_b[1]

    board = Board([grandparent])
    child_a_0.mark_done()

    assert board.get_unfinished_cards() == [child_a_1, child_b_0, child_b_1]


def test_string_representation():
    not_done = Card(name="Not Done")
    not_done_2 = Card(name="Not Done2")
    done = Card(name="Done")
    done.mark_done()

    board = Board([done, not_done, not_done_2])
    assert str(board) == \
        '''Not Done:
    0. Not Done
    1. Not Done2
Done:
    0. Done'''


def test_board_add_card():
    board = Board([])
    board.add_card(Card(name="Test"))

    assert board.get_all_cards() == [Card(name="Test")]