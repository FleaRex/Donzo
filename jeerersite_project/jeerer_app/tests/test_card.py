from jeerer.card import Card


def test_can_create_card():
    assert Card(name="Card A") == Card(name="Card A")
    assert Card(name="Card A") != Card(name="Card B")


def test_card_can_be_split():
    parent = Card(name="Parent")
    assert parent.split(["A", "B"]) == [
        Card(name="A", parent=parent), Card(name="B", parent=parent)
    ]


def test_can_get_child_cards():
    parent = Card(name="Parent")
    parent.split(["A", "B"])
    assert parent.get_children() == [
        Card(name="A", parent=parent), Card(name="B", parent=parent)
    ]


def test_can_get_parent():
    parent = Card(name="Parent")
    children = parent.split(["A", "B"])
    assert parent.get_parent() is None
    assert children[0].get_parent() == parent


def test_can_set_done():
    card = Card(name="A")
    assert not card.is_done()
    card.mark_done()
    assert card.is_done()


def test_done_if_children_done():
    parent = Card(name="Parent")
    children = parent.split(["A", "B"])
    assert not parent.is_done()
    for child in children:
        child.mark_done()

    assert parent.is_done()


def test_children_done_if_parent_mark_done():
    parent = Card(name="Parent")
    children = parent.split(["A", "B"])
    parent.mark_done()
    for child in children:
        assert child.is_done()


def test_top_level_mark_done():
    grandparent = Card(name="Grandparent")
    parent = grandparent.split(["Parent"])[0]
    child = parent.split(["Child"])[0]

    grandparent.mark_done()
    assert child.is_done()


def test_bottom_level_mark_done():
    grandparent = Card(name="Grandparent")
    parent = grandparent.split(["Parent"])[0]
    child = parent.split(["Child"])[0]

    child.mark_done()
    assert grandparent.is_done()


def test_get_all_children():
    grandparent = Card(name="Grandparent")
    parents = grandparent.split(["Parent A", "Parent B"])
    parent_a = parents[0]
    parent_b = parents[1]
    children_a = parent_a.split(["Child 1", "Child 2"])
    children_b = parent_b.split(["Child 3", "Child 4"])

    assert grandparent.get_all_children() == [parent_a] + children_a + [parent_b] + children_b


def test_string():
    grandparent = Card(name="Grandparent")
    parent = grandparent.split(["Parent"])[0]
    child = parent.split(["Child"])[0]

    assert str(grandparent) == "Grandparent"
    assert str(parent) == "Grandparent~>Parent"
    assert str(child) == "Grandparent~>Parent~>Child"
