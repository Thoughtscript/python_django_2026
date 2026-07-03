from django.test import TestCase
from djangoexample.models import Example, SubExample


class ExampleTestCase(TestCase):
    def setUp(self):
        Example.objects.create(name="a")
        Example.objects.create(name="b")

    def test_examples_have_names(self):
        a = Example.objects.get(name="a")
        b = Example.objects.get(name="b")
        self.assertEqual(a.name, "a")
        self.assertEqual(b.name, "b")

class SubExampleTestCase(TestCase):
    def setUp(self):
        SubExample.objects.create(name="a")
        SubExample.objects.create(name="b")

    def test_sub_examples_have_names(self):
        a = SubExample.objects.get(name="a")
        b = SubExample.objects.get(name="b")
        self.assertEqual(a.name, "a")
        self.assertEqual(b.name, "b")