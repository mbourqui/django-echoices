# -*- coding: utf-8 -*-

from django.test import TestCase

from echoices.tests.models import ETestAutoChoices
from echoices.tests.models import ETestCharChoices, ETestStrChoices, ETestIntChoices
from echoices.tests.models import ETestCharOrderedChoices, ETestStrOrderedChoices, ETestIntOrderedChoices
from echoices.tests.models import TestAutoChoicesModel
from echoices.tests.models import TestCharChoicesModel, TestStrChoicesModel, TestIntChoicesModel
from echoices.tests.models import TestCharOrderedChoicesModel, TestStrOrderedChoicesModel, TestIntOrderedChoicesModel
from echoices.tests.models import TestEChoiceCharFieldEStrChoicesModel
from echoices.tests.models import TestEChoiceCharFieldEStrOrderedChoicesModel


class EChoiceTest(TestCase):
    def test_echoices(self):
        self.assertEqual(ETestCharChoices.values(), ('u', 'v'))
        self.assertEqual(ETestCharChoices.max_value_length(), 1)
        self.assertEqual(ETestCharChoices.choices(), (('u', 'Label 1'), ('v', 'Label 2')))
        self.assertEqual(ETestCharChoices.FIELD1.label, 'Label 1')
        self.assertIs(ETestCharChoices.from_value('u'), ETestCharChoices.FIELD1)

        self.assertEqual(ETestStrChoices.values(), ('value1', 'value2'))
        self.assertEqual(ETestStrChoices.max_value_length(), 6)
        self.assertEqual(ETestStrChoices.choices(), (('value1', 'Label 1'), ('value2', 'Label 2')))
        self.assertEqual(ETestStrChoices.FIELD1.label, 'Label 1')
        self.assertIs(ETestStrChoices.from_value('value1'), ETestStrChoices.FIELD1)

        self.assertEqual(ETestIntChoices.values(), (10, 20))
        self.assertEqual(ETestIntChoices.choices(), ((10, 'Label 1'), (20, 'Label 2')))
        self.assertEqual(ETestIntChoices.FIELD1.label, 'Label 1')
        self.assertIs(ETestIntChoices.from_value(10), ETestIntChoices.FIELD1)

    def test_create_empty_instances(self):
        TestCharChoicesModel.objects.create()
        TestStrChoicesModel.objects.create()
        TestIntChoicesModel.objects.create()


class EOrderedChoiceTest(TestCase):
    def test_echoices(self):
        self.assertEqual(ETestCharOrderedChoices.values(), ('w', 'u', 'v'))
        self.assertEqual(ETestCharOrderedChoices.max_value_length(), 1)
        self.assertEqual(ETestCharOrderedChoices.choices(), (('w', 'Label 1'), ('u', 'Label 2'), ('v', 'Label 3')))
        self.assertEqual(ETestCharOrderedChoices.choices('sorted'),
                         (('u', 'Label 2'), ('v', 'Label 3'), ('w', 'Label 1')))
        self.assertEqual(ETestCharOrderedChoices.choices('reverse'),
                         (('w', 'Label 1'), ('v', 'Label 3'), ('u', 'Label 2')))
        self.assertEqual(ETestCharOrderedChoices.choices('natural'), ETestCharOrderedChoices.choices())
        self.assertRaises(AssertionError, ETestCharOrderedChoices.choices, 'foobar')
        self.assertEqual(ETestCharOrderedChoices.FIELD1.label, 'Label 1')
        self.assertIs(ETestCharOrderedChoices.from_value('v'), ETestCharOrderedChoices.FIELD3)
        self.assertTrue(ETestCharOrderedChoices.FIELD1 > ETestCharOrderedChoices.FIELD2)

        self.assertEqual(ETestStrOrderedChoices.values(), ('value3', 'value1', 'value2'))
        self.assertEqual(ETestStrOrderedChoices.max_value_length(), 6)
        self.assertEqual(ETestStrOrderedChoices.choices(),
                         (('value3', 'Label 1'), ('value1', 'Label 2'), ('value2', 'Label 3')))
        self.assertEqual(ETestStrOrderedChoices.choices('sorted'),
                         (('value1', 'Label 2'), ('value2', 'Label 3'), ('value3', 'Label 1')))
        self.assertEqual(ETestStrOrderedChoices.choices('reverse'),
                         (('value3', 'Label 1'), ('value2', 'Label 3'), ('value1', 'Label 2')))
        self.assertEqual(ETestStrOrderedChoices.choices('natural'),
                         (('value3', 'Label 1'), ('value1', 'Label 2'), ('value2', 'Label 3')))
        self.assertEqual(ETestStrOrderedChoices.choices('natural'), ETestStrOrderedChoices.choices())
        self.assertRaises(AssertionError, ETestCharOrderedChoices.choices, 'foobar')
        self.assertEqual(ETestStrOrderedChoices.FIELD1.label, 'Label 1')
        self.assertIs(ETestStrOrderedChoices.from_value('value2'), ETestStrOrderedChoices.FIELD3)
        self.assertTrue(ETestStrOrderedChoices.FIELD1 > ETestStrOrderedChoices.FIELD2)

        self.assertEqual(ETestIntOrderedChoices.values(), (30, 10, 20))
        self.assertEqual(ETestIntOrderedChoices.choices(), ((30, 'Label 1'), (10, 'Label 2'), (20, 'Label 3')))
        self.assertEqual(ETestIntOrderedChoices.choices('sorted'), ((10, 'Label 2'), (20, 'Label 3'), (30, 'Label 1')))
        self.assertEqual(ETestIntOrderedChoices.choices('reverse'), ((30, 'Label 1'), (20, 'Label 3'), (10, 'Label 2')))
        self.assertEqual(ETestIntOrderedChoices.choices('natural'), ((30, 'Label 1'), (10, 'Label 2'), (20, 'Label 3')))
        self.assertEqual(ETestIntOrderedChoices.choices('natural'), ETestIntOrderedChoices.choices())
        self.assertRaises(AssertionError, ETestIntOrderedChoices.choices, 'foobar')
        self.assertEqual(ETestIntOrderedChoices.FIELD1.label, 'Label 1')
        self.assertIs(ETestIntOrderedChoices.from_value(20), ETestIntOrderedChoices.FIELD3)
        self.assertTrue(ETestIntOrderedChoices.FIELD1 > ETestIntOrderedChoices.FIELD2)

    def test_create_empty_instances(self):
        TestCharOrderedChoicesModel.objects.create()
        TestStrOrderedChoicesModel.objects.create()
        TestIntOrderedChoicesModel.objects.create()


