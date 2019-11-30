from django.test import TestCase

from jeerer_app.models import CardModel


class CardModelTests(TestCase):
    def test_card_can_be_split(self):
        parent = CardModel.objects.create(name="Parent")
        parent.split(["A", "B"])
        children = CardModel.objects.filter(parent=parent)
        a = CardModel.objects.filter(name="A")[0]
        b = CardModel.objects.filter(name="B")[0]
        self.assertIn(a, children)
        self.assertIn(b, children)

    def test_can_get_child_cards(self):
        parent = CardModel.objects.create(name="Parent")
        parent.split(["A", "B"])
        children = parent.get_children()
        a = CardModel.objects.filter(name="A")[0]
        b = CardModel.objects.filter(name="B")[0]
        self.assertIn(a, children)
        self.assertIn(b, children)

    def test_can_get_parent(self):
        parent = CardModel.objects.create(name="Parent")
        self.assertIsNone(parent.get_parent())

        parent.split(["A", "B"])

        for child in parent.get_children():
            self.assertEqual(parent, child.get_parent())

    def test_can_set_done(self):
        card = CardModel.objects.create(name="A")
        self.assertFalse(card.is_done())
        card.mark_done()
        self.assertTrue(card.is_done())

    def test_done_if_children_done(self):
        parent = CardModel.objects.create(name="Parent")
        parent.split(["A", "B"])
        children = parent.get_children()
        self.assertFalse(parent.is_done())
        for child in children:
            child.mark_done()

        self.assertTrue(parent.is_done())

    def test_bottom_level_mark_done(self):
        grandparent = CardModel.objects.create(name="Grandparent")
        grandparent.split(["Parent"])
        parent = grandparent.get_children()[0]
        parent.split(["Child"])
        child = parent.get_children()[0]

        child.mark_done()
        self.assertTrue(grandparent.is_done())

    def test_get_all_children(self):
        grandparent = CardModel.objects.create(name="Grandparent")
        grandparent.split(["Parent A", "Parent B"])
        parents = grandparent.get_children()
        parent_a = parents[0]
        parent_b = parents[1]
        parent_a.split(["Child 1", "Child 2"])
        children_a = parent_a.get_children()
        parent_b.split(["Child 3", "Child 4"])
        children_b = parent_b.get_children()

        assert grandparent.get_all_children() == [parent_a] + children_a + [parent_b] + children_b

    def test_top_level_mark_done(self):
        grandparent = CardModel.objects.create(name="Grandparent")
        grandparent.split(["Parent"])
        parent = grandparent.get_children()[0]
        parent.split(["Child"])
        child = parent.get_children()[0]

        grandparent.mark_done()
        # Parent gets all children from db and sees child is done, child needs refreshing as looks at own attribute
        child.refresh_from_db()
        self.assertTrue(parent.is_done())
        self.assertTrue(child.is_done())

    def test_children_done_if_parent_mark_done(self):
        parent = CardModel.objects.create(name="Parent")
        parent.split(["A", "B"])
        parent.mark_done()
        children = parent.get_children()
        for child in children:
            child.refresh_from_db()
            self.assertTrue(child.is_done())

    def test_string(self):
        grandparent = CardModel.objects.create(name="Grandparent")
        grandparent.split(["Parent"])
        parent = grandparent.get_children()[0]
        parent.split(["Child"])
        child = parent.get_children()[0]

        self.assertEqual(str(grandparent), "Grandparent")
        self.assertEqual(str(parent), "Grandparent~>Parent")
        self.assertEqual(str(child), "Grandparent~>Parent~>Child")