class EAutoChoiceTest(TestCase):
    def test_echoices(self):
        self.assertEqual(ETestAutoChoices.values(), (1, 2, 3))
        self.assertEqual(ETestAutoChoices.choices(), ((1, 'Label 1'), (2, 'Label 2'), (3, 'Label 3')))
        self.assertEqual(ETestAutoChoices.choices('sorted'), ((1, 'Label 1'), (2, 'Label 2'), (3, 'Label 3')))
        self.assertEqual(ETestAutoChoices.choices('reverse'), ((3, 'Label 3'), (2, 'Label 2'), (1, 'Label 1')))
        self.assertEqual(ETestAutoChoices.choices('natural'), ((1, 'Label 1'), (2, 'Label 2'), (3, 'Label 3')))
        self.assertEqual(ETestAutoChoices.choices('natural'), ETestAutoChoices.choices())
        self.assertRaises(AssertionError, ETestAutoChoices.choices, 'foobar')
        self.assertEqual(ETestAutoChoices.FIELD1.label, 'Label 1')
        self.assertIs(ETestAutoChoices.from_value(2), ETestAutoChoices.FIELD2)
        self.assertTrue(ETestAutoChoices.FIELD1 < ETestAutoChoices.FIELD2)
        self.assertTrue(ETestAutoChoices.FIELD2 < ETestAutoChoices.FIELD3)

    def test_create_empty_instances(self):
        TestAutoChoicesModel.objects.create()


class ChoiceCharFieldTest(TestCase):
    def test_create_empty_instance(self):
        TestEChoiceCharFieldEStrChoicesModel.objects.create()

    def test_create_instance(self):
        instance = TestEChoiceCharFieldEStrChoicesModel.objects.create(choice=ETestStrChoices.FIELD1)
        choice = instance.choice
        self.assertIs(choice, ETestStrChoices.FIELD1)
        self.assertEqual(choice.value, 'value1')
        self.assertEqual(choice.label, 'Label 1')
        self.assertEqual(instance._meta.fields[1].choices, ETestStrChoices.choices())
        self.assertIs(instance._meta.fields[1].default, ETestStrChoices.FIELD1.value)
        self.assertIs(instance._meta.fields[1].get_default(), ETestStrChoices.FIELD1)
        instance.delete()


class OrderedChoiceCharFieldTest(TestCase):
    def test_create_empty_instance(self):
        TestEChoiceCharFieldEStrOrderedChoicesModel.objects.create()

    def test_create_instance(self):
        instance = TestEChoiceCharFieldEStrOrderedChoicesModel.objects.create(choice=ETestStrOrderedChoices.FIELD1)
        choice = instance.choice
        self.assertIs(choice, ETestStrOrderedChoices.FIELD1)
        self.assertEqual(choice.value, 'value3')
        self.assertEqual(choice.label, 'Label 1')
        self.assertEqual(instance._meta.fields[1].choices, ETestStrOrderedChoices.choices())
        self.assertIs(instance._meta.fields[1].default, ETestStrOrderedChoices.FIELD1.value)
        self.assertIs(instance._meta.fields[1].get_default(), ETestStrOrderedChoices.FIELD1)
        instance.delete()
